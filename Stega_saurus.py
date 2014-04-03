import Image
from getpass import getpass
import hashlib
import sys
import os
import itertools


class DecodedFileInfo:

    #Properties of the file stored for easy access
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
    #System args
    if len(system_args) < 2:
        print "Not enough arguments supplied, try help for available commands"
        return

    command = system_args[1]
    args = system_args[2:]

    #embed into a png image
    if command == "embed":
        if len(args) != 2:
            print "Incorrect number of arguments for embed command, expected two."
            return
        embed(args[0], args[1])
    #extract from an image
    elif command == "extract":
        if len(args) != 1:
            print "Incorrect number of arguments for extract command, expected one."
            return
        extract(args[0])
    #pull info from a file
    elif command == "info":
        if len(args) != 1:
            print "Incorrect number of arguments for info command, expected one."
            return
        else:
            info(args[0])
    #display help info
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

    #Grab the files as objects so we can work with them
    source_file = get_file(source_file_path, "r")
    target_file = get_file(target_file_path, "rb")

    #Error checking
    if source_file is None or target_file is None:
        return
    elif source_file == target_file:
        print "Cannot embed a file into itself!"
        return

    # Encoding Pattern: PASSPHRASE FILENAME @# SIZE @# FILE
    # Grabs an entered password and hashes it, gets the size of the source file and the contents
    data_to_embed = get_password() + os.path.split(source_file_path)[1] + "@#" + str(
        source_file.__sizeof__()) + "@#" + source_file.read()

    #open the image file, then convert it to RGB to modify bits
    image = Image.open(target_file_path)
    image = image.convert("RGB")

    #Encode the data into an image, then save it as a ping.
    image = encode_into_image(image, data_to_embed)
    image.save(target_file_path[:-4] + "-secret.png", 'PNG')


def extract(file_path):
    """
    Extracts an embedded file if it exists and matches the entered password
    file_path - Path to the file the user requested to extract
    """

    #Open the source file
    source_file = get_file(file_path, "r")

    #If we can't find the file, exit
    if source_file is None:
        return

    #get the password
    password = get_password()

    #Here we return the decoded string from the file
    decoded_string = decode_from_image(file_path)

    #If we can't find the password, then we throw an error
    if decoded_string.find(password) < 0:
        print "Password incorrect or file has no secret contents!"
        return
    #If we do find it, continue
    else:
        #Take out the password, it's no longer needed
        decoded_string = decoded_string[len(password):]
        #Grab the file info
        file_info = DecodedFileInfo(decoded_string)
        #Split the file name over the dot so we get something like ["blah","txt"]
        file_name_split = file_info.file_name.split(".")
        #modify the name of the file so that it shows as output
        save_file_name = file_name_split[0] + "-output." + file_name_split[1]
        #Open the new file
        save_file = open(save_file_name, "wb")
        #Save that bad boy
        save_file.write(file_info.contents)

        print "File Decoded, a file called '{0}' which is {1} bytes long has been created in the current directory."\
            .format(save_file_name, file_info.size)


def info(file_path):
    """Grabs info about an embedded file if it exists and if the password matches what was encoded.
    file_path - The path to the file the user wants to inspect"""

    #Open the source file
    source_file = get_file(file_path, "r")

    #If we can't find the file, exit
    if source_file is None:
        return

    #get the password
    password = get_password()

    #Here we return the decoded string from the file
    decoded_string = decode_from_image(file_path)

    #If we can't find the password, then we throw an error
    if decoded_string.find(password) < 0:
        print "Password incorrect or file has no secret contents!"
        return
    #If we do find it, continue
    else:
        #Remove the password from the decoded string since it's no longer needed
        decoded_string = decoded_string[len(password):]
        #Grab the file info
        file_info = DecodedFileInfo(decoded_string)
        print "There is a embedded file called '{0}' which is {1} bytes long inside the chosen file".format(
            file_info.file_name, file_info.size)


def program_help():
    """Displays help"""
    #If you need explanation of what's going on here, heaven help you
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
    #Ask for a password and return a hashed version of it
    return hashlib.sha512(getpass()).hexdigest()


def get_file(file_path, mode):
    """Function which attempts to find the file given. If it is not found, returns None.
    file_path - path to the file the user wishes to fetch
    mode - Mode with which the file is supposed to be open
    """

    #check if file exists and return the opened version of it
    if os.path.exists(file_path):
        return open(file_path, mode)
    else:
        split_path = os.path.split(file_path)
        print u'File "{0}" could not be found'.format(split_path[1])


def encode_into_image(image, payload):
    #This is the pixel array of the image
    pixels = image.load()
    #Dimensions of the image
    pwidth, pheight = image.size

    #Turn payload into a list of binary bits
    payload_bits = [bin(ord(x))[2:] for x in payload]
    #add trailing zeros to each bit
    payload_bits = [x.rjust(7, '0') for x in payload_bits]
    #turn it into a string
    payload_bits = ''.join(payload_bits)
    #add the final bits which denote the encryption is finished
    payload_bits += "0000000"

    #Iterates the payload bits
    i_bytes = iter(payload_bits)
    #Grab the number of bits to write
    num_bits = len(payload_bits)
    #Total number of rows we can write the image on
    total_rows = (num_bits / (pwidth * 3)) + 1

    if total_rows > pheight:
        print "message too long, try a larger target file!"
        exit(2)

    # main writing loop
    # pixel[x, y] - goes through and modifies each pixel
    for y in range(total_rows):
        for x in range(pwidth):
            rgb = pixels[x, y]
            pixels[x, y] = modify_pixel(list(rgb), i_bytes, x, y)
    #Return the modified image
    return image


def decode_from_image(file_path):
    #This can take awhile for large files
    print "Trying to decode, please be patient..."

    #Open the image
    image = Image.open(file_path)
    #Here is my list of pixels
    pixels = list(image.getdata())
    #The list is now in binary triplets of the LSBs ex: (1, 0, 1)
    pixels = [read_pixel(x) for x in pixels]
    #Flatten the list into a long list of binary numbers
    pixels = list(itertools.chain.from_iterable(pixels))

    #This turns the binary list int a list of lists which contain 7 bits. IE: ascii characters
    pixels = pad_and_split_7(pixels)
    pixels = list(pixels)

    #Turn that into a list of ascii characters
    pixels = [chr(int("".join([str(x) for x in li]), 2)) for li in pixels]
    #Remove the final designating null character
    pixels = pixels[:pixels.index('\x00')]
    #return the decoded file string
    return "".join([x for x in pixels])


#Modify pixels so that the LSBs for each pixel color value match a binary value 0 or 1
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


#Read the LSB for each pixel color value and return it as a binary triplet ex: [1, 0, 1]
def read_pixel(pixel):
    return [(p % 2) for p in pixel]


#Take in a list which contains binary values and returns a list of list where each entry is a padded binary list
def pad_and_split_7(l):
    for i in xrange(0, len(l), 7):
        yield l[i:i + 7]


if __name__ == "__main__":
    main(sys.argv)
