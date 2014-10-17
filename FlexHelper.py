__author__ = 'juju'
import datetime
import time


#Post: Returns current running Operating System - Used to determine if we are using Windows or mac
def getPlatform():
	return str(platform.system())

#Post: Returns current time as string so we can use it for logging
def getNow():
	return str(datetime.datetime.now())

#Post: Generates a filename sufficient date string
def getNowFilename():
	return str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))

#Pre: Given a time and type of wait will wait for a given amount of time
#Post: Waited for the given amount of time and exits
def litewait(WAITTIME,TYPE):
    if TYPE=="s":
        print getNow() + ": Waiting for: " + str(WAITTIME) + " seconds"
        time.sleep(WAITTIME)
    if TYPE=="m":
        WAITTIME=WAITTIME*60
        print getNow() + ": Waiting for: " + str(WAITTIME/60) + " minutes"
        time.sleep(WAITTIME)
    if TYPE=="h":
        WAITTIME=(WAITTIME*60)*60
        print getNow() + ": Waiting for: " + str((WAITTIME/60)/60) + " hours"
        time.sleep((WAITTIME*60)*60)

#Pre: Given a clear text string log it to the given FILENAMEPATH
#Post: Logs the given clear text into the filenamepath
def log(DATA,FILENAMEPATH,FILEHANDLESETTING):
    file = open(FILENAMEPATH, FILEHANDLESETTING)
    file.write( getNow() + ": " + DATA)
    file.close()