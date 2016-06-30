"""
 Author: frenchdj

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
 """

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime
from resources.lib.common_variables import *
from resources.lib.directory import *
from resources.lib.youtubewrapper import *
from resources.lib.watched import * 

fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami', 'fanart.jpg'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami/resources/', 'fan01.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami/resources/img', ''))
art01 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami/resources/img/Series', ''))
art02 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami/resources/img/Herois', ''))
art03 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami/resources/img/Panda', ''))
art04 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami/resources/img/Bebe', ''))
art05 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami/resources/img/Princesas', ''))
art06 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.jami/resources/img/Classicos', ''))

def CATEGORIES():
        addDir(''+translate(10012)+'','PLo2-ar7cjUFNkyRq6Kix6R5uFjXAzukiB',1,art+ 'Filmes.png')
        addDir('[B]Series Recentes[/B]','url',11,art + 'Series.png')
        addDir('[B]Super Herois[/B]','url',12,art + 'Herois.png')
        addDir('[B]Recreio do Panda[/B]','url',13,art + 'Panda.png')
        addDir(''+translate(60001)+'','PLo2-ar7cjUFNrfAJkl_sT2OIOrlSmkp4X',1,art+ 'Animais.png')
        addDir(''+translate(70001)+'','PLsWbExGo1KPaTOkYs05uzBxX5DThs3jAC',1,art+ 'Curtas.png')
        addDir('Cantinho do Bebe ','url',16,art + 'Bebe.png')
        addDir('[B]Princesas e Musicais[/B]','url',17,art + 'Princesas.png') 
        addDir('[B]Classicos Antigos[/B]','url',18,art + 'Classicos.png')
        addDir(''+translate(110001)+'','PLo2-ar7cjUFNwjVPIwGuRoMWbviK75uD3',1,art+ 'Disney.png')

def Series():
        addDir(''+translate(30021)+'Ruca [PT]','PLsWbExGo1KPaYUuRSfzyF1X11Czip4259',1,art01 + 'icon01.png')
        addDir(''+translate(30022)+'Aventuras de Max [PT]','PLsWbExGo1KPbil5fBWgJlv2gQPTcABI7x',1,art01 + 'icon02.png')
        addDir(''+translate(30023)+'Octonautas [PT]','PLsWbExGo1KPazbyjJE2UwlXn5rYZMDVoh',1,art01 + 'icon03.png')
        addDir(''+translate(30024)+'Noddy [PT]','PLsWbExGo1KPZTiUyNEHtkbN2atTuAoQHL',1,art01 + 'icon04.png') 
        addDir(''+translate(30025)+'Vila Moleza [PT]','PLsWbExGo1KPaYskF8yclTCPUNCvvNP35E',1,art01 + 'icon05.png')
        addDir(''+translate(30026)+'Alvin e os Esquilos [BR]','PLo2-ar7cjUFPE2qHjXMek1lpexq-fOzCl',1,art01 + 'icon06.png')
        addDir(''+translate(30027)+'Mate e os Carrinhos [BR]','PLo2-ar7cjUFOFp-eQ7cEc27f3YfpTBZG2',1,art01 + 'icon07.png')
        addDir(''+translate(30028)+'Jelly Jamm [BR]','PLo2-ar7cjUFPQrsD_lKAu-mJJx01xZrm9',1,art01 + 'icon08.png')
        addDir(''+translate(30029)+'Chaves [BR]','PLo2-ar7cjUFNWPjayCxIDJOdBRNh4ZVbk',1,art01 + 'icon09.png')
        addDir(''+translate(30030)+'[ Bernard Bear ]','PLo2-ar7cjUFN0WaCIqv_lJVJRv1AmzKZQ',1,art01 + 'icon10.png')
        addDir(''+translate(30031)+'[ Angry Birds ]','PLo2-ar7cjUFPEbbV7nuMX_LOFTVd1xb-c',1,art01 + 'icon11.png')
        addDir(''+translate(30032)+'[ A Ovelha Chone ]','PLo2-ar7cjUFNSsvOA-qhQUua3MQsFHhlc',1,art01 + 'icon12.png')
        addDir(''+translate(30033)+'[ Minions Cartoon ]','PLo2-ar7cjUFMPDPmCDue6EFF1yq1bca-C',1,art01 + 'icon13.png')
			
def Herois():
        addDir(''+translate(40033)+'Tartarugas Ninja [PT]','PLsWbExGo1KPZpo076XQwp5nzVco5ZRUcN',1,art02 + 'icon01.png')
        addDir(''+translate(40034)+'Sonic Underground [BR]','PLo2-ar7cjUFPAGakDRSgXXBQcvFuItuJP',1,art02 + 'icon02.png')
        addDir(''+translate(40035)+'Sonic Boom [BR]','PLo2-ar7cjUFNiVdqPL58P6Caaw-1d-HU9',1,art02 + 'icon03.png')
        addDir(''+translate(40036)+'Sonic X [BR]','PLo2-ar7cjUFM7Zsz6VIhqHEw7cmb7SMC1',1,art02 + 'icon04.png')
        addDir(''+translate(40037)+'Team Hot Wheels [BR]','PLo2-ar7cjUFPm8yNpZ_AL6Q3b2oQDWcsa',1,art02 + 'icon05.png') 
        
def Panda():
        addDir(''+translate(50001)+'Panda e os Amigos [PT]','PLsWbExGo1KPaOQDuO_oLgY-ar_AzpF3c5',1,art03 + 'icon01.png')  
        addDir(''+translate(50002)+'Panda e os Caricas [PT]','PLsWbExGo1KPY2PlA-4IKzcPKdrEWXAkp_',1,art03 + 'icon02.png')  
        addDir(''+translate(50003)+'Bairro do Panda [PT]','PLsWbExGo1KPbH7Tlh5kkcMiNXCulEtRXL',1,art03 + 'icon03.png') 
        addDir(''+translate(50004)+'Festival Panda [PT]','PLsWbExGo1KPbfrDHpmegNmqUPf-EKax_w',1,art03 + 'icon04.png')
    
def Bebe():
        addDir(''+translate(80001)+'Baby TV [PT]','PLsWbExGo1KPblPXGlEcuaG-ES6yWIAYJM',1,art04 + 'icon01.png')	
        addDir(''+translate(80002)+'Herois da Cidade [PT]','PLFepGKlvmn74D95OwZkSSQR3uk4T2ReHD',1,art04 + 'icon02.png')
        addDir(''+translate(80003)+'Pocoyo [PT]','PLsWbExGo1KPZHaxIGBKNfTymSWDdCW2mC',1,art04 + 'icon03.png')
        addDir(''+translate(80004)+'Bob o Construtor [PT]','PLsWbExGo1KPZITh_DyO7ye-UVdMfAQXfh',1,art04 + 'icon04.png')
        addDir(''+translate(80005)+'Joao Bebe [PT]','PLsWbExGo1KPYZSZpWWz7knn6HlZuvH0C0',1,art04 + 'icon05.png')
        addDir(''+translate(80006)+'Thomas e Amigos [PT/BR]','PLo2-ar7cjUFPRDkbVFxbir24fCk7fJJ30',1,art04 + 'icon06.png')
        addDir(''+translate(80007)+'Daniel Tigre [BR]','PLo2-ar7cjUFO0QnmuVESjoDmCinO5leMZ',1,art04 + 'icon07.png')	 
        addDir(''+translate(80008)+'[ Tutitut ] ','PLo2-ar7cjUFMTvmJwl1i-wlu6S8Jj_oEd',1,art04 + 'icon08.png')	    	
                     	
def Princesas():
        addDir(''+translate(90001)+'Heidi 3D [PT]','PLsWbExGo1KPZKVQoMG3-ikbIIyU5_AsvY',1,art05 + 'icon01.png')
        addDir(''+translate(90002)+'Abelha Maia 3D [PT]','PLsWbExGo1KPaQx2dXjba2q29_teZBeEfm',1,art05 + 'icon02.png')
        addDir(''+translate(90003)+'Hello Kitty [PT]','PLsWbExGo1KPZxKeoOmZQNe-UpKotBwcbt',1,art05 + 'icon03.png')
        addDir(''+translate(90004)+'Masha e o Urso [BR]','PLo2-ar7cjUFMYfCv_fOqvrU1kE_CWlEIo',1,art05 + 'icon04.png')
        addDir(''+translate(90005)+'Turma da Monica [BR]','PLo2-ar7cjUFPMncfl2az_nAEObDAzilgu',1,art05 + 'icon05.png')
        addDir(''+translate(90006)+'Musicas da Disney [PT]','PLsWbExGo1KPbfgemAaGoVS3eZpx4gxd8n',1,art05 + 'icon06.png')
        addDir(''+translate(90007)+'Musicas do Frozen [PT]','PLsWbExGo1KPaVbT6Wze_cs7zK9oCkdgGg',1,art05 + 'icon07.png')
        addDir(''+translate(90008)+'Xana Toc Toc [PT]','PLsWbExGo1KPYu3w9mnbqvlPQMaTVEixF7',1,art05 + 'icon08.png')
        addDir(''+translate(90009)+'Violetta [ES]','PLo2-ar7cjUFNy9tL19UbYpibvvMpSFZIi',1,art05 + 'icon09.png')     
		
def Classicos():
        addDir(''+translate(100001)+'Rua Sesamo [PT]','PLsWbExGo1KPZMSjszQz49Let2KEsNptif',1,art06 + 'icon01.png')   
        addDir(''+translate(100002)+'Era uma Vez [PT]','PLsWbExGo1KPZRlqvLY2Ja_SAJZMgBcdxD',1,art06 + 'icon02.png')   
        addDir(''+translate(100003)+'Sinsala Grimm [PT]','PLsWbExGo1KPaDiMryemJSKfU-nksiKkkA',1,art06 + 'icon03.png')   
        addDir(''+translate(100004)+'Misteriosas Cidades [PT]','PLsWbExGo1KPbQemayFmjCFhcg_Okm8Nvz',1,art06 + 'icon04.png')
        addDir(''+translate(100005)+'Dartacao [PT]','PLsWbExGo1KPb3QuNAHUoBDBGdA981SDjP',1,art06 + 'icon05.png')   
        addDir(''+translate(100007)+'Tom Sawyer [PT]','PLsWbExGo1KPbgxDBmh-wn0zIzJY8kiqSY',1,art06 + 'icon06.png') 
        addDir(''+translate(100007)+'Shin Chan [PT]','PLsWbExGo1KPYbO6J7dXHS_A8pSgIPyU2m',1,art06 + 'icon07.png') 
        addDir(''+translate(100008)+'Conan o Rapaz do Futuro [PT]','PLsWbExGo1KPYzDLiL1KXwNPL83lTJUKjz',1,art06 + 'icon08.png') 
        addDir(''+translate(100009)+'Carrinha Magica [PT]','PLsWbExGo1KPau8sdE0xa0-99JcMJ3Zf8q',1,art06 + 'icon09.png') 		
        addDir(''+translate(100010)+'Charlie Brown [BR]','PLo2-ar7cjUFO_ZKIkP-754NjK9McM6aN_',1,art06 + 'icon10.png')     
		


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


params=get_params()
url=None
name=None
mode=None
iconimage=None
page = None
token = None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except:
	try: 
		mode=params["mode"]
	except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: token=urllib.unquote_plus(params["token"])
except: pass
try: page=int(params["page"])
except: page = 1

print ("Mode: "+str(mode))
print ("URL: "+str(url))
print ("Name: "+str(name))
print ("iconimage: "+str(iconimage))
print ("Page: "+str(page))
print ("Token: "+str(token))

		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        return_youtubevideos(name,url,token,page)

elif mode==5: 
        play_youtube_video(url)

elif mode==6:
        mark_as_watched(url)

elif mode==7:
        removed_watched(url)

elif mode==8:
        add_to_bookmarks(url)

elif mode==9:
        remove_from_bookmarks(url)
		
elif mode==11:
        print ""+url
        Series()

elif mode==12:
        print ""+url
        Herois()

elif mode==13:
        print ""+url
        Panda()
        
elif mode==16:
        print ""+url
        Bebe()
		
elif mode==17:
        print ""+url
        Princesas()
		
elif mode==18:
        print ""+url
        Classicos()
		
		
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))
