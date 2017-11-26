import sys
import os
import xbmc
import xbmcgui
import xbmcaddon
import threading
import time
import subprocess
import decimal
from threading import Thread

# Get global paths
addon = xbmcaddon.Addon(id='plugin.program.pidash')
addonpath = addon.getAddonInfo('path').decode("utf-8")
monitor=xbmc.Monitor()
package_ok = 0

#global used to tell the worker thread the status of the window
windowopen  = True

def kill_process(pstring):
    for line in os.popen("sudo ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        pid = int(fields[0])
	os.system("sudo kill -9  %s" % pid)

def backgroundService():
    service = os.system("/usr/bin/python " + addonpath + "/resources/pidash-server.py " + addonpath + " &")

def backgroundThread():
    t1 = Thread( target=backgroundService)
    t1.setDaemon( True )
    t1.start()

def install_picamera():
    install = os.system("sudo apt-get install -f -y python-picamera")
    if install == 0:
	picamera_check = str.strip(subprocess.check_output("dpkg -l | awk '$2==\"python-picamera\" { print $3 }'", shell=True))
	xbmcgui.Dialog().ok("$ADDON[plugin.program.pidash 30106] ","$ADDON[plugin.program.pidash 30108] " + str(picamera_check))
	backgroundThread()
    else:
	xbmcgui.Dialog().ok("$ADDON[plugin.program.pidash 30104]","$ADDON[plugin.program.pidash 30105]")
	quit()

# versioncheck python-picamera
picamera_version = str.strip(subprocess.check_output("dpkg -l | awk '$2==\"python-picamera\" { print $3 }'", shell=True))
picamera_check = picamera_version.replace("-","")

if picamera_check == "":
    dialog = xbmcgui.Dialog()
    ask = dialog.yesno("$ADDON[plugin.program.pidash 30100]","$ADDON[plugin.program.pidash 30101]")
    if ask == 1:
	install_picamera()
    else:
	xbmcgui.Dialog().ok("$ADDON[plugin.program.pidash 30109]","$ADDON[plugin.program.pidash 30110]")
	quit()

else:
    picamera_version = float(picamera_check)
    if picamera_version < 1.11:
	xbmcgui.Dialog().ok("$ADDON[plugin.program.pidash 30100]","$ADDON[plugin.program.pidash 30103] " + str(picamera_version),"\n$ADDON[plugin.program.pidash 30102]")
        install_picamera()
    else:
	backgroundThread()

# Wait
while not monitor.abortRequested():
    if monitor.waitForAbort():
	kill_process("pidash-server.py")
	break
    time.sleep(0.3)

quit()