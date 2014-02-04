import sys
import gzip
import tarfile
import os


def universal_extractor(target, file_list):
    source = os.getcwd()

    if not os.path.isdir(target):
        os.makedirs(target)

    for file_name in file_list:
        if tarfile.is_tarfile(file_name):
            unzip_and_copy_tar_file(file_name, source, target)
        else:
            unzip_and_copy_gzip_file(file_name, source, target)


def unzip_and_copy_gzip_file(filename, source, target):
    zip_file = gzip.open(filename, "rb")
    decoded = zip_file.read()
    zip_file.close()

    os.chdir(target)

    uncompressed_file = open(os.path.splitext(filename)[0], "wb")
    uncompressed_file.write(decoded)
    uncompressed_file.close()

    os.chdir(source)


def unzip_and_copy_tar_file(filename, source, target):
    #create the copy directory if it doesn't exist
    os.chdir(target)
    os.makedirs(os.path.splitext(filename)[0])
    copy_directory = os.path.splitext(filename)[0]
    os.chdir(source)
    tar = tarfile.open(filename)
    os.chdir(target)
    tar.extractall(copy_directory)
    tar.close()
    os.chdir(source)


if '__main__' == __name__:
    if len(sys.argv) < 3:
        print "Program invoked with not enough arguments. Closing."
        exit()
    universal_extractor(sys.argv[1], sys.argv[2:])
