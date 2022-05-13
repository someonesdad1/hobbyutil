'''
Make a file of specified size
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Make a file of specified size
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import os
    import secrets
    import random
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
def Error(*s):
    print(*s, file=sys.stderr)
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
    d["-b"] = None
    d["-r"] = False
    d["-s"] = None
    d["-u"] = False
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "b:rs:u")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "ru":
            d[o] = not d[o]
        if o == "-b":
            d["-b"] = int(a)
            if not 0 <= d["-b"] < 256:
                Error("-b option must be an integer between 0 and 255")
        elif o == "-s":
            d["-s"] = a
            random.seed(a)
    if len(args) != 2:
        Usage()
    size = InterpretSize(args[0])
    return size, args[1]
def Usage(status=1):
    print(dedent(f'''
    Usage: {sys.argv[0]} [options] size filename
      Makes a file of specified size.  size is in bytes and can have the
      SI suffixes k, M, or G (no space between the letter and number).
      The default is to fill the file with random bytes using the
      secrets.token_bytes() method.  The -r method is about 3 times slower
      than the other methods.
    Options:
      -b n      Fill with byte value n
      -r        Fill with pseudorandom bytes (uses random module)
      -s seed   Seed for the -r random number generator
      -u        Same as -r except os.urandom() is used
    '''))
    exit(status)
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
    random_bytes = 3    # secrets.token_bytes() method
    if d["-b"] is not None:
        random_bytes = 0
    elif d["-r"]:
        random_bytes = 1
    elif d["-u"]:
        random_bytes = 2
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
    size, file = ParseCommandLine(d)
    MakeFile(size, file, d)
