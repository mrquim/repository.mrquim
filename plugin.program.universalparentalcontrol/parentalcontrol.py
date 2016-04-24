#coding=UTF8
import urllib,urllib2,re,xbmcplugin,xbmcgui,os,xbmcaddon,xbmc
import settings
import time,datetime
from datetime import date
from hashlib import md5
from metahandler import metahandlers
from threading import Thread
import json
import shutil
metainfo = metahandlers.MetaData()
CUSTOM_PC = settings.pc_custom_pc_file()
ADDON_STR = settings.pc_customstrings()
EX_ADDONS = settings.pc_exclude_addons()
EX_MODES = settings.pc_exclude_modes()
FORCE_ADDONS=settings.pc_force_addons()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
settingfile = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.program.universalparentalcontrol'), "settings.xml")
mrating = ['NC-17', 'R','PG-13','PG','G']
tvrating = ['TV-MA','TV-14','TV-PG','TV-G','TV-Y7-FV','TV-Y7','TV-Y']
PC = 'TIMER'

class play_timer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        xbmc.sleep(5000)
        if xbmc.getCondVisibility('Window.IsActive(virtualkeyboard)') or xbmc.getCondVisibility('Window.IsActive(selectdialog)') or xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
            xbmc.sleep(5000)
            if xbmc.getCondVisibility('Window.IsActive(virtualkeyboard)') or xbmc.getCondVisibility('Window.IsActive(selectdialog)') or xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
                xbmc.sleep(5000)
                if xbmc.getCondVisibility('Window.IsActive(virtualkeyboard)') or xbmc.getCondVisibility('Window.IsActive(selectdialog)') or xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
                    xbmc.sleep(5000)
                    if xbmc.getCondVisibility('Window.IsActive(virtualkeyboard)') or xbmc.getCondVisibility('Window.IsActive(selectdialog)') or xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
                        xbmc.sleep(5000)
                        if xbmc.getCondVisibility('Window.IsActive(virtualkeyboard)') or xbmc.getCondVisibility('Window.IsActive(selectdialog)') or xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
                            xbmc.sleep(5000)
                            if xbmc.getCondVisibility('Window.IsActive(virtualkeyboard)') or xbmc.getCondVisibility('Window.IsActive(selectdialog)') or xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
                                xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":1,"method":"Player.Stop","params":{"playerid":1}}')
                                xbmc.executebuiltin('Dialog.Close(all,true)')
                                xbmc.sleep(500)
                                xbmc.executebuiltin('Dialog.Close(virtualkeyboard,true)')
                                xbmc.sleep(500)
                                xbmc.executebuiltin('Dialog.Close(yesnodialog,true)')
		
def checkrating(name,year,mpaa,type,folderpath,foldername):
    oldhubpcontrol=os.path.join(xbmc.translatePath('special://home/addons'), 'script.module.hubparentalcontrol')
    if os.path.isdir(oldhubpcontrol):
        shutil.rmtree(oldhubpcontrol)
    sf=read_from_file(settingfile)
    PC_ENABLE = regex_from_to(sf,'pc_enable_pc" value="', '"')
    id = regex_from_to(sf,'pc_watershed_pc" value="', '"')
    if id == '9':PC_WATERSHED = 25
    elif id == '8':PC_WATERSHED = 23 
    elif id == '7':PC_WATERSHED = 22 
    elif id == '6':PC_WATERSHED = 21
    elif id == '5':PC_WATERSHED = 20
    elif id == '4':PC_WATERSHED = 19
    elif id == '3':PC_WATERSHED = 18
    elif id == '2':PC_WATERSHED = 17
    elif id == '1':PC_WATERSHED = 16
    else:PC_WATERSHED = 15
    id = regex_from_to(sf,'pc_pw_required_at" value="', '"')
    if id == '3':PC_RATING = 4
    elif id == '2':PC_RATING = 3
    elif id == '1':PC_RATING = 2
    else:PC_RATING = 1
    PC_PASS = regex_from_to(sf,'pc_pass" value="', '"')
    playThread = play_timer()
    playThread.start()
    if os.path.isfile(EX_ADDONS):
        ex_s = read_from_file(EX_ADDONS)
    if 'plugin.' in folderpath or 'script.' in folderpath:
        addon_name = regex_from_to(folderpath, 'plugin://', '/')
        if addon_name in ex_s:
            PC = "PC_PLAY"
            print '## UNIVERSAL PARENTAL CONTROL ## PLAY - Addon Excluded'
            return PC,"",name
    if os.path.isfile(EX_MODES):
        ex_m = read_from_file(EX_MODES)
    if ('plugin.' in folderpath or 'script.' in folderpath) and 'mode=' in folderpath:
        addon_name = regex_from_to(folderpath, 'plugin://', '/')
        data = urllib.unquote(folderpath.split(addon_name + '/')[1])
        modetext = regex_from_to(data, 'mode=', '<')
        modestring="%s | mode=%s" % (addon_name,modetext)
        if modestring in ex_m:
            PC = "PC_PLAY"
            print '## UNIVERSAL PARENTAL CONTROL ## PLAY - Mode Excluded'
            return PC,"",name
    addon_name = "notapplicable"
    nm=re.search('(.+?) [(]([0-9]{4})[)]',name)
    if nm:
        name = nm.group(1)
        year = nm.group(2)
    if type == 'stream' and mpaa == "" and ('plugin.' in folderpath or 'script.' in folderpath):
        addon_name = regex_from_to(folderpath, 'plugin://', '/')
    if PC_ENABLE != 'true':
        print '## UNIVERSAL PARENTAL CONTROL ## PLAY - PC Disabled'
        PC = "PC_PLAY"
        return PC,"",name
    else:
        name = clean_file_name(name, use_blanks=False)
        if ' [' in name:
            name = name.split(' [')[0]
        now = time.strftime("%H")
        dialog = xbmcgui.Dialog()
        mpaa,mpaaname,name = parental_control(name,year,mpaa,type,folderpath)

        pw=''
        if mpaa >= PC_RATING and PC_ENABLE == 'true' and ((int(now) < int(PC_WATERSHED) and int(now) > 6) or int(PC_WATERSHED) == 25):
            keyboard = xbmc.Keyboard(pw, name + ' [' + mpaaname + ']\n Enter your PIN/Password to play', True)
            keyboard.doModal()
            if keyboard.isConfirmed():
                pw = keyboard.getText()
            else:
                pw=''
        if int(now) >= int(PC_WATERSHED) or ((pw == PC_PASS) or mpaa < PC_RATING or (int(now) < 6 and int(PC_WATERSHED) != 25)):
            print '## UNIVERSAL PARENTAL CONTROL ## PLAY - params met ' + name + ' ' + mpaaname
            PC = "PC_PLAY"
            return PC,mpaaname,name
        else:
            print '## UNIVERSAL PARENTAL CONTROL ## BLOCKED - ' + name + ' ' + mpaaname
            PC = "PC_BLOCKED"
            return PC,mpaaname,name
		
def parental_control(name,year,vmpaa,type,folderpath):
    sf=read_from_file(settingfile)
    PC_PASS = regex_from_to(sf,'pc_pass" value="', '"')
    id = regex_from_to(sf,'pc_default" value="', '"')
    if id == '1':PC_DEFAULT = "REQUIRE PIN"
    else:PC_DEFAULT = "PLAY"
    if os.path.isfile(FORCE_ADDONS):
        force_s = read_from_file(FORCE_ADDONS)
    if 'plugin.' in folderpath or 'script.' in folderpath:
        addon_name = regex_from_to(folderpath, 'plugin://', '/')
        if addon_name in force_s:
            return 5,"Addon Blocked",name
    mpaa = PC_DEFAULT
    if mpaa == "PLAY":
        mpaa_n = 0
    elif mpaa == "REQUIRE PIN":
        mpaa_n = 4
    nm=re.search('(.+?) [(]([0-9]{4})[)]',name)
    if nm:
        name = nm.group(1)
        year = nm.group(2)
    if ' s0' in name:
        name = name.split(' s0')[0]
    if ' S0' in name:
        name = name.split(' S0')[0]

    if type == 'stream':
        if vmpaa in mrating or vmpaa in tvrating:
            mpaa = vmpaa
        elif vmpaa == 'Not Rated':
            mpaa = 'Unrated'
        else:
            infoLabels = infoLabels = get_meta(name,'movie',year=year)
            if infoLabels['mpaa']=='':
                infoLabels = get_meta(name,'tvshow',year=None,season=None,episode=None,imdb=None)
                if infoLabels['mpaa']=='':
                    nm=re.search('(.+?) [0-9]x[0-9]',name)
                    if nm:
                        name = nm.group(1)
                        infoLabels = get_meta(name,'tvshow',year=None,season=None,episode=None,imdb=None)
                        if infoLabels['mpaa']=='':
                            mpaa = 'notfound'
                        elif infoLabels['mpaa']=='N/A' or infoLabels['mpaa']=='Not Rated':
                            mpaa = 'Unrated'
                        else:
                            mpaa = infoLabels['mpaa']
                elif infoLabels['mpaa']=='N/A' or infoLabels['mpaa']=='Not Rated':
                    mpaa = 'Unrated'
                else:
                    mpaa = infoLabels['mpaa']
            elif infoLabels['mpaa']=='N/A' or infoLabels['mpaa']=='Not Rated':
                mpaa = 'Unrated'
            else:
                mpaa = infoLabels['mpaa']
        if vmpaa=='' and ('plugin.' in folderpath or 'script.' in folderpath) and (mpaa == 'notfound' or mpaa == PC_DEFAULT):#  and name == '' and (name == '..' or name =='' or '=Season' in folderpath)
            name = plugin_mpaa(folderpath)
            if name != "" and ' (' in name and ')' in name:
                name = name.split(' (')[0]
                if year == '':
                    try:
                        year = name.split(' (')[1].replace('(', '').replace(')', '')
                    except:
                        year = ''
        
            if name == 'ADDON_EXCLUDED':
                return 0,'na',name
            if name == 'MODE_EXCLUDED':
                return 0,'na',name
            else:
                infoLabels = infoLabels = get_meta(name,'movie',year=year)
                if infoLabels['mpaa']=='':
                    infoLabels = get_meta(name,'tvshow',year=None,season=None,episode=None,imdb=None)
                    if infoLabels['mpaa']=='N/A':
                        mpaa = 'Unrated'
                    else:
                        mpaa = infoLabels['mpaa']
                elif infoLabels['mpaa']=='N/A':
                    mpaa = 'Unrated'
                else:
                    mpaa = infoLabels['mpaa']
    elif type == 'movies':
        if vmpaa in mrating:
            mpaa = vmpaa
        else:
            infoLabels = infoLabels = get_meta(name,'movie',year=year)
            if infoLabels['mpaa']=='' or infoLabels['mpaa']=='N/A':
                mpaa = 'Unrated'
            else:
                mpaa = infoLabels['mpaa']
    else:
        if vmpaa in tvrating:
            mpaa = vmpaa
        else:
            infoLabels = get_meta(name,'tvshow',year=None,season=None,episode=None,imdb=None)
            if infoLabels['mpaa']=='' or infoLabels['mpaa']=='N/A':
                mpaa = 'Unrated'
            else:
                mpaa = infoLabels['mpaa']
		
    dialog = xbmcgui.Dialog()
    if type == 'movies':
        rating_list = ["No thanks, I'll choose later", "G", "PG","PG-13", "R", "NC-17"]
        rating_list_return = ["No thanks, I'll choose later", "G", "PG","PG-13", "R", "NC-17"]
    elif type == 'stream':
        rating_list = ["Exclude Addon", "Exclude Mode","No thanks, I'll choose later", "G", "PG","PG-13", "R", "NC-17", "TV-Y", "TV-Y7-FG", "TV-PG", "TV-14", "TV-MA"]
        rating_list_return = ["PLAY", "PLAY_mode", "No thanks, I'll choose later", "G", "PG","PG-13", "R", "NC-17", "TV-Y", "TV-Y7-FG", "TV-PG", "TV-14", "TV-MA"]
    else:
        rating_list = ["No thanks, I'll choose later", "TV-Y", "TV-Y7-FG", "TV-PG", "TV-14", "TV-MA"]
        rating_list_return = ["No thanks, I'll choose later", "TV-Y", "TV-Y7-FG", "TV-PG", "TV-14", "TV-MA"]
    if mpaa=="Unrated" or mpaa=="" or ( mpaa=="notfound" and name !=""):
        mpaa = PC_DEFAULT
        if os.path.isfile(CUSTOM_PC):
            s = read_from_file(CUSTOM_PC)
            if name in s:
                search_list = s.split('\n')
                for list in search_list:
                    if list != '':
                        list1 = list.split('<>')
                        title = list1[0]
                        cmpaa = list1[1]
                        vtype = list1[2]
                        if title==name and vtype==type:
                            mpaa=cmpaa
            else:		
                rating_id = dialog.select(name + ":  not found, set your own?", rating_list)
                if(rating_id <= 0):
                    mpaa = PC_DEFAULT
                else:
                    pw=''
                    keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password to save the rating', True)
                    keyboard.doModal()
                    if keyboard.isConfirmed():
                        pw = keyboard.getText()
                    else:
                        pw=''
                    if pw == PC_PASS:
                        mpaa = rating_list_return[rating_id]
                        if mpaa == "PLAY":
                            addon_name = regex_from_to(folderpath, 'plugin://', '/')
                            add_to_list(addon_name,EX_ADDONS)
                        elif mpaa == "PLAY_mode":
                            data = urllib.unquote(folderpath.split('?')[1])
                            modetext = regex_from_to(data, 'mode=', '<')
                            modestring="%s | mode=%s" % (addon_name,modetext)
                            add_to_list(modestring,EX_MODES)
                            mpaa == "PLAY"
                        else:
                            content = '%s<>%s<>%s' % (name, mpaa,type)
                            add_to_list(content,CUSTOM_PC)
                    else:
                        mpaa = PC_DEFAULT


    if mpaa == "PLAY":
        mpaa_n = 0
    elif mpaa == "G" or mpaa == "TV-Y" or mpaa == "TV-Y7-FG":
        mpaa_n = 1
    elif mpaa == "PG" or mpaa == "TV-PG":
        mpaa_n = 2
    elif mpaa == "PG-13" or mpaa == "TV-14":
        mpaa_n = 3
    elif mpaa == "R" or mpaa == "NC-17" or mpaa == "TV-MA" or mpaa == "REQUIRE PIN":
        mpaa_n = 4
    elif mpaa == "Addon Blocked":
        mpaa_n = 5
    return mpaa_n,mpaa,name

def plugin_mpaa(folderpath):
    sf=read_from_file(settingfile)
    PC_PASS = regex_from_to(sf,'pc_pass" value="', '"')
    dialog = xbmcgui.Dialog()
    menu_texts = []
    menu_data = []    
    addon_name = regex_from_to(folderpath, 'plugin://', '/')
    data = urllib.unquote(folderpath.split(addon_name + '/')[1])
    if os.path.isfile(ADDON_STR):
        s = read_from_file(ADDON_STR)
        if addon_name in s:
            search_list = s.split('\n')
            for list in search_list:
                if list != '':
                    list1 = list.split('|')
                    an = list1[0]
                    a_str1 = list1[1]
                    a_str2 = list1[2]
                    if an==addon_name:
                        name = urllib.unquote(regex_from_to(data, a_str1, a_str2))
                        if '<|>' in data:
                            name=name.split('<|>')[0]
                        if ' s0' in data:
                            name=name.split(' s0')[0]
                        if ' S0' in data:
                            name=name.split(' S0')[0]
                        if ' [' in name:
                            name=name.split(' [')[0]
        else:
            pw=''
            keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password to configure this addon', True)
            keyboard.doModal()
            if keyboard.isConfirmed():
                pw = keyboard.getText()
            else:
                pw=''
            if pw == PC_PASS:
                option_list = ["Exclude Addon from Parental Control", "Exclude this mode from Parental Control", "Configure Addon for name search"]
                option_id = dialog.select("What would you like to do?", option_list)
                if(option_id <= 0):
                    name = ""
                if(option_id == 0):
                    add_to_list(addon_name,EX_ADDONS)
                    name = 'ADDON_EXCLUDED'
                if(option_id == 1):
                    data = urllib.unquote(folderpath.split('?')[1])
                    modetext = regex_from_to(data, 'mode=', '<')
                    modestring="%s | mode=%s" % (addon_name,modetext)
                    add_to_list(modestring,EX_MODES)
                    name = 'MODE_EXCLUDED'
                if(option_id == 2):
                    data = urllib.unquote(folderpath.split('?')[1])
                    par = regex_get_all(data, '>', '<')
                    for p in par:
                        text = p
                        if ' [' in text:
                            text = text.split(' [')[0]
                        if '<|>' in text:
                            text = text.split('<|>')[0]
                        if ' s0' in text:
                            text = text.split(' s0')[0]
                        if ' S0' in text:
                            text = text.split(' S0')[0]
                        menu_data.append(p)
                        menu_texts.append(text.replace('<','').replace('>',''))
                    dialog = xbmcgui.Dialog()
                    menu_id = dialog.select('Select the string containing the movie/show name', menu_texts)
                    if(menu_id < 0):
                        name = ""
                    else:
                        textstring = str(menu_data[menu_id])
                        a_str1 = regex_from_to(textstring, '>', '=') + '='
                        a_str2 = '<'
                        
                        name = urllib.unquote(regex_from_to(folderpath, a_str1, a_str2))
                        if ' [' in textstring:
                            name=name.split(' [')[0]
                        if '<|>' in textstring:
                            name=name.split('<|>')[0]
                        if ' s0' in textstring:
                            name=name.split(' s0')[0]
                        if ' S0' in textstring:
                            name=name.split(' S0')[0]
                        content = '%s|%s|%s' % (addon_name, a_str1,a_str2)
                        add_to_list(content,ADDON_STR)
            else:
                name = ""

    return clean_file_name(name, use_blanks=False)
	
    	
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

def strip_text(r, f, t, excluding=True):
    r = re.search("(?i)" + f + "([\S\s]+?)" + t, r).group(1)
    return r

def get_meta(name,types=None,year=None,season=None,episode=None,imdb=None,episode_title=None):
    if 'movie' in types:
        meta = metainfo.get_meta('movie',name,year)
        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa': meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Aired': meta['premiered'],'year': meta['year']}
    else:
        meta = metainfo.get_meta('tvshow',name,'','','')
        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa': meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Episode': meta['episode'],'Aired': meta['premiered'],'Playcount': meta['playcount'],'Overlay': meta['overlay'],'year': meta['year']}
    return infoLabels

#### HELPERS ####
def batch_replace(s, replace_info):
    for r in replace_info:
        s = str(s).replace(r[0], r[1])
    return s

def get_items_in_dir(path):
    items = []
    for dirpath, dirnames, filenames in os.walk(path): 
        for subdirname in dirnames: 
            items.append(subdirname) 
        for filename in filenames:
            items.append(filename)
            #if filename.endswith(".strm"): 
            #    items.append(filename[:-5])
        
    return items


def string_to_list(s):
    r = []
    s = 'r = ' + s
    exec(s)
    return r

def clean_file_name(s, use_encoding=False, use_blanks=True):
    hex_entities = [['&#x26;', '&'], ["&#x27;", "'"], ['&#xC6;', 'AE'], ['&#xC7;', 'C'],
                ['&#xF4;', 'o'], ['&#xE9;', 'e'], ['&#xEB;', 'e'], ['&#xED;', 'i'],
                ['&#xEE;', 'i'], ['&#xA2;', 'c'], ['&#xE2;', 'a'], ['&#xEF;', 'i'],
                ['&#xE1;', 'a'], ['&#xE8;', 'e'], ['%2E', '.'], ['&frac12;', '%BD'],
                ['&#xBD;', '%BD'], ['&#xB3;', '%B3'], ['&#xB0;', '%B0'], ['&amp;', '&'], ['&#xB7;', '.'], ['&#xE4;', 'A'], ["&#39", "'"]]
    
    special_encoded = [['"', '%22'], ['*', '%2A'], ['/', '%2F'], [':', ','], ['<', '%3C'],
                        ['>', '%3E'], ['?', '%3F'], ['\\', '%5C'], ['|', '%7C']]
    
    special_blanks = [['"', ' '], ['*', ' '], ['/', ' '], [':', ' '], ['<', ' '],
                        ['>', ' '], ['?', ' '], ['\\', ' '], ['|', ' '], ['%BD;', ' '],
                        ['%B3;', ' '], ['%B0;', ' ']]
    
    s = batch_replace(s, hex_entities)
    if use_encoding:
        s = batch_replace(s, special_encoded)
    if use_blanks:
        s = batch_replace(s, special_blanks)
    s = s.strip()
    
    return s
	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path


def strip_text(r, f, t, excluding=True):
    r = re.search("(?i)" + f + "([\S\s]+?)" + t, r).group(1)
    return r


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
    list = list.replace('artist_pl', 'favartist_pl')
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

	

		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")



