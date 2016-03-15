#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import shutil
import random
import socket
import time
import urllib
import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon

#addon = xbmcaddon.Addon()
#addonID = addon.getAddonInfo('id')
addonID = 'plugin.video.vevo_tv'
addon = xbmcaddon.Addon(id=addonID)
pluginhandle = int(sys.argv[1])
socket.setdefaulttimeout(30)
opener = urllib2.build_opener()
xbox = xbmc.getCondVisibility("System.Platform.xbox")
icon = xbmc.translatePath('special://home/addons/'+addonID+'/icon.png')
addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
simpleChannelsFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/simple.channel")
advancedChannelsDir = xbmc.translatePath("special://profile/addon_data/"+addonID+"/advanced")
playlistsDir = xbmc.translatePath("special://profile/addon_data/"+addonID+"/playlists")
libDir = xbmc.translatePath("special://profile/addon_data/"+addonID+"/library")
tv1 = addon.getSetting("tv1") == "true"
tv2 = addon.getSetting("tv2") == "true"
tv3 = addon.getSetting("tv3") == "true"
tv4 = addon.getSetting("tv4") == "true"
cat1 = addon.getSetting("cat1") == "true"
cat2 = addon.getSetting("cat2") == "true"
cat3 = addon.getSetting("cat3") == "true"
cat4 = addon.getSetting("cat4") == "true"
cat5 = addon.getSetting("cat5") == "true"
cat6 = addon.getSetting("cat6") == "true"
cat7 = addon.getSetting("cat7") == "true"
cat8 = addon.getSetting("cat8") == "true"
cat9 = addon.getSetting("cat9") == "true"
cat10 = addon.getSetting("cat10") == "true"
cat11 = addon.getSetting("cat11") == "true"
cat12 = addon.getSetting("cat12") == "true"
cat13 = addon.getSetting("cat13") == "true"
blacklist = addon.getSetting("blacklist").split(',')
showInfo = addon.getSetting("showInfo") == "true"
infoType = addon.getSetting("infoType")
infoDelay = int(addon.getSetting("infoDelay"))
infoDuration = int(addon.getSetting("infoDuration"))
resolutionOfficial = addon.getSetting("resolutionOfficial")
resolutionOfficial = ["1672000", "2640000", "4000000"][int(resolutionOfficial)]
resolutionCustom = addon.getSetting("resolutionCustom")
resolutionCustom = ["640x360", "960x540", "1280x720", "1920x1080"][int(resolutionCustom)]
cdnCustom = addon.getSetting("cdnCustom")
cdnCustom = ["hls-aws", "hls-aka", "hls-lvl3"][int(cdnCustom)]
userAgent = "Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0"
opener.addheaders = [('User-Agent', userAgent)]
urlMainApi = "http://api.vevo.com/mobile/v1"
urlMain = "http://www.vevo.com"

if not os.path.isdir(addonUserDataFolder):
    os.mkdir(addonUserDataFolder)
if not os.path.isdir(advancedChannelsDir):
    os.mkdir(advancedChannelsDir)
if not os.path.isdir(playlistsDir):
    os.mkdir(playlistsDir)
if len(os.listdir(playlistsDir))==0:
    fh = open(os.path.join(playlistsDir, 'new artists (dutch)'), 'w')
    fh.write("33347ae5-f4b5-4ff0-a83e-646899eece75")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (american)'), 'w')
    fh.write("1bdbc337-36e8-4864-b60f-7de6d6eb6be7")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (canadian)'), 'w')
    fh.write("a341cbb0-6ae4-42b9-bad7-bc452db77795")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (english)'), 'w')
    fh.write("799962e0-1e5a-4e50-aec1-af35b81cb775")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (british)'), 'w')
    fh.write("7a1fec0d-5efd-45aa-946b-84e69d0cd225")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (irish)'), 'w')
    fh.write("799962e0-1e5a-4e50-aec1-af35b81cb775")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (australian)'), 'w')
    fh.write("495ee93b-7e14-4319-beae-6ed6e176e46e")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (polish)'), 'w')
    fh.write("63384529-32c2-498a-bce1-4d23367a79b1")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (spanish)'), 'w')
    fh.write("b2a83aea-8cee-4509-82d7-b73a97cff949")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (portugese)'), 'w')
    fh.write("af1abbc6-c937-45f9-8a89-354a32ed7aba")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (french)'), 'w')
    fh.write("472cd938-bc76-4db9-a671-9c50a169b090")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (dutch)'), 'w')
    fh.write("76ba2991-5791-48a2-a28e-f1074d356ccb")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (italian)'), 'w')
    fh.write("9e122f0f-f4b4-401d-a67d-cd9f0a0cec2b")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'featured (german)'), 'w')
    fh.write("819d8490-9250-41a3-b188-e39ab956cc17")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (american'), 'w')
    fh.write("8b75ba3c-4322-4946-9288-949b6ac1bf5b")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (german)'), 'w')
    fh.write("4d9ce4e3-3391-45cf-a472-b968ef6f4ba9")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (italian)'), 'w')
    fh.write("eede427e-06e1-489e-8493-312dd8774940")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (polish)'), 'w')
    fh.write("1b463ddf-3303-42e9-8931-e7f83a4edcd4")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (french)'), 'w')
    fh.write("692d8694-34d5-4aed-a5cc-7eb672c5d3a5")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (brazilian)'), 'w')
    fh.write("f36806ad-afa9-4e18-a531-1a0ae20226ba")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (spanish)'), 'w')
    fh.write("97f0ef24-5950-4c88-9b87-2a384ac639a7")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (dutch)'), 'w')
    fh.write("93f9a5ee-7543-4281-a6b4-0cc5403329a0")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (australian)'), 'w')
    fh.write("20cf8575-867f-43c1-bc28-b04cda70d47c")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (british)'), 'w')
    fh.write("37de2753-b687-4fcb-81e0-88a64aeec570")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'staff picks (mexican)'), 'w')
    fh.write("8414fece-92e4-4a40-bf2f-226628321115")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (american)'), 'w')
    fh.write("cdefd9b9-6401-481d-a063-c8f77435b29d")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (german)'), 'w')
    fh.write("07422048-d4b0-4660-9e03-a15166474238")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (italian)'), 'w')
    fh.write("de10ea42-b6c9-47c7-9b1d-f05174fedf8c")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (polish)'), 'w')
    fh.write("ae064eaf-dedf-421b-9a75-65f3801bac23")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (french)'), 'w')
    fh.write("44e59183-a622-4061-a248-25802f440b0e")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (brazilian)'), 'w')
    fh.write("7cf20646-7516-4052-9587-ae151a84ae77")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (spanish)'), 'w')
    fh.write("9d03262b-fa86-48ab-a6d0-3da73df05066")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (dutch)'), 'w')
    fh.write("ae064eaf-dedf-421b-9a75-65f3801bac23")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (australian)'), 'w')
    fh.write("e743b4f5-c707-4f49-9688-d74f88a9f513")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (british)'), 'w')
    fh.write("188abb56-1a28-4478-9237-04d5a3349182")
    fh.close()
    fh = open(os.path.join(playlistsDir, 'emerging artists (mexican)'), 'w')
    fh.write("ad30fa43-7c9e-40f3-a717-eab83174fb31")
    fh.close()


def index():
    if tv1:
        addLink(translation(30150), "TIVEVSTRUS00", 'playOfficial', "")
    if tv2:
        addLink(translation(30151), "TIVEVSTRUS01", 'playOfficial', "")
    if tv3:
        addLink(translation(30152), "TIVEVSTRUS02", 'playOfficial', "")
    if tv4:
        addLink(translation(30153), "TIVEVSTRDE00", 'playOfficial', "")
    addDir(translation(30001), "default", 'customMain', "")
    addDir(translation(30002), "live", 'customMain', "")
    addDir(translation(30003), "", 'listPlaylists', "")
    addDir(translation(30004), "", 'listChannelsAdvancedMain', "")
    xbmcplugin.endOfDirectory(pluginhandle)
    
#api.vevo.com/mobile/v1/genre/list.json responses seems to depend on the country
    #and does not always return all genres that are listed on the website

def customMain(type):
    if type == "default":
        currentMode = 'listCustomModes'
    elif type == "live":
        currentMode = 'listCustomModesLive'
    content = opener.open(urlMain+"/browse").read()
    data=re.findall('browseCategoryList(.*?)]',content,re.S)[0]
    for id, title in re.findall('id":"(.*?)","loc":"(.*?)"',data,re.S):
		print id
		print title
		addDir(title, id, currentMode, "")
    xbmcplugin.endOfDirectory(pluginhandle)
   # else:
        #xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30030)+',5000)')


def listCustomModes(id, type=""):
    genres = ""
    if id != "all":
        genres = "genres="+id+"&"
    isLive = ""
    if type == "live":
        isLive = "&islive=true"
    if cat1:
        addDir(translation(30130), urlMainApi+"/video/list.json?"+genres+"order=MostViewedToday&offset=0&max=200"+isLive, 'playCustom', "", "false")
    if cat2:
        addDir(translation(30131), urlMainApi+"/video/list.json?"+genres+"order=MostViewedToday&offset=0&max=10"+isLive, 'playCustom', "", "true")
    if cat3:
        addDir(translation(30132), urlMainApi+"/video/list.json?"+genres+"order=MostViewedToday&offset=0&max=20"+isLive, 'playCustom', "", "true")
    if cat4:
        addDir(translation(30133), urlMainApi+"/video/list.json?"+genres+"order=MostViewedToday&offset=0&max=50"+isLive, 'playCustom', "", "true")
    if cat5:
        addDir(translation(30134), urlMainApi+"/video/list.json?"+genres+"order=MostViewedToday&offset=0&max=100"+isLive, 'playCustom', "", "true")
    if cat6:
        addDir(translation(30135), urlMainApi+"/video/list.json?"+genres+"order=MostViewedToday&offset=0&max=200"+isLive, 'playCustom', "", "true")
    if cat7:
        addDir(translation(30136), urlMainApi+"/video/list.json?"+genres+"order=MostViewedAllTime&offset=0&max=200"+isLive, 'playCustom', "", "false")
    if cat8:
        addDir(translation(30137), urlMainApi+"/video/list.json?"+genres+"order=MostViewedAllTime&offset=0&max=10"+isLive, 'playCustom', "", "true")
    if cat9:
        addDir(translation(30138), urlMainApi+"/video/list.json?"+genres+"order=MostViewedAllTime&offset=0&max=20"+isLive, 'playCustom', "", "true")
    if cat10:
        addDir(translation(30139), urlMainApi+"/video/list.json?"+genres+"order=MostViewedAllTime&offset=0&max=50"+isLive, 'playCustom', "", "true")
    if cat11:
        addDir(translation(30140), urlMainApi+"/video/list.json?"+genres+"order=MostViewedAllTime&offset=0&max=100"+isLive, 'playCustom', "", "true")
    if cat12:
        addDir(translation(30141), urlMainApi+"/video/list.json?"+genres+"order=MostViewedAllTime&offset=0&max=200"+isLive, 'playCustom', "", "true")
    if cat13:
        addDir(translation(30142), urlMainApi+"/video/list.json?"+genres+"order=Random&offset=0&max=200"+isLive, 'playCustom', "", "true")
    xbmcplugin.endOfDirectory(pluginhandle)


def playOfficial(id):
        if id=="TIVEVSTRUS00":
                fullUrl = "http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch1/appleman.m3u8"
        elif id=="TIVEVSTRUS01":
            fullUrl = "http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch2/appleman.m3u8"
        elif id=="TIVEVSTRUS02":
            fullUrl = "http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch3/appleman.m3u8"
        elif id=="TIVEVSTRDE00":
            fullUrl = "http://vevoplaylist-eu01-live.hls.adaptive.level3.net/vevoeu/ch01/appleman.m3u8"
        content = opener.open(fullUrl).read()
        match = re.compile('BANDWIDTH='+resolutionOfficial+'.*?(.+?).m3u8', re.DOTALL).findall(content)
        fullUrl = fullUrl[:fullUrl.rfind("/")]+"/"+match[len(match)-1].strip()+".m3u8"
        print 'Ffffffffffffffffffffffffffffffffffffffffff'+fullUrl
        listitem = xbmcgui.ListItem(path=fullUrl)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
    


def listChannelsSimple():
    addDir("- "+translation(30005), "", 'addSimpleChannel', "")
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    if os.path.exists(simpleChannelsFile):
        fh = open(simpleChannelsFile, 'r')
        all_lines = fh.readlines()
        for line in all_lines:
            addSimpleChannelDir(line.strip().title(), urlMainApi+"/search/videos.json?q="+line.strip().lower().replace(" ","%23")+"&offset=0&max=200", 'playCustom', "", "true")
        fh.close()
    xbmcplugin.endOfDirectory(pluginhandle)


def listChannelsAdvancedMain():
    addDir("- "+translation(30005), "", 'addAdvancedChannel', "")
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    for dir in os.listdir(advancedChannelsDir):
        addAdvancedChannelDir(dir.strip().title(), dir, 'playAdvancedChannel', "")
    xbmcplugin.endOfDirectory(pluginhandle)


def listAdvancedChannel(channel):
    channelDir = os.path.join(advancedChannelsDir, channel)
    addDir("- "+translation(30008), channel, 'addAdvancedChannelArtist', "")
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    if os.path.exists(channelDir):
        for file in os.listdir(channelDir):
            count = str(len(os.listdir(os.path.join(channelDir, file)))-1)
            addArtistDir(file+" ("+count+")", channel, 'updateArtist', "", file)
    xbmcplugin.endOfDirectory(pluginhandle)


def addSimpleChannel():
    keyboard = xbmc.Keyboard('', translation(30011))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        query = keyboard.getText()
        fh = open(simpleChannelsFile, 'a')
        fh.write(query+"\n")
        fh.close()


def addAdvancedChannel():
    keyboard = xbmc.Keyboard('', translation(30005))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        channel = keyboard.getText()
        os.mkdir(os.path.join(advancedChannelsDir, channel))


def addAdvancedChannelArtist(channel):
    channelDir = os.path.join(advancedChannelsDir, channel)
    keyboard = xbmc.Keyboard('', translation(30010))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        artist = keyboard.getText().replace(" ", "+")
        titles = []
        titlesRaw = []
        ids = []
        content = opener.open("http://api.vevo.com/mobile/v1/search/artists.json?q="+artist+"&offset=0&max=100").read()
        content = json.loads(content)
        for item in content["result"]:
            title = item["name"].encode('utf-8')
            id = item["id"].encode('utf-8')
            videos = str(item["video_count"])
            titles.append(title+" ("+videos+")")
            titlesRaw.append(title)
            ids.append(id)
        dialog = xbmcgui.Dialog()
        nr=dialog.select("Results", titles)
        if nr >=0:
          id = ids[nr]
          title = titlesRaw[nr]
          dirName = (''.join(c for c in unicode(title, 'utf-8') if c not in '/\\:?"*|<>')).strip()
          artistDir = os.path.join(channelDir, dirName)
          if not os.path.exists(artistDir):
              os.mkdir(artistDir)
          artistIdFile = os.path.join(artistDir, "artistID")
          if not os.path.exists(artistIdFile):
              fh = open(artistIdFile, 'w')
              fh.write(id)
              fh.close()
          content = opener.open("http://api.vevo.com/mobile/v1/artist/"+id+"/videos.json?order=MostViewedToday&offset=0&max=200").read()
          content = json.loads(content)
          count = 0
          for item in content["result"]:
              title = item["artists_main"][0]["name"].encode('utf-8')+" - "+item["title"].encode('utf-8')
              videoID = item["isrc"]
              thumb = item["image_url"].encode('utf-8')
              videoFile = os.path.join(artistDir, videoID)
              if not os.path.exists(videoFile):
                  fh = open(videoFile, 'w')
                  fh.write(title+"#"+thumb)
                  fh.close()
                  count+=1
          xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30013)+' '+str(count)+' '+translation(30014)+',5000)')


def addArtistChannel(name):
    artist = name.replace(" ", "+")
    titles = []
    titlesRaw = []
    ids = []
    content = opener.open("http://api.vevo.com/mobile/v1/search/artists.json?q="+artist+"&offset=0&max=100").read()
    content = json.loads(content)
    for item in content["result"]:
        title = item["name"].encode('utf-8')
        id = item["id"].encode('utf-8')
        videos = str(item["video_count"])
        titles.append(title+" ("+videos+")")
        titlesRaw.append(title)
        ids.append(id)
    dialog = xbmcgui.Dialog()
    nr=dialog.select("Results", titles)
    if nr >=0:
      id = ids[nr]
      title = titlesRaw[nr]
      channel = title.replace("+", " ")
      channelDir = os.path.join(advancedChannelsDir, title)
      if not os.path.exists(os.path.join(advancedChannelsDir, title)):
          os.mkdir(os.path.join(advancedChannelsDir, title))
      dirName = (''.join(c for c in unicode(title, 'utf-8') if c not in '/\\:?"*|<>')).strip()
      artistDir = os.path.join(channelDir, dirName)
      if not os.path.exists(artistDir):
          os.mkdir(artistDir)
      artistIdFile = os.path.join(artistDir, "artistID")
      if not os.path.exists(artistIdFile):
          fh = open(artistIdFile, 'w')
          fh.write(id)
          fh.close()
      content = opener.open("http://api.vevo.com/mobile/v1/artist/"+id+"/videos.json?order=MostViewedToday&offset=0&max=200").read()
      content = json.loads(content)
      count = 0
      for item in content["result"]:
          title = item["artists_main"][0]["name"].encode('utf-8')+" - "+item["title"].encode('utf-8')
          videoID = item["isrc"]
          thumb = item["image_url"].encode('utf-8')
          videoFile = os.path.join(artistDir, videoID)
          if not os.path.exists(videoFile):
              fh = open(videoFile, 'w')
              fh.write(title+"#"+thumb)
              fh.close()
              count+=1
      xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30013)+' '+str(count)+' '+translation(30014)+',5000)')
      if not os.path.exists(libDir):
          os.mkdir(libDir)
      if not os.path.exists(os.path.join(libDir, channel)):
          os.mkdir(os.path.join(libDir, channel))
      libartistDir = os.path.join(libDir, channel)
      for root, dirs, files in os.walk(os.path.join(advancedChannelsDir, channel)):
          for filename in files:
              if filename!="artistID":
                  fh = open(os.path.join(root, filename), 'r')
                  entry = fh.read()
                  fh.close()
                  title = entry[:entry.rfind("#")]
                  if '-' in title:
                      newtitle = title.rsplit('-',1)
                      title = newtitle[1]
                  thumb = entry[entry.rfind("#")+1:]
                  if xbox:
                      url = "plugin://video/VEVO TV/?url="+filename+"&mode=playVideo"
                  else:
                      url = "plugin://plugin.video.vevo_tv/?url="+filename+"&mode=playVideo"
                  musicVideoStrmFile = os.path.join(libartistDir, title.replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_')+".strm")
                  if not os.path.exists(musicVideoStrmFile):
                      fh = open(musicVideoStrmFile, 'w')
                      fh.write(url)
                      fh.close()
      xbmc.executebuiltin("UpdateLibrary(video,special://profile/addon_data/plugin.video.vevo_tv/library)")
      playAdvancedChannel(channel)


def updateArtist(channel, artist):
    channelDir = os.path.join(advancedChannelsDir, channel)
    artistDir = os.path.join(channelDir, artist)
    artistIdFile = os.path.join(artistDir, "artistID")
    fh = open(artistIdFile, 'r')
    id = fh.read()
    fh.close()
    content = opener.open("http://api.vevo.com/mobile/v1/artist/"+id+"/videos.json?order=MostViewedToday&offset=0&max=200").read()
    content = json.loads(content)
    count = 0
    for item in content["result"]:
        title = item["artists_main"][0]["name"].encode('utf-8')+" - "+item["title"].encode('utf-8')
        videoID = item["isrc"]
        thumb = item["image_url"].encode('utf-8')
        videoFile = os.path.join(artistDir, videoID)
        if not os.path.exists(videoFile):
            fh = open(videoFile, 'w')
            fh.write(title+"#"+thumb)
            fh.close()
            count+=1
    xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30013)+' '+str(count)+' '+translation(30014)+',5000)')


def removeArtist(artist, channel):
    channelDir = os.path.join(advancedChannelsDir, channel)
    artistDir = os.path.join(channelDir, artist)
    try:
        shutil.rmtree(artistDir)
    except:
        shutil.rmtree(artistDir)


def removeAdvancedChannel(channel):
    channelDir = os.path.join(advancedChannelsDir, channel)
    try:
        shutil.rmtree(channelDir)
    except:
        shutil.rmtree(channelDir)


def renameAdvancedChannel(channel):
    keyboard = xbmc.Keyboard(channel, translation(30012))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        channelNew = keyboard.getText()
        channelDir = os.path.join(advancedChannelsDir, channel)
        channelDirNew = os.path.join(advancedChannelsDir, channelNew)
        os.rename(channelDir, channelDirNew)


def editSimpleChannel(query):
    fh = open(simpleChannelsFile, 'r')
    content = fh.read()
    fh.close()
    keyboard = xbmc.Keyboard(query, translation(30011))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        queryNew = keyboard.getText()
        fh = open(simpleChannelsFile, 'w')
        fh.write(content.replace(query, queryNew))
        fh.close()
    xbmc.executebuiltin("Container.Refresh")


def removeSimpleChannel(query):
    fh = open(simpleChannelsFile, 'r')
    content = fh.read()
    fh.close()
    fh = open(simpleChannelsFile, 'w')
    fh.write(content.replace(query+"\n", ""))
    fh.close()
    xbmc.executebuiltin("Container.Refresh")


def playCustom(url, shuffled):
    entries = []
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    if "order=Random" in url:
        url += "&rnd="+str(random.randint(1, 999999))
    content = opener.open(url).read()
    content = json.loads(content)
    try:
        content = content["result"]["videos"]
    except:
        content = content["result"]
    for item in content:
        artist = item["artists_main"][0]["name"].encode('utf-8')
        filtered = False
        for entry in blacklist:
            if entry.strip().lower() and entry.lower() in artist.lower():
                filtered = True
        if filtered:
            continue
        title = artist+" - "+item["title"].encode('utf-8')
        thumb = item["image_url"].encode('utf-8')
        if xbox:
            url = "plugin://video/VEVO TV/?url="+item["isrc"]+"&mode=playVideo"
        else:
            url = "plugin://plugin.video.vevo_tv/?url="+item["isrc"]+"&mode=playVideo"
        entries.append([title, url, thumb])
    if shuffled:
        random.shuffle(entries)
    for title, url, thumb in entries:
        listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
        playlist.add(url, listitem)
    xbmc.Player().play(playlist)


def playAdvancedChannel(channel):
    entries = []
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    for root, dirs, files in os.walk(os.path.join(advancedChannelsDir, channel)):
        for filename in files:
            if filename!="artistID":
                fh = open(os.path.join(root, filename), 'r')
                entry = fh.read()
                fh.close()
                title = entry[:entry.rfind("#")]
                thumb = entry[entry.rfind("#")+1:]
                if xbox:
                    url = "plugin://video/VEVO TV/?url="+filename+"&mode=playVideo"
                else:
                    url = "plugin://plugin.video.vevo_tv/?url="+filename+"&mode=playVideo"
                entries.append([title, url, thumb])
    if len(entries)>0:
        random.shuffle(entries)
        for title, url, thumb in entries:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)
    else:
        listAdvancedChannel(channel)
        xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30015)+',5000)')


def playVideo(id):
    try:
        content = opener.open("http://videoplayer.vevo.com/VideoService/AuthenticateVideo?isrc="+id).read()
        content = str(json.loads(content))
        match = re.compile('<rendition name="HTTP Live Streaming" url="(.+?)"', re.DOTALL).findall(content)
        fullUrl = ""
        for url in match:
          if cdnCustom in url:
              fullUrl = url
        content = opener.open(fullUrl).read()
        match = re.compile('RESOLUTION='+resolutionCustom+'.*?\n(.+?)\n', re.DOTALL).findall(content)
        fullUrl = fullUrl[:fullUrl.rfind("/")]+"/"+match[len(match)-1].strip()
        listitem = xbmcgui.ListItem(path=fullUrl)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        if showInfo:
            xbmc.sleep(infoDelay*1000)
            if infoType == "0":
                xbmc.executebuiltin('XBMC.ActivateWindow(12901)')
                xbmc.sleep(infoDuration*1000)
                xbmc.executebuiltin('XBMC.ActivateWindow(12005)')
            elif infoType == "1":
                title = 'Now playing:'
                videoTitle = xbmc.getInfoLabel('VideoPlayer.Title')
                thumb = xbmc.getInfoImage('VideoPlayer.Cover')
                xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title, videoTitle, infoDuration*1000, thumb))
    except:
        pass


def listPlaylists():
    for root, dirs, files in os.walk(playlistsDir):
        for filename in files:
            fh = open(os.path.join(root, filename), 'r')
            playlistID = fh.read()
            fh.close()
            addDir(filename.title(), "http://api.vevo.com/mobile/v2/playlist/"+playlistID+".json", 'playCustom', "", "true")
    xbmcplugin.endOfDirectory(pluginhandle)


def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


def addLink(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, shuffled="false"):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&shuffled="+str(shuffled)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addSimpleChannelDir(name, url, mode, iconimage, shuffled="false"):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&shuffled="+str(shuffled)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    entries = []
    entries.append((translation(30006), 'RunPlugin(plugin://'+addonID+'/?mode=editSimpleChannel&url='+urllib.quote_plus(name.lower())+')',))
    entries.append((translation(30007), 'RunPlugin(plugin://'+addonID+'/?mode=removeSimpleChannel&url='+urllib.quote_plus(name.lower())+')',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def addAdvancedChannelDir(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    entries = []
    entries.append((translation(30006), 'Container.Update(plugin://'+addonID+'/?mode=listAdvancedChannel&url='+urllib.quote_plus(url)+')',))
    entries.append((translation(30012), 'Container.Update(plugin://'+addonID+'/?mode=renameAdvancedChannel&url='+urllib.quote_plus(url)+')',))
    entries.append((translation(30007), 'Container.Update(plugin://'+addonID+'/?mode=removeAdvancedChannel&url='+urllib.quote_plus(url)+')',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addArtistDir(name, url, mode, iconimage, artist):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+str(artist)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    entries = []
    entries.append((translation(30009), 'Container.Update(plugin://'+addonID+'/?mode=removeArtist&url='+urllib.quote_plus(url)+"&name="+str(artist)+')',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
shuffled = urllib.unquote_plus(params.get('shuffled', ''))
name = urllib.unquote_plus(params.get('name', ''))

if mode == 'playVideo':
    playVideo(url)
elif mode == 'playOfficial':
    playOfficial(url)
elif mode == 'playCustom':
    playCustom(url, shuffled == "true")
elif mode == 'playAdvancedChannel':
    playAdvancedChannel(url)
elif mode == 'playPlaylist':
    playPlaylist(url)
elif mode == 'customMain':
    customMain(url)
elif mode == 'listCustomModes':
    listCustomModes(url)
elif mode == 'listCustomModesLive':
    listCustomModes(url, "live")
elif mode == 'listChannelsSimple':
    listChannelsSimple()
elif mode == 'listChannelsAdvancedMain':
    listChannelsAdvancedMain()
elif mode == 'listPlaylists':
    listPlaylists()
elif mode == 'addSimpleChannel':
    addSimpleChannel()
elif mode == 'addAdvancedChannel':
    addAdvancedChannel()
elif mode == 'listAdvancedChannel':
    listAdvancedChannel(url)
elif mode == 'addAdvancedChannelArtist':
    addAdvancedChannelArtist(url)
elif mode == 'addArtistChannel':
    addArtistChannel(name)
elif mode == 'editSimpleChannel':
    editSimpleChannel(url)
elif mode == 'removeSimpleChannel':
    removeSimpleChannel(url)
elif mode == 'removeAdvancedChannel':
    removeAdvancedChannel(url)
elif mode == 'renameAdvancedChannel':
    renameAdvancedChannel(url)
elif mode == 'removeArtist':
    removeArtist(name, url)
elif mode == 'updateArtist':
    updateArtist(url, name)
else:
    index()
