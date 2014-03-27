import getpass
import sys
import hashlib
import os

# Encoding Pattern:  PASSPHRASE @# FILENAME @# SIZE @# FILE @#


def steganography(command, args):
    if command == "embed":
        if len(args) != 2:
            print "Incorrect number of arguments for embed command, expected two."
            return
        embed(args[0], args[1])
    elif command == "extract":
        if len(args) != 1:
            print "Incorrect number of arguments for extract command, expected one."
            return
        extract(args[0])
    elif command == "info":
        if len(args) != 1:
            print "Incorrect number of arguments for info command, expected one."
            return
        else:
            info(args[0])
    elif command == "help":
        print "Help"
    else:
        print u'Could not recognize the command "{0}"'.format(command)
        return


def embed(source_file_path, target_file_path):
    """
    Embeds one file into another with a provided password
    source_file_path - Path to the file the user wishes to embed
    target_file_path - Path to the file the user wishes to embed into
    """

    source_file = get_file(source_file_path, "r")
    target_file = get_file(target_file_path, "rs")

    if source_file is None or target_file is None:
        return
    elif source_file == target_file:
        print "Cannot embed a file into itself!"
        return

    #Encoding Pattern: PASSPHRASE FILENAME @# SIZE @# FILE @#
    data_to_embed = get_password() + os.path.split(source_file_path)[1] + "@#" + str(
        source_file.__sizeof__()) + "@#" + source_file.read() + "@#"

    source_binary = convert_to_binary(data_to_embed)
    target_bytes = bytearray(target_file.read())
    data = embed_source_into_target(source_binary, target_bytes)
    target_file.close()
    write_file = open("x.jpg", "wb")
    write_file.write(data)


def embed_source_into_target(source_binary, target_byte_array):
    position = 50000
    for character in range(len(source_binary)):
        for digit in range(8):
            bit = int(source_binary[character][digit])
            value = target_byte_array[position]

            if value is 255 and bit is 1:
                target_byte_array[position] = 0
            else:
                target_byte_array[position] = value + bit

            position += 1

    return target_byte_array



def extract(file_path):
    """
    Extracts an embedded file if it exists and matches the entered password
    file_path - Path to the file the user requested to extract
    """

    source_file = get_file(file_path, "r")

    if source_file is None:
        return

    password = get_password()


def info(file_path):
    """Grabs info about an embedded file if it exists and if the password matches what was encoded.
    file_path - The path to the file the user wants to inspect"""

    source_file = get_file(file_path, "r")

    if source_file is None:
        return

    password = get_password()


def program_help():
    """Displays help"""
    print "HELP"


def convert_to_binary(contents):
    """
    Converts a string of into a list of 8 bit binary strings and returns it
    contents - the contents to be converted
    """
    binary_list = []
    for byte in bytearray(contents):
        binary = ("{0:b}".format(byte))
        while len(binary) < 8:
            binary = '0' + binary

        binary_list.append(binary)

    return binary_list


def convert_to_string(binary_list):
    """
    Converts a list of 8 bit binary strings into a string and returns it
    binary_list  - the list of binary strings
    """
    return_string = ""
    for binary in binary_list:
        return_string = return_string + chr(int(binary, 2))
    return return_string


def get_password():
    """
    Gets the password and returns a hashed version of it to the program
    """
    return hashlib.sha512(getpass.getpass()).hexdigest()


def get_file(file_path, mode):
    """Function which attempts to find the file given. If it is not found, returns None.
    file_path - path to the file the user wishes to fetch
    mode - Mode with which the file is supposed to be open
    """
    if os.path.exists(file_path):
        return open(file_path, mode)
    else:
        split_path = os.path.split(file_path)
        print u'File "{0}" could not be found'.format(split_path[1])


if __file__ == "__main__":
    if len(sys.argv) < 2:
        print "Not enough arguments supplied, try help for available commands"
    else:
        steganography(sys.argv[1], sys.argv[2:])