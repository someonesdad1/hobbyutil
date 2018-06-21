// Sat 29 Apr 2017 11:18:52 AM   I first wrote this program around 1994
// when I was working in the controller section; I used it for e.g.
// determining differences in firmware images.  It would have compiled both
// with Borland's compiler under Windows NT and the Linux compiler for the
// 1.2.13 kernel, which we used for years (why can I remember such stuff
// and not remember where my glasses are?).  Interestingly, it still
// compiles fine today under the 5.4.0 version of gcc under cygwin, so it
// was written in a reasonably portable fashion.





/*
bd   This program will compare the two files on the command line in
a binary fashion and print out in hex dump format any bytes that
are different.  The return status is 0 if the files are identical
and 1 if they are not identical.  If the files are not the same size,
then only the number of bytes in the smaller file are read in and
compared.

The basic method is to read in blocks of the files and perform
comparisons on the blocks.  Any differences are stored in a range
structure (that is just two integers) that gives the offset of the
sequence of bytes that were different.  The scan through the files
produces an array of these range structures.  Then this information
is processed for display to the user.  Here, the sequences are
displayed as hex dumps, but other software could e.g. display it
on the screen using curses.

The program was written to work in both 32 bit Windows and Linux.

The basic algorithm for generating the ranges is based on a state
machine.  The main variables are offset (the position of the pointer
into the file stream), start, the beginning of a range, and end,
the end of a range.  The states are:

    S0       Beginning state
    S1       Range on state (a difference was found, so we're in a state
             of bytes continuing to be different)
    S2       Range off state (we were in a range on state, but now we 
             found two bytes that were equal, so switch to range off state)
    S3       Ending state (processing of block finished)

State transitions are caused by the events of the next two
correspondings bytes are equal, not equal, or the end of the block
is encountered.

The state transitions and their actions are (= means bytes were equal,
!= means they were unequal, EOB means end of block):

    Transition  Caused by   Action
    ----------  ---------   --------------------------------------------------
    S0-S1          !=       Set start = end = offset
    S0-S2          =        No action
    S1-S1          !=       Set end = offset
    S1-S2          =        Append [start, end] to range list.
                            Then set start = end = INVALID_VALUE 
    S1-S3          EOB      If start != INVALID_VALUE append [start, end] to
    range list.
    S2-S1          !=       Set start = end = offset
    S2-S2          =        No action
    S2-S3          EOB      No action
    --------------------------------------------------------------------------

(This looks a little cleaner on a state machine diagram.)

9 Mar 2001:

Added -a option that prints out an ASCII picture of where the
differences are.

   ----------+---------+---------+---------+---------+---------
   0         1         2         3         4         5
  +------------------------------------------------------------
 0|
 5|
10|
15|
20|
25|
30|
35|
40|
45|
50|
55|
60|
65|
70|
75|
80|
85|
90|
95|

The numbers down the side are in 5% chunks through the file.

Copyright (C) 1994, 2001, 2005 Don Peterson

This program is licensed under the Open Software License version 3.0.  See
http://opensource.org/licenses/OSL-3.0.

*/

#include <assert.h>
#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#ifdef DEBUG
    #define DBG(x) printf x
#else
    #define DBG(x) /* Nothing */
#endif


/* Exit status codes for the program */
#define EXIT_FILES_SAME          0
#define EXIT_FILES_DIFFERENT     1
#define EXIT_DIFFERENT_SIZE      2
#define EXIT_USAGE               3
#define EXIT_STAT_ERROR          4
#define EXIT_FILE_NOT_OPENED     5
#define EXIT_FILE_ZERO_SIZE      6
#define EXIT_NOT_REG_FILE        7
#define EXIT_MALLOC_FAILED       8
#define EXIT_REALLOC_FAILED      9
#define EXIT_STREAM_ERROR        10
#define EXIT_UNEXPECTED_STATE    11

#define ARRAY_SIZE               1000  /* Allocate space in these chunks */
#define BUFSIZE                  8192  /* Read buffer size */
#define LNSZ                     16    /* How many bytes to print on a line */
#define LNSZJUMP                 8     /* Where to print extra space*/


/* The following character is printed in the ASCII area for unprintable
characters.  183 is a centered small dot that works on Linux and 1 is
a small diamond that also works on Linux. */
#define UNPRINTABLE_CHARACTER    183

/* State machine states */
#define STATE_START              0
#define STATE_RANGE_ON           1
#define STATE_RANGE_OFF          2
#define STATE_END                3
#define INVALID_VALUE           -1     /* For offsets */

typedef struct {
    int start;
    int end;
} RANGE;

/* The following structure contains all the global information. */
struct {
    int   files_are_different;
    int   file1_size;           /* stat size of file 1 */
    int   file2_size;           /* stat size of file 2 */
    int   compare_size;         /* Number of bytes we should compare */
    FILE *ifp1;
    FILE *ifp2;
    char *filename1;
    char *filename2;
    RANGE *rng;                 /* Array of range objects describing diffs */
    int   rng_size;             /* Current max num of elements in rng array */
    int   rng_numel;            /* Current number of elements in rng */
    char *buf1;                 /* Buffer for file data */
    char *buf2;                 /* Buffer for file data */
} globals;

FILE *ofp;                      /* Where to send the output to */
char *version = "$Revision: 1.3 $";

/* Stuff to define the -c printout option's characteristics */
int histogram = 0;
const int rows    = 20;
const int columns = 60;
#define COUNT_SIZE 1200
unsigned char diff_count[COUNT_SIZE]; /* Holds differences histogram */

/**************************************************************************/

void GetFileSize(char *filename, int *size)
{
    struct stat st;

    /* Get the stat structure */
    if (stat(filename, &st)) {
        perror(NULL);
        fprintf(stderr, "Couldn't stat %s\n", filename);
        exit(EXIT_STAT_ERROR);
    }
    /* Get the size */
    *size = (int) st.st_size;
    if (*size == 0) {
        fprintf(stderr, "File %s is of zero size\n", filename);
        exit(EXIT_FILE_ZERO_SIZE);
    }
}

void OpenFile(FILE **ifp, char *filename)
{
    if ((*ifp = fopen(filename, "rb")) == NULL) {
        fprintf(stderr, "Couldn't open %s\n", filename);
        exit(EXIT_FILE_NOT_OPENED);
    }
}

/****************************************************************************
Read into the buffers another block from each file.  It's a fatal error
if either of the reads fails.  Return the smaller of the number of bytes
read for each stream.  The function returns 0 when one of the streams
is at EOF.
****************************************************************************/

int ReadBlock(void)
{
    int numbytes1;
    int numbytes2;

    assert(globals.ifp1 != NULL);
    assert(globals.ifp2 != NULL);

    if (feof(globals.ifp1) || feof(globals.ifp2)) {
        return 0;
    }
    numbytes1 = fread(globals.buf1, 1, BUFSIZE, globals.ifp1);
    if (ferror(globals.ifp1)) {
        fprintf(stderr, "I/O error on stream 1\n");
        exit(EXIT_STREAM_ERROR);
    }
    numbytes2 = fread(globals.buf2, 1, BUFSIZE, globals.ifp2);
    if (ferror(globals.ifp2)) {
        fprintf(stderr, "I/O error on stream 2\n");
        exit(EXIT_STREAM_ERROR);
    }
    /*
    DBG(("Read %d bytes from stream1\n", numbytes1));
    DBG(("Read %d bytes from stream2\n", numbytes2));
    */
    if (numbytes1 > numbytes2) {
        return numbytes2;
    }
    return numbytes1;
}

void IncreaseArraySize(void)
{
    int ix;
    int old_size;
    int new_size;

    old_size = globals.rng_size;
    new_size = old_size + ARRAY_SIZE;

    globals.rng = realloc(globals.rng, (size_t)(sizeof(RANGE) * new_size));
    if (globals.rng == NULL) {
        fprintf(stderr, "Couldn't allocate new memory\n");
        exit(EXIT_REALLOC_FAILED);
    }

    for (ix = old_size; ix < new_size; ix++) {
        globals.rng[ix].start = 0;
        globals.rng[ix].end   = 0;
    }
    globals.rng_size = new_size;
}

void Usage(void)
{
    fprintf(stderr, 
    "Usage:  bd [-a] file1 file2\n"
    "  Prints hex dumps of the differences between two files.\n"
    "  The -a option prints an ASCII graphical summary indexed by %%.\n"
    );
    exit(EXIT_USAGE);
}

void Initialize(int argc, char **argv)
{
    int ix;
    if (argc != 3 && argc != 4) {
        Usage();
    }
    if (argc == 4) {
        if (argv[1][0] != '-') {
            Usage();
        }
        if (argv[1][1] != 'a') {
            Usage();
        }
        histogram = 1;
        argv++;
        argc--;
        /* Initialize histogram array */
        for(ix = 0; ix < ARRAY_SIZE; ix++) {
            diff_count[ix] = 0;
        }
    }
    globals.filename1 = argv[1];
    globals.filename2 = argv[2];
    globals.files_are_different = 0;
    GetFileSize(globals.filename1, &globals.file1_size);
    GetFileSize(globals.filename2, &globals.file2_size);
    if (globals.file1_size < globals.file2_size) {
        globals.compare_size = globals.file1_size;
    } else {
        globals.compare_size = globals.file2_size;
    }
    /* Allocate dynamic memory for the array. */
    if ((globals.rng = (RANGE *) calloc(sizeof(RANGE), ARRAY_SIZE)) == NULL) {
        fprintf(stderr, "Couldn't allocate array memory\n");
        exit(EXIT_MALLOC_FAILED);
    }
    /* Initialize the array elements (even though calloc sets everything
    to zero). */
    for (ix = 0; ix < ARRAY_SIZE; ix++) {
        globals.rng[ix].start = 0;
        globals.rng[ix].end   = 0;
    }
    globals.rng_size  = ARRAY_SIZE;
    globals.rng_numel = 0;
    /* Allocate memory for the buffers */
    if ((globals.buf1 = (char *) malloc(BUFSIZE)) == NULL) {
        fprintf(stderr, "Couldn't allocate memory for buffer 1\n");
        exit(EXIT_MALLOC_FAILED);
    }
    if ((globals.buf2 = (char *) malloc(BUFSIZE)) == NULL) {
        fprintf(stderr, "Couldn't allocate memory for buffer 2\n");
        exit(EXIT_MALLOC_FAILED);
    }
    /* Open the files for reading */
    OpenFile(&globals.ifp1, globals.filename1);
    OpenFile(&globals.ifp2, globals.filename2);
}

void Terminate(void)
{
    fclose(globals.ifp1);
    fclose(globals.ifp2);
    free(globals.rng);
    free(globals.buf1);
    free(globals.buf2);
}

void AddRangeToArray(int start, int end)
{
    int ix;
    DBG(("Adding range:  [%d, %d]\n", start, end));
    if (globals.rng_numel > 0) {
        /* Make sure this range isn't the same as the previous one */
        ix = globals.rng_numel - 1;
        assert(start >= globals.rng[ix].end);
        if (globals.rng[ix].start == start && globals.rng[ix].end == end) {
            DBG(("  Same as previous range; not adding...\n"));
            return;
        }
        /* See if we can make this range contiguous with the last range 
        in the array. */
        DBG(("  Checking for continuity with previous range %d:  [%d, %d]\n", ix, globals.rng[ix].start, globals.rng[ix].end));
        if (globals.rng[ix].end+1 == start) {
            DBG(("  Was contiguous\n"));
            globals.rng[ix].end = end;
            DBG(("  New range %d is [%d, %d]\n", ix, globals.rng[ix].start, globals.rng[ix].end));
            return;
        } else {
            DBG(("  Was not contiguous\n"));
        }
    }
    if (globals.rng_numel == globals.rng_size) {
        IncreaseArraySize();
    }
    globals.rng[globals.rng_numel].start = start;
    globals.rng[globals.rng_numel].end   = end;
    globals.rng_numel++;
}

void Compare(void)
{
    int blocksize;
    int numblocks    = -1;
    int offset       = 0;
    int block_offset = 0;
    int equal_bytes  = 0;
    int start        = INVALID_VALUE;
    int end          = INVALID_VALUE;
    int state        = STATE_START;
    while (blocksize = ReadBlock()) { /* Single '=' is intended */
        numblocks++;
        state = STATE_START;
        for (block_offset = 0; block_offset < blocksize; block_offset++) {
            offset = numblocks*BUFSIZE + block_offset;
            equal_bytes = (globals.buf1[block_offset] == globals.buf2[block_offset]);
            DBG(("offset = %d, block_offset = %d, state = %d, bytes equal = %d, ", offset, block_offset, state, equal_bytes));
            /*DBG(("byte1 = 0x%02x   byte2 = 0x%02x\n", globals.buf1[block_offset], globals.buf2[block_offset]));*/
            switch (state) {
                case STATE_START:
                    if (equal_bytes) {
                        state = STATE_RANGE_OFF;
                        DBG(("new state = %d\n", state));
                    } else {
                        state = STATE_RANGE_ON;
                        DBG(("new state = %d\n", state));
                        start = offset;
                        end   = offset;
                        globals.files_are_different = 1;
                    }
                    break;
                case STATE_RANGE_ON:
                    if (equal_bytes) {
                        state = STATE_RANGE_OFF;
                        DBG(("new state = %d\n", state));
                        assert(start != INVALID_VALUE);
                        assert(end   != INVALID_VALUE);
                        DBG(("Found end of range [%d, %d]\n", start, end));
                        AddRangeToArray(start, end);
                        start = INVALID_VALUE;
                        end   = INVALID_VALUE;
                    } else {
                        state = STATE_RANGE_ON;
                        DBG(("new state = %d\n", state));
                        end = offset;
                        globals.files_are_different = 1;
                    }
                    break;
                case STATE_RANGE_OFF:
                    if (equal_bytes) {
                        state = STATE_RANGE_OFF;
                        DBG(("new state = %d\n", state));
                    } else {
                        state = STATE_RANGE_ON;
                        DBG(("new state = %d\n", state));
                        start = offset;
                        end   = offset;
                        globals.files_are_different = 1;
                    }
                    break;
                default:
                    fprintf(stderr, "Unexpected state in Compare()\n");
                    exit(EXIT_UNEXPECTED_STATE);
            }
        }
        /* End of block implies transition to STATE_END */
        if (state == STATE_RANGE_ON && 
            start != INVALID_VALUE &&
            end   != INVALID_VALUE) {
            state  = STATE_END;
            DBG(("End of block:  adding range [%d, %d]\n", start, end));
            AddRangeToArray(start, end);
            start = INVALID_VALUE;
            end   = INVALID_VALUE;
        }
        DBG(("======================== EOB ========================\n"));
    }
}

void PrintHeader(void)
{
    if (globals.file1_size == globals.file2_size) {
        fprintf(ofp, "Files are %d (0x%x) bytes in size\n", 
                     globals.file1_size, globals.file1_size);
    } else {
        fprintf(ofp, "File %s is %d (0x%x) bytes in size\n", 
                     globals.filename1, globals.file1_size, globals.file1_size);
        fprintf(ofp, "File %s is %d (0x%x) bytes in size\n", 
                     globals.filename2, globals.file2_size, globals.file2_size);
        fprintf(ofp, "Only the first %d (0x%x) bytes are compared\n", 
                     globals.compare_size, globals.compare_size);
    }
}

void PrintSeparator(void)
{
    int ix;
    for (ix = 0; ix < 77; ix++) {
        fputc('-', ofp);
    }
    fputc('\n', ofp);
}

void PrintLine(int offset, unsigned char *buf, int numbytes)
{
    int ix;
    int printed_sep = 0;
    unsigned int c;
    fprintf(ofp, "%08x  ", offset);
    /* Print the hex bytes */
    for (ix = 0; ix < numbytes; ix++) {
        fprintf(ofp, "%02x ", buf[ix]);
        if (ix == LNSZJUMP - 1) {
            fprintf(ofp, " ");
            printed_sep = 1;
        }
    }
    /* Print spaces for any missing ones */
    for (ix = 0; ix < LNSZ - numbytes; ix++) {
        fprintf(ofp, "   ");
        if (ix == LNSZJUMP - 1 && printed_sep == 0) {
            fprintf(ofp, " ");
        }
    }
    /* Print them in ASCII */
    fprintf(ofp, "| ");
    for (ix = 0; ix < numbytes; ix++) {
        c = buf[ix];
        if (isprint(c)) {
            fputc(c, ofp);
        } else {
            fputc(UNPRINTABLE_CHARACTER, ofp);
        }
    }
    fprintf(ofp, "\n");
}

void HexDump(FILE *ifp, int offset, int numbytes)
{
    int block;
    int ix;
    int bytes_this_line = 0;
    int numlines;
    unsigned char buf[LNSZ];
    fseek(ifp, offset, 0);
    numlines = numbytes/LNSZ;
    DBG(("numlines = %d\n", numlines));
    for (block = 0; block < numlines; block++) {
        bytes_this_line = fread(buf, 1, LNSZ, ifp);
        PrintLine(offset + block*LNSZ, buf, bytes_this_line);
    }
    /* Now print any remaining partial line */
    bytes_this_line = numbytes % LNSZ;
    if (bytes_this_line != 0) {
        if (fread(buf, 1, bytes_this_line, ifp) != (size_t) bytes_this_line) {
            fprintf(stderr, "HexDump:  unexpected number of characters\n");
            exit(1);
        }
        if (numlines == 0) {
            PrintLine(offset, buf, bytes_this_line);
        } else {
            PrintLine(offset + numlines*LNSZ, buf, bytes_this_line);
        }
    }
}

void PrintRange(int starting_offset, int ending_offset)
{
    char plural[2] = "";
    int num_bytes_diff;
    assert(starting_offset >= 0);
    assert(starting_offset <= ending_offset);
    if (starting_offset < ending_offset) {
        strcpy(plural, "s");
    }
    num_bytes_diff = ending_offset - starting_offset + 1;
    fprintf(ofp, "File %s:  %d (0x%x) byte%s different\n", 
                 globals.filename1, num_bytes_diff, num_bytes_diff, plural);
    HexDump(globals.ifp1, starting_offset, num_bytes_diff);
    fprintf(ofp, "File %s:\n", globals.filename2);
    HexDump(globals.ifp2, starting_offset, num_bytes_diff);
    PrintSeparator();
}


void PrintHistogram(void)
{
    int size;
    int ix;
    int jx;
    int index;
    if (globals.file1_size < globals.file2_size) {
        size = globals.file2_size;
    } else {
        size = globals.file1_size;
    }
    #define INC(x) if ((x) < 255) { (x)++; }
    for (ix = 0; ix < globals.rng_numel; ix++) {
        for(jx = globals.rng[ix].start; jx <= globals.rng[ix].end; jx++) {
            index = (int)(1.0*jx/size*COUNT_SIZE);
            INC(diff_count[index]);
        }
    }
    /* Print the results */
    printf("Size = %d (0x%08x)\n\n", size, size);
    printf("   0         1         2         3         4         5\n");
    printf("  +------------------------------------------------------------");
    for(ix = 0; ix < COUNT_SIZE; ix++) {
        if (ix % columns == 0) {
            printf("\n%2d|", (100/rows)*ix/columns);
        }
        if (ix % columns == (columns - 1)) {
            printf("|");
            continue;
        }
        if (diff_count[ix]) {
            printf(".");
        } else {
            printf(" ");
        }
    }
    printf("\n  +------------------------------------------------------------\n");
}

void PrintResults(void)
{
    int ix;
#ifdef DEBUG
    fprintf(ofp, "Debug dump of globals global struct:\n");
    fprintf(ofp, "  files_are_different = %d\n", globals.files_are_different);
    fprintf(ofp, "  file1_size          = %d\n", globals.file1_size);
    fprintf(ofp, "  file2_size          = %d\n", globals.file2_size);
    fprintf(ofp, "  compare_size        = %d\n", globals.compare_size);
    fprintf(ofp, "  filename1           = '%s'\n", globals.filename1);
    fprintf(ofp, "  filename2           = '%s'\n", globals.filename2);
    fprintf(ofp, "  rng_size            = %d\n", globals.rng_size);
    fprintf(ofp, "  rng_numel           = %d\n", globals.rng_numel);
    fprintf(ofp, "Debug dump of range array:\n");
    for (ix = 0; ix < globals.rng_numel; ix++) {
        fprintf(ofp, "  %8d %8d\n", globals.rng[ix].start, globals.rng[ix].end);
    }
#endif
    if (histogram) {
        PrintHistogram();
    } else {
        PrintHeader();
        PrintSeparator();
        for (ix = 0; ix < globals.rng_numel; ix++) {
            PrintRange(globals.rng[ix].start, globals.rng[ix].end);
        }
    }
}

int main(int argc, char **argv)
{
    int status = 0;
    ofp = stdout;  /* Where the output will go */
    Initialize(argc, argv);
    Compare();
    if (globals.files_are_different) {
        PrintResults();
    }
    Terminate();
    return status;
}
