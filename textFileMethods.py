#!/usr/bin/env pytho

"""textFileMethods.py -- create and read text files"""

import os

#This specifies which character separates folders in the path,
#  since its OS dependent
ls = os.linesep


def create_text_file():
    """Function which prompts for a file name, attempts to open that file, then writes text inputted by the user"""
    fname = raw_input('Enter filename: ')

    # attempt to create file
    try:
        if os.path.exists(fname):
            raise NameError("'%s' File Already Exists." % fname)
    except NameError, e:
        print "ERROR: ", e

    # get file content (text) lines
    input_data = []
    print "\nEnter lines ('.' by itself to quit).\n"

    # loop until user terminates input
    while True:
        line = raw_input('> ')
        if line == '.':
            break
        else:
            input_data.append(line)

    # write lines to file with proper line-ending
    fobj = open(fname, 'w')
    fobj.writelines(['%s%s' % (x, ls) for x in input_data])
    fobj.close()

    print 'DONE!'


def read_text_file():
    """Function which prompts for a file name, then attempts to read that file"""
    # get filename
    fname = raw_input('Enter filename: ')
    print

    if not os.path.exists(fname):
        print "ERROR: '%s' does not exist" % fname
    else:
        fobj = open(fname, 'r')
        for eachLine in fobj:
            print eachLine
        fobj.close()


if __name__ == '__main__':
    while True:
        entry = raw_input('(r)ead, (c)reate, or (q)uit: ')
        if entry.lower() == "q":
            break
        elif entry.lower() == "r":
            read_text_file()
        elif entry.lower() == "c":
            create_text_file()