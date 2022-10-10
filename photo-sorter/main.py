#!/bin/env python3

import os
import sys
import time
import shutil
from PIL import Image, ExifTags, UnidentifiedImageError


def get_file(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            yield (root, file, file.split(".")[-1])


def get_metadata(file):
    raw_creation_datetime = time.localtime(os.path.getctime(file))
    creation_date = time.strftime("%Y-%m", raw_creation_datetime)
    return creation_date


def get_exif(file):
    try:
        img = Image.open(file)
        exif = img.getexif()
        if exif is not None:
            for key, val in exif.items():
                if ExifTags.TAGS[key] == "DateTime" and not val == "":
                    date = "-".join(val.split(":")[:2])
                    return date
        date = get_metadata(file)
    except (UnidentifiedImageError, KeyError):
        date = get_metadata(file)
    return date


def main():
    src = input(r">>> Source path: ")
    dest = input(r">>> Destination path: ")

    if not os.path.exists(dest):
        os.mkdir(dest)

    files = get_file(src)

    for path, file, extension in files:
        source = os.path.join(path, file)
        cdate = get_exif(source)
        date = os.path.join(dest, cdate)

        if not os.path.exists(date):
            os.mkdir(date)

        if not os.path.exists(os.path.join(date, extension.lower())):
            os.mkdir(os.path.join(date, extension.lower()))

        destination = os.path.join(date, extension.lower(), file)
        if not os.path.exists(destination):
            shutil.move(source, destination)

    print(">>> [*] Files sorted")


try:
    main()
except KeyboardInterrupt:
    print()
    sys.exit("[!] Ctrl-C detected")
