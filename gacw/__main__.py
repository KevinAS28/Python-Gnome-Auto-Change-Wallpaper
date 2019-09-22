import os
from threading import Thread
import sys
import time
import random

msg = """
Gnome Auto Change Wallpaper v 0.1
started at: {0}
Kevin AS

Keep your mind fresh :v
""".format(time.ctime())

print(msg)
real_path = os.path.dirname(os.path.realpath(__file__))
#config_file = os.path.join(real_path, "gacw.config")
config_file = "/etc/gacw.config"

def getConfig(key):
    try:
        with open(config_file, "r") as fs:
#        allconfig = dict()
#        for i in fs.read().split("\n"):
#            kv = i.split("=", 1)
#            print(kv)	
#            k, v = kv
#            allconfig[k] = v
#        return allconfig[key]
            return dict([i.split("=", 1) for i in fs.read().split("\n") if i!=""])[key]

    except FileNotFoundError:
        print("Configuration file not found at %s . please reinstall GACW"%(config_file))

wallpaper_directory = getConfig("wallpaper_dir")
#wallpaper_directory = os.path.join(real_path, "wallpaper")
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
        try:
            wallpaper = [i for i in os.listdir(wallpaper_directory)]
        except:
            print("Wallpaper directory at %s not found. please change it in gacw.config file"%(wallpaper_directory))
            sys.exit(1)
        if (wallpaper_index>=len(wallpaper)):
            wallpaper_index = 0
        command = "gsettings set org.gnome.desktop.background picture-uri file://{0}".format( os.path.join(wallpaper_directory, wallpaper[wallpaper_index]))
        print(command)        
        os.system(command)
        wallpaper_index+=1
        time.sleep(time_change)
        
    printLog("Done. exited at {0}".format(time.ctime()))

#handle --now
#not using argparse because we just handle 1 argument
if len(sys.argv)>1:
    if (sys.argv[1]=="--now"):
        try:
            wallpaper = [i for i in os.listdir(wallpaper_directory)]
        except:
            print("Wallpaper directory at %s not found. please change it in gacw.config file"%(wallpaper_directory))
            sys.exit(1)
        command = "gsettings set org.gnome.desktop.background picture-uri file://{0}".format( os.path.join(wallpaper_directory, wallpaper[random.randrange(0, len(wallpaper))]))
        os.system(command)
        sys.exit(0)

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
        
    

