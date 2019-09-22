"""
GACW installer for Ubuntu.
"""

import platform
import sys
import os
import shutil

config_file = "/etc/gacw.config"

#check python version
if (int(platform.python_version()[0])<3):
    print("ERROR: GACW require python 3")
    sys.exit(1)

#check su
try:
    with open("/test_su", "w+") as testsu:
        testsu.write("testsu")
except PermissionError:
    print("ERROR: Installer need super user privelege")
    sys.exit(1)


#begin asking

while True:
    install_dir = input("Installation directory (default=%s): "%(os.path.join(os.environ["HOME"], "gacw")))
    if (install_dir==""):
        install_dir=os.path.join(os.environ["HOME"], "gacw")
    try:
        shutil.copytree(os.path.join(os.getcwd(), "gacw"), install_dir)
        break
    except Exception as e:
        try:
            install_dir = os.path.join(install_dir, "gacw")
            shutil.copytree(os.path.join(os.getcwd(), "gacw"), install_dir)
            break
        except:
            pass
        print("ERROR: directory %s not writeable/empty: %s"%(install_dir, str(e)))
        print("Please select another installation directory")
        


config = {
    "timechange": ["2", "Time Change in second"],
    "logfile": [os.path.join(install_dir, "gacw.log"), "Log file location"],
    "wallpaper_dir": [os.path.join(os.environ["HOME"], "Pictures", "Wallpaper"), "Wallpaper collection directory"]
    }

try:
    os.remove(config_file)
except:
    pass
with open(config_file, "a+") as tulis:
    for key in config:
    # try:
        #os.path.join(install_dir, conf_file)
        
            ans = input("{question} (default={default}): ".format( question=config[key][1], default=config[key][0]) )
            if (ans==""):
                ans = config[key][0]
            config[key][0] = ans
            tulis.write("{k}={v}\n".format(k=key, v=ans))
    # except Exception as e:
    #     print("Error while generating config file: %s"%(str(e)))
    #     sys.exit(1)

#copy wallpaper example
try:
    shutil.copytree("gacw/wallpaper", config["wallpaper_dir"][0])
except:
    print("Please copy your wallpapers to %s"%(config["wallpaper_dir"][0]))


#generate autostart
with open("gacw_autostart.desktop", "r") as baca:
    with open("/etc/xdg/autostart/gacw_autostart.desktop", "w+") as tulis:
        tulis.write(baca.read().format(install_dir= os.path.join(install_dir, "__main__.py") ))

print("Done!!!")

# os.chdir(install_dir)
# try:
#     os.system("python3 __main__.py")
# except:
#     try:
#         os.system("python __main__.py")
#     except:
#         print("Please reboot to take change")

print("Please reboot to take change")

