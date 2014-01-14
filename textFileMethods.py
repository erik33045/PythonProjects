"""textFileMethods.py -- create and read text files"""

import os
# noinspection PyUnresolvedReferences
# Ignoring this unused import warning because the eval call should be able
#  to interperet math functions
import math

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
    fname = raw_input('Enter filename: ')
    print

    try:
        if not os.path.exists(fname):
            raise NameError("'%s' does not exist." % fname)
        else:
            fobj = open(fname, 'r')
            for eachLine in fobj:
                line = eachLine.strip()
                if line != "":
                    print line
            fobj.close()
    except NameError, e:
        print "ERROR: ", e


def eval_loop():
    expression = ""
    while True:
        user_input = raw_input("enter an expression to be evaluated or 'done' to quit: ")
        if user_input == "done":
            if expression == "":
                print ""
            else:
                print eval(expression)
            break
        else:
            expression = user_input


def is_palindrome(s):
    """ Returns True if s is a palindrome, False otherwise"""
    return s == s[::-1]


def rotate_word(s, i):
    """Returns a string rotated by the specfied amount"""
    word = s.lower()
    rotated_word = ""
    for letter in word:
        if ord(letter) + i > 122:
            rotated_word = rotated_word + chr((ord(letter) + i) - 26)
        elif ord(letter) + i < 97:
            rotated_word = rotated_word + chr((ord(letter) + i) + 26)
        else:
            rotated_word = rotated_word + chr((ord(letter) + i))
    print rotated_word


if __name__ == '__main__':
    eval_loop()

    while True:
        entry = raw_input('(r)ead, (c)reate, or (q)uit: ')
        if entry.lower() == "q":
            break
        elif entry.lower() == "r":
            read_text_file()
        elif entry.lower() == "c":
            create_text_file()