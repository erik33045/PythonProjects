"""
Erik Hendrickson
Python UniversalExtractor
2-28-14
"""
import sys
import tarfile
import os
import gzip
import bz2
import zipfile


def universal_extractor(target, file_list):
    source = os.getcwd()

    if not os.path.isdir(target):
        os.makedirs(target)

    for file_name in file_list:
        file_type = determine_file_type(file_name)

        if tarfile.is_tarfile(file_name):
            unzip_and_copy_compressed_archive(file_name, source, target)
        elif file_type == "gz":
            unzip_and_copy_compressed_gz_file(file_name, source, target)
        elif file_type == "bz2":
            unzip_and_copy_compressed_bz2_file(file_name, source, target)
        elif file_type == "zip":
            unzip_and_copy_compressed_zip_file(file_name, source, target)
        else:
            print file_name + " is not a supported file type!"


def unzip_and_copy_compressed_gz_file(filename, source, target):
    zip_file = gzip.open(filename, "rb")
    decoded = zip_file.read()
    zip_file.close()

    os.chdir(target)

    uncompressed_file = open(os.path.splitext(filename)[0], "wb")
    uncompressed_file.write(decoded)
    uncompressed_file.close()

    os.chdir(source)


def unzip_and_copy_compressed_bz2_file(filename, source, target):
    zip_file = bz2.BZ2File(filename)
    decoded = zip_file.read()
    zip_file.close()

    os.chdir(target)

    uncompressed_file = open(os.path.splitext(filename)[0], "wb")
    uncompressed_file.write(decoded)
    uncompressed_file.close()

    os.chdir(source)


def unzip_and_copy_compressed_zip_file(filename, source, target):
    zip_file = zipfile.ZipFile(filename)
    zip_file.extractall(target)
    os.chdir(source)


def unzip_and_copy_compressed_archive(filename, source, target):
    copy_directory = os.path.splitext(filename)[0]
    tar = tarfile.open(filename)
    os.chdir(target)
    tar.extractall(copy_directory)
    tar.close()
    os.chdir(source)


def determine_file_type(filename):
    file_type_dictionary = {
        "\x1f\x8b\x08": "gz",
        "\x42\x5a\x68": "bz2",
        "\x50\x4b\x03\x04": "zip",
    }

    max_len = max(len(x) for x in file_type_dictionary)

    with open(filename) as f:
        file_start = f.read(max_len)
    for key, filetype in file_type_dictionary.items():
        if file_start.startswith(key):
            return filetype

    return "no match"


if '__main__' == __name__:
    if len(sys.argv) < 3:
        print "Program invoked with not enough arguments. Closing."
        exit()

    universal_extractor(sys.argv[1], sys.argv[2:])
