import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os,re
import subprocess
import settings
import json
import parentalcontrol
import shutil
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.program.universalparentalcontrol/art', 'lock.png'))


class CapturePlayer(xbmc.Player):
    PC = 'TIMER'
    def __init__(self, *args):
        xbmc.Player.__init__(self)
		
    def onPlayBackStarted(self):
        vlabel = xbmc.getInfoLabel('ListItem.Label')
        vtitle = xbmc.getInfoLabel('ListItem.Title')
        vfolderpath = xbmc.getInfoLabel('Container.FolderPath')
        vfoldername = xbmc.getInfoLabel('Container.FolderName')
        vmpaa = xbmc.getInfoLabel('ListItem.Mpaa')
        vmeta_title = xbmc.getInfoLabel('VideoPlayer.Title')
        vmeta_mpaa = xbmc.getInfoLabel('VideoPlayer.mpaa')
        playerid = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'))['result'][0]['type']
        
        t = 'stream'
        settingfile = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.program.universalparentalcontrol'), "settings.xml")
        s=read_from_file(settingfile)
        PC_ENABLE = regex_from_to(s,'pc_enable_pc" value="', '"')
        xbmc.log( str(PC_ENABLE) )
        if playerid == 'video' and PC_ENABLE == 'true':
            if xbmc.getCondVisibility("VideoPlayer.Content(movies)"):
                xbmc.log( "###MOVIE###" )
                try:
                    title = xbmc.getInfoLabel('VideoPlayer.Title')
                    mpaa = xbmc.getInfoLabel('VideoPlayer.mpaa')
                    year = xbmc.getInfoLabel('VideoPlayer.Year')
                    t = 'movies'
                except:
                    xbmc.log( "Movie File not working" )
            elif xbmc.getCondVisibility('VideoPlayer.Content(episodes)'):
                xbmc.log( "###TV SHOW###" )
            # Check for tv show title and season to make sure it's really an episode
                try:
                    tvtitle = xbmc.getInfoLabel('VideoPlayer.TVShowTitle')
                    tvmpaa = xbmc.getInfoLabel('VideoPlayer.mpaa')
                    tvyear = xbmc.getInfoLabel('VideoPlayer.Year')
                    t = 'tvshow'
                except:
                    xbmc.log( "TV File not working" )
	
            if t == 'movies':
                title = title
                mpaa = mpaa
                year = year
            elif t == 'tvshow':
                title = tvtitle
                mpaa = tvmpaa
                year = tvyear
            elif t == 'stream':
                if vmeta_title != "":
                    title = vmeta_title
                else:
                    title = vlabel
                if vmeta_mpaa != "":
                    mpaa = vmeta_mpaa
                else:
                    mpaa = vmpaa
                year = ""
            xbmc.log("##### Playback started vlabel is " + vlabel + "--" + t + " : "  + title + " " + mpaa+ " " + year + " " + vfolderpath, level=xbmc.LOGNOTICE)			
            PC,mpaaname,name = parentalcontrol.checkrating(title,year,mpaa.replace('Rated ','').replace('rated ',''),t,vfolderpath.replace('?', '?<>').replace('&', '<>') + '<>"',vfoldername)
            if PC != 'PC_PLAY':
                xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":1,"method":"Player.Stop","params":{"playerid":1}}')
                xbmc.sleep(500)
                xbmc.executebuiltin('Dialog.Close(yesnodialog,true)')
                notification('UNIVERSAL Parental Control', 'Incorrect PIN', '3000', iconart)
            else:
                speed = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Player.GetProperties","params":{"playerid":1,"properties":["speed"]},"id":"1"} '))['result']['speed']
                if int(speed) == 0:
                    xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":1,"method":"Player.PlayPause","params":{"playerid":1}}')


def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
	
def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None
			
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def main():

    player = CapturePlayer()
    while not xbmc.abortRequested:
        xbmc.sleep(500)
    del player

xbmc.log("##### UNIVERSAL PARENTAL CONTROL STARTED")
main()





		
