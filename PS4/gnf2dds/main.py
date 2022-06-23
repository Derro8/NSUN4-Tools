
'''
 Scans through all the xfbins in the given directory then replaces dds data with gnf data.
'''

import sys
import os
import subprocess
import shutil

from random import randint
from os import path
from threading import Thread


currentDirectory = __file__.replace(__file__.split("/")[len(__file__.split("/")) - 1],"")
args = sys.argv[1:]

def getDirectory():
    if(len(args) > 0):
        return args[0]
    return input("Main Directory: ")

def convertXFBin(file):
    with open(file, "rb") as f:
        data = f.read()
    if(data.find(b'.dds\x00')==-1):
        return
    data = data.replace(b'.dds\x00',b'.gnf\x00')
    for i in range(1,len(data.split(b'DDS\x20\x7C'))):
        startIndex = data.find(b'DDS\x20\x7C')
        fileSizeBytes = data[startIndex-3:startIndex]
        fileSize = int.from_bytes(data[startIndex-3:startIndex],"big")
        ddsData = data[startIndex:startIndex+fileSize]
        randomName = str(randint(0, len(ddsData) ^ 32))
        with open(currentDirectory+randomName+".dds","wb") as f:
            f.write(ddsData)
        subprocess.call([currentDirectory+"orbis-image2gnf.exe","-i",currentDirectory+randomName+".dds", "-o",currentDirectory+"gnf/"+randomName+".gnf","-f","Auto","-q"])
        os.remove(currentDirectory+randomName+".dds")
        with open(currentDirectory+"gnf/"+randomName+".gnf", "rb") as f:
            gnfData = f.read()
        data = data.replace(ddsData, gnfData)
        data = data.replace(fileSizeBytes, int.to_bytes(len(gnfData), 3, "big"))
        data = data.replace(int.to_bytes(fileSize + 4, 3, "big"), int.to_bytes(len(gnfData) + 4, 3, "big"))
    with open(file, "wb") as f:
        f.write(data)
def scanDirectory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            t = Thread(target=convertXFBin, args=[path.join(root, file)])
            t.start()

scanDirectory(getDirectory())


shutil.rmtree(currentDirectory + "gnf")

os.mkdir(currentDirectory + "gnf")

