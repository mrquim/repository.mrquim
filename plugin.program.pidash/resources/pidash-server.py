import socket
import sys
import os
import threading
import time
import datetime as dt
from threading import Thread
import imp
from PIL import Image

# import adondirpath from commandline
addondir = str.strip(sys.argv[1])

try:
    imp.find_module('picamera')
    import picamera
    from picamera import PiCamera
except ImportError:
    print >>sys.stderr, 'PiCamera-Modul muss noch installiert werden !'
    quit()

# load external xbmcclient and open connection
sys.path.append(os.path.abspath(addondir))
from xbmcclient import XBMCClient,ACTION_EXECBUILTIN
host = "127.0.0.1"
port = 9777
xbmc = XBMCClient("Dashcam-Server","")
xbmc.connect()

def xbmc_SendCommand(command):
	xbmc.send_action(command)

# Create a TCP/IP socket
sockdc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get display resolution
rescheck = str.strip(os.popen("fbset | grep geometry").read())
resarray = rescheck.split(' ')
resx = int(resarray[1])
resy = int(resarray[2])
# init preview in half size of display in center of screen
respreview_w = int(resx * 0.5)
respreview_h = int(resy * 0.5)
respreview_x = int((resx - respreview_w) / 2)
respreview_y = int((resy - respreview_h) / 2)
respreview_y_correction = 0
respreview_zoom = 1

# Initial Parameters for Cam
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 24
camera.annotate_text_size = 45
camera.awb_mode = 'auto'
camera.exposure_mode = 'auto'
camera.rotation = '0'
rearcammode = "false"
rearcamoverlay = "false"

# set default record path till addon sets correct one
recordpath = "/tmp/"
xbmc_SendCommand("SetProperty(PiDash.RecordPath," + recordpath + ",10000)")

# Bind the socket to the address given on the command line
server_address = ('127.0.0.1', 6000)
sockdc.bind(server_address)
print >>sys.stderr, 'starting up on %s port %s' % sockdc.getsockname()
sockdc.listen(1)

# define default values
camera_recording = 0
loop_recording = 0
camera_preview = 0
camera_awbmode = "auto"
camera_expmode = "auto"
camera_rearcam = 0
recordtime = 300
exit = 0

# Add default overlay for rearcam mode
sizeA=(1280,720)
img = Image.open(addondir + "/resources/overlay.png")
pad = Image.new("RGB", ( ((img.size[0] + 31) // 32) * 32, ((img.size[1] + 15) // 16) * 16))
pad.paste(img, (0, 0), img)
overlay = camera.add_overlay(pad.tostring(), size=sizeA)
overlay.alpha = 0
overlay.layer = 0

def freespace(p):
    s = os.statvfs(p)
    return s.f_bsize * s.f_bavail / 1024 / 1024 / 1024

def updateWindow():
    counter = 0
    while True:
	if camera_recording == 1:
	    camera.annotate_text = "RPi-Dashcam - " + dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	    if loop_recording == 1:
		counter = counter + 1
		if counter > recordtime:
		    camera.stop_recording()
	            time.sleep(1.0)
		    camera.start_recording(recordpath + 'PIDC_' + dt.datetime.now().strftime('%d%m%Y') + '.h264')
		    counter = 0
	if camera_recording == 0 and camera_preview == 1:
	    camera.annotate_text = ''        
        # give us a break
        time.sleep(0.3)

t1 = Thread( target=updateWindow)
t1.setDaemon( True )
t1.start()

def fsCheck():
    global camera_preview
    while True:
	if camera_preview == 1:
	    free = freespace(recordpath)
	    xbmc_SendCommand("SetProperty(PiDash.StorageFree," + str(free) + " GB,10000)")
	time.sleep(30)

t2 = Thread( target=fsCheck)
t2.setDaemon( True )
t2.start()

def updateStatus():
    if camera_recording == 1:
	xbmc_SendCommand("SetProperty(PiDash.Record,true,10000)")
    else:
	xbmc_SendCommand("SetProperty(PiDash.Record,false,10000)")

updateStatus()

def cameraStartPreview():
	global camera_rearcam, overlay, rearcamoverlay, rearcammode

	if rearcammode == "false":
	    respreview_w = int(resx * 0.5 * respreview_zoom)
    	    respreview_h = int(resy * 0.5 * respreview_zoom)
	    respreview_x = int((resx - respreview_w) / 2)
	    respreview_y = int((resy - respreview_h) / 2)
	    camera.start_preview(fullscreen=False, window = (respreview_x,respreview_y + respreview_y_correction,respreview_w,respreview_h))
	    if camera_rearcam == 1:
		overlay.layer = 0
		overlay.alpha = 0
		camera_rearcam = 0
	else:
	    overlay.layer = 3
	    if rearcamoverlay == "false":
		overlay.alpha = 0
	    else:
		overlay.alpha = 64

	    camera_rearcam = 1
	    camera.start_preview()

UDP_IP = "127.0.0.1"
UDP_PORT = 6000

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((UDP_IP, UDP_PORT))

while exit != 1:
    dataudp, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data= dataudp.rstrip('\x00')
    print "received message:", data

    if data == "Status":
        updateStatus()

    if data == "Foreground":
        if camera_preview == 0:
	    cameraStartPreview()
	    camera_preview = 1

    if data == "Background":
        if camera_preview == 1:
	    camera.stop_preview()
	    camera_preview = 0
	    overlay.layer = 0
	    overlay.alpha = 0
	    camera_rearcam = 0

    if data == "AWB":
        if camera_awbmode == "auto":
	    camera.awb_mode = 'shade'
	    camera_awbmode = "shade"
	else:
	    camera.awb_mode = 'auto'
	    camera_awbmode = "auto"
	    updateStatus()

    if data == "EXP":
        if camera_expmode == "auto":
	    camera.exposure_mode = 'nightpreview'
	    camera_expmode = "night"
	else:
	    camera.exposure_mode = 'auto'
	    camera_expmode = "auto"
	    updateStatus()

    if data == "Record":
        if camera_recording == 0:
	    if loop_recording == 0:
		camera.annotate_background = picamera.Color('black')
		camera.annotate_text = "RPi-Dashcam - " + dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
		camera.start_recording(recordpath + 'PIDC_' + dt.datetime.now().strftime('%d%m%Y') + '_' + dt.datetime.now().strftime('%H%M%S') + '.h264')
		camera_recording = 1
		updateStatus()
	    else:
		camera.annotate_background = picamera.Color('black')
		camera.annotate_text = "RPi-Dashcam - " + dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
		camera.start_recording(recordpath + 'PIDC_' + dt.datetime.now().strftime('%d%m%Y') + '.h264')
		camera_recording = 1
		updateStatus()

    if data == "Stop":
	if camera_recording == 1:
	    camera.stop_recording()
	    camera_recording = 0
	    updateStatus()

    if data == "SaveEvent":
	source = recordpath + 'PIDC_' + dt.datetime.now().strftime('%d%m%Y') + '.h264'
	destination = recordpath + 'PIDC_SAVEDEVENT_' + dt.datetime.now().strftime('%d%m%Y') + '_' + dt.datetime.now().strftime('%H%M%S') + '.h264'
	os.system("cp " + source + " " + destination)

    if "YCorrection" in data:
	splitposy = data.split(',')
	respreview_y_correction = int(splitposy[1])

    if "PosYUp" in data:
	splitposy = data.split(',')
	respreview_y_correction = int(splitposy[1])
	cameraStartPreview()

    if "PosYDown" in data:
        splitposy = data.split(',')
	respreview_y_correction = int(splitposy[1])
	cameraStartPreview()

    if "Zoom" in data:
	splitzoom = data.split(',')
	respreview_zoom = float(splitzoom[1])
	cameraStartPreview()

    if "Path" in data:
	splitpath = data.split(',')
	recordpath = splitpath[1]
	xbmc_SendCommand("SetProperty(PiDash.RecordPath," + recordpath + ",10000)")
	free = freespace(recordpath)
	xbmc_SendCommand("SetProperty(PiDash.StorageFree," + str(free) + " GB,10000)")

    if "Rotation" in data:
	splitrotation = data.split(',')
	rotation = str(splitrotation[1])
	if rotation == "0":
	    camera.rotation = '0'
	if rotation == "1":
	    camera.rotation = '90'
	if rotation == "2":
	    camera.rotation = '180'
	if rotation == "3":
	    camera.rotation = '270'

    if "AWB" in data:
	splitawb = data.split(',')
	awb = str(splitawb[1])
	if awb == "0":
	    camera.awb_mode = 'off'
	if awb == "1":
	    camera.awb_mode = 'auto'
	if awb == "2":
	    camera.awb_mode = 'sunlight'
	if awb == "3":
	    camera.awb_mode = 'cloudy'
	if awb == "4":
	    camera.awb_mode = 'shade'
	if awb == "5":
	    camera.awb_mode = 'tungsten'
	if awb == "6":
	    camera.awb_mode = 'fluorescent'
	if awb == "7":
	    camera.awb_mode = 'incandescent'
	if awb == "8":
	    camera.awb_mode = 'flash'
	if awb == "9":
	    camera.awb_mode = 'horizon'

    if "EXP" in data:
	splitexp = data.split(',')
	exp = str(splitexp[1])
	if exp == "0":
	    camera.exposure_mode = 'off'
	if exp == "1":
	    camera.exposure_mode = 'auto'
	if exp == "2":
	    camera.exposure_mode = 'night'
	if exp == "3":
	    camera.exposure_mode = 'nightpreview'
	if exp == "4":
	    camera.exposure_mode = 'backlight'
	if exp == "5":
	    camera.exposure_mode = 'spotlight'
	if exp == "6":
	    camera.exposure_mode = 'sports'
	if exp == "7":
	    camera.exposure_mode = 'snow'
	if exp == "8":
	    camera.exposure_mode = 'beach'
	if exp == "9":
	    camera.exposure_mode = 'verylong'
	if exp == "10":
	    camera.exposure_mode = 'fixedfps'
	if exp == "11":
	    camera.exposure_mode = 'antishake'
	if exp == "12":
	    camera.exposure_mode = 'fireworks'

    if "RearcamMode" in data:
	splitoverlay = data.split(',')
	rearcammode = str(splitoverlay[1])
	if rearcammode == "true":
	    xbmc_SendCommand("SetProperty(PiDash.Rearcam,true,10000)")
	else:
	    xbmc_SendCommand("SetProperty(PiDash.Rearcam,false,10000)")

    if "RearcamOverlay" in data:
	splitoverlay = data.split(',')
	rearcamoverlay = str(splitoverlay[1])

    if "RecordMode" in data:
	splitrecordmode = data.split(',')
	recordmode = str(splitrecordmode[1])
	recordtimeloop = str(splitrecordmode[2])
	if recordtimeloop == "0":
	    recordtime = 300
	if recordtimeloop == "1":
	    recordtime = 600
	if recordtimeloop == "2":
	    recordtime = 900
	if recordtimeloop == "3":
	    recordtime = 1800
	if recordtimeloop == "4":
	    recordtime = 3600
	if recordmode == "true":
	    loop_recording = 1
	else:
	    loop_recording = 0

    if "HFlip" in data:
	splitflip = data.split(',')
	hflip = str(splitflip[1])
	if hflip == "true":
	    camera.hflip = True
	else:
	    camera.hflip = False

    if "Exit" in data:
        exit = 1
        break

sock.close()
xbmc.close()
camera.close()
