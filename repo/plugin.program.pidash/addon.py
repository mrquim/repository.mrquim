import calendar
import datetime
import sys
import os
import xbmc
import xbmcgui
import xbmcaddon
import socket
import threading
import time
import subprocess
import decimal
import subprocess
import datetime as dt
from threading import Thread

# Get global paths
addon = xbmcaddon.Addon(id='plugin.program.pidash')
addonpath = addon.getAddonInfo('path').decode("utf-8")

#control
HOME_BUTTON  = 1201
BACK_BUTTON  = 1202
BUTTON_FOCUS = 1203
PLAY_BUTTON  = 1204
RECORD_BUTTON  = 1205
STOP_BUTTON  = 1206
LIST_BUTTON  = 1207
SETTINGS_BUTTON  = 1210
LIVEVIEW_UP_BUTTON  = 1211
LIVEVIEW_DOWN_BUTTON  = 1212
LIVEVIEW_PLUS_BUTTON  = 1213
LIVEVIEW_MINUS_BUTTON  = 1214
SAVE_BUTTON  = 1215

ACTION_BACK  = 92

UDP_IP = "127.0.0.1"
UDP_PORT = 6000

#global used to tell the worker thread the status of the window
windowopen  = True

def PiCam_SendCommand(command):
    # Create a TCP/IP socket with check
    try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(command, (UDP_IP, UDP_PORT))
	time.sleep(0.1)
	sock.close()

    except:
	xbmcgui.Dialog().ok("$LOCALIZE[257]","$ADDON[plugin.program.pidash 30000]")
	quit()

# Init values from addon settings
xbmcgui.Window(10000).setProperty('LiveviewControls',addon.getSetting('LiveviewControls'))
xbmcgui.Window(10000).setProperty('Pidash.Rearcam',addon.getSetting('RearcamMode'))
xbmcgui.Window(10000).setProperty('RecordMode',addon.getSetting('RecordMode'))
PiCam_SendCommand("YCorrection," + addon.getSetting('YCorrection'))

if str(os.path.exists(addon.getSetting('RecordPath'))) == "True":
    PiCam_SendCommand("Path," + addon.getSetting('RecordPath'))
else:
    PiCam_SendCommand("Path,/tmp/")
    addon.setSetting('RecordPath',"/tmp/")
    xbmcgui.Dialog().ok("$ADDON[plugin.program.pidash 30031]","$ADDON[plugin.program.pidash 30032]")

PiCam_SendCommand("Rotation," + addon.getSetting('Rotation'))
PiCam_SendCommand("AWB," + addon.getSetting('AWBMode'))
PiCam_SendCommand("EXP," + addon.getSetting('EXPMode'))
PiCam_SendCommand("Zoom," + addon.getSetting('Zoom'))
PiCam_SendCommand("RearcamMode," + addon.getSetting('RearcamMode'))
PiCam_SendCommand("RearcamOverlay," + addon.getSetting('RearcamOverlay'))
PiCam_SendCommand("RecordMode," + addon.getSetting('RecordMode') + "," + addon.getSetting('RecordTime'))
PiCam_SendCommand("HFlip," + addon.getSetting('HFlip'))
PiCam_SendCommand("Status")
PiCam_SendCommand("Foreground")

class pidash(xbmcgui.WindowXMLDialog):

    def onInit(self):
        pidash.button_home=self.getControl(HOME_BUTTON)
        pidash.button_back=self.getControl(BACK_BUTTON)
        pidash.buttonfocus=self.getControl(BUTTON_FOCUS)

    def onAction(self, action):
        global windowopen
        
    def onClick(self, controlID):

        if controlID == HOME_BUTTON:
            windowopen = False
	    PiCam_SendCommand("Background")
            self.close()

        if controlID == BACK_BUTTON:
            windowopen = False
	    PiCam_SendCommand("Background")
            self.close()

        if controlID == PLAY_BUTTON:
            windowopen = False
	    PiCam_SendCommand("Play")
	    self.setFocus(self.buttonfocus)

        if controlID == LIST_BUTTON:
            windowopen = False
	    PiCam_SendCommand("Background")
            self.close()

        if controlID == STOP_BUTTON:
            windowopen = False
	    PiCam_SendCommand("Stop")
	    self.setFocus(self.buttonfocus)

        if controlID == RECORD_BUTTON:
            windowopen = False
	    PiCam_SendCommand("Record")
	    self.setFocus(self.buttonfocus)

        if controlID == LIVEVIEW_UP_BUTTON:
            windowopen = False
	    YCorrection = int(addon.getSetting('YCorrection')) - 5
	    PiCam_SendCommand("PosYUp," + str(YCorrection))
	    addon.setSetting('YCorrection',str(YCorrection))
	    self.setFocus(self.buttonfocus)

        if controlID == LIVEVIEW_DOWN_BUTTON:
            windowopen = False
	    YCorrection = int(addon.getSetting('YCorrection')) + 5
	    PiCam_SendCommand("PosYDown," + str(YCorrection))
	    addon.setSetting('YCorrection',str(YCorrection))
	    self.setFocus(self.buttonfocus)

        if controlID == LIVEVIEW_MINUS_BUTTON:
            windowopen = False
	    Zoom = float(addon.getSetting('Zoom')) - 0.05
	    PiCam_SendCommand("Zoom," + str(Zoom))
	    addon.setSetting('Zoom',str(Zoom))
	    self.setFocus(self.buttonfocus)

        if controlID == LIVEVIEW_PLUS_BUTTON:
            windowopen = False
	    Zoom = float(addon.getSetting('Zoom')) + 0.05
	    PiCam_SendCommand("Zoom," + str(Zoom))
	    addon.setSetting('Zoom',str(Zoom))
	    self.setFocus(self.buttonfocus)

        if controlID == SAVE_BUTTON:
            windowopen = False
	    PiCam_SendCommand("SaveEvent")
	    self.setFocus(self.buttonfocus)


        if controlID == SETTINGS_BUTTON:
            windowopen = False
	    PiCam_SendCommand("Background")
	    self.setFocus(self.buttonfocus)
	    addon.openSettings()
	    xbmcgui.Window(10000).setProperty('LiveviewControls',addon.getSetting('LiveviewControls'))
	    xbmcgui.Window(10000).setProperty('Pidash.Rearcam',addon.getSetting('RearcamMode'))
	    xbmcgui.Window(10000).setProperty('RecordMode',addon.getSetting('RecordMode'))
	    PiCam_SendCommand("Path," + addon.getSetting('RecordPath'))
	    PiCam_SendCommand("Rotation," + addon.getSetting('Rotation'))
	    PiCam_SendCommand("AWB," + addon.getSetting('AWBMode'))
	    PiCam_SendCommand("EXP," + addon.getSetting('EXPMode'))
	    PiCam_SendCommand("YCorrection," + addon.getSetting('YCorrection'))
	    PiCam_SendCommand("Zoom," + addon.getSetting('Zoom'))
	    PiCam_SendCommand("RearcamMode," + addon.getSetting('RearcamMode'))
	    PiCam_SendCommand("RearcamOverlay," + addon.getSetting('RearcamOverlay'))
	    PiCam_SendCommand("RecordMode," + addon.getSetting('RecordMode') + "," + addon.getSetting('RecordTime'))
	    PiCam_SendCommand("HFlip," + addon.getSetting('HFlip'))
	    PiCam_SendCommand("Foreground")
	    self.setFocus(self.buttonfocus)

    def onFocus(self, controlID):
        pass
    
    def onControl(self, controlID):
        pass
 
dashdialog = pidash("Custom_PiDashcam.xml", addonpath, 'default', '720')

dashdialog.doModal()
del dashdialog
