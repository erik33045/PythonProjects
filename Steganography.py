import getpass
import sys
import hashlib


def steganography():
    print sys.argv
    if len(sys.argv) < 2:
        print "Not enough arguments supplied, try help for available commands"
        return

    command = sys.argv[1].lower()

    if command == "embed":
        password = get_password()
    elif command == "extract":
        password = get_password()
    elif command == "info":
        print "Info"
    elif command == "help":
        print "Help"
    else:
        print u'Could not recognize the command "%"'.format(command)
        return


def get_password():
    return hashlib.sha512(getpass.getpass()).hexdigest()


#Actions:
#embed FileToEmbedPath TargetFilePath   -- Embeds one file into another
#extract PathToFileToExtractFrom        -- Extracts an embedded file if it exists
#info PathToFile                        -- Grabs info about an embedded file if it exists
#help                                   -- Displays help


#Encoding Pattern:    @# PASSPHRASE @# FILENAME @# SIZE @# FILE @#


if __file__ == "__main__":
    steganography()