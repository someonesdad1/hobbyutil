/***********************************************************************
This file sums the ASCII values of the bytes in the files on the
command line  and prints various statistics to stdout.

----------------------------------------------------------------------
Copyright (C) 2012 Don Peterson
Contact:  gmail.com@someonesdad1
  
                    The Wide Open License (WOL)
  
Permission to use, copy, modify, distribute and sell this software and
its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice and this license appear in
all copies.  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT EXPRESS OR
IMPLIED WARRANTY OF ANY KIND. See
http://www.dspguru.com/wide-open-license for more information.
***********************************************************************/

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <fstream>

using namespace std;

typedef unsigned long long ulong;
typedef unsigned char uchar;

int ReadWholeFile(const string & filename, string & bytes)
{
    /* Read all the bytes from file filename into the string bytes.
    Return 0 if successful, 1 if not. */
    ifstream in(filename.c_str(), ios::binary);
    if (! in)
    {
        cerr << "Couldn't open '" << filename << "' file" << endl;
        return(1);
    }
    // Go to the end of the file so we can use in.tellg() to get the
    // file's size in bytes
    in.seekg(0, ios::end);
    // Make the string bytes' size same as file
    bytes.resize(in.tellg());
    // Reset file pointer to beginning of file
    in.seekg(0, ios::beg);
    // Read all the bytes in at once
    in.read(& bytes[0], bytes.size());
    in.close();
    // Ensure we have at least one byte
    if (bytes.empty())
    {
        cerr << "Error:  '" << filename 
             << "' file is empty or doesn't exist." << endl;
        return(1);
    }
    return(0);
}

string Normalize(const char * path)
{
    /* Replace any backslashes in path with forward slashes. */
    const string bs = "\\";
    string npath = path;
    string::size_type pos = npath.find(bs);
    while (pos != string::npos)
    {
        npath[pos] = '/';
        pos = npath.find(bs);
    }
    return npath;
}

void Usage(const string & name)
{
    cerr << "Usage:  " << name << " file1 [file2 ...]\n"
"  Reads the bytes from each file and sums their values.  The sum and\n"
"  other statistics are printed to stdout.\n"
;
    exit(1);
}

void PrintReport(const int numfiles, 
                 const ulong num_bytes, 
                 const ulong sum, 
                 const double sum_squares,
                 const uchar max,
                 const uchar min,
                 const int bad_files
                 )
{
    double mean = double(sum)/num_bytes;
    double numerator = abs(sum_squares - num_bytes*mean*mean);
    double sdev = sqrt(numerator/(num_bytes - 1));
    cout << "Number of files processed = " << numfiles << endl;
    if (bad_files)
        cout << "  (" << bad_files << " files couldn't be read)" << endl;
    cout << "  Number of bytes         = " << num_bytes   << " = 0x"
             << hex << num_bytes   << dec << endl
         << "  Sum of bytes            = " << sum         << " = 0x"
             << hex << sum         << dec << endl
         << "  Sum of squares of bytes = " << sum_squares << " = 0x"
             << hex << ulong(sum_squares) << dec << endl
         << "  Mean                    = " << mean << endl
         << "  Standard deviation      = " << sdev << endl
         << "  (min, max) byte values  = (" << int(min) << ", " 
         << int(max) << ")" << endl
         ;
}

int ProcessFile(const string & filename, 
                ulong & num_bytes,
                ulong & sum,
                double & sum_squares,
                uchar & max,
                uchar & min
               )
{
    string data;
    int rc = ReadWholeFile(filename, data);
    if (rc)
        return(rc);
    for (ulong i=0; i < data.size(); i++)
    {
        uchar c = data.c_str()[i];
        num_bytes++;
        sum += c;
        sum_squares += (c*c);
        if (c > max)
            max = uchar(c);
        if (c < min)
            min = uchar(c);
    }
    return(0);
}

int main(int numfiles, char **argv)
{
    // The key requirement is to have a >= 64 bit unsigned integer.
    if (sizeof(ulong) < 8)
    {
        cerr << "Size of ulong must be 64 bits or more" << endl;
        exit(1);
    }
    const string program_name = Normalize(argv[0]);
    argv++;
    numfiles--;
    if (! numfiles) 
        Usage(program_name);
    // Remaining argv strings will be files to open and sum their
    // bytes.
    ulong sum = 0;
    ulong num_bytes = 0;
    double sum_squares = 0;
    uchar max = 0;
    uchar min = 255;
    int bad_files = 0;
    for (int i=0; i < numfiles; i++)
    {
        int rc = ProcessFile(string(argv[i]), 
                             num_bytes, 
                             sum, 
                             sum_squares,
                             max,
                             min
                            );
        if (rc)
            bad_files++;
    }
    PrintReport(numfiles, 
                num_bytes, 
                sum, 
                sum_squares,
                max,
                min,
                bad_files
               );
}
