###################################
# Author: Stautyr                 #
# Date: 7-16-2020                 #
# Language: Python 3.6.4          #
# Program: Auto-sort(v. 2.0)      #   
###################################

#Setup
from mutagen.asf import ASF         #
from mutagen.easyid3 import EasyID3 # if an error occurs, you may need to pip install mutagen, shutil, and os
from mutagen.mp4 import MP4         # 
import os
import shutil
import send2trash
from pathlib import Path

DEBUG = False

#User of system
user = "[ENTER USER HERE]"

#Enable if OneDrive is active
OneDrive = False

#OneDrive check
startPath = Path("/Users/"+user)
if(OneDrive == False):
                 DocPath = startPath/"Documents"
else:
                 DocPath = startPath/"OneDrive/Documents"

#Path shortcuts
compSci = DocPath/"Comp Sci Stuff"
docSort = DocPath/"Download Sort"
downloads = startPath/"downloads"
musicSort = startPath/"Music"
picSort = startPath/"Pictures/Camera Roll"
solidworks = DocPath/"SOLIDWORKS"
videoSort = startPath/"Videos"

#folder assignment
doc = docSort/"DOC FILES"
exe = docSort/"EXE FILES"
jpg = picSort/"JPG"
lvix =  videoSort/"LVIX"
mov = videoSort/"Captures"
mp4 = musicSort/"MP4"
other = docSort/"OTHER"
pdf = docSort/"PDFs"
placeholder = "Not setup yet"
png = picSort/"PNG"
pptx = docSort/"PPTX FILES"
psarc = docSort/"PSARC FILES"
py = compSci/"Python Scripts/Download Sort"
sldasm = solidworks/"SOLIDWORKS Assembly"
sldprt = solidworks/"SOLIDWORKS Parts"
txt = docSort/"TXT FILES"
wav = musicSort/"WAV"
zipFolder = docSort/"ZIP FILES"

#Checks for folders and creates them if they do not exist 
def check():
    folders = [doc, exe, jpg, lvix, mov, mp4, other, pdf, png, pptx, psarc, py, sldasm, sldprt, txt, wav, zipFolder]
    for count in range(len(folders)):
                 if Path(folders[count]).is_dir():
                     if(DEBUG):
                        print ("{} exist".format(folders[count]))
                 else:
                     if(DEBUG):
                         print ("{} does not exist".format(folders[count]))
                         print ("Creating {}".format(folders[count]))
                     os.mkdir(folders[count])

#Sorting functions
def send(file, ext):
    """Sends files to their sorted locations based on the file extension. 
    If not extension is not listed then it is sent to other by default."""
    if(ext == ".doc" or ext == ".docx"):
        folder = doc

    elif(ext == ".exe"):
        folder = exe

    elif(ext == ".jpg"):
        folder = jpg

    elif(ext == ".lvix"):
        folder = lvix

    elif(ext == ".mov"):
        folder = mov

    elif(ext == ".mp3" or ext == ".m4a" or ext == ".wma"):
        folder = songSort(startFolder/file, ext)

    elif(ext == ".mp4"):
        folder = mp4

    elif(ext == ".pdf"):
        folder = pdf

    elif(ext == ".png"):
        folder = png

    elif(ext == ".pptx"):
        folder = pptx

    elif(ext == ".psarc"):
        folder = psarc
        
    elif(ext == ".py"):
        folder = py

    elif(ext == ".sldasm"):
        folder = sldasm
        
    elif(ext == ".sldprt"):
        folder = sldprt

    elif(ext == ".txt"):
        folder = txt

    elif(ext == ".wav"):
        folder = wav
   
    elif(ext == ".zip"):
        folder = zipFolder
        
    else:
        print ("Other file type found: " + ext)
        folder = other    
    
    if(folder == placeholder):
        print ("Cannot send '{}'. File path not setup yet".format(file))
        
    else:
        if (DEBUG):
            print("Sending {} to {}".format(file,folder))
        shutil.move(startFolder/file, folder/file)        

def songSort(song, ext):
    if(ext == ".mp3"):
        metadata = EasyID3(song)
        album = str(metadata['album'])
    
    elif(ext == ".m4a"):
        metadata = MP4(song)
        album = str(metadata["\xa9alb"])
    
    elif(ext == ".wma"):
        metadata = ASF(song)
        album = str(metadata["WM/AlbumTitle"])

    if (ext == ".wma"):
        album = album[22:-3]
    else:
        album = album[2:-2]

    albumList = os.listdir(musicSort/"Albums")
    
    #album folder check
    if (album not in albumList):
        if(DEBUG):
            print(song)
            print(album + " not found")
        os.mkdir(musicSort/"Albums"/album)
    return(musicSort/"Albums"/album)

def delEmpty(startFolder):
    for folderName, subfolders, filenames in os.walk(startFolder):
        folderSize = os.path.getsize(folderName)
        if (folderSize == 0):
            if (DEBUG):
                print(folderName + " is empty \n deleting " + folderName)
            send2trash.send2trash(folderName)

###########################################################################################
#                                        MAIN PROGRAM                                     #
###########################################################################################

#Checks for valid folders
check()

#starting point
startFolder = downloads

#Sorting method
o = os.listdir(startFolder)                  #creates list of all files in starting folder
for x in range(len(o)):
    file = o[x] 
    ext = os.path.splitext(file)[-1].lower() #isolates file extension
    if(DEBUG):
        print(ext)
    send(file, ext)                          #sorts file

