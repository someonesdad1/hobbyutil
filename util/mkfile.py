'''
Make a file of specified size.
'''
# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
import sys
import getopt
import os
import random
import secrets
from pdb import set_trace as xx 

def Usage(status=1):
    name = sys.argv[0]
    print('''Usage: {name} [options] size filename
  Makes a file of specified size.  size is in bytes and can have the
  SI suffixes k, M, or G (no space between the letter and number).
 
Options:
    -b n
        Fill with byte value n (default 0).
    -r
        Fill with random bytes (uses python's random module as the
        pseudorandom number generator).
    -s seed
        Seed for the random number generator.
    -t
        Same as -r except secrets.token_bytes() is used, providing an
        allegedly cryptographically-secure set of random bytes.
    -u
        Same as -r except os.urandom() is used, providing an allegedly
        cryptographically-secure set of random bytes.
        
Notes:
    Creating a file with the -u or -t options take about the same time.
    The same file size with the -r option takes about 4 to 5 times
    longer.  With no option (filling the file with 0x00 bytes) takes 
    about 6 times as long.
'''[:-1].format(**locals()))
    sys.exit(status)

def Error(s):
    print(s, file=sys.stderr)
    exit(1)

def InterpretSize(s):
    multiplier = 1
    if s[-1] == "k":
        multiplier = 1000
        s = s[:-1]
    elif s[-1] == "M":
        multiplier = 1000*1000
        s = s[:-1]
    elif s[-1] == "G":
        multiplier = 1000*1000*1000
        s = s[:-1]
    try:
        size = int(float(s)*multiplier)
    except Exception:
        Error("'%s':  bad size specifier" % s)
    return size

def ParseCommandLine(d):
    d["-b"] = 0
    d["-r"] = False
    d["-s"] = None
    d["-t"] = False
    d["-u"] = False
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "b:rs:tu")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-b":
            d["-b"] = int(opt[1])
            if not 0 <= d["-b"] < 256:
                Error("-b option must be a byte value between 0 and 255")
        elif opt[0] == "-r":
            d["-r"] = True
        elif opt[0] == "-s":
            d["-s"] = opt[1]
            random.seed(opt[1])
        elif opt[0] == "-t":
            d["-t"] = not d["-t"]
        elif opt[0] == "-u":
            d["-u"] = not d["-u"]
    if len(args) != 2:
        Usage()
    size = InterpretSize(args[0])
    return size, args[1]

def RandomBytes(n):
    for i in range(n):
        yield "{:02x}".format(random.randint(0, 255))

def MakeFile(size, filename, d):
    chunksize = int(1e5)
    def WriteBytes(stream, byte, number_of_bytes, random_bytes):
        if random_bytes == 1:
            if 0:
                # This slow method is used because I think there's a bug in
                # what random.getrandbits() returns.
                b = [i for i in RandomBytes(number_of_bytes)]
                assert(len(b) == number_of_bytes)
                stream.write(b''.fromhex(''.join(b)))
            else:
                n = 2*number_of_bytes
                i = random.getrandbits(4*n)
                s = str(hex(i))[2:]
                if len(s) > n:
                    s = s[:n]
                elif len(s) < n:
                    while len(s) < n:
                        s += str(hex(random.getrandbits(1)))[0]
                stream.write(b''.fromhex(s))
        elif random_bytes == 2:
            stream.write(os.urandom(number_of_bytes))
        elif random_bytes == 3:
            stream.write(secrets.token_bytes(number_of_bytes))
        else:
            stream.write(bytearray([byte]*number_of_bytes))
    random_bytes = 0
    if d["-r"]:
        random_bytes = 1
    if d["-u"]:
        random_bytes = 2
    if d["-t"]:
        random_bytes = 3
    byte_value = d["-b"]
    # We'll write the file in chunks so that we don't run out of memory for
    # large files.
    try:
        ofp = open(filename, "wb")
    except Exception:
        Error("Couldn't open '%s' for writing" % filename)
    numchunks, remainder = divmod(size, chunksize)
    for i in range(numchunks):
        WriteBytes(ofp, byte_value, chunksize, random_bytes)
    if remainder:
        WriteBytes(ofp, byte_value, remainder, random_bytes)

if __name__ == "__main__":
    d = {}
    size, filename = ParseCommandLine(d)
    MakeFile(size, filename, d)
