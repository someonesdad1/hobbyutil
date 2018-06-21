/***************************************************************************

Program to spell check and cross reference text files with special
options to help with source code.  See the Usage() function for
calling details.

If you compile this for your own use, you should change the location
of the default dictionary by modifying the function InitializeGlobals.

Implementation
--------------

  Tokenizing:

    Lines from the input files are read in one at a time.  The tokens
    are gotten by replacing the non-alphanumeric characters with
    spaces, then parsing on space characters.  Composite tokens are
    those that contain underscores or have upper case letters other
    than the first character.

    2017 update:  fixed an embarrasing tokenizing bug in GotAnotherToken
    (shown by trying to cross-reference a file with one line of 'self.d'
    and not getting the 'd').  Update the man page output and noted that
    Unicode characters will cause a warning and a listing to stderr of
    the location of those non-7-bit characters.  These non-7-bit
    characters are left in, so you'll see them in or as tokens.  For
    example, tokenize this file and you'll see the token '0Δ'.

  Spelling:

    Words from the dictionaries are read into an STL map.  The lookup
    of words is case-insensitive.

    Misspelled words (tokens) are stored in a map; the tokens are the
    map's keys.  The value is a map whose keys are the file name and
    the value is a set of line numbers in that file for each
    occurrence of the misspelled token.

----------------------------------------------------------------------
Copyright (C) 2003, 2005, 2017 Don Peterson
Contact:  gmail.com@someonesdad1

                  The Wide Open License (WOL)

Permission to use, copy, modify, distribute and sell this software and
its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice and this license appear in
all copies.  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT EXPRESS OR
IMPLIED WARRANTY OF ANY KIND. See
http://www.dspguru.com/wide-open-license for more information.
***************************************************************************/

#include <cstdlib>
#include <ctime>
#include <ctype.h>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using namespace std;

typedef set <string> DictionaryContainer;
typedef set <string>::const_iterator DictionaryContainerIterator;

// The following container contains the information on the file and
// line numbers of a misspelled word.  The map key is the filename and
// the container is a set of line numbers.
typedef map<string, set<int> > Misspelled;
typedef map<string, set<int> >::iterator MisspelledIterator;
typedef set <int>::iterator LineNumberIterator;

// Container for misspelled tokens.
typedef map<string, Misspelled> MisspelledTokens;
typedef MisspelledTokens::iterator MisspelledTokensIterator;

class Dictionary
{
    // The Dictionary class is used to contain the tokens of one or more
    // given word lists.

public:
    void AddToken(const string & token);
    void ReadFile(const string & filename);
    bool IsSpelledCorrectly(const string & word);
    inline int size(void)
    {
        return tokens.size();
    }

private:
    set<string> tokens;
}
dictionary;

struct anon_type
{
    // Global variable container

    // We use a struct to make things a bit more tidy.  The 'g.' prefix
    // on a variable indicates it's a global.

    // Note:  you can define the default dictionary to be the empty
    // string.  This will have the effect of printing out the tokens
    // of all the files when doing a spelling check.  I recommend
    // appending a goodly number of spaces to this string (they're
    // stripped when it is used) to allow someone to hack the binary
    // to give a new location.
    string default_dictionary;

    // Whether to print the long listing or not by default.  If this
    // is false, then the long listing (tokens, files and line
    // numbers) is printed.  If true, only the tokens are printed.
    bool tokens_only;

    // If this is true, composite tokens such as CompositeToken are
    // split into two words and these words are spell checked
    // separately.  Otherwise, this typical programming token would
    // be declared misspelled.
    bool split_composite_tokens;

    // If set to false, ignore common programming keywords.
    bool include_programming_keywords;

    // If set to true, remove digits from tokens.
    bool remove_digits;

    // If true, print out the time to load the dictionaries and the
    // processing times.
    bool print_times;

    // The -@ option allows the user to send the files to be processed
    // via stdin (after any command line files are processed).
    bool read_files_from_stdin;

    // Print a '.' to stderr after each file processed if true
    bool verbose;

    // If true, add in tokens resulting from contractions
    bool add_contractions;

    // Print only tokens that are in the dictionary
    bool negate_spell_check;

    bool print_informational_statistics;
    bool perform_spell_check;
    string program_name;

    // For capturing statistics
    unsigned int tokens_with_one_reference;
    unsigned int maximum_number_of_references;
    string token_max_references;  // Which one has max references
    unsigned int total_number_of_tokens;

    // Container for any misspelled tokens
    MisspelledTokens BadTokens;

    // Characters with the 8th bit set will turn the following Boolean
    // on.  If flag_8_bit_characters is true (use -8 option), then the
    // line:offsets are sent to stderr.
    bool found_8_bit_characters;
    bool flag_8_bit_characters;
}
g;

// Character to break tokens with
const string space = " ";



void ToLower(string & s)
{

    // Convert a string to all lower case letters.

    for (unsigned int ix = 0; ix < s.length(); ix++)
    {
        s[ix] = tolower(s[ix]);
    }
}

void Dictionary::ReadFile(const string & filename)
{

    // Read the tokens in from a text file.  The tokens should be
    // separated by whitespace.

    ifstream ifs(filename.c_str(), ios::in);
    if (! ifs)
    {
        cerr << g.program_name << ": error:  couldn't open dictionary file "
             << filename << endl;
        exit(1);
    }

    string word;

    while (! ifs.eof())
    {
        ifs >> word;
        // Convert the first character to a lower case letter
        word[0] = tolower(word[0]);
        tokens.insert(word);
    }
}

bool Dictionary::IsSpelledCorrectly(const string & word)
{
    if (tokens.find(word) != tokens.end())
    {
        return true;
    }
    else
    {
        return false;
    }
}

void Dictionary::AddToken(const string & token)
{
    string token_copy = token;
    ToLower(token_copy);
    tokens.insert(token_copy);
}

void manpage(void)
{
    cout <<
     "NAME\n"
     "    xref - produce a cross reference of tokens in a set of text files\n"
     "\n"
     "SYNOPSIS\n"
     "    xref [options] [file1 [file2...]]\n"
     "\n"
     "DESCRIPTION\n"
     "    Tokens are gotten by replacing non-alphanumeric characters by\n"
     "    space characters, then parsing on whitespace.  The output is\n"
     "    printed to stdout and is the token on its own line followed by the\n"
     "    files and line numbers that contain that token.  The -t option\n"
     "    causes only the tokens to be printed out, one per line.\n"
     "\n"
     "    Tab and carriage return characters will be replaced by spaces, but\n"
     "    other control characters won't.  To see them, you may need to save\n"
     "    the output to a file and view it with your editor.\n"
     "\n"
     "    The program is also capable of spell checking the text files.  You\n"
     "    may compile in the location of a default dictionary to use.  A\n"
     "    dictionary is a list of tokens separated by whitespace that give\n"
     "    the correct spelling of the tokens.  Letter case is ignored.\n"
     "    Any misspelled tokens are printed to stdout.\n"
     "\n"
     "    During spell checking, the program will parse compound tokens such\n"
     "    as 'MyFunction' and 'my_function' into the tokens 'my' and\n"
     "    'function', then look them up in the dictionary.  This allows\n"
     "    programmers to help ensure they're using descriptive names for\n"
     "    symbols in their programs.  The algorithm for splitting a compound\n"
     "    token is to replace underscores by space characters, then put a\n"
     "    space character before each upper case letter.  Single letters as\n"
     "    tokens are ignored.  Tokens that are misspelled are printed to\n"
     "    stdout.  The program includes a built-in dictionary for keywords\n"
     "    in C, C++, python, and shell programming.  Tokens that begin with\n"
     "    '0' are ignored, as they are likely octal or hex constants.\n"
     "    Tokens that are composed of all digits are also ignored.\n"
     "\n"
     "    In the source code, you can define a default dictionary to use for\n"
     "    spell checking (if the string is empty, no default dictionary is\n"
     "    used).  It is not an error if this file is not present.\n"
     "\n"
     "    Because of the algorithm used for splitting composite tokens,\n"
     "    tokens with all uppercase letters will be ignored when spell\n"
     "    checking.\n"
     "\n"
     "    Non-7-bit characters seen in e.g. UTF-8 encoded files will be seen\n"
     "    in tokens, so this program should work on encoded files in a\n"
     "    suitable terminal.  The line numbers and offsets of these non-\n"
     "    7-bit characters will be sent to stderr if the -8 option is used.\n"
     "\n"
     "CROSS-REFERENCING OPTIONS\n"
     "    -8\n"
     "        Flag line:offset of 8-bit characters.  Messages are sent to\n"
     "        stderr.\n"
     "    -@\n"
     "        Get file list from stdin\n"
     "\n"
     "    -h\n"
     "        Print this man page to stdout.\n"
     "\n"
     "    -i\n"
     "        Print informational statistics at end of report.\n"
     "\n"
     "    -l  Print the tokens found in sorted order, one token per line, \n"
     "        followed by the file name and line numbers where that token\n"
     "        appears.\n"
     "\n"
     "    -t\n"
     "        Print the tokens found in sorted order, one token per line.\n"
     "\n"
     "    -T\n"
     "        Print the processing times.\n"
     "\n"
     "    Note:  a compile-time switch determines whether the -l or -t\n"
     "    format is the default output.\n"
     "\n"
     "SPELL CHECKING OPTIONS\n"
     "    -c\n"
     "        Do not use the built-in keywords for C/C++, python, and Bourne\n"
     "        type shell scripts when spell checking.  You can replace the\n"
     "        list in the source code with your own list of words.\n"
     "\n"
     "    -C \n"
     "        Remove tokens resulting from common English contractions (e.g.,\n"
     "        'didn', 'hasn', etc.).\n"
     "\n"
     "    -d dict     \n"
     "        Specify a spelling dictionary in addition to the default\n"
     "        dictionary.  Use this option to add correctly spelled tokens\n"
     "        that are not in the default dictionary.  You can have more\n"
     "        than one -d option.\n"
     "\n"
     "    -D dict\n"
     "        Specify a spelling dictionary that replaces the default\n"
     "        dictionary.  You can have more than one -D option, but the\n"
     "        last one on the command line is used.\n"
     "\n"
     "    -g\n"
     "        Do not remove digits from tokens when spell checking.\n"
     "        Normally, a token such as MyFunction4 would have the 4 removed\n"
     "        before spell checking.\n"
     "\n"
     "    -k\n"
     "        When spell checking, split composite words such as TwoWords\n"
     "        or two_words into the simple words Two and Words.  This is\n"
     "        intended to allow you to spell check source code.  Many of\n"
     "        us programmers feel variable names should be spelled correctly\n"
     "        and use words in the dictionary, rather than abbreviations.\n"
     "\n"
     "    -n\n"
     "        Don't read in the default dictionary.\n"
     "\n"
     "    -s\n"
     "        Perform a spell check on the tokens (uses the default\n"
     "        dictionary if one was compiled in).  Any tokens not found in\n"
     "        the dictionary will be printed to stdout.\n"
     "\n"
     "EXAMPLES\n"
     "    xref file1\n"
     "    xref -l file1\n"
     "        Print a list of tokens in file1 with filename and line numbers.\n"
     "\n"
     "    xref -t file1\n"
     "        Print a list of tokens only in file1.\n"
     "\n"
     "    xref -s -d dict file1\n"
     "        Spell check file1 using an explicitly specified dictionary.\n"
     "\n"
     "NOTES\n"
     "    You may want to append numerous trailing spaces after the\n"
     "    definition of the default dictionary in the source code.  This\n"
     "    would allow a user to change the dictionary in a compiled binary.\n"
     "    Trailing space characters in the string are stripped.\n"
     "\n"
     "    Please send bug reports/improvements to someonesdad1@gmail.com.\n"
     "\n"
     "BUGS\n"
     "    * If -g not used, tokens printed out are missing digits in spell check.\n"
     ;
    exit(1);
}

void Usage(void)
{
    cout << "Usage:  " << g.program_name <<
         " [options] [source_file_1 [source_file_2...]]\n"
         "  A token cross-referencing and spell checking tool.\n"
         "    -8          Flag line:offset of 8-bit characters\n"
         "    -@          Get file list from stdin\n"
         "    -h          Print man page to stdout\n"
         "    -i          Print informational statistics to stdout\n"
         "    -l          Long listing:  tokens, files, and line numbers\n"
         "    -t          Short listing:  print tokens only\n"
         "    -T          Print the processing times\n"
         "Spell checking:\n"
         "    -c          Do not use built-in keywords for C/C++, python, shell \n"
         "    -C          Remove common English contractions\n"
         "    -d dict     Specify a spelling dictionary in addition to default dict\n"
         "    -D dict     Specify a spelling dictionary (replaces default dictionary)\n"
         "    -g          Do not remove digits from tokens when spell checking\n"
         "    -k          Split composite tokens when spell checking\n"
         "    -n          Negate spell check:  only print tokens in dictionaries\n"
         "    -s          Perform a spell check of the tokens (uses default\n"
         "                dictionary if one was compiled in)\n"
         "Default dictionary = '"
         << g.default_dictionary
         << "'\n"
         ;
    exit(1);
}

void GetProgramName(const char *name)
{
    string s = name;

    // Find the last backslash or forward slash
    bool found = false;
    int slash_position;
    for (slash_position= s.length() - 1; slash_position > 0; slash_position--)
    {
        if (s[slash_position] == '\\' || s[slash_position] == '/')
        {
            found = true;
            break;
        }
    }
    if (found == false)
    {
        g.program_name = name;
    }
    else
    {
        g.program_name =
            s.substr(slash_position + 1, s.length() - slash_position + 1);
    }
}

void ReadDictionaries(const DictionaryContainer & dictionaries)
{
    DictionaryContainerIterator it;

    for (it = dictionaries.begin(); it != dictionaries.end(); ++it)
    {
        if (*it != "")
        {   // Allow for empty strings
            dictionary.ReadFile(it->c_str());
        }
    }

    // Add in tokens commonly used in programming languages.
    // Customize this list for your favorite languages.

    if (g.include_programming_keywords)
    {
        string keywords[] = {

            "abs",
            "acos",
            "acosh",
            "acosl",
            "alloc",
            "amode",
            "argc",
            "argv",
            "asctime",
            "asin",
            "asinh",
            "asinl",
            "atan",
            "atan2",
            "atan2l",
            "atanh",
            "atanl",
            "atexit",
            "atof",
            "atoi",
            "atol",
            "bitset",
            "bool",
            "boolalpha",
            "brk",
            "bsearch",
            "calloc",
            "ceil",
            "ceill",
            "cerr",
            "cgets",
            "chdir",
            "chmod",
            "cin",
            "clearerr",
            "cmode",
            "conio",
            "const",
            "const_iterator",
            "cosh",
            "coshl",
            "cosl",
            "cout",
            "cprintf",
            "cputs",
            "creat",
            "cscanf",
            "cstdlib",
            "ctime",
            "ctype",
            "difftime",
            "dup",
            "dup2",
            "ecvt",
            "elif",
            "endif",
            "endl",
            "erf",
            "erfc",
            "errno",
            "esac",          // Shell
            "exec",
            "execl",
            "execle",
            "execlp",
            "execlpe",
            "execv",
            "execve",
            "execvp",
            "execvpe",
            "exp",
            "expl",
            "extern",
            "fabs",
            "fabsl",
            "fclose",
            "fcloseall",
            "fcntl",
            "fcvt",
            "fdopen",
            "feof",
            "ferror",
            "fflush",
            "fgetc",
            "fgetchar",
            "fgetpos",
            "fgets",
            "fileno",
            "fi",            // Shell
            "floorl",
            "flushall",
            "fmod",
            "fmodl",
            "fopen",
            "fprint",
            "fprintf",
            "fputc",
            "fputchar",
            "fputs",
            "fread",
            "freopen",
            "frexp",
            "frexpl",
            "fscanf",
            "fseek",
            "fsetpos",
            "fstat",
            "fstream",
            "ftell",
            "func",
            "fwrite",
            "gcvt",
            "getc",
            "getch",
            "getchar",
            "getche",
            "getcwd",
            "getenv",
            "getline",
            "getw",
            "gmtime",
            "gsignal",
            "ifdef",
            "ifndef",
            "ifstream",
            "inline",
            "int",
            "ios",
            "iostream",
            "isalnum",
            "isalpha",
            "isascii",
            "isatty",
            "iscntrl",
            "isdigit",
            "isgraph",
            "islower",
            "isprint",
            "ispunct",
            "isspace",
            "istring",
            "istrstream",
            "isupper",
            "isxdigit",
            "iterator",
            "itoa",
            "labs",
            "ldexp",
            "ldexpl",
            "ldiv",
            "lfind",
            "localtime",
            "log10",
            "log10l",
            "logl",
            "longjmp",
            "lsearch",
            "lseek",
            "ltoa",
            "malloc",
            "matherr",
            "mblen",
            "mbstowcs",
            "mbtowc",
            "memccpy",
            "memchr",
            "memcmp",
            "memcpy",
            "memicmp",
            "memmove",
            "memset",
            "mkdir",
            "mktemp",
            "mktime",
            "modf",
            "modfl",
            "namespace",
            "noboolalpha",
            "nocreate",
            "noreplace",
            "oct",
            "ofstream",
            "ostream",
            "perror",
            "pow",
            "pow10",
            "pow10l",
            "powl",
            "printf",
            "putc",
            "putchar",
            "putenv",
            "putw",
            "qsort",
            "readonly",     // shell
            "realloc",
            "resetiosflags",
            "rmdir",
            "sbrk",
            "scanf",
            "setbase",
            "setbuf",
            "setf",
            "setfill",
            "setiosflags",
            "setjmp",
            "setmode",
            "setprecision",
            "setvbuf",
            "setw",
            "showbase",
            "showpoint",
            "showpos",
            "signal",
            "sinh",
            "sinhl",
            "sinl",
            "sizeof",
            "skipws",
            "spawnl",
            "spawnle",
            "spawnlp",
            "spawnlpe",
            "spawnv",
            "spawnve",
            "spawnvp",
            "spawnvpe",
            "sprintf",
            "sqrt",
            "sqrtl",
            "srand",
            "sscanf",
            "stat",
            "std",
            "stderr",
            "stdin",
            "stdio",
            "stdlib",
            "stdout",
            "stime",
            "stpcpy",
            "str",
            "strcat",
            "strchr",
            "strcmp",
            "strcmpi",
            "strcoll",
            "strcpy",
            "strcspn",
            "strdup",
            "strerror",
            "strftime",
            "stricmp",
            "strlen",
            "strlwr",
            "strncat",
            "strncmp",
            "strncmpi",
            "strncpy",
            "strnicmp",
            "strnset",
            "strpbrk",
            "strrchr",
            "strrev",
            "strset",
            "strspn",
            "strstr",
            "strstream",
            "strtod",
            "strtok",
            "strtol",
            "strtoul",
            "struct",
            "strupr",
            "strxfrm",
            "substr",
            "swprintf",
            "tanh",
            "tanhl",
            "tanl",
            "tmpfile",
            "tmpnam",
            "toascii",
            "tolower",
            "toupper",
            "trunc",
            "typedef",
            "typename",
            "tzset",
            "ultoa",
            "undef",
            "ungetc",
            "ungetch",
            "unitbuf",
            "unset",
            "uppercase",
            "va",           // Allows va_arg stuff
            "vfprintf",
            "vfscanf",
            "vprintf",
            "vscanf",
            "vsprintf",
            "vsscanf",
            "wcstombs",
            "wctomb",

            // python keywords
            "and",
            "ascii",
            "bytearray",
            "bytes",
            "callable",
            "chr",
            "classmethod",
            "cmath",
            "cmp",
            "copysign",
            "def",
            "delattr",
            "delitem",
            "delslice",
            "dict",
            "dir",
            "divmod",
            "eq",
            "eval",
            "excepthook",
            "frozenset",
            "gamma",
            "getattr",
            "getitem",
            "getslice",
            "getstate",
            "globals",
            "hasattr",
            "hex",
            "hypot",
            "id",
            "init",
            "isinstance",
            "issubclass",
            "iter",
            "len",
            "lgamma",
            "locals",
            "lshift",
            "max",
            "memoryview",
            "min",
            "mul",
            "ord",
            "or",
            "radd",
            "rcmp",
            "rdiv",
            "rdivmod",
            "repr",
            "rlshift",
            "rmod",
            "rmul",
            "rop",
            "ror",
            "rpow",
            "rrshift",
            "rshift",
            "rsub",
            "rxor",
            "setattr",
            "setitem",
            "setslice",
            "setstate",
            "staticmethod",
            "tuple",
            "ufloat",
            "UFloat",
            "umath",
            "uncertainties",
            "vars",
            "xor",
            "xrange",
            "zip",

            ""              // Flags end of array
        };
        int keyword = 0;
        while(keywords[keyword] != "")
        {
            dictionary.AddToken(keywords[keyword++]);
        }

        // Some of these came from
        // http://teachers.net/gazette/APR03/images/haskinscontractions.pdf
        string contractions[] = {
            "ain",
            "aren",
            "couldn",
            "didn",
            "doesn",
            "hadn",
            "hadn",
            "hasn",
            "isn",
            "ll",
            "mayn",
            "mightn",
            "mustn",
            "needn",
            "oughtn",
            "shan",
            "shouldn",
            "twouldn",
            "wasn",
            "weren",
            "wouldn",
            ""
        };

        keyword = 0;
        if (g.add_contractions)
        {
            while(contractions[keyword] != "")
            {
                dictionary.AddToken(contractions[keyword++]);
            }
        }

    }
}

int PrintReport(double read_dictionary_time_sec, double processing_time_sec)
{

    // Print misspelled tokens with filename and line numbers.  If there
    // are no misspelled tokens, return 0; otherwise return 1.  Note
    // this function also prints the correctly spelled tokens if the -n
    // option was given.

    unsigned int size = g.BadTokens.size();
    if (size == 0)
    {
        return 0;
    }

    MisspelledTokensIterator wit;

    for (wit = g.BadTokens.begin(); wit != g.BadTokens.end(); ++wit)
    {
        // Print the misspelled token
        cout << wit->first << endl;
        if (g.tokens_only)
        {
            continue;
        }

        MisspelledIterator it;
        unsigned int number_of_references = 0;

        for (it = wit->second.begin(); it != wit->second.end(); ++it)
        {
            // Print filename
            cout << "    " << it->first << ": ";
            LineNumberIterator lit;
            cout << "[" << it->second.size() << "] ";
            for (lit = it->second.begin();
                    lit != it->second.end();
                    ++lit)
            {
                if (lit != it->second.begin() && lit != it->second.end())
                {
                    cout << ", ";
                }
                cout << *lit;
                number_of_references++;
            }
            cout << endl;
        }

        if (number_of_references == 1)
        {
            g.tokens_with_one_reference++;
        }
        if (number_of_references > g.maximum_number_of_references)
        {
            g.maximum_number_of_references = number_of_references;
            g.token_max_references = wit->first;
        }
    }

    if (g.print_times)
    {
        if (g.perform_spell_check)
        {
            cout << "Time to read dictionaries (sec) = "
                 << read_dictionary_time_sec << endl;
            cout << "Time to process files (sec)     = "
                 << processing_time_sec << endl;
        }
        else
        {
            cout << "Time to process files (sec) = "
                 << processing_time_sec << endl;
        }
    }

    if (g.print_informational_statistics)
    {
        cout << endl
             << "Tokens with one reference    = "
             << g.tokens_with_one_reference << endl
             << "Maximum number of references = "
             << g.maximum_number_of_references
             << " (" << g.token_max_references << ")" << endl
             << "Total number of tokens       = "
             << g.total_number_of_tokens << endl;
    }

    if (g.perform_spell_check)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

void ReplacePunctuationWithSpaces(string & line, const string & filename,
                                  const int line_number)
{
    bool message_printed = false;

    // In the following, we'll check to see if 8th bit is set -- if so,
    // it's either not a plain ASCII file or it has Unicode characters.
    // The test is because the elements are signed characters and if the
    // 8th bit is set, they'll be negative.

    for (unsigned ix = 0; ix < line.length(); ix++)
    {
        if (line[ix] < 0)
        {
            if (! message_printed and g.flag_8_bit_characters)
            {
                cerr << "'" << filename << "':[" << line_number 
                     << "] 8-bit character offsets:  " << ix;
                message_printed = true;
            }
            else
            {
                if (g.flag_8_bit_characters)
                    // Only show the offset of other characters
                    cerr << ", " << ix;
            }
            // Flag for the end-of-program message
            g.found_8_bit_characters = true;
        }

        // If the character is a punctuation character defined by
        // ispunc() and is not an underscore (which is a valid character
        // in C/python identifiers), replace it with a space character.
        // Do the same for horizontal tab characters and carriage
        // returns so they don't wind up in tokens.  All other control
        // characters like formfeeds will wind up in tokens.
        if (
            (ispunct(line[ix]) && line[ix] != '_') or
            line[ix] == '\t' or
            line[ix] == '\r'
        )
        {
            line[ix] = ' ';
        }
    }
    if (message_printed and g.flag_8_bit_characters)
    {
        cerr << endl;
    }
}

void RemoveLeadingSpaces(string & line)
{
    unsigned int white_space = 0;

    while (line[white_space] == ' ')
    {
        white_space++;
    }
    line = line.substr(white_space);
}

bool GotAnotherToken(string & token, string & line)
{
    // Get the next token from the line.  Return true if a token was
    // found; false if not.

    string::size_type pos;

    if (! line.size())
        return false;
    RemoveLeadingSpaces(line);
    if (! line.size())
        return false;

    // Find next space
    pos = line.find_first_of(space);
    if (pos == string::npos)
    {
        // Space not found, so we're on the last token
        token = line;
        line = "";
        return true;
    }
    // Did find a space
    token = line.substr(0, pos);
    line = line.substr(pos);
    return true;
}

void Tokenize(const string & str, vector<string> & tokens,
              const string & delimiters = " ")
{
    // A tokenizer from
    // http://oopweb.com/CPP/Documents/CPPHOWTO/Volume/C++Programming-HOWTO-7.html
    // Downloaded 30 Jan 2017 to fix a bug in the old code's splitting
    // on space characters.

    // Skip delimiters at beginning.
    string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    string::size_type pos = str.find_first_of(delimiters, lastPos);

    while (string::npos != pos || string::npos != lastPos)
    {
        // Found a token; add it to the vector.
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        // Skip delimiters.  Note the "not_of"
        lastPos = str.find_first_not_of(delimiters, pos);
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}

bool IsAllDigits(const string & token)
{

    // Ignore numbers.  We define a token that begins with "0" to also
    // be a number.

    if (token[0] == '0')
    {
        return true;
    }

    for (unsigned int ix = 0; ix < token.length(); ix++)
    {
        if (! isdigit(token[ix]))
        {
            return false;
        }
    }
    return true;
}

bool IsAllUpperCase(const string & token)
{
    for (unsigned int ix = 0; ix < token.length(); ix++)
    {
        if (! isupper(token[ix]))
        {
            return false;
        }
    }
    return true;
}

void RemoveDigits(string & token)
{
    unsigned int ix = 0;

    while (ix < token.length())
    {
        if (isdigit(token[ix]))
        {
            token.erase(ix, 1);
            continue;
        }
        ix++;
    }
}

bool IsCompositeToken(const string & token)
{

    // A composite token is one that has an upper case letter in a
    // position other than the first character or contains an
    // underscore.

    for (unsigned int ix = 0; ix < token.length(); ix++)
    {
        if (token[ix] == '_' || (isupper(token[ix]) && ix != 0))
        {
            return true;
        }
    }
    return false;
}

void ProcessSimpleToken(string & token, const string & original_token,
                        const string & file, const int line_number)
{

    // Check this token for spelling; if it's misspelled, put it into
    // the BadTokens container.  The original_token string is the
    // original token in the user's file; here, token could be a
    // sub-token gotten after splitting on upper case letters and
    // underscores.  If a word is misspelled, the key into the BadTokens
    // container is the original_token, not token.

    if (g.remove_digits)
    {
        RemoveDigits(token);
    }

    // Ignore single characters
    if (token.length() < 2)
    {
        return;
    }

    string token_copy = token;
    ToLower(token_copy);

    bool is_spelled_correctly = dictionary.IsSpelledCorrectly(token_copy);

    if ((! is_spelled_correctly && ! g.negate_spell_check) ||
            (  is_spelled_correctly &&   g.negate_spell_check))
    {
        // Add it to BadTokens
        MisspelledTokensIterator it = g.BadTokens.find(original_token);
        if (it != g.BadTokens.end())
        {
            // It's already in the map
            it->second[file].insert(line_number);
        }
        else
        {
            // Add it to the map
            g.BadTokens[original_token][file].insert(line_number);
        }
    }

}

void ProcessCompositeToken(const string & composite_token, const string & file,
                           const int line_number)
{
    string composite_token_copy = composite_token;
    unsigned int ix;
    for (ix = 0; ix < composite_token_copy.length(); ix++)
    {
        // Replace all underscores by space characters
        if (composite_token_copy[ix] == '_')
        {
            composite_token_copy[ix] = ' ';
        }
        if (ix > 0)
        {
            // Insert a space character before each capital letter
            // except if it's the first character.
            if (isupper(composite_token_copy[ix]))
            {
                composite_token_copy.insert(ix, " ");
                // Update the counter so we don't create an infinite loop.
                ix++;
            }
        }
    }

    // Now process the sub-tokens as simple tokens.
    static string token;
    while (GotAnotherToken(token, composite_token_copy))
    {
        ProcessSimpleToken(token, composite_token, file, line_number);
    }
}

void SpellProcessToken(string & token, const string & file, const int line_number)
{
    if (g.perform_spell_check)
    {
        if (IsAllDigits(token)    ||
                IsAllUpperCase(token) ||
                token.length() == 1)
        {
            return;
        }
    }

    g.total_number_of_tokens++;

    if (IsCompositeToken(token) and g.split_composite_tokens)
    {
        ProcessCompositeToken(token, file, line_number);
    }
    else
    {
        ProcessSimpleToken(token, token, file, line_number);
    }

}

void TokenProcessToken(string & token, const string & file, const int line_number)
{
    // Note we use the BadWords container from the spell checking to
    // contain all the tokens.

    MisspelledTokensIterator it = g.BadTokens.find(token);
    if (it != g.BadTokens.end())
    {
        // It's already in the map
        it->second[file].insert(line_number);
    }
    else
    {
        // Add it to the map
        g.BadTokens[token][file].insert(line_number);
        g.total_number_of_tokens++;
    }
}

void ProcessLine(string & line, const string & filename, const int line_number)
{
    // Process the tokens in this line.

    ReplacePunctuationWithSpaces(line, filename, line_number);
    static string token;
    while (GotAnotherToken(token, line))
    {
        if (g.perform_spell_check)
        {
            SpellProcessToken(token, filename, line_number);
        }
        else
        {
            TokenProcessToken(token, filename, line_number);
        }
    }
}

void ProcessFile(const string & filename)
{

    // The file's tokens and symbols are found by replacing all
    // punctuation by space characters, then parsing on spaces.  If a
    // resulting token isn't found in the dictionary (or the
    // corresponding tokens in a composite word), the word is added to
    // the misspelled container, along with the file name and line
    // number.

    ifstream stream;
    stream.open(filename.c_str());
    if (! stream)
    {
        cerr << g.program_name << ": warning:  couldn't open file "
             << filename << endl;
        return;
    }

    string line;
    int line_number = 0;
    while (getline(stream, line))
    {
        ProcessLine(line, filename, ++line_number);
    }

    if (g.verbose)
    {
        cerr << ".";
    }
}

void InitializeGlobals(void)
{
#ifdef LINUX
    g.default_dictionary = "/pylib/pgm/words.2005.wayne";
#else
    g.default_dictionary = "c:/cygwin/home/Don/bin/data/words";
#endif
    g.tokens_only                       = false;
    g.include_programming_keywords      = true;
    g.remove_digits                     = true;
    g.print_times                       = false;
    g.split_composite_tokens            = false;
    g.read_files_from_stdin             = false;
    g.verbose                           = false;
    g.print_informational_statistics    = false;
    g.negate_spell_check                = false;
    g.perform_spell_check               = false;
    g.tokens_with_one_reference         = 0;
    g.maximum_number_of_references      = 0;
    g.token_max_references              = "";
    g.total_number_of_tokens            = 0;
    g.add_contractions                  = true;
    g.found_8_bit_characters            = false;
    g.flag_8_bit_characters             = false;
}

void NeedsArgument(const char *option)
{
    cerr << g.program_name << ":  " << option
         << " option requires argument" << endl;
    exit(1);
}

int SpellCheck(DictionaryContainer & dictionaries, char **argv)
{
    clock_t start, stop;
    start = clock();
    ReadDictionaries(dictionaries);
    stop = clock();
    double read_dictionary_time_sec = (stop-start)/double(CLOCKS_PER_SEC);

    start = clock();
    // Process any command line files
    string filename;
    while (*argv)
    {
        filename = *argv;
        ProcessFile(filename);
        argv++;
    }
    // Read any remaining files from stdin
    if (g.read_files_from_stdin)
    {
        while (cin >> filename)
        {
            ProcessFile(filename);
        }
    }
    stop = clock();
    double processing_time_sec = (stop-start)/double(CLOCKS_PER_SEC);

    return PrintReport(read_dictionary_time_sec, processing_time_sec);
}

int main(int argc, char **argv)
{
#if 0
    string line = "abc";
    string token = "";
    token = line;
    line = "";
    cout << "token = " << token << endl;
    cout << "line = " << line << endl;

#else
    GetProgramName(*argv);
    InitializeGlobals();
    if (argc < 2)
    {
        Usage();
    }

    // Process options
    argv++;
    DictionaryContainer dictionaries;
    string dictionary;
    bool read_in_default_dictionary = true;

    while (*argv && argv[0][0] == '-')
    {
        switch (argv[0][1])
        {
        case '8':  // Send file:offset to stderr for non-7-bit chars
            g.flag_8_bit_characters = true;
            break;
        case '@':  // Read files to process from stdin
            g.read_files_from_stdin = true;
            break;
        case 'c':  // Don't ignore common programming keywords
            g.include_programming_keywords = false;
            break;
        case 'C':  // Ignore contraction tokens
            g.add_contractions = false;
            break;
        case 'd':  // Define another dictionary file
            argv++;
            if (! *argv)
            {
                NeedsArgument("-d");
            }
            dictionary = *argv;
            dictionaries.insert(dictionary);
            break;
        case 'D':  // Default alternate default dictionary file
            argv++;
            if (! *argv)
            {
                NeedsArgument("-D");
            }
            g.default_dictionary = *argv;
            break;
        case 'g':  // Don't delete digits in tokens
            g.remove_digits = false;
            break;
        case 'h':  // Print man page
            manpage();
            break;
        case 'k':  // Split composite tokens when spelling
            g.split_composite_tokens = true;
            break;
        case 'i':  // Print informational statistics
            g.print_informational_statistics = true;
            break;
        case 'l':  // Turn on the long listing
            g.tokens_only = false;
            break;
        case 'n':  // Ignore the default dictionary
            read_in_default_dictionary = false;
            break;
        case 's':  // Perform a spell check
            g.perform_spell_check = true;
            break;
        case 't':  // Print tokens only
            g.tokens_only = true;
            break;
        case 'T':  // Print load and processing times
            g.print_times = true;
            break;
        case 'v':  // Print "." after each file processed
            g.verbose = true;
            break;
        default:
            cerr << g.program_name << ":  error:  -" << argv[0][1]
                 << " is an unrecognized option\n";
            Usage();
        }
        argv++;
    }

    // We need at least one file on the command line if we're not
    // reading files from stdin.

    if (! *argv && g.read_files_from_stdin == false)
    {
        Usage();
    }

    if (read_in_default_dictionary)
    {
        dictionaries.insert(g.default_dictionary);
    }

    if (g.perform_spell_check)
    {
        return SpellCheck(dictionaries, argv);
    }

    // Generate a token cross-reference or listing
    clock_t start, stop;
    start = clock();

    // Process any command line files
    string filename;
    while (*argv)
    {
        filename = *argv;
        ProcessFile(filename);
        argv++;
    }
    // Read any remaining files from stdin
    if (g.read_files_from_stdin)
    {
        while (cin >> filename)
        {
            ProcessFile(filename);
            cerr << ".";
        }
    }
    if (g.read_files_from_stdin)
        cerr << endl;

    stop = clock();
    double processing_time_sec = (stop-start)/double(CLOCKS_PER_SEC);

    int status = PrintReport(0.0, processing_time_sec);

    if (g.found_8_bit_characters and g.flag_8_bit_characters)
    {
        cerr << endl
             << "Note:  characters with 8th bit set were found."
             << endl;
    }

    return status;
#endif
}
