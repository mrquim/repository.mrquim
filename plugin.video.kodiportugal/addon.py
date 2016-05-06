#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2015 xsteal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xbmcplugin,xbmc,xbmcgui,xbmcaddon,xbmcplugin,xbmcvfs
import urllib,os,sys,base64,urllib2,json,math


__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo("id")
__ADDON__   = xbmcaddon.Addon(__ADDON_ID__)
__ADDON_FOLDER__    = __ADDON__.getAddonInfo('path')
__SETTING__ = xbmcaddon.Addon().getSetting
__ART_FOLDER__  = os.path.join(__ADDON_FOLDER__,'resources','img')
__FANART__      = os.path.join(__ADDON_FOLDER__,'fanart.jpg')

__ALERTA__ = xbmcgui.Dialog().ok

__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'} #ISO-8859-1,

__CANAL_ID__ = base64.urlsafe_b64decode('VUNkYUJCWTV1a0ZUVnVjdHpmckM5NnRB')
__YOUTUBE_API__ = base64.urlsafe_b64decode('QUl6YVN5RC1NMURHd1JRVk04czBkY0VMeFFJcmh5RkQxNHNjNEJV')


def menu():

    url = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&channelId=%s&maxResults=50&key=%s' % (__CANAL_ID__, __YOUTUBE_API__)
    dados = abrir_url(url)
    resultado = json.loads(dados)

    total = len(resultado["items"])
    for item in resultado["items"]:
        itemId = item["id"]
        imagem = item["snippet"]["thumbnails"]["high"]["url"]
        titulo = item["snippet"]["title"]
        addDir('[B]'+titulo.encode('utf-8')+'[/B]',itemId,1,imagem,1,total,token='token')

    vista_menu()

def listaVideos(nome, url, token, pagina):

    if pagina == 1:
        urlAPI = 'https://www.googleapis.com/youtube/v3/playlistItems?part=id,snippet,contentDetails&maxResults=%s&playlistId=%s&key=%s' % (str(20), url, __YOUTUBE_API__)
    else:
        urlAPI = 'https://www.googleapis.com/youtube/v3/playlistItems?part=id,snippet,contentDetails&maxResults=%s&playlistId=%s&key=%s&pageToken=%s' % (str(20), url, __YOUTUBE_API__, token)

    resultado = abrir_url(urlAPI)
    resultado = json.loads(resultado)

    try:
        proximo = resultado["nextPageToken"]
    except:
        proximo = ''
    try:
        total = resultado["pageInfo"]["totalResults"]
    except:
        total = 1

    lista = resultado["items"]
    totalLista = len(lista)
    totalPaginas = int(math.ceil((float(total)/20)))

    videos = []

    if lista:
        for video in lista:
            videoId = video["contentDetails"]["videoId"]
            videos.append(videoId)

        videos = ','.join(videos)
        urlAPI = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id=%s&key=%s' % (videos, __YOUTUBE_API__)
        resultado = abrir_url(urlAPI)
        resultado = json.loads(resultado)

        listagem = resultado["items"]

        for video in listagem:
            titulo = video["snippet"]["title"]
            plot = video["snippet"]["description"]
            imagem = video["snippet"]["thumbnails"]["high"]["url"]
            videoId = video["id"]

            infolabels = {'Plot':plot.encode('utf-8'),'Title':titulo.encode('utf-8')}

            addVideo(titulo.encode('utf-8'), videoId, 2, imagem, pagina, infolabels)


        if totalPaginas > 1 and totalPaginas >= (pagina+1):
            addDir('Proxima pagina '+str(pagina+1), url, 1, 'proximo.png', pagina+1, 1, token=proximo)

        vista_episodios()
    	xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    	return




###################################################################################
#                              DEFININCOES                                        #
###################################################################################

def abrirDefinincoes():
    __ADDON__.openSettings()
    addDir('Entrar novamente','url',None,os.path.join(__ART_FOLDER__, __SKIN__,'retroceder.png'), 0)
    vista_menu()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def vista_menu():
    opcao = __ADDON__.getSetting('menuView')
    if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
    elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51")


def vista_episodios():
    opcao = __ADDON__.getSetting('episodiosView')
    if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
    elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
    elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")

###################################################################################
#                               FUNCOES JA FEITAS                                 #
###################################################################################


def abrir_url(url, post=None, header=None, code=False, erro=False):
    if header == None:
        header = __HEADERS__

    if post:
        req = urllib2.Request(url, data=post, headers=header)
    else:
        req = urllib2.Request(url, headers=header)

    try:
        response = urllib2.urlopen(req, timeout=30)
    except urllib2.HTTPError as response:
        if erro == True:
            return str(response.code), "asd"

    link=response.read()

    if code:
        return str(response.code), link

    response.close()
    return link


def addDir(nome,url,mode,iconimage,pagina,numero,token):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(nome)+"&pagina="+str(pagina)+"&token="+urllib.quote_plus(token)
	ok=True
	liz=xbmcgui.ListItem(nome)
	liz.setInfo( type="Video", infoLabels={ "Title": nome })
	liz.setArt({ 'thumb': iconimage })
	liz.setPath(u)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=numero)
	return ok


def addVideo(nome, url, mode, iconImage, pagina, infoLabels):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(nome)+"&pagina="+str(pagina)
    ok=True

    liz=xbmcgui.ListItem(nome, iconImage="DefaultVideo.png", thumbnailImage=iconImage)
    liz.setPath(u)
    liz.setInfo(type="Video", infoLabels=infoLabels)

    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def clean(text):
    command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def player(url):
    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % url
    item = xbmcgui.ListItem(path=url)
    item.setProperty('IsPlayable', 'true')
    xbmc.Player().play(url, item)


########################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
    return param


params=get_params()
url=None
name=None
mode=None
iconimage=None
link=None
pagina=None
token=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: link=urllib.unquote_plus(params["link"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: token=urllib.unquote_plus(params["token"])
except: pass
try: pagina=int(params["pagina"])
except: pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "LINK. "+str(link)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Pagina: "+str(pagina)


###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################
if mode==None or url==None or len(url)<1:
    menu()
    xbmcplugin.setContent(int(sys.argv[1]), 'files')
elif mode==1: listaVideos(name, url, token, pagina)
elif mode==2: player(url)
elif mode==1000: abrirDefinincoes()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
