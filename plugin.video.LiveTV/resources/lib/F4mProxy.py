"""
XBMCLocalProxy 0.1
Copyright 2011 Torben Gerkensmeyer
 
Modified for F4M format by Shani
 
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""
 
import base64
import re
import time
import urllib
import urllib2
import sys
import traceback
import socket
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urllib import *
import urlparse

import xbmc
import thread
import zlib
from StringIO import StringIO
import hmac
import hashlib
import base64
import threading 
import xbmcgui,xbmcplugin
import xbmc 
import hashlib
g_stopEvent=None
g_downloader=None
HOST_NAME = '127.0.0.1'
PORT_NUMBER = 55333

class f4mProxy():

    def start(self,stopEvent,port=PORT_NUMBER):
        global PORT_NUMBER
        global HOST_NAME
        global g_stopEvent
        print 'port',port,'HOST_NAME',HOST_NAME
        g_stopEvent = stopEvent
        #socket.setdefaulttimeout(10)
        #server_class = ThreadedHTTPServer
        #MyHandler.protocol_version = "HTTP/1.1"
        #MyHandler.protocol_version = "HTTP/1.1"
        #httpd = server_class((HOST_NAME, port), MyHandler)
        #
        #print "XBMCLocalProxy Starts - %s:%s" % (HOST_NAME, port)
        #while(True and not stopEvent.isSet()):
        #    httpd.handle_request()
        #httpd.server_close()
        #print "XBMCLocalProxy Stops %s:%s" % (HOST_NAME, port)
    def prepare_url(self,url,proxy=None, use_proxy_for_chunks=True,port=PORT_NUMBER, maxbitrate=0,simpleDownloader=False,auth=None, streamtype='HDS',swf=None):
        global PORT_NUMBER
        global PORT_NUMBER
        #newurl=urllib.urlencode({url,,'streamtype':streamtype})
        #link = url+'?maxbitrate='+maxbitrate+'&streamtype='+streamtype
        return (url) #make a url that caller then call load into player

class f4mProxyHelper():

    def playF4mLink(self,url,name,proxy=None,use_proxy_for_chunks=False, maxbitrate=0, simpleDownloader=False, auth=None, streamtype='HDS',setResolved=False,swf=None, iconImage=None):
        try:
            #print "URL: " + url
            stopPlaying=threading.Event()
            progress = xbmcgui.DialogProgress()
            #import checkbad
            #checkbad.do_block_check(False)

            
            f4m_proxy=f4mProxy()
            stopPlaying.clear()
            runningthread=thread.start_new_thread(f4m_proxy.start,(stopPlaying,))
            progress.create('Live!t-TV')
            stream_delay = 1
            progress.update( 20, "", 'A abrir: '+name, "" )
            xbmc.sleep(stream_delay*1000)
            progress.update( 100, "", 'Por favor, Aguarde.', "" )
            url_to_play=f4m_proxy.prepare_url(url,proxy,use_proxy_for_chunks,maxbitrate=maxbitrate,simpleDownloader=simpleDownloader,auth=auth, streamtype=streamtype, swf=swf)
            
            listitem = xbmcgui.ListItem(name,path=url_to_play,iconImage=iconImage, thumbnailImage=iconImage)
            try: listitem.setArt({'icon': iconImage, 'thumb': iconImage})
            except: pass
            listitem.setInfo('video', {'Title': name})


            if setResolved:
                return url_to_play, listitem
            mplayer = MyPlayer()    
            mplayer.stopPlaying = stopPlaying
            progress.close() 
            mplayer.play(url_to_play,listitem)
           
            #xbmc.Player().play(url, listitem)
            firstTime=True
            played=False
            while True:
                if stopPlaying.isSet():
                    break;
                if xbmc.Player().isPlaying():
                    played=True
                #xbmc.log('Sleeping...')
                xbmc.sleep(220)
                #if firstTime:
                #    xbmc.executebuiltin('Dialog.Close(all,True)')
                #    firstTime=False
            stopPlaying.isSet()

            #print 'Job done'
            return played
        except: return False




class MyPlayer (xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def play(self, url, listitem):
        print 'Now im playing... %s' % url
        self.stopPlaying.clear()
        xbmc.Player( ).play(url, listitem)
        
    def onPlayBackEnded( self ):
        # Will be called when xbmc stops playing a file
        print "seting event in onPlayBackEnded " 
        self.stopPlaying.set();
        print "stop Event is SET" 
    def onPlayBackStopped( self ):
        # Will be called when user stops xbmc playing a file
        print "seting event in onPlayBackStopped " 
        self.stopPlaying.set();
        print "stop Event is SET" 


            