from PIL import Image
from getpass import getpass
import hashlib
import sys
import os
import itertools


class DecodedFileInfo:
    file_name = ""
    size = ""
    contents = ""

    def __init__(self, decoded_string):
        self.file_name = decoded_string[0:decoded_string.find("@#")]
        decoded_string = decoded_string[len(self.file_name) + 2:]
        self.size = decoded_string[0:decoded_string.find("@#")]
        decoded_string = decoded_string[len(self.size) + 2:]
        self.contents = decoded_string


def main(system_args):
    if len(system_args) < 2:
        print "Not enough arguments supplied, try help for available commands"
        return

    command = system_args[1]
    args = system_args[2:]

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
        program_help()
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
    target_file = get_file(target_file_path, "rb")

    if source_file is None or target_file is None:
        return
    elif source_file == target_file:
        print "Cannot embed a file into itself!"
        return

    # Encoding Pattern: PASSPHRASE FILENAME @# SIZE @# FILE
    data_to_embed = get_password() + os.path.split(source_file_path)[1] + "@#" + str(
        source_file.__sizeof__()) + "@#" + source_file.read()

    image = Image.open(target_file_path)
    image = image.convert("RGB")

    image = encode_into_image(image, data_to_embed)
    image.save(target_file_path[:-4] + "-secret.png", 'PNG')


def extract(file_path):
    """
    Extracts an embedded file if it exists and matches the entered password
    file_path - Path to the file the user requested to extract
    """

    source_file = get_file(file_path, "r")

    if source_file is None:
        return

    password = get_password()

    decoded_string = decode_from_image(file_path)
    if decoded_string.find(password) < 0:
        print "Password incorrect or file has no secret contents"
        return
    else:
        decoded_string = decoded_string[len(password):]
        file_info = DecodedFileInfo(decoded_string)
        file_name_split = file_info.file_name.split(".")
        save_file_name = file_name_split[0] + "-output." + file_name_split[1]
        save_file = open(save_file_name, "wb")
        save_file.write(file_info.contents)

        print "File Decoded, a file called '{0}' which is {1} bytes long has been created in the current directory."\
            .format(save_file_name, file_info.size)


def info(file_path):
    """Grabs info about an embedded file if it exists and if the password matches what was encoded.
    file_path - The path to the file the user wants to inspect"""

    source_file = get_file(file_path, "r")

    if source_file is None:
        return

    password = get_password()

    decoded_string = decode_from_image(file_path)
    if decoded_string.find(password) < 0:
        print "Password incorrect or file has no secret contents"
        return
    else:
        decoded_string = decoded_string[len(password):]
        file_info = DecodedFileInfo(decoded_string)
        print "There is a embedded file called '{0}' which is {1} bytes long inside the chosen file".format(
            file_info.file_name, file_info.size)


def program_help():
    """Displays help"""
    print "\nStega_saurus.py - A simple command line application which will hide a file into a .PNG file."
    print "\nAvailable commands: "
    print "embed - Embeds one file into another with a provided password"
    print "\tsource_file_path - Path to the file the user wishes to embed"
    print "\ttarget_file_path - Path to the file the user wishes to embed into"
    print "extract - Extracts an embedded file if it exists and matches the entered password"
    print "\tfile_path - Path to the file the user requested to extract"
    print "info - Grabs info about an embedded file if it exists and if the password matches what was encoded."
    print "\tfile_path - The path to the file the user wants to inspect"
    print "help - Displays this help!"
    print "\nGroup project created by Mark Brophy, Erik Hendrickson, and Astrid Suarez"


def get_password():
    """
    Gets the password and returns a hashed version of it to the program
    """
    return hashlib.sha512(getpass()).hexdigest()


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


def encode_into_image(cover_image, payload):
    pixels = cover_image.load()
    pwidth, pheight = cover_image.size

    payload_bits = [bin(ord(x))[2:] for x in payload]
    payload_bits = [x.rjust(7, '0') for x in payload_bits]
    payload_bits = ''.join(payload_bits)
    payload_bits += "0000000"

    i_bytes = iter(payload_bits)
    num_bits = len(payload_bits)
    total_rows = (num_bits / (pwidth * 3)) + 1

    if total_rows > pheight:
        print "message too long"
        exit(2)

    # main writing loop
    # pixel[x, y]
    for y in range(total_rows):
        for x in range(pwidth):
            # print (x,y)
            rgb = pixels[x, y]
            pixels[x, y] = modify_pixel(list(rgb), i_bytes, x, y)
    return cover_image


def decode_from_image(file_path):
    print "Trying to decode, please be patient..."
    cover_image = Image.open(file_path)
    pixels = list(cover_image.getdata())
    pixels = [read_pixel(x) for x in pixels]
    pixels = list(itertools.chain.from_iterable(pixels))
    pixels = split_7(pixels)
    pixels = list(pixels)
    pixels = [chr(int("".join([str(x) for x in li]), 2)) for li in pixels]
    pixels = pixels[:pixels.index('\x00')]
    return "".join([x for x in pixels])


def modify_pixel(pixel, iterb, i, j):
    out = []
    for p in pixel:
        try:
            i = iterb.next()
            if (p % 2) == 0:
                if i == '1':
                    out.append(p + 1)
                else:
                    out.append(p)
            else:
                if i == '0':
                    out.append(p - 1)
                else:
                    out.append(p)
        except StopIteration:
            out.append(p)

    return tuple(out)


def read_pixel(pixel):
    return [(p % 2) for p in pixel]


def split_7(l):
    for i in xrange(0, len(l), 7):
        yield l[i:i + 7]


main(sys.argv)
