###################################
# Author: Stautyr                 #
# Date: 1-5-2021                  #
# Language: Python 3.6.4          #
# Program: Auto-sort(v. 2.1)      #
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
if (DEBUG):
	print("IN DEBUGGING MODE")
	#User of system
	user = "[INSERT USER HERE]"

	#Enable if OneDrive is active
	OneDrive = True

else:
        OneDrive = False
        pathList = str(Path.cwd()).split("\\")
        user = pathList[2]
        if (pathList[3] == "OneDrive"):
                OneDrive = True

        #OneDrive check
        startPath = Path("/Users/"+user)
        if(OneDrive == False):
                                        DocPath = startPath/"Documents"
        else:
                                        DocPath = startPath/"OneDrive/Documents"


#Path shortcuts
docSort = DocPath/"Download Sort"
downloads = startPath/"downloads"
musicSort = startPath/"Music"
picSort = startPath/"Pictures/Camera Roll"
videoSort = startPath/"Videos"

#folder assignment
folders = {"doc" : docSort/"DOC FILES",
	   "exe" : docSort/"EXE FILES",
	   "jpg" : picSort/"JPG",
	   "mov" : videoSort/"Captures",
	   "mp4" : musicSort/"MP4",
	   "other" : docSort/"OTHER",
	   "pdf" : docSort/"PDFs",
	   "png" : picSort/"PNG",
	   "pptx" : docSort/"PPTX FILES",
	   "txt" : docSort/"TXT FILES",
	   "wav" : musicSort/"WAV",
	   "zip" : docSort/"ZIP FILES"}

#Checks for folders and creates them if they do not exist
def check():
	for count in folders:
		if Path(folders[count]).is_dir():
			if(DEBUG):
				print ("{} exist".format(folders[count]))
			pass
		else:
			if(DEBUG):
				print ("{} does not exist".format(folders[count]))
				print ("Creating {}".format(folders[count]))
			os.mkdir(folders[count])

def songSort(song, ext):
    if(ext == "mp3"):
        metadata = EasyID3(song)
        album = str(metadata['album'])

    elif(ext == "m4a"):
        metadata = MP4(song)
        album = str(metadata["\xa9alb"])

    elif(ext == "wma"):
        metadata = ASF(song)
        album = str(metadata["WM/AlbumTitle"])
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

#Sorting functions
def send(file, ext):
        shortExt = str(ext[1:])
        try:
                if(shortExt == "docx"):
                        folder = folders["doc"]

                elif(shortExt == "mp3" or shortExt == "m4a" or shortExt == "wma"):
                        folder = songSort(startFolder/file, shortExt)

                else:
                        folder = folders[shortExt]
        except:
                if(shortExt == "mp3" or shortExt == "m4a" or shortExt == "wma"):
                        folder = songSort(startFolder/file, shortExt)

                else:
                        print ("Other file type found: " + shortExt)
                        folder = folders["other"]
                        if (DEBUG):
                                print("Sending {} to {}".format(file,folder))
                        try:
                                shutil.move(startFolder/file, folder/file)

                        except:
                                pass
        else:
                if (DEBUG):
                        print("Sending {} to {}".format(file,folder))
                shutil.move(startFolder/file, folder/file)



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
