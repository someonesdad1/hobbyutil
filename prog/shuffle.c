/*

Shuffle the bytes of a file in a reversible fashion.  See Usage() for
how to use.

Warning:  this program needs to read all the bytes of a file into memory
at once, so it will not work on large files.  On my Windows 10 machine
running cygwin, it fails for files of 430 MB in size.

If you have a source of random bytes (e.g., a large file of bytes
produced by a properly-vetted physical process), then this file used as
a seed file with this program can scramble a file in a cryptographically
secure way.  One source might be https://www.random.org/bytes/, which
generates random numbers from atmospheric noise.  Understandably, they
limit the number of bits you can download unless you're willing to pay
money.  Years ago Silicon Graphics had a web page that generated random
numbers from the chaotic behavior of a Lava Lamp.  

You can download a text file of The Rand Corporation's famous 1955
publication "A Million Random Digits" from
https://www.rand.org/pubs/monograph_reports/MR1418.html.  Here's a
python script that will convert the digits to a binary file of 415241
bytes (it works by converting the million digits to a single large
integer, converting this integer to a hex string, then using a library
function to convert it to a bytes string):

    from binascii import unhexlify
    lines = <get lines of million digits text file>
    s = []
    remove_line_number = lambda x: x.split()[1:]
    for line in lines:
        t = remove_line_number(line)
        s.append(''.join(t))
    n = int(''.join(s))
    ofp = open(outfile, "wb").write(unhexlify(hex(n)[2:]))

Once you have the 415241 byte binary file, you could derive larger files
from it in a variety of ways using this program.  For example,
compressed files (using e.g. zip, gzip, or bzip2) might look like files
of random bytes (after removing known fixed information in the file like
the leading 'PK' of a zip file) and a compressed file shuffled by the
million digit file's bytes might be a usable source of random bytes as a
seed file for this program.

You can do a web search for something like "build a physical random
number generator" or "hardware random number generator" and find sites
that instruct you on how to build some hardware.  These may be suitable
for your needs.  One common design uses a reverse-biased PN junction and
an Arduino to get a random bit data rate of about 1 kbit/s (see
http://iank.org/trng.html and
https://en.wikipedia.org/wiki/Hardware_random_number_generator).
Letting such a generator run for a day would yield a file of about 10
MBytes.  Documentation on the web from experienced folks show that it's
much harder than you think to generate random bytes because there are so
many sources of non-randomness and biases; it can take exhaustive
attention to detail and sophisticated testing to generate a useful
generator..

You may want to consider purchasing a hardware random number generator.
Here's one that's about $50:  http://ubld.it/truerng_v3.  You can spend
hundreds or thousands of dollars for one too.

Internally, this program uses a linear congruential generator to
generate a random number stream if you don't use the -f option.  There's
no way a 32 bit linear congruential random number generator is capable
of generating all the permutations of a file of reasonable size.  The
period of the generator is at best 2**32 and it is capable of only
providing on the order of 1e9 different permutations.  A file of one
million bytes will have about 1e5565709 possible permutations.
Therefore, you can't consider this program's shuffling to be
cryptographically secure unless you use a seed file of
cryptographically-secure bytes.

At https://someonesdad1.github.io/hobbyutil/project_list.html I provide
some tools that might be helpful:
    
    util/mkfile.py
        Makes files of random bytes (use -u and -t).
    util/cnt.py
        Prints histograms of byte counts.
    util/bd.c
        Compares binary files.

You can use the allegedly cryptographically-secure services of your OS
(see
https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator).
For example, in python, the os.urandom() function is labeled as
providing cryptographically secure random bytes (see also python's
secrets module); you'll have to decide whether you trust such
generators.  If you do trust such things, you can use the above
util/mkfile.py python script at to make files of random bytes (use the
-u and -t options).  On my older computer, mkfile (-u or -t) takes a few
seconds to create a 1 GByte file with random bytes.

If you wish to perform some simple testing, test on small files with
known contents.  For example, I create a file named 'a' that contains
the bytes 

    Simple

Then a command like

    shuffle a b c

makes the file b contain the string

    epSlmi

Run the command 

    shuffle -u b c c

and you'll find the output file c has the same bytes as the original
file 'a'.  This demonstrates the process is reversible.

Also perform the same tests using the -f option.

----------------------------------------------------------------------
Algorithm

The Moses-Oakford algorithm is used for shuffling (see Knuth, vol. 2,
2nd ed.).  Given the array X[0], X[1], ..., X[n-1], the algorithm is :
   1.  i = n - 1  (Start with last element in array)
   2.  Generate random number U on [0, 1).
   3.  j = int(U*i) so that j is an integer in [0, i-1].
   4.  Exchange X[i] with X[j].
   5.  Decrement i by 1.
   6.  If i > 0, go to step 2.

Example for use with the string s = "abcde".  Use the random number
stream u = (0.943, 0.830, 0.935, 0.237).

Shuffling:
    s = abcde
    Step 1:                       Ran. num stream
        i = 4
        j = int(0.943*4) = 3        u[0]
        s = abced
    Step 2:
        i = 3
        j = int(0.830*3) = 2        u[1]
        s = abecd
    Step 3:
        i = 2
        j = int(0.935*2) = 1        u[2]
        s = aebcd
    Step 4:
        i = 1
        j = int(0.237*1) = 0        u[3]
        s = eabcd
    Step 5:
        i = 0
        End of algorithm

To undo the shuffling, one needs to have the random number stream in
its reverse order (this is why I decided to just read things into
memory, as this makes the programming simplest).  The algorithm is (n
= length of string = 5)
    s = eabcd
    Step 1:
        i = 1
        j = u[n - i - 1]*i = u(3)*i = 0
        s = aebcd
    Step 2:
        i = 2
        j = u[n - i - 1]*i = u(2)*i = 1
        s = abecd
    Step 3:
        i = 3
        j = u[n - i - 1]*i = u(1)*i = 2
        s = abced
    Step 4:
        i = 4
        j = u[n - i - 1]*i = u(0)*i = 3
        s = abcde
    Step 4:
        i = 5
        End of algorithm
    s is now unshuffled

In the following performance numbers, the code was compiled with no
optimizations enabled. 

The linear congruential generator 'idum = 1664525L*idum + 1013904223L;'
can generate 4e9 numbers in 14.5 s; this is 276 million numbers per
second.

The Mersenne Twister code generates 1e9 numbers in 28.6 s for about 35
million numbers per second.

If the file is n bytes, then 5*n bytes need to be stored; each random
number takes 4 bytes.  Using a simple memory allocation that increased
by 1.01 each time showed that about 2 GB of memory can be successfully
allocated before failing on my Windows XP machine with the MinGW
compiler; this gives an upper limit of about 400 MB for files that can
be processed in memory.  Using a C++ string, the limit was 102 MB.

Simulation of the shuffling algorithm shows that the code is capable
of shuffling at about 5 MB/s, excluding the time needed to read in the
file's bytes.

The conclusion from this testing is that it makes sense to write this
in C, not C++; there's probably a way to get larger allocations in C++
strings, but I don't feel like trying to figure out how...

----------------------------------------------------------------------
Copyright (C) 2012 Don Peterson
Contact:  gmail.com@someonesdad1
  
                         The Wide Open License (WOL)
  
Permission to use, copy, modify, distribute and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice and this license appear in all copies.
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY OF
ANY KIND. See http://www.dspguru.com/wide-open-license for more
information.

*/

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

typedef unsigned long ulong;
typedef unsigned char byte;

// Constants for linear congruential generator.  This generator
// requires a 32 bit integer to work correctly.
const ulong m = 1664525L;           // Multiplier
const ulong c = 1013904223L;        // Additive constant
const double scale = 4294967296.0;  // double(2**32)

// Structure for random number generation, file processing, and
// program state (i.e., this structure contains global variables).
typedef struct {
    ulong * rn;         // Array of random numbers
    ulong num_rn;       // Number of random numbers
    byte * bytes;       // Buffer to store the bytes from the file
    ulong N;            // The number of bytes in the bytes array
    int unshuffle;      // If true, undo shuffling
    int seed_is_file;   // If true, seed argument is a file name
    char * infile;      // First command-line non-option argument 
    char * outfile;     // Second command-line non-option argument
    char * seed;        // Third command-line non-option argument
    int debug;          // Debug print things if true
    ulong (*rnd)();     // Random number generator
    ulong randnum;      // Integer for linear congruential generator
    ulong rnd_count;    // Counter to use with rn array access
} RNG;

RNG g;

// I've included the MD5 code here to avoid having to have more than
// one source code file.

/*
 ***********************************************************************
 ** md5.c -- the source code for MD5 routines                         **
 ** RSA Data Security, Inc. MD5 Message-Digest Algorithm              **
 ** Created: 2/17/90 RLR                                              **
 ** Revised: 1/91 SRD,AJ,BSK,JT Reference C ver., 7/10 constant corr. **
 **          1992.2.13 Jouko Holopainen, 80x86 version                **
 ***********************************************************************
 */

/*
 ***********************************************************************
 ** Copyright (C) 1990, RSA Data Security, Inc. All rights reserved.  **
 **                                                                   **
 ** License to copy and use this software is granted provided that    **
 ** it is identified as the "RSA Data Security, Inc. MD5 Message-     **
 ** Digest Algorithm" in all material mentioning or referencing this  **
 ** software or this function.                                        **
 **                                                                   **
 ** License is also granted to make and use derivative works          **
 ** provided that such works are identified as "derived from the RSA  **
 ** Data Security, Inc. MD5 Message-Digest Algorithm" in all          **
 ** material mentioning or referencing the derived work.              **
 **                                                                   **
 ** RSA Data Security, Inc. makes no representations concerning       **
 ** either the merchantability of this software or the suitability    **
 ** of this software for any particular purpose.  It is provided "as  **
 ** is" without express or implied warranty of any kind.              **
 **                                                                   **
 ** These notices must be retained in any copies of any part of this  **
 ** documentation and/or software.                                    **
 ***********************************************************************
 */

/*
 ***********************************************************************
 **  Message-digest routines:                                         **
 **  To form the message digest for a message M                       **
 **    (1) Initialize a context buffer mdContext using MD5Init        **
 **    (2) Call MD5Update on mdContext and M                          **
 **    (3) Call MD5Final on mdContext                                 **
 **  The message digest is now in mdContext->digest[0...15]           **
 ***********************************************************************
 */

// ----------------------------------------------------------------------
// The following items came from md5.h.

/* typedef a 32-bit type */
typedef unsigned long int UINT4;

/* Data structure for MD5 (Message-Digest) computation */
typedef struct {
  UINT4 i[2];                   /* number of _bits_ handled mod 2^64 */
  UINT4 buf[4];                                    /* scratch buffer */
  unsigned char in[64];                              /* input buffer */
  unsigned char digest[16];     /* actual digest after MD5Final call */
} MD5_CTX;

// ----------------------------------------------------------------------

static unsigned char PADDING[64] = {
  0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

/* F, G, H and I are basic MD5 functions */
#define F(x, y, z) (((x) & (y)) | ((~x) & (z)))
#define G(x, y, z) (((x) & (z)) | ((y) & (~z)))
#define H(x, y, z) ((x) ^ (y) ^ (z))
#define I(x, y, z) ((y) ^ ((x) | (~z)))

/* ROTATE_LEFT rotates x left n bits */
#define ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32-(n))))

/* FF, GG, HH, and II transformations for rounds 1, 2, 3, and 4 */
/* Rotation is separate from addition to prevent recomputation */
#define FF(a, b, c, d, x, s, ac) \
  {(a) += F ((b), (c), (d)) + (x) + (UINT4)(ac); \
   (a) = ROTATE_LEFT ((a), (s)); \
   (a) += (b); \
  }
#define GG(a, b, c, d, x, s, ac) \
  {(a) += G ((b), (c), (d)) + (x) + (UINT4)(ac); \
   (a) = ROTATE_LEFT ((a), (s)); \
   (a) += (b); \
  }
#define HH(a, b, c, d, x, s, ac) \
  {(a) += H ((b), (c), (d)) + (x) + (UINT4)(ac); \
   (a) = ROTATE_LEFT ((a), (s)); \
   (a) += (b); \
  }
#define II(a, b, c, d, x, s, ac) \
  {(a) += I ((b), (c), (d)) + (x) + (UINT4)(ac); \
   (a) = ROTATE_LEFT ((a), (s)); \
   (a) += (b); \
  }

/* Basic MD5 step. Transforms buf based on in.
 */
void MD5Transform (UINT4 *buf, UINT4 *in)
{
  UINT4 a = buf[0], b = buf[1], c = buf[2], d = buf[3];

  /* Round 1 */
#define S11 7
#define S12 12
#define S13 17
#define S14 22
  FF ( a, b, c, d, in[ 0], S11, 3614090360ul); /* 1 */
  FF ( d, a, b, c, in[ 1], S12, 3905402710ul); /* 2 */
  FF ( c, d, a, b, in[ 2], S13,  606105819ul); /* 3 */
  FF ( b, c, d, a, in[ 3], S14, 3250441966ul); /* 4 */
  FF ( a, b, c, d, in[ 4], S11, 4118548399ul); /* 5 */
  FF ( d, a, b, c, in[ 5], S12, 1200080426ul); /* 6 */
  FF ( c, d, a, b, in[ 6], S13, 2821735955ul); /* 7 */
  FF ( b, c, d, a, in[ 7], S14, 4249261313ul); /* 8 */
  FF ( a, b, c, d, in[ 8], S11, 1770035416ul); /* 9 */
  FF ( d, a, b, c, in[ 9], S12, 2336552879ul); /* 10 */
  FF ( c, d, a, b, in[10], S13, 4294925233ul); /* 11 */
  FF ( b, c, d, a, in[11], S14, 2304563134ul); /* 12 */
  FF ( a, b, c, d, in[12], S11, 1804603682ul); /* 13 */
  FF ( d, a, b, c, in[13], S12, 4254626195ul); /* 14 */
  FF ( c, d, a, b, in[14], S13, 2792965006ul); /* 15 */
  FF ( b, c, d, a, in[15], S14, 1236535329ul); /* 16 */

  /* Round 2 */
#define S21 5
#define S22 9
#define S23 14
#define S24 20
  GG ( a, b, c, d, in[ 1], S21, 4129170786ul); /* 17 */
  GG ( d, a, b, c, in[ 6], S22, 3225465664ul); /* 18 */
  GG ( c, d, a, b, in[11], S23,  643717713ul); /* 19 */
  GG ( b, c, d, a, in[ 0], S24, 3921069994ul); /* 20 */
  GG ( a, b, c, d, in[ 5], S21, 3593408605ul); /* 21 */
  GG ( d, a, b, c, in[10], S22,   38016083ul); /* 22 */
  GG ( c, d, a, b, in[15], S23, 3634488961ul); /* 23 */
  GG ( b, c, d, a, in[ 4], S24, 3889429448ul); /* 24 */
  GG ( a, b, c, d, in[ 9], S21,  568446438ul); /* 25 */
  GG ( d, a, b, c, in[14], S22, 3275163606ul); /* 26 */
  GG ( c, d, a, b, in[ 3], S23, 4107603335ul); /* 27 */
  GG ( b, c, d, a, in[ 8], S24, 1163531501ul); /* 28 */
  GG ( a, b, c, d, in[13], S21, 2850285829ul); /* 29 */
  GG ( d, a, b, c, in[ 2], S22, 4243563512ul); /* 30 */
  GG ( c, d, a, b, in[ 7], S23, 1735328473ul); /* 31 */
  GG ( b, c, d, a, in[12], S24, 2368359562ul); /* 32 */

  /* Round 3 */
#define S31 4
#define S32 11
#define S33 16
#define S34 23
  HH ( a, b, c, d, in[ 5], S31, 4294588738ul); /* 33 */
  HH ( d, a, b, c, in[ 8], S32, 2272392833ul); /* 34 */
  HH ( c, d, a, b, in[11], S33, 1839030562ul); /* 35 */
  HH ( b, c, d, a, in[14], S34, 4259657740ul); /* 36 */
  HH ( a, b, c, d, in[ 1], S31, 2763975236ul); /* 37 */
  HH ( d, a, b, c, in[ 4], S32, 1272893353ul); /* 38 */
  HH ( c, d, a, b, in[ 7], S33, 4139469664ul); /* 39 */
  HH ( b, c, d, a, in[10], S34, 3200236656ul); /* 40 */
  HH ( a, b, c, d, in[13], S31,  681279174ul); /* 41 */
  HH ( d, a, b, c, in[ 0], S32, 3936430074ul); /* 42 */
  HH ( c, d, a, b, in[ 3], S33, 3572445317ul); /* 43 */
  HH ( b, c, d, a, in[ 6], S34,   76029189ul); /* 44 */
  HH ( a, b, c, d, in[ 9], S31, 3654602809ul); /* 45 */
  HH ( d, a, b, c, in[12], S32, 3873151461ul); /* 46 */
  HH ( c, d, a, b, in[15], S33,  530742520ul); /* 47 */
  HH ( b, c, d, a, in[ 2], S34, 3299628645ul); /* 48 */

  /* Round 4 */
#define S41 6
#define S42 10
#define S43 15
#define S44 21
  II ( a, b, c, d, in[ 0], S41, 4096336452ul); /* 49 */
  II ( d, a, b, c, in[ 7], S42, 1126891415ul); /* 50 */
  II ( c, d, a, b, in[14], S43, 2878612391ul); /* 51 */
  II ( b, c, d, a, in[ 5], S44, 4237533241ul); /* 52 */
  II ( a, b, c, d, in[12], S41, 1700485571ul); /* 53 */
  II ( d, a, b, c, in[ 3], S42, 2399980690ul); /* 54 */
  II ( c, d, a, b, in[10], S43, 4293915773ul); /* 55 */
  II ( b, c, d, a, in[ 1], S44, 2240044497ul); /* 56 */
  II ( a, b, c, d, in[ 8], S41, 1873313359ul); /* 57 */
  II ( d, a, b, c, in[15], S42, 4264355552ul); /* 58 */
  II ( c, d, a, b, in[ 6], S43, 2734768916ul); /* 59 */
  II ( b, c, d, a, in[13], S44, 1309151649ul); /* 60 */
  II ( a, b, c, d, in[ 4], S41, 4149444226ul); /* 61 */
  II ( d, a, b, c, in[11], S42, 3174756917ul); /* 62 */
  II ( c, d, a, b, in[ 2], S43,  718787259ul); /* 63 */
  II ( b, c, d, a, in[ 9], S44, 3951481745ul); /* 64 */

  buf[0] += a;
  buf[1] += b;
  buf[2] += c;
  buf[3] += d;
}

/* The routine MD5Init initializes the message-digest context
   mdContext. All fields are set to zero.
 */
void MD5Init (MD5_CTX *mdContext)
{
  mdContext->i[0] = mdContext->i[1] = (UINT4)0;

  /* Load magic initialization constants.
   */
  mdContext->buf[0] = (UINT4)0x67452301ul;
  mdContext->buf[1] = (UINT4)0xefcdab89ul;
  mdContext->buf[2] = (UINT4)0x98badcfeul;
  mdContext->buf[3] = (UINT4)0x10325476ul;
}

/* The routine MD5Update updates the message-digest context to
   account for the presence of each of the characters inBuf[0..inLen-1]
   in the message whose digest is being computed.
 */
void MD5Update(MD5_CTX *mdContext, 
               unsigned char *inBuf, 
               unsigned int inLen)
{
  UINT4 in[16];
  int mdi;
  unsigned int i, ii;

  /* compute number of bytes mod 64 */
  mdi = (int)((mdContext->i[0] >> 3) & 0x3F);

  /* update number of bits */
  if ((mdContext->i[0] + ((UINT4)inLen << 3)) < mdContext->i[0])
    mdContext->i[1]++;
  mdContext->i[0] += ((UINT4)inLen << 3);
  mdContext->i[1] += ((UINT4)inLen >> 29);
#ifdef  LITTLE_ENDIAN
  /* Speedup for little-endian machines suggested in MD5 report --P Karn */
	if(mdi == 0 && ((int)inBuf & 3) == 0){
		while(inLen >= 64){
			MD5Transform(mdContext->buf,(UINT4 *)inBuf);
			inLen -= 64;
			inBuf += 64;
		}               
	}
#endif  /* LITTLE_ENDIAN */
  while (inLen--) {
    /* add new character to buffer, increment mdi */
    mdContext->in[mdi++] = *inBuf++;

    /* transform if necessary */
    if (mdi == 0x40) {
      for (i = 0, ii = 0; i < 16; i++, ii += 4)
	in[i] = (((UINT4)mdContext->in[ii+3]) << 24) |
		(((UINT4)mdContext->in[ii+2]) << 16) |
		(((UINT4)mdContext->in[ii+1]) << 8) |
		((UINT4)mdContext->in[ii]);
      MD5Transform (mdContext->buf, in);
      mdi = 0;
    }
  }
}

/* The routine MD5Final terminates the message-digest computation and
   ends with the desired message digest in mdContext->digest[0...15].
 */
void MD5Final(MD5_CTX *mdContext)
{
  UINT4 in[16];
  int mdi;
  unsigned int i, ii;
  unsigned int padLen;

  /* save number of bits */
  in[14] = mdContext->i[0];
  in[15] = mdContext->i[1];

  /* compute number of bytes mod 64 */
  mdi = (int)((mdContext->i[0] >> 3) & 0x3F);

  /* pad out to 56 mod 64 */
  padLen = (mdi < 56) ? (56 - mdi) : (120 - mdi);
  MD5Update (mdContext, PADDING, padLen);

  /* append length in bits and transform */
  for (i = 0, ii = 0; i < 14; i++, ii += 4)
    in[i] = (((UINT4)mdContext->in[ii+3]) << 24) |
	    (((UINT4)mdContext->in[ii+2]) << 16) |
	    (((UINT4)mdContext->in[ii+1]) << 8) |
	    ((UINT4)mdContext->in[ii]);
  MD5Transform (mdContext->buf, in);

  /* store buffer in digest */
  for (i = 0, ii = 0; i < 4; i++, ii += 4) {
    mdContext->digest[ii] = (unsigned char)(mdContext->buf[i] & 0xFF);
    mdContext->digest[ii+1] =
      (unsigned char)((mdContext->buf[i] >> 8) & 0xFF);
    mdContext->digest[ii+2] =
      (unsigned char)((mdContext->buf[i] >> 16) & 0xFF);
    mdContext->digest[ii+3] =
      (unsigned char)((mdContext->buf[i] >> 24) & 0xFF);
  }
}

//----------------------------------------------------------------------

void Normalize(char * path)
{
    // Replace backslashes with forward slashes
    while (*path)
    {
        if (*path == '\\')
            *path = '/';
        path++;
    }
}

void Usage(const char *pgmname, const int status)
{
    fprintf(stderr, 
"Usage:  %s [-f] [-u] infile outfile seed\n"
"  Shuffle the bytes of infile and write them to outfile.  The bytes of\n"
"  infile are all read into memory, so this program will fail for files\n"
"  of sufficient size.\n"
"\n"
"  seed is used to set the state of the random number generator and can\n"
"  be any string (it is hashed).  If the -f option is given, then seed\n"
"  names a file whose bytes are used as a stream of random integers for\n"
"  shuffling.  If there are not enough bytes in the seed file, they are\n"
"  used in a circular fashion.\n"
"\n"
"  The -u option can be used to undo the shuffling done by this\n"
"  program.  You must use the same seed or seed file originally used.\n"
"\n"
"  This shuffling is not cryptographically secure unless the -f option\n"
"  is used with a cryptographically-secure stream of random bytes in the\n"
"  seed file.\n"
    , pgmname);
    exit(status);
}

void ProcessCommandLine(int argc, char **argv)
{
    char * pgmname = *argv;
    Normalize(pgmname);
    if (argc < 2)
        Usage(pgmname, 1);
    argc--;
    argv++;
    g.unshuffle    = 0;
    g.seed_is_file = 0;
    while (*argv)
    {
        if (strcmp(*argv, "-u") == 0)
            g.unshuffle = 1;
        else
            if (strcmp(*argv, "-f") == 0)
                g.seed_is_file = 1;
            else
                break;
        argc--;
        argv++;
    }
    // Now set remaining strings
    if (argc != 3)
        Usage(pgmname, 1);
    g.infile  = argv[0];
    g.outfile = argv[1];
    g.seed    = argv[2];
}

void ReadFile(const char *filename, byte ** bytes, ulong * numbytes)
{
    /* Read all the bytes in and set the global variable N to the
    number of bytes in the file.  Allocate memory for the bytes array.
    */
    FILE * ifp = 0;
    size_t bytes_read = 0;
    long number_of_bytes = 0;
    ifp = fopen(filename, "rb");
    if (ifp == NULL)
    {
        fprintf(stderr, "Couldn't open file '%s' for reading\n", filename);
        exit(1);
    }
    // Figure out total number of bytes in file
    if (fseek(ifp, 0, SEEK_END))
    {
        fprintf(stderr, "Couldn't seek to end of input file\n");
        exit(1);
    }
    number_of_bytes = ftell(ifp);
    if (number_of_bytes == -1)
    {
        fprintf(stderr, "Couldn't get size of input file\n");
        exit(1);
    }
    if (number_of_bytes < 1)
    {
        fprintf(stderr, "Input file is empty\n");
        exit(1);
    }
    *numbytes = (ulong) number_of_bytes;
    // Allocate memory
    *bytes = (byte *) malloc(*numbytes);
    if (! *bytes)
    {
        fprintf(stderr, "Couldn't allocate %lu bytes\n", *numbytes);
        exit(1);
    }
    // Seek back to start of file
    if (fseek(ifp, 0, SEEK_SET))
    {
        fprintf(stderr, "Couldn't seek to beginning of input file\n");
        exit(1);
    }
    // Read all the bytes
    bytes_read = fread(*bytes, 1, *numbytes, ifp);
    if (bytes_read != *numbytes)
    {
        fprintf(stderr, "Expected %lu bytes; read %d\n", *numbytes, bytes_read);
        exit(1);
    }
    fclose(ifp);
    if (g.debug)
        printf("Read %d bytes from %s\n", bytes_read, filename);
}

ulong Rndr(void)
{
    /* Generate random numbers from the array in g.rn and do it in
    reverse order.  InitializeGenerator has already initialized the
    g.rn array of data and set our counter g.rndr_count to the proper
    starting value.  */
    return g.rn[g.rnd_count--];
}

ulong Rnd(void)
{

    /* Generate random numbers from the array in g.rn.
    InitializeGenerator has already initialized the g.rn array of data
    and set our counter g.rnd_count to the proper starting value.  */
    return g.rn[g.rnd_count++];
}

void InitializeGenerator(void)
{
    /* Set the function pointer g.rnd to the random number generator
    to use.  If the -f option was used, then the user supplied a file
    whose bytes will (circularly) supply the random bytes.  If no file
    was given, the random numbers will be computed from a linear
    congruential generator (LCG).  
    
    For the LCG, we'll hash the seed command line string using the MD5
    hashing algorithm.  The message digest (a 16-byte string) gets
    cast to a ulong and put in g.randnum to start the LCG.
 
    If g.seed_is_file is true (the -f option was used), then we'll
    read the bytes in from the seed file and put them in memory
    starting at the g.rn pointer.  We'll circularly fill this buffer
    until we have enough bytes to make up g.N integers.
 
    The end result after exiting this function is that the array g.rn
    is filled with g.N random integers.  To use these in the shuffling
    or unshuffling algorithms, they must be divided by the constant
    scale to convert them to doubles on [0, 1). 
    
    Finally, we set the g.rnd function pointer to the appropriate
    function to read out the random numbers from the g.rn array and
    initialize the counter appropriately (these two functions just
    return the array elements in forward or reverse order; the only
    requirement is to initialize the index integer g.rnd_count
    correctly. */
    ulong i = 0;
    ulong needed_num_bytes = g.N*sizeof(ulong);
    // Allocate memory for g.rn
    g.rn = (ulong *) malloc(needed_num_bytes);
    if (! g.rn)
    {
        fprintf(stderr, 
                "Couldn't allocate %lu bytes for random number array\n",
                g.N);
        exit(1);
    }
    if (g.seed_is_file)
    {
        /* Read in the seed file's bytes and circularly put them into
        the buffer beginning at g.rn so that there are enough bytes to
        generate g.N random integers. */
        byte * seed_bytes;
        ulong num_seed_bytes = 0;
        g.rn = (ulong *) malloc(needed_num_bytes);
        if (! g.rn)
        {
            fprintf(stderr, "Couldn't allocate %lu bytes for g.rn\n", 
                needed_num_bytes);
            exit(1);
        }
        byte * dest = (byte *) g.rn;
        ReadFile(g.seed, &seed_bytes, &num_seed_bytes);
        for (i=0; i < needed_num_bytes; i++)
            dest[i] = seed_bytes[i % num_seed_bytes];
        free(seed_bytes);
    }
    else
    {
        // Initialize the linear congruential generator with the hash
        // of the command line seed argument.
        MD5_CTX context;
        MD5Init(&context);
        MD5Update(&context, (unsigned char *)g.seed, strlen(g.seed));
        MD5Final(&context);
        g.randnum = *((ulong *) context.digest);
        if (g.debug)
            printf("Seeded with %lu\n", g.randnum);
        // Put the random bytes in the g.rn array.
        for (i=0; i < g.N; i++)
        {
            /* Generate a random unsigned long on [0, 2**32 - 1].
            This linear congruential generator is randq1 from
            "Numerical Recipes in C", 2nd ed.).  */
            g.randnum = m*g.randnum + c;
            g.rn[i] = g.randnum;
        }
    }
    /* Set up the random number generator function to use.  There are
    two cases:  1) deliver from g.rn in forward order (Rnd) or 2)
    reverse order (Rndr). */
    if (g.unshuffle)
    {
        g.rnd = Rndr;
        /* Note it's important to start 2 numbers under g.N because
        the unshuffle algorithm doesn't use all g.N of the random
        numbers (the easiest way to see this is to put a few bytes
        into an input file, turn on g.debug, and look at the output of
        the indexes and random numbers).  An even better reason is 
        that you don't get correct unshuffling unless you do. :^) */
        g.rnd_count = g.N - 2;
        // Dump the numbers for debugging
        if (g.debug)
        {
            fprintf(stderr, "Random numbers in reverse order for unshuffling:\n");
            for (i=0; i < g.N - 1; i++)
                fprintf(stderr, "  %f\n", Rndr()/scale);
            g.rnd_count = g.N - 2;
        }
    }
    else
    {
        g.rnd = Rnd;
        g.rnd_count = 0;
        if (g.debug)
        {
            fprintf(stderr, "Random numbers in order for shuffling:\n");
            for (i=0; i < g.N - 1; i++)
                fprintf(stderr, "  %f\n", Rnd()/scale);
            g.rnd_count = 0;
        }
    }
}

void Shuffle(void)
{
    /* Shuffle the input file with the Moses-Oakford algorithm and
    write the shuffled bytes to the output file.  */
    FILE * ofp  = 0;
    ulong i     = 0;
    ulong j     = 0;
    byte tmp    = 0;
    double u    = 0;
    size_t bytes_written = 0;
 
    // Open output file for writing
    ofp = fopen(g.outfile, "wb");
    if (ofp == NULL)
    {
        fprintf(stderr, "Couldn't open file '%s' for writing\n", g.outfile);
        exit(1);
    }
    // Shuffle the input file's bytes using the Moses-Oakford algorithm.
    if (g.debug)
        printf("Shuffling %lu bytes\n", g.N);
    i = g.N - 1;
    while (i)
    {
        // Make j an integer in the interval [0, i-1]
        u = g.rnd()/scale;
        j = (ulong)(i*u);
        if (g.debug)
            fprintf(stderr, "i = %lu, j = %lu, u = %f\n", i, j, u);
        // Swap bytes at positions i and j
        tmp = g.bytes[i];
        g.bytes[i] = g.bytes[j];
        g.bytes[j] = tmp;
        i--;
    }
    // Write the output file
    bytes_written = fwrite(g.bytes, 1, g.N, ofp);
    if (bytes_written != g.N)
    {
        fprintf(stderr, "Expected to write %lu bytes; wrote %d to output\n", 
            g.N, bytes_written);
        exit(1);
    }
    fclose(ofp);
    if (g.debug)
        printf("Wrote %d bytes to %s\n", bytes_written, g.outfile);
}

void Unshuffle(void)
{
    /* Unshuffle the bytes in infile by applying the inverse of the
    Moses-Oakford algorithm. */
    FILE *  ofp  = 0;
    ulong i      = 0;
    ulong j      = 0;
    double u     = 0;
    byte tmp     = 0;
    size_t bytes_written = 0;
    // Open output file for writing
    ofp = fopen(g.outfile, "wb");
    if (ofp == NULL)
    {
        fprintf(stderr, "Couldn't open file '%s' for writing\n", g.outfile);
        exit(1);
    }
    // We have what we need, so work backwards through the
    // Moses-Oakford algorithm.
    i = 1;
    while (i < g.N)
    {
        u = g.rnd()/scale;
        j = (ulong)(u*i);
        if (g.debug)
            fprintf(stderr, "i = %lu, j = %lu, u = %f\n", i, j, u);
        // Swap bytes at positions i and j
        tmp = g.bytes[i];
        g.bytes[i] = g.bytes[j];
        g.bytes[j] = tmp;
        i++;
    }
    // Write the output file
    bytes_written = fwrite(g.bytes, 1, g.N, ofp);
    if (bytes_written != g.N)
    {
        fprintf(stderr, "Expected to write %lu bytes; wrote %d to output\n", 
            g.N, bytes_written);
        exit(1);
    }
    fclose(ofp);
    if (g.debug)
        printf("Wrote %d bytes to %s\n", bytes_written, g.outfile);
}

int main(int argc, char **argv)
{
    // Initialize global structure
    g.rn           = 0;
    g.num_rn       = 0;
    g.bytes        = 0;
    g.N            = 0;
    g.unshuffle    = 0;
    g.seed_is_file = 0;
    g.infile       = 0;
    g.outfile      = 0;
    g.seed         = 0;
    g.debug        = 0;
    g.rnd          = 0;
    g.randnum      = 0;
    g.rnd_count    = 0;
    // Make sure we have a 4-byte integer
    if (sizeof(ulong) != 4)
    {
        fprintf(stderr, "unsigned long isn't 4 bytes\n");
        exit(1);
    }
    ProcessCommandLine(argc, argv);
    if (g.debug)
    {
        printf("Input file  = '%s'\n", g.infile);
        printf("Output file = '%s'\n", g.outfile);
        printf("Seed        = '%s'\n", g.seed);
    }
    // Get input bytes
    ReadFile(g.infile, &g.bytes, &g.N);
    if (g.N < 2)
    {
        fprintf(stderr, "Must have at least 2 bytes in input file.\n");
        fprintf(stderr, "Fix:  change the typedef appropriately for ulong.\n");
        exit(1);
    }
    // Set up random number generation facilities.  The end result
    // will be the array of integers g.rn and having the function
    // pointer g.rnd pointing to the correct function to call to get
    // each random integer (each integer needs to be divided by scale
    // to get the random double on [0, 1)).
    InitializeGenerator();
    // Do the required work
    if (g.unshuffle)
        Unshuffle();
    else
        Shuffle();
    // Free allocated memory.  Note if a seed file was read in, the
    // memory for that was freed in InitializeGenerator().
    free(g.rn);
    free(g.bytes);
    return 0;
}
