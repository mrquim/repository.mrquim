#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
try: import simplejson as json
except ImportError: import json
import random
import socket
import urllib
import urllib2
import urlparse
import datetime
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import time
from operator import itemgetter
from StringIO import StringIO
import gzip
import ssl

try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	# Legacy Python that doesn't verify HTTPS certificates by default
	pass
else:
	# Handle target environment that doesn't support HTTPS verification
	ssl._create_default_https_context = _create_unverified_https_context

pluginhandle = int(sys.argv[1])
socket.setdefaulttimeout(40)
addonID = 'plugin.video.spotitube'
addon = xbmcaddon.Addon(id=addonID)
addonPath = xbmc.translatePath(addon.getAddonInfo('path')).decode('utf-8')
dataPath = os.path.join(xbmc.translatePath('special://profile/addon_data/'+addonID), '')
translation = addon.getLocalizedString
region = xbmc.getLanguage(xbmc.ISO_639_1, region=True).split("-")[1]
icon = os.path.join(addonPath, 'icon.png').decode('utf-8')
fanart = os.path.join(addonPath, 'fanart.jpg').decode('utf-8')
pic = os.path.join(addonPath, 'resources/media/')
blacklist = addon.getSetting("blacklist").split(',')
infoEnabled = addon.getSetting("showInfo") == "true"
infoType = addon.getSetting("infoType")
infoDelay = int(addon.getSetting("infoDelay"))
infoDuration = int(addon.getSetting("infoDuration"))
useThumbAsFanart = addon.getSetting("useThumbAsFanart") == 'true'
cachePath = os.path.join(xbmc.translatePath(addon.getSetting("cacheDir")))
cacheDays = int(addon.getSetting("cacheLong"))
beatportShowSubGenres = addon.getSetting("beatportShowSubGenres") == 'true'
deezerSearchDisplay = str(addon.getSetting("deezerSearch_count"))
deezerVideosDisplay = str(addon.getSetting("deezerVideos_count"))
itunesShowSubGenres = addon.getSetting("itunesShowSubGenres") == 'true'
itunesForceCountry = addon.getSetting("itunesForceCountry") == 'true'
itunesCountry = addon.getSetting("itunesCountry")
spotifyForceCountry = addon.getSetting("spotifyForceCountry") == 'true'
spotifyCountry = addon.getSetting("spotifyCountry")
forceView = addon.getSetting("forceView") == 'true'
viewIDGenres = str(addon.getSetting("viewIDGenres"))
viewIDPlaylists = str(addon.getSetting("viewIDPlaylists"))
viewIDVideos = str(addon.getSetting("viewIDVideos"))
urlMainBP = "https://www.beatport.com"
urlMainBB = "http://www.billboard.com"
urlMainHypem = "https://hypem.com"
urlMainOC = "http://www.officialcharts.com"
token = "AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo"
	
if itunesForceCountry and itunesCountry:
	iTunesRegion = itunesCountry
else:
	iTunesRegion = region
	
if spotifyForceCountry and spotifyCountry:
	spotifyRegion = spotifyCountry
else:
	spotifyRegion = region
	
if not os.path.isdir(dataPath):
	os.makedirs(dataPath)
	
if cachePath == "":
	addon.setSetting(id='cacheDir', value='special://profile/addon_data/'+addonID+'/cache')
elif cachePath != "" and not os.path.isdir(cachePath) and not cachePath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')):
	os.mkdir(cachePath)
elif cachePath != "" and not os.path.isdir(cachePath) and cachePath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')):
	addon.setSetting(id='cacheDir', value='special://profile/addon_data/'+addonID+'/cache') and os.mkdir(cachePath)
elif cachePath != "" and os.path.isdir(cachePath):
		xDays = cacheDays # Days after which Files would be deleted
		now = time.time() # Date and time now
		for root, dirs, files in os.walk(cachePath):
			for name in files:
				filename = os.path.join(root, name).decode('utf-8')
				try:
					if os.path.exists(filename):
						if os.path.getmtime(filename) < now - (60*60*24*xDays): # Check if CACHE-File exists and remove CACHE-File after defined xDays
							os.unlink(filename)
				except: pass
	
def index():
	addDir(translation(40203), "", "SearchDeezer", pic+'deepsearch.gif')
	addDir(translation(40101), "", "bpMain", pic+'beatport.png')
	addDir(translation(40102), "", "billboardMain", pic+'billboard.png')
	addDir(translation(40103), "", "hypemMain", pic+'hypem.png')
	addDir(translation(40104), "", "itunesMain", pic+'itunes.png')
	addDir(translation(40105), "", "ocMain", pic+'official.png')
	addDir(translation(40106), "", "spotifyMain", pic+'spotify.png')
	addDir(translation(40202), "", "Settings", pic+'settings.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def bpMain():
	content = cache('https://pro.beatport.com', 30)
	content = content[content.find('<span class="genres-text">Genres</span>')+1:]
	content = content[:content.find('<!-- End Mobile Touch Menu -->')]
	match = re.compile('<a href="(.*?)" class="(.*?)" data-name=".+?">(.*?)</a>', re.DOTALL).findall(content)
	oTitle = translation(40135)
	addAutoPlayDir(oTitle, urlMainBP+"/top-100", "listBP", pic+'beatport.png', "", "browse")
	for genreID, type, title in match:
		topUrl = urlMainBP+genreID+'/top-100'
		subUrl = urlMainBP+genreID
		title = cleanTitle(title)
		if not 'subgenre' in type:
			if beatportShowSubGenres:
				title = '[COLOR FF1E90FF]'+title+'[/COLOR]'
			addAutoPlayDir(title, topUrl, "listBP", pic+'beatport.png', "", "browse")
		elif beatportShowSubGenres:
			title = '     '+title
			addAutoPlayDir(title, subUrl, "listBP", pic+'beatport.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listBP(type, url, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	spl = content.split('bucket-item ec-item track')
	count = 0
	pos = 1
	for i in range(1,len(spl),1):
		count += 1
		entry = spl[i]
		artist = re.compile('data-artist=".+?">(.*?)</a>', re.DOTALL).findall(entry)[0]
		song = re.compile('<span class="buk-track-primary-title" title=".+?">(.*?)</span>', re.DOTALL).findall(entry)[0]
		remix = re.compile('<span class="buk-track-remixed">(.*?)</span>', re.DOTALL).findall(entry)
		if "(original mix)" in song.lower():
			song = song.lower().split('(original mix)')[0]
		song = cleanTitle(song)
		if "(feat." in song.lower() and " feat." in song.lower():
			song = song.split(')')[0]+')'
		elif not "(feat." in song.lower() and " feat." in song.lower():
			firstTitle = song.lower().split(' feat.')[0]
			secondTitle = song.lower().split(' feat.')[1]
			song = firstTitle+' (feat.'+secondTitle+')'
		if remix and not "original" in remix[0].lower():
			newRemix = remix[0].replace('[', '').replace(']', '')
			song += ' ['+newRemix.strip()+']'
		title = cleanTitle(artist.strip()+" - "+song.strip())
		newName = title
		try:
			oldDate = re.compile('<p class="buk-track-released">(.*?)</p>', re.DOTALL).findall(entry)[0]
			convert = time.strptime(oldDate,'%Y-%m-%d')
			newDate = time.strftime('%d.%m.%Y',convert)
			newName += '   [COLOR deepskyblue]['+str(newDate)+'][/COLOR]'
		except: pass
		try:
			photo = re.compile('data-src="(http.*?.jpg)"', re.DOTALL).findall(entry)[0]
			thumb = photo.split('image_size_hq/')[0]+'image/'+photo.split('/')[-1]
			#thumb = thumb.replace("/30x30/","/500x500/").replace("/60x60/","/500x500/").replace("/95x95/","/500x500/").replace("/250x250/","/500x500/")
		except:
			thumb = pic+'noimage.png'
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "browse":
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+newName
			addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
		else:
			url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			musicVideos.append([title, url, thumb])
			if limit and int(limit)==pos:
				break
			pos += 1
	if type == "browse":
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def billboardMain():
	addAutoPlayDir(translation(40107), urlMainBB+"/charts/hot-100", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
	addAutoPlayDir(translation(40108), urlMainBB+"/charts/billboard-200", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
	addDir(translation(40110), "", "listBillboardArchiveMain", pic+'billboard.png', "", "browse")
	addDir(translation(40111), "genre", "listBillboardChartsTypes", pic+'billboard.png', "", "browse")
	addDir(translation(40112), "country", "listBillboardChartsTypes", pic+'billboard.png', "", "browse")
	addDir(translation(40113), "other", "listBillboardChartsTypes", pic+'billboard.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listBillboardArchiveMain():
	for i in range(datetime.date.today().year,1957,-1):
		addAutoPlayDir(str(i), urlMainBB+"/archive/charts/"+str(i), "listBillboardArchive", pic+'billboard.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listBillboardArchive(url):
	UN_Supported = ['album', 'artist 100', 'greatest of all time', 'next big', 'social 50', 'uncharted'] # if Artist and Song are the same
	content = cache(url, 30)
	match = re.compile('<span class="field-content">\s*<a href="(.*?)">(.*?)</a>', re.DOTALL).findall(content)
	for url, title in match:
		if any(x in title.strip().lower() for x in UN_Supported):
			continue
		addAutoPlayDir(cleanTitle(title), urlMainBB+url, "listBillboardArchiveVideos", pic+'billboard.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listBillboardArchiveVideos(type, url, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	musicIsolated = set()
	content = cache(url, 30)
	content = content[content.find('<tbody>')+1:]
	content = content[:content.find('</tbody>')]
	spl = content.split('<td class="views-field views-field-field-chart-item-song"')
	pos = 1
	for i in range(1,len(spl),1):
		entry = spl[i]
		try:
			song = re.compile('>\s+(.*?)</td>').findall(entry)[0]
		except: pass
		try:
			match = re.compile('<td class="views-field views-field-field-chart-item-arti.+?">\s+<a href="(.*?)">(.*?)</td>\s+</tr>').findall(entry)
			if "/artist/" in match[0][0] or "/music/" in match[0][0]:
				artist = match[0][1].split('</a>')[0]
		except:
			try:
				artist = re.compile('<td class="views-field views-field-field-chart-item-arti.+?">(.*?)</td>\s+</tr>', re.DOTALL).findall(entry)[0]
			except: pass
		if song == "" or artist == "":
			continue
		if song.strip().lower() != artist.strip().lower():
			title = cleanTitle(artist.strip()+" - "+song.strip())
			newTitle = song.strip().lower()
			if newTitle in musicIsolated:
				continue
			musicIsolated.add(newTitle)
			if title.isupper():
				title = title.title()
			filtered = False
			for entry2 in blacklist:
				if entry2.strip().lower() and entry2.strip().lower() in title.lower():
					filtered = True
			if filtered:
				continue
			if type == "browse":
				addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
				musicVideos.append([title, url, ""])
				if limit and int(limit) == pos:
					break
				pos += 1
	if type == "browse":
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def listBillboardChartsTypes(type):
	if type == "genre":
		addAutoPlayDir("Pop", urlMainBB+"/charts/pop-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rock", urlMainBB+"/charts/rock-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Alternative", urlMainBB+"/charts/alternative-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("R&B/Hip-Hop", urlMainBB+"/charts/r-b-hip-hop-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("R&B", urlMainBB+"/charts/r-and-b-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rap", urlMainBB+"/charts/rap-song", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Gospel", urlMainBB+"/charts/gospel-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Country", urlMainBB+"/charts/country-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40114), urlMainBB+"/charts/latin-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40115), urlMainBB+"/charts/jazz-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40116), urlMainBB+"/charts/tropical-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40117), urlMainBB+"/charts/soundtracks", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rhythmic", urlMainBB+"/charts/rhythmic-40", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Dance/Club", urlMainBB+"/charts/dance-club-play-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Dance/Electronic", urlMainBB+"/charts/dance-electronic-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
	elif type == "country":
		addAutoPlayDir(translation(40118), urlMainBB+"/charts/canadian-hot-100", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40119), urlMainBB+"/charts/japan-hot-100", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40120), urlMainBB+"/charts/germany-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40121), urlMainBB+"/charts/france-digital-song-sales", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40122), urlMainBB+"/charts/official-uk-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
	elif type == "other":
		addAutoPlayDir(translation(40123), urlMainBB+"/charts/radio-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Digital", urlMainBB+"/charts/digital-song-sales", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40124), urlMainBB+"/charts/streaming-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40125), urlMainBB+"/charts/on-demand-songs", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
		addAutoPlayDir("TOP on Youtube", urlMainBB+"/charts/youtube", "listBillboardCharts_HTML", pic+'billboard.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listBillboardCharts_HTML(type, url, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<div class="chart-data js-chart-data" data-trackaction="Chart List"')+1:]
	content = content[:content.find('<audio class="chart__audio-element js-audio-element"></audio>')]
	spl = content.split('<div class="chart-row__main-display">')
	pos = 1
	for i in range(1,len(spl),1):
		entry = spl[i]
		position = re.compile('<span class="chart-row__current-week">(.*?)</span>', re.DOTALL).findall(entry)[0]
		try:
			thumb = re.compile('data-imagesrc="(http.*?.jpg)"', re.DOTALL).findall(entry)[0]
		except:
			try:
				thumb = re.compile('style="background-image.+?(http.*?.jpg)', re.DOTALL).findall(entry)[0]
			except:
				thumb = pic+'noimage.png'
		song = re.compile('<h2 class="chart-row__song">(.*?)</h2>', re.DOTALL).findall(entry)[0]
		try:
			artist = re.compile('data-tracklabel="Artist Name">(.*?)</a>', re.DOTALL).findall(entry)[0]
		except:
			artist = re.compile('<span class="chart-row__artist">(.*?)</span>', re.DOTALL).findall(entry)[0]
		title = cleanTitle(artist.strip()+" - "+song.strip())
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "browse":
			name = '[COLOR chartreuse]'+str(position)+' •  [/COLOR]'+title
			addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
		else:
			url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			musicVideos.append([title, url, thumb])
			if limit and int(limit) == pos:
				break
			pos += 1
	if type == "browse":
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def hypemMain():
	addAutoPlayDir(translation(40136), urlMainHypem+"/popular?ax=1&sortby=shuffle", 'listHypem', pic+'hypem.png', "", "browse")
	addAutoPlayDir(translation(40137), urlMainHypem+"/popular/lastweek?ax=1&sortby=shuffle", 'listHypem', pic+'hypem.png', "", "browse")
	addAutoPlayDir(translation(40138), "", 'listTimeMachine', pic+'hypem.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listHypem(type, url, limit):
	musicVideos = []
	if type == "play":
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<div id="track-list">')+1:]
	content = content[:content.find('<script type="application/json" id="displayList-data">')]
	spl = content.split('<div class="section-player">')
	for i in range(1,len(spl),1):
		entry = spl[i]
		rank = re.compile('<span class="rank">(.*?)</span>', re.DOTALL).findall(entry)[0]
		artist = re.compile('href="/artist/.+?">(.*?)</a>', re.DOTALL).findall(entry)[0]
		song = re.compile('<span class="base-title">(.*?)</span>', re.DOTALL).findall(entry)[0]
		remix = re.compile('<span class="remix-link">(.*?)</span>', re.DOTALL).findall(entry)
		if remix:
			song += ' ['+remix[0].strip()+']'
		title = cleanTitle(artist.strip()+" - "+song.strip())
		try:
			photo = re.findall('<span style="background.+?https://static.hypem.com([^"]+);',entry,re.S)[0]
			if "/solid_color" in photo and ".jpg" in photo:
				thumb = "https://static.hypem.com"+photo.split('/solid_color')[1].replace(')', '') #.replace('_320.jpg)', '_500.jpg')
			else:
				thumb = ""#pic+'noimage.png'
		except:
			thumb = ""#pic+'noimage.png'
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([int(rank), title, url, thumb])
	musicVideos = sorted(musicVideos, key=itemgetter(0))
	if type == "browse":
		for rank, title, url, thumb in musicVideos:
			name = '[COLOR chartreuse]'+str(rank)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for rank, title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def listTimeMachine():
	for i in range(1, 210, 1):
		dt = datetime.date.today()
		while dt.weekday() != 0:
			dt -= datetime.timedelta(days=1)
		dt -= datetime.timedelta(weeks=i)
		months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		month = months[int(dt.strftime("%m")) - 1]
		addAutoPlayDir(dt.strftime("%d. %b - %Y").replace("Mar", translation(40156)).replace("May", translation(40157)).replace("Oct", translation(40158)).replace("Dec", translation(40159)), urlMainHypem+"/popular/week:"+month+"-"+dt.strftime("%d-%Y")+"?ax=1&sortby=shuffle", 'listHypem', pic+'hypem.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def itunesMain():
	content = cache("https://itunes.apple.com/"+iTunesRegion+"/genre/music/id34", 30)
	content = content[content.find('id="genre-nav"'):]
	content = content[:content.find('</div>')]
	match = re.compile('<li><a href="https://itunes.apple.com/.+?/genre/.+?/id(.*?)"(.*?)title=".+?">(.*?)</a>', re.DOTALL).findall(content)
	oTitle = translation(40135)
	addAutoPlayDir(oTitle, "0", "listItunesVideos", pic+'itunes.png', "", "browse")
	for genreID, type, title in match:
		title = cleanTitle(title)
		if 'class="top-level-genre"' in type:
			if itunesShowSubGenres:
				title = '[COLOR FF1E90FF]'+title+'[/COLOR]'
			addAutoPlayDir(title, genreID, "listItunesVideos", pic+'itunes.png', "", "browse")
		elif itunesShowSubGenres:
			title = '     '+title
			addAutoPlayDir(title, genreID, "listItunesVideos", pic+'itunes.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listItunesVideos(type, genreID, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	url = "https://itunes.apple.com/"+iTunesRegion+"/rss/topsongs/limit=100"
	if genreID != "0":
		url += "/genre="+genreID
	url += "/explicit=true/json"
	content = cache(url, 1)
	response = json.loads(content)
	musicIsolated = set()
	pos = 1
	try:
		for item in response['feed']['entry']:
			artist = item['im:artist']['label'].encode('utf-8')
			song = item['im:name']['label'].encode('utf-8')
			#if " (" in song:
				#song = song[:song.rfind(' (')]
			title = cleanTitle(artist.strip()+" - "+song.strip())
			newTitle = song.strip().lower()
			if newTitle in musicIsolated:
				continue
			musicIsolated.add(newTitle)
			if len(artist) > 30:
				artist = artist[:30]
			if len(song) > 30:
				song = song[:30]
			shortenTitle = cleanTitle(artist.strip()+" - "+song.strip())
			try:
				thumb = item['im:image'][2]['label']
				#thumb = thumb.split('/170x170')[0]+"/320x320bb-85.jpg"
			except:
				thumb = pic+'noimage.png'
			aired = item['im:releaseDate']['attributes']['label']
			filtered = False
			for entry2 in blacklist:
				if entry2.strip().lower() and entry2.strip().lower() in title.lower():
					filtered = True
			if filtered:
				continue
			if type == "browse":
				name = title+"   [COLOR deepskyblue]["+str(aired)+"][/COLOR]"
				addLink(name, shortenTitle.replace(" - ", " "), "playYTByTitle", thumb)
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(shortenTitle.replace(" - ", " "))+"&mode=playYTByTitle"
				musicVideos.append([title, url, thumb])
				if limit and int(limit)==pos:
					break
				pos += 1
		if type == "browse":
			xbmcplugin.endOfDirectory(pluginhandle)
			if forceView:
				xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
		else:
			random.shuffle(musicVideos)
			for title, url, thumb in musicVideos:
				listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
				playlist.add(url, listitem)
			xbmc.Player().play(playlist)
	except: pass
	
def ocMain():
	addAutoPlayDir(translation(40139), urlMainOC+"/charts/singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40140), urlMainOC+"/charts/uk-top-40-singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40141), urlMainOC+"/charts/asian-download-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40142), urlMainOC+"/charts/singles-chart-update/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40143), urlMainOC+"/charts/singles-downloads-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40144), urlMainOC+"/charts/singles-sales-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40145), urlMainOC+"/charts/audio-streaming-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40146), urlMainOC+"/charts/vinyl-singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40147), urlMainOC+"/charts/scottish-singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40148), urlMainOC+"/charts/physical-singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40149), urlMainOC+"/charts/end-of-year-singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40150), urlMainOC+"/charts/classical-singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40151), urlMainOC+"/charts/dance-singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir("R&B", urlMainOC+"/charts/r-and-b-singles-chart/", "listOC", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40152), urlMainOC+"/charts/rock-and-metal-singles-chart/", "listOC", pic+'official.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listOC(type, url, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	match = re.compile('class="track">(.*?)<div class="label-cat">', re.DOTALL).findall(content)
	spl = content.split('<div class="track">')
	count = 0
	pos = 1
	for i in range(1,len(spl),1):
		count += 1
		entry=spl[i]
		photo = re.findall('<img src="(.*?)"',entry,re.S)[0]
		if "images-amazon" in photo or "coverartarchive.org" in photo:
			thumb = photo.split('img/small?url=')[1]
		elif "/img/small?url=/images/artwork/" in photo:
			thumb = photo.replace("/img/small?url=", "")
		else:
			thumb = pic+'noimage.png'
		song = re.findall('<a href=".+?">(.*?)</a>',entry,re.S)[0]
		artist = re.findall('<a href=".+?">(.*?)</a>',entry,re.S)[1]
		if "/" in artist:
			artist = artist.split('/')[0]
		title = cleanTitle(artist.strip()+" - "+song.strip())
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "browse":
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title.title()
			addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
		else:
			url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			musicVideos.append([title, url, thumb])
			if limit and int(limit)==pos:
				break
			pos += 1
	if type == "browse":
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def spotifyMain():
	addDir(translation(40153), "https://api.tunigo.com/v3/space/toplists?region="+spotifyRegion+"&page=0&per_page=50&platform=web", "listSpotifyPlaylists", pic+'spotify.png')
	addDir(translation(40154), "https://api.tunigo.com/v3/space/featured-playlists?region="+spotifyRegion+"&page=0&per_page=50&dt="+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M").replace(":","%3A")+"%3A00&platform=web", "listSpotifyPlaylists", pic+'spotify.png')
	addDir(translation(40155), "https://api.tunigo.com/v3/space/genres?region="+spotifyRegion+"&per_page=1000&platform=web", "listSpotifyGenres", pic+'spotify.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listSpotifyGenres(url):
	content = cache(url, 30)
	response = json.loads(content)
	for item in response['items']:
		title = item['genre']['name'].encode('utf-8')
		if title.isupper():
			title = title.title()
		genreID = item['genre']['templateName'].encode('utf-8')
		try:
			thumb = item['genre']['iconUrl']
		except:
			thumb = pic+'noimage.png'
		if not "top lists" in title.strip().lower():
			addDir(title, "https://api.tunigo.com/v3/space/"+genreID+"?region="+spotifyRegion+"&page=0&per_page=50&platform=web", "listSpotifyPlaylists", thumb)
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listSpotifyPlaylists(url):
	content = cache(url, 1)
	response = json.loads(content)
	for item in response['items']:
		title = item['playlist']['title'].encode('utf-8')
		if title.isupper():
			title = title.title()
		description = item['playlist']['description'].encode('utf-8')
		uriUrl = item['playlist']['uri']
		try:
			thumb = item['playlist']['image']
			if not thumb.startswith("http"):
				#thumb = "https://u.scdn.co/images/pl/default/"+thumb
				thumb = "https://i.scdn.co/image/"+thumb
		except:
			thumb = pic+'noimage.png'
		addAutoPlayDir(title, uriUrl, "listSpotifyVideos", thumb, description, "browse")
	match = re.compile('page=(.+?)&per_page=(.+?)&', re.DOTALL).findall(url)
	currentPage = int(match[0][0])
	perPage = int(match[0][1])
	goNextPage = currentPage+1
	if goNextPage*perPage < response['totalItems']:
		addDir(translation(40206), url.replace("page="+str(currentPage),"page="+str(goNextPage)), "listSpotifyPlaylists", pic+'nextpage.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listSpotifyVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	#content = cache("https://open.spotify.com/embed?uri="+url, 1)
	content = cache("https://embed.spotify.com/?uri="+url, 1)
	if '<div class="ppbtn"></div>' in content:
		spl = content.split('music-paused item')
		x=0
	else:
		result = content[content.find('<ul class="track-list">')+1:]
		result = result[:result.find('<button id')]
		spl = result.split('class="track-row"')
		x=1
	for i in range(1,len(spl),1):
		entry = spl[i]
		if x==0:
			song = re.compile('class="track-title.+?>(.*?)<', re.DOTALL).findall(entry)[0]
		else:
			song = re.compile('data-name="(.*?)"', re.DOTALL).findall(entry)[0]
		if x==0:
			artist = re.compile('class="artist.+?>(.*?)<', re.DOTALL).findall(entry)[0]
		else:
			artist = re.compile('data-artists="(.*?)"', re.DOTALL).findall(entry)[0]
		if "(original mix)" in song.lower():
			song = song.lower().split('(original mix)')[0]
		#if " [" in song:
			#song = song.split(' [')[0]
		if " - " in song:
			firstTitle = song[:song.rfind(' - ')]
			secondTitle = song[song.rfind(' - ')+3:]
			song = firstTitle+' ['+secondTitle+']'
		if "," in artist:
			artist = artist.split(',')[0]
		if artist.islower():
			artist = artist.title()
		title = cleanTitle(artist.strip()+" - "+song.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		try:
			if x==0:
				thumb = re.compile('data-ca="(.*?)"', re.DOTALL).findall(entry)[0]
			else:
				thumb = re.findall('data-size-[0-9]+="(.*?)"',entry,re.S)[0]
		except:
			thumb = pic+'noimage.png'
		rank = re.compile('class="track-row-number">(.*?)</div>', re.DOTALL).findall(entry)[0]
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([int(rank), title, url, thumb])
	musicVideos = sorted(musicVideos, key=itemgetter(0))
	if type == "browse":
		for rank, title, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for rank, title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def SearchDeezer():
	someReceived = False
	dialog = xbmcgui.Dialog()
	word = dialog.input(translation(40204), type=xbmcgui.INPUT_ALPHANUM)
	word = urllib.quote(word, safe='')
	if word == "": return
	artistSEARCH = cache("https://api.deezer.com/search/artist?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	trackSEARCH = cache("https://api.deezer.com/search/track?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	albumSEARCH = cache("https://api.deezer.com/search/album?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	playlistSEARCH = cache("https://api.deezer.com/search/playlist?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	userlistSEARCH = cache("https://api.deezer.com/search/user?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	strukturARTIST = json.loads(artistSEARCH)
	if strukturARTIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]ARTIST[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerArtists", pic+'searchartists.png')
		someReceived = True
	strukturTRACK = json.loads(trackSEARCH)
	if strukturTRACK['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]SONG[COLOR orangered]     •  •  •[/COLOR][/B]', word, "listDeezerTracks", pic+'searchsongs.png')
		someReceived = True
	strukturALBUM = json.loads(albumSEARCH)
	if strukturALBUM['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]ALBUM[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerAlbums", pic+'searchalbums.png')
		someReceived = True
	strukturPLAYLIST = json.loads(playlistSEARCH)
	if strukturPLAYLIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]PLAYLIST[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerPlaylists", pic+'searchplaylists.png')
		someReceived = True
	strukturUSERLIST = json.loads(userlistSEARCH)
	if strukturUSERLIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]USER[COLOR orangered]     •  •  •[/COLOR][/B]', word, "listDeezerUserlists", pic+'searchuserlists.png')
		someReceived = True
	if not someReceived:
		addDir(translation(40205), word, "", pic+'noresults.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listDeezerArtists(url):
	musicVideos = []
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/artist?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = cleanTitle(item["name"].encode('utf-8'))
		if artist.strip().lower() in musicIsolated or artist == "":
			continue
		musicIsolated.add(artist)
		try:
			thumb = item["picture_big"].encode('utf-8')
			if thumb.endswith('artist//500x500-000000-80-0-0.jpg'):
				thumb = pic+'noavatar.gif'
		except:
			thumb = pic+'noavatar.gif'
		liked = item['nb_fan']
		tracksUrl = item['tracklist'].encode('utf-8').split('top?limit=')[0]+"top?limit="+deezerVideosDisplay+"&index=0"
		musicVideos.append([int(liked), artist, tracksUrl, thumb])
	musicVideos = sorted(musicVideos, key=itemgetter(0), reverse=True)
	for liked, artist, tracksUrl, thumb in musicVideos:
		name = artist+"   [COLOR FFFFA500][Fans: "+str(liked).strip()+"][/COLOR]"
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerArtists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerTracks(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/track?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = item['artist']['name'].encode('utf-8')
		song = item['title'].encode('utf-8')
		title = cleanTitle(artist.strip()+" - "+song.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		album = cleanTitle(item['album']['title'].encode('utf-8'))
		try:
			thumb = item['album']['cover_big'].encode('utf-8')
		except:
			thumb = pic+'noimage.png'
		#rank = item['rank']
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		name = title+"   [COLOR deepskyblue][Album: "+album+"][/COLOR]"
		addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerTracks", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerAlbums(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/album?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = item['artist']['name'].encode('utf-8')
		album = item['title'].encode('utf-8')
		title = cleanTitle(artist.strip()+" - "+album.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		try:
			thumb = item['cover_big'].encode('utf-8')
		except:
			thumb = pic+'noimage.png'
		numbers = item['nb_tracks']
		tracksUrl = item['tracklist'].encode('utf-8')+"?limit="+deezerVideosDisplay+"&index=0"
		version = item['record_type'].encode('utf-8')
		name = title+"   [COLOR deepskyblue]["+version.title().strip()+"[/COLOR] - [COLOR FFFFA500]Tracks: "+str(numbers).strip()+"][/COLOR]"
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerAlbums", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerPlaylists(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/playlist?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = cleanTitle(item['title'].encode('utf-8'))
		try:
			thumb = item['picture_big'].encode('utf-8')
		except:
			thumb = pic+'noimage.png'
		numbers = item['nb_tracks']
		tracksUrl = item['tracklist'].encode('utf-8')+"?limit="+deezerVideosDisplay+"&index=0"
		user = cleanTitle(item['user']['name'].encode('utf-8'))
		name = artist.title()+"   [COLOR deepskyblue][User: "+user.title()+"[/COLOR] - [COLOR FFFFA500]Tracks: "+str(numbers).strip()+"][/COLOR]"
		special = artist+" - "+user.title()
		if special in musicIsolated or artist == "":
			continue
		musicIsolated.add(special)
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerPlaylists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerUserlists(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/user?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		user = cleanTitle(item['name'].encode('utf-8'))
		try:
			thumb = item['picture_big'].encode('utf-8')
			if thumb.endswith('user//500x500-000000-80-0-0.jpg'):
				thumb = pic+'noavatar.gif'
		except:
			thumb = pic+'noavatar.gif'
		tracksUrl = item['tracklist'].encode('utf-8')+"?limit="+deezerVideosDisplay+"&index=0"
		name = user.title()
		if name in musicIsolated or user == "":
			continue
		musicIsolated.add(name)
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerUserlists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerVideos(type, url, thumb, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	if not "&index=0" in url:
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache(url, 1)
		response = json.loads(Original)
	for item in response['data']:
		song = item['title'].encode('utf-8')
		if song.isupper():
			song = song.title()
		artist = item['artist']['name'].encode('utf-8')
		#rank = item['rank']
		title = cleanTitle(artist.strip()+" - "+song.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, url, thumb])
	if type == "browse":
		for title, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		try:
			nextPage = response['next']
			if 'https://api.deezer.com/' in nextPage:
				addAutoPlayDir(translation(40206), nextPage, "listDeezerVideos", thumb, "", "browse")
		except: pass
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def playYTByTitle(title):
	try:
		finalUrl = ""
		youtubeID = getYoutubeId(title)
		plugin = xbmcaddon.Addon(id='plugin.video.youtube')
		finalUrl = 'plugin://'+plugin.getAddonInfo('id')+'/play/?video_id='+youtubeID
		listitem = xbmcgui.ListItem(path=finalUrl)
		xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
		xbmc.sleep(2000)
		if infoEnabled and not xbmc.abortRequested:
			showInfo()
	except: pass
	
def getYoutubeId(title):
	title = urllib.quote_plus(title.lower()).replace('%5B', '').replace('%5D', '').replace('%28', '').replace('%29', '')
	videoBest = False
	movieID = []
	content = cache("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&order=relevance&q=%s&key=%s" %(title,token), 1)
	response = json.loads(content)
	for videoTrack in response.get('items', []):
		if videoTrack['id']['kind'] == "youtube#video":
			movieID.append('%s @@@ %s' %(videoTrack['snippet']['title'], videoTrack['id']['videoId']))
	if len(movieID) > 0:
		for videoTrack in movieID:
			best = movieID[:]
			if not 'audio' in best[0].strip().lower():
				VIDEOexAUDIO = best[0].split('@@@ ')[1].strip()
			elif not 'audio' in best[1].strip().lower():
				VIDEOexAUDIO = best[1].split('@@@ ')[1].strip()
			elif not 'audio' in best[2].strip().lower():
				VIDEOexAUDIO = best[2].split('@@@ ')[1].strip()
			else:
				VIDEOexAUDIO = best[0].split('@@@ ')[1].strip()
		videoBest = VIDEOexAUDIO
	else:
		xbmc.executebuiltin('Notification(Youtube Music : [COLOR red]!!! URL - ERROR !!![/COLOR], ERROR = [COLOR red]No *SingleEntry* found on YOUTUBE ![/COLOR],6000,'+icon+')')
	return videoBest
	
def queueVideo(url, name, thumb):
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	listitem = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
	playlist.add(url, listitem)
	
def makeRequest(url,headers=False):
	req = urllib2.Request(url)
	if headers:
		for key in headers:
			req.add_header(key, headers[key])
	else:
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
		req.add_header('Accept-Encoding','gzip, deflate')
	response = urllib2.urlopen(req, timeout=30)
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(response.read())
		f = gzip.GzipFile(fileobj=buf)
		link = f.read()
	else:
		link = response.read()
	response.close()
	return link
	
def cache(url, duration=0):
	cacheFile = os.path.join(cachePath, (''.join(c for c in unicode(url, 'utf-8') if c not in '/\\:?"*|<>')).strip())
	if len(cacheFile) > 255:
		cacheFile = cacheFile.replace("part=snippet&type=video&maxResults=5&order=relevance&q", "")
		cacheFile = cacheFile[:255]
	if os.path.exists(cacheFile) and duration!=0 and (time.time()-os.path.getmtime(cacheFile) < 60*60*24*duration):
		fh = xbmcvfs.File(cacheFile, 'r')
		content = fh.read()
		fh.close()
	else:
		content = makeRequest(url)
		fh = xbmcvfs.File(cacheFile, 'w')
		fh.write(content)
		fh.close()
	return content
	
def showInfo():
	count = 0
	while not xbmc.Player().isPlaying():
		xbmc.sleep(200)
		if count == 50:
			break
		count += 1
	xbmc.sleep(infoDelay*1000)
	if xbmc.Player().isPlaying() and infoType == "0":
		xbmc.executebuiltin('XBMC.ActivateWindow(12901)')
		xbmc.sleep(infoDuration*1000)
		xbmc.executebuiltin('ActivateWindow(12005)')
		xbmc.sleep(500)
		xbmc.executebuiltin('Action(Back)')
	elif xbmc.Player().isPlaying() and infoType == "1":
		TOP = translation(40207)
		relTitle = xbmc.getInfoLabel('Player.Title').decode('utf-8').encode('utf-8').replace(", ", "; ")
		relTitle = cleanTitle(relTitle)
		if relTitle.isupper() or relTitle.islower():
			relTitle = relTitle.title()
		runTime = xbmc.getInfoLabel('Player.Duration')
		picture = xbmc.getInfoImage('Player.Art(thumb)')
		if relTitle:
			xbmc.executebuiltin('Notification(%s,%s,%d,%s)' %(TOP, relTitle+"[COLOR blue]  * "+runTime+" *[/COLOR]", infoDuration*1000, picture))
	else:
		pass
	
def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-").replace("#", "").replace('–', '-').replace(';', ' ')
	title = title.replace("&#x00c4", "Ä").replace("&#x00e4", "ä").replace("&#x00d6", "Ö").replace("&#x00f6", "ö").replace("&#x00dc", "Ü").replace("&#x00fc", "ü").replace("&#x00df", "ß")
	title = title.replace("&Auml;", "Ä").replace("&Ouml;", "Ö").replace("&Uuml;", "Ü").replace("&auml;", "ä").replace("&ouml;", "ö").replace("&uuml;", "ü")
	title = title.replace("&agrave;", "à").replace("&aacute;", "á").replace("&egrave;", "è").replace("&eacute;", "é").replace("&igrave;", "ì").replace("&iacute;", "í")
	title = title.replace("&ograve;", "ò").replace("&oacute;", "ó").replace("&ugrave;", "ù").replace("&uacute;", "ú").replace(" ft ", " feat. ").replace(" FT ", " feat. ").replace(" Ft ", " feat. ").replace("Ft.", "feat.").replace("ft.", "feat.").replace(" FEAT ", " feat. ").replace(" Feat ", " feat. ").replace("Feat.", "feat.").replace("Featuring", "feat.")
	title = title.replace("\\'", "'").replace("&x27;", "'").replace("&iexcl;", "¡").replace("&raquo;", "»").replace("&laquo;", "«").replace("►", "*").replace("◄", "*")
	title = title.strip()
	return title
	
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
	liz = xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, 'mediatype':'video'})
	liz.setProperty('IsPlayable', 'true')
	if useThumbAsFanart:
		liz.setProperty("fanart_image", fanart)
	xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')
	entries = []
	entries.append((translation(40208),'RunPlugin(plugin://'+addonID+'/?mode=queueVideo&url='+urllib.quote_plus(u)+'&name='+urllib.quote_plus(name)+'&thumb='+urllib.quote_plus(iconimage)+')',))
	liz.addContextMenuItems(entries)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok
	
def addDir(name, url, mode, iconimage="", description="", type="", limit=""):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
	if useThumbAsFanart:
		liz.setProperty("fanart_image", fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok
	
def addAutoPlayDir(name, url, mode, iconimage="", description="", type="", limit=""):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)+'&thumb='+urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description, 'mediatype':'video'})
	if useThumbAsFanart:
		liz.setProperty("fanart_image", fanart)
	entries = []
	entries.append((translation(40170), 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=)',))
	entries.append((translation(40171), 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=10)',))
	entries.append((translation(40172), 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=20)',))
	entries.append((translation(40173), 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=30)',))
	entries.append((translation(40174), 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=40)',))
	entries.append((translation(40175), 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=50)',))
	liz.addContextMenuItems(entries)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok
	
params = parameters_string_to_dict(sys.argv[2])
name = urllib.unquote_plus(params.get('name', ''))
url = urllib.unquote_plus(params.get('url', ''))
mode = urllib.unquote_plus(params.get('mode', ''))
thumb = urllib.unquote_plus(params.get('thumb', ''))
type = urllib.unquote_plus(params.get('type', ''))
limit = urllib.unquote_plus(params.get('limit', ''))
	
if mode == 'bpMain':
	bpMain()
elif mode == 'listBP':
	listBP(type, url, limit)
elif mode == 'billboardMain':
	billboardMain()
elif mode == 'listBillboardArchiveMain':
	listBillboardArchiveMain()
elif mode == 'listBillboardArchive':
	listBillboardArchive(url)
elif mode == 'listBillboardArchiveVideos':
	listBillboardArchiveVideos(type, url, limit)
elif mode == 'listBillboardChartsTypes':
	listBillboardChartsTypes(url)
elif mode == 'listBillboardCharts_HTML':
	listBillboardCharts_HTML(type, url, limit)
elif mode == 'hypemMain':
	hypemMain()
elif mode == 'listHypem':
	listHypem(type, url, limit)
elif mode == 'listTimeMachine':
	listTimeMachine()
elif mode == 'itunesMain':
	itunesMain()
elif mode == 'listItunesVideos':
	listItunesVideos(type, url, limit)
elif mode == 'ocMain':
	ocMain()
elif mode == 'listOC':
	listOC(type, url, limit)
elif mode == 'spotifyMain':
	spotifyMain()
elif mode == 'listSpotifyGenres':
	listSpotifyGenres(url)
elif mode == 'listSpotifyPlaylists':
	listSpotifyPlaylists(url)
elif mode == 'listSpotifyVideos':
	listSpotifyVideos(type, url, limit)
elif mode == 'SearchDeezer':
	SearchDeezer()
elif mode == 'listDeezerArtists':
	listDeezerArtists(url) 
elif mode == 'listDeezerTracks':
	listDeezerTracks(url) 
elif mode == 'listDeezerAlbums':
	listDeezerAlbums(url)
elif mode == 'listDeezerPlaylists':
	listDeezerPlaylists(url)
elif mode == 'listDeezerUserlists':
	listDeezerUserlists(url)
elif mode == 'listDeezerVideos':
	listDeezerVideos(type, url, thumb, limit)
elif mode == 'playYTByTitle':
	playYTByTitle(url)
elif mode == 'queueVideo':
	queueVideo(url, name, thumb)
elif mode == 'Settings':
	addon.openSettings()
else:
	index()