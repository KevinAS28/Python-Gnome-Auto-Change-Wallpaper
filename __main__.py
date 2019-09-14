import os
from threading import Thread
import sys
import time

msg = """
Gnome Auto Change Wallpaper v 0.1
started at: {0}
Kevin AS

Keep your mind fresh :v
""".format(time.ctime())

print(msg)

def getConfig(key):
    with open(config_file, "r+") as fs:
#        allconfig = dict()
#        for i in fs.read().split("\n"):
#            kv = i.split("=", 1)
#            print(kv)	
#            k, v = kv
#            allconfig[k] = v
#        return allconfig[key]
        return dict([i.split("=", 1) for i in fs.read().split("\n") if i!=""])[key]


real_path = os.path.dirname(os.path.realpath(__file__))
wallpaper_directory = os.path.join(real_path, "wallpaper")
config_file = os.path.join(real_path, "gacw.config")
refresh_config_rate = 1 # 1 second
#print(real_path)
log_file = os.path.join(real_path, getConfig("logfile"))

def printLog(string):
    global log_file
    with open(log_file, "w+") as fs:
        fs.write(string+"\n")
    print(string)

time_change = float(getConfig("timechange"))

wallpaper_index = 0
not_stop = True

def changeWallpaper():
    while not_stop:
        global wallpaper_index
        global time_change
        wallpaper = [i for i in os.listdir(wallpaper_directory)]
        if (wallpaper_index>=len(wallpaper)):
            wallpaper_index = 0
        command = "gsettings set org.gnome.desktop.background picture-uri file://{0}".format( os.path.join(wallpaper_directory, wallpaper[wallpaper_index]))
        #print(command)        
        os.system(command)
        wallpaper_index+=1
        time.sleep(time_change)
        
    printLog("Done. exited at {0}".format(time.ctime()))

thr = Thread(target=changeWallpaper)
thr.start()

#keep refreshing the configuration file
while True:
    try:
        new_time = float(getConfig("timechange"))
        if (new_time!=time_change):
            printLog("time changed from {0} to {1}".format(time_change, new_time))
            time_change = new_time
        time.sleep(refresh_config_rate)
    except KeyboardInterrupt:
        printLog("Control + C Captured. Exiting...")
        printLog("please wait until last wallpaper changed...")
        not_stop = False
        sys.exit(0)
        
    

