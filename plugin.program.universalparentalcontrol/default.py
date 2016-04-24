import xbmc,xbmcaddon,xbmcgui,xbmcplugin,os,sys,re,time,datetime,settings,urllib
from hashlib import md5
import hashlib
import glob
import shutil
AddonTitle="Universal Parental Control"
addon_id='plugin.program.universalparentalcontrol'
local=xbmcaddon.Addon(id=addon_id); maintenancepath=xbmc.translatePath(local.getAddonInfo('path'))
art=xbmc.translatePath(os.path.join('special://home/addons/plugin.program.universalparentalcontrol/art', ''))
PC_ENABLE=settings.pc_enable_pc(); PC_WATERSHED=settings.pc_watershed_pc(); PC_RATING=settings.pc_pw_required_at(); PC_PASS=settings.pc_pass(); PC_DEFAULT=settings.pc_default(); PC_TOGGLE=settings.pc_enable_pc_settings(); CUSTOM_PC=settings.pc_custom_pc_file(); ADDON_STR=settings.pc_customstrings(); EX_ADDONS=settings.pc_exclude_addons(); EX_MODES=settings.pc_exclude_modes(); CUSTOMSTRINGS=settings.pc_customstrings(); FORCE_ADDONS=settings.pc_force_addons()
profiles_path=xbmc.translatePath(os.path.join('special://profile','profiles.xml'))

def CATEGORIES():
    addDir("Settings",'url',63,xbmc.translatePath(os.path.join(art, 'settings.png')),"")
    addDir("Help",'url',61,xbmc.translatePath(os.path.join(art, 'info.png')),"")
    addDir("Exclude Addons (select to add/remove)","req",64,xbmc.translatePath(os.path.join(art, 'list.png')),"")
    addDir("Always require PIN for selected addons (select to add/remove)","req",72,xbmc.translatePath(os.path.join(art, 'list.png')),"")
    addDir("Excluded Addon Modes (select to remove)","req",67,xbmc.translatePath(os.path.join(art, 'list.png')),"")
    addDir("Custom Addon Strings (select to remove)","req",68,xbmc.translatePath(os.path.join(art, 'list.png')),"")
    addDir("Custom Ratings (select to remove)","req",69,xbmc.translatePath(os.path.join(art, 'ratings.jpg')),"")
    if PC_TOGGLE=='LOCKED': addDir('[COLOR green]'+'UNLOCK Parental Control Settings'+'[/COLOR]','url',62,xbmc.translatePath(os.path.join(art, 'lock.png')),"")
    else: addDir('[COLOR red]'+'LOCK Parental Control Settings'+'[/COLOR]','url',62,xbmc.translatePath(os.path.join(art, 'unlock.png')),"")
    addDir("[COLOR gold]How to stop this this addon being disabled or removed[/COLOR]","req",71,xbmc.translatePath(os.path.join(art, 'info.png')),"")
    #addDir("Lock Addon Manager and Programs","req",70,xbmc.translatePath(os.path.join(art, 'settings.png')),"")
	
################################
###     PARENTAL CONTROLS    ###
################################
def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        for l in lines:
            print l
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file):
    dialog=xbmcgui.Dialog(); keyboard=xbmc.Keyboard("",'Enter your PIN/Password',True); keyboard.doModal()
    if keyboard.isConfirmed():
        pw=keyboard.getText()
        if pw==PC_PASS:
            if find_list(list, file) >= 0:
                return

            if os.path.isfile(file):
                content = read_from_file(file)
            else:
                content = ""

            lines = content.split('\n')
            s = '%s\n' % list
            for line in lines:
                if len(line) > 0:
                    s = s + line + '\n'
            write_to_file(file, s)
    xbmc.executebuiltin("Container.Refresh")
    
def remove_from_list(list, file):
    dialog=xbmcgui.Dialog(); keyboard=xbmc.Keyboard("",'Enter your PIN/Password',True); keyboard.doModal()
    if keyboard.isConfirmed():
        pw=keyboard.getText()
        if pw==PC_PASS:
            if '[COLOR' in list: list=list.replace('[COLOR red]','').replace('[/COLOR]','')
            index = find_list(list, file)
            if index >= 0:
                content = read_from_file(file)
                lines = content.split('\n')
                lines.pop(index)
                s = ''
                for line in lines:
                    if len(line) > 0:
                        s = s + line + '\n'
                write_to_file(file, s)
        xbmc.executebuiltin("Container.Refresh")
		
def write_to_file(path, content, append=False, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print("Could not write to " + path)
        return False

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

#def master_lock():
    #hpass = hashlib.md5(PC_PASS).hexdigest()
    #s = read_from_file(profiles_path)
    #s=re.sub('<lockcode>.*?</lockcode>','<lockcode>'+hpass+'</lockcode>',s)
    #s=re.sub('<lockaddonmanager>.*?</lockaddonmanager>','<lockaddonmanager>true</lockaddonmanager>',s)
    #s=re.sub('<lockprograms>.*?</lockprograms>','<lockprograms>true</lockprograms>',s)
    #s=re.sub('<lockmode>.*?</lockmode>','<lockmode>3</lockmode>',s)
    #write_to_file(profiles_path, s)
def pc_setting(pw=""): #Lock or unlock Parental Control Settings		
    dialog=xbmcgui.Dialog(); keyboard=xbmc.Keyboard(pw,'Enter your PIN/Password',True); keyboard.doModal()
    if keyboard.isConfirmed():
        pw=keyboard.getText()
        if pw==PC_PASS:
            if PC_TOGGLE=="UNLOCKED": local.setSetting('pc_enable_pc_settings',value='LOCKED'); xbmc.executebuiltin("Container.Refresh")
            else: local.setSetting('pc_enable_pc_settings',value='UNLOCKED'); xbmc.executebuiltin("Container.Refresh"); local.openSettings()				
        else: dialog.ok("HUB Parental Control","Incorrect PIN/Password")
def pc_exclude(pw): #Include/Exclude Addons	
    if os.path.isfile(EX_ADDONS): s = read_from_file(EX_ADDONS)
    pluginpath = xbmc.translatePath(os.path.join('special://home/addons',''))
    for file in os.listdir(pluginpath):
        if 'plugin.' in file or 'script.' in file:
            if file in s:addDir('[COLOR red]'+file+'[/COLOR]',EX_ADDONS,65,"","")
            else:addDir(file,EX_ADDONS,66,"","")
def pc_force_addons(pw): #Force PIN entry for all videos played from selected addons	
    if os.path.isfile(FORCE_ADDONS): s = read_from_file(FORCE_ADDONS)
    pluginpath = xbmc.translatePath(os.path.join('special://home/addons',''))
    for file in os.listdir(pluginpath):
        if 'plugin.' in file or 'script.' in file:
            if file in s:addDir('[COLOR red]'+file+'[/COLOR]',FORCE_ADDONS,65,"","")
            else:addDir(file,FORCE_ADDONS,66,"","")
def pc_excludemode(): #Include/Exclude Addons	
    if os.path.isfile(EX_MODES): 
        s = read_from_file(EX_MODES)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':addDir(list,EX_MODES,65,"","")
def pc_customstring(): #Include/Exclude Addons	
    if os.path.isfile(CUSTOMSTRINGS): 
        s = read_from_file(CUSTOMSTRINGS)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':addDir(list,CUSTOMSTRINGS,65,"","")
def pc_customratings():
    if os.path.isfile(CUSTOM_PC): 
        s = read_from_file(CUSTOM_PC)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':addDir(list,CUSTOM_PC,65,"","")			
def parentalcontrol_help(text): header="[B][COLOR red]"+text+"[/B][/COLOR]"; msg=os.path.join(local.getAddonInfo('path'),'resources','help','parental_control.txt'); TextBoxes(header,msg)
def ml_protect(text): header="[B][COLOR red]"+text+"[/B][/COLOR]"; msg=os.path.join(local.getAddonInfo('path'),'resources','help','ml_protect.txt'); TextBoxes(header,msg)
def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
            WINDOW=10147; CONTROL_LABEL=1; CONTROL_TEXTBOX=5 # constants
            def __init__(self,*args,**kwargs):
                xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW,)) # activate the text viewer window
                self.win=xbmcgui.Window(self.WINDOW) # get window
                xbmc.sleep(500) # give window time to initialize
                self.setControls()
            def setControls(self):
                self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
                try: f=open(anounce); text=f.read()
                except: text=anounce
                self.win.getControl(self.CONTROL_TEXTBOX).setText(text); return
        TextBox()
################################
###    END PARENTAL CONTROLS ###
################################


		
def addDir(name,url,mode,iconimage,fanart):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart); ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo(type="Video",infoLabels={"Title":name,"Plot":name}); liz.setProperty("Fanart_Image",fanart)
    if mode==61 or mode==62 or mode==63 or mode==65 or mode==66 or mode==70 or mode==71:
          ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else: ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
def get_params(param=[]):
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]; cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&'); param={}
        for i in range(len(pairsofparams)):
             splitparams={}; splitparams=pairsofparams[i].split('=')
             if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
    return param
params=get_params(); url=None; name=None; mode=None; iconimage=None; fanart=None
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    mode=int(params["mode"])
except: pass
try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name); print "IconImage: "+str(iconimage)
if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==60: parental_controls(name)
elif mode==61: parentalcontrol_help(name)
elif mode==62: pc_setting()
elif mode==63: local.openSettings()
elif mode==64: pc_exclude(url)
elif mode==65: remove_from_list(name,url)
elif mode==66: add_to_list(name,url)
elif mode==67: pc_excludemode()	
elif mode==68: pc_customstring()
elif mode==69: pc_customratings()
elif mode==70: master_lock()
elif mode==71: ml_protect(name)
elif mode==72: pc_force_addons(url)		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
