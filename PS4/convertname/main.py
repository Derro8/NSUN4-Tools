'''
Renames directories to fit PS4 version
'''

import os
import sys
import shutil

from os import path

args = sys.argv[1:]

def getDirectory():
    if(len(args) > 0):
        return args[0]
    return input("Main Directory: ")

directory = getDirectory()

for root, dirs, files in os.walk(directory):
    for dir in dirs:
        if(dir != "WIN64" and dir != "PC" and dir != "OTHER"):
            continue
        shutil.move(path.join(root, dir), path.join(root, "PS4"))