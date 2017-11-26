# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcvfs
import json
import re
import urllib
import os

__addon__               = xbmcaddon.Addon()

import debug

class LINK:
    def start(self, id, type):
        
        # methods from settings
        # 0 - Disabled
        # 1 - TMDb
        # 2 - IMDB
        # 3 - Filmweb
        
        methods =   ['Disabled', 'TMDb', 'IMDB', 'Filmweb']
        order =     ['firstLink', 'secondLink', 'thirdLink']
        
        for o in order:
            first = int(__addon__.getSetting(o))
            if first > 0:
                methodCall = getattr(self, methods[first])
                link = methodCall(id, type)
                if link is not None:
                    return link
        return None

    def TMDb(self, id, type):
        host_url = 'https://www.themoviedb.org/movie/'
    
        jsonGet = '{"jsonrpc": "2.0", "method": "VideoLibrary.Get' + type.title() + 'Details", "params": { "properties" : ["file", "imdbnumber", "runtime"], "' + type + 'id": ' + str(id) + '}, "id": "1"}'
        jsonGet = xbmc.executeJSONRPC(jsonGet)
        jsonGet = json.loads(unicode(jsonGet, 'utf-8', errors='ignore'))
        debug.debug('TMDb: ' + str(jsonGet))
        
        if 'result' in jsonGet and type + 'details' in jsonGet['result'] and 'imdbnumber' in jsonGet['result'][type + 'details'] and jsonGet['result'][type + 'details']['imdbnumber'][:2] == 'tt':
            imdbid = jsonGet['result'][type + 'details']['imdbnumber']
            tmdb = self.findTMDbID(imdbid)
            if tmdb is not False and 'movie_results' in tmdb and len(tmdb['movie_results']) == 1 and 'id' in tmdb['movie_results'][0]:
                tmdbid = tmdb['movie_results'][0]['id']
                lang = xbmc.getLanguage(xbmc.ISO_639_1)
                link = [host_url + str(tmdbid) + '/' + lang, jsonGet['result'][type + 'details']['runtime']]
            else:
                link = None
        else:
            link = None
        return link
        
    def IMDB(self, id, type):
        host_url = 'http://www.imdb.com/title/'
    
        jsonGet = '{"jsonrpc": "2.0", "method": "VideoLibrary.Get' + type.title() + 'Details", "params": { "properties" : ["file", "art", "trailer", "imdbnumber", "runtime"], "' + type + 'id": ' + str(id) + '}, "id": "1"}'
        jsonGet = xbmc.executeJSONRPC(jsonGet)
        jsonGet = json.loads(unicode(jsonGet, 'utf-8', errors='ignore'))
        debug.debug('IMDB: ' + str(jsonGet))
        
        if 'result' in jsonGet and type + 'details' in jsonGet['result'] and 'imdbnumber' in jsonGet['result'][type + 'details'] and jsonGet['result'][type + 'details']['imdbnumber'][:2] == 'tt':
            imdbid = jsonGet['result'][type + 'details']['imdbnumber']
            link = [host_url + imdbid + '/', jsonGet['result'][type + 'details']['runtime']]
        else:
            link = None
        return link

    def Filmweb(self, id, type):
        host_url = 'http://www.filmweb.pl/Film?id='
    
        patterns = [
            'fwcdn.pl/po/[^/]+/[^/]+/([0-9]+)/',
            'fwcdn.pl/ph/[^/]+/[^/]+/([0-9]+)/',
            '<trailer>http://mm.filmweb.pl/([0-9]+)/',
            'http://mm.filmweb.pl/([0-9]+)/',
            'http://www.filmweb.pl/Film?id=([0-9]+)'
        ]
        
        jsonGet = '{"jsonrpc": "2.0", "method": "VideoLibrary.Get' + type.title() + 'Details", "params": { "properties" : ["file", "art", "trailer", "runtime"], "' + type + 'id": ' + str(id) + '}, "id": "1"}'
        jsonGet = xbmc.executeJSONRPC(jsonGet)
        jsonGet = json.loads(unicode(jsonGet, 'utf-8', errors='ignore'))
        debug.debug('Filmweb: ' + str(jsonGet))
        
        for pat in patterns:
            result = re.search(pat, urllib.unquote(str(jsonGet)))
            if result is not None:
                return [host_url + result.group(1), jsonGet['result'][type + 'details']['runtime']]
        
        filePath, fileExt = os.path.splitext(jsonGet['result']['moviedetails']['file'])
        fileNfo = filePath + '.nfo'
        
        if xbmcvfs.exists(fileNfo):
        
            file = xbmcvfs.File(fileNfo, 'r')
            file_data = file.read()
            file.close()
            
            for pat in patterns:
                result = re.search(pat, urllib.unquote(str(file_data)))
                if result is not None:
                    return [host_url + result.group(1), jsonGet['result'][type + 'details']['runtime']]
                
        return None
    
    
    def findTMDbID(self, imdbid):
        API_KEY     = '1009b5cde25c7b0692d51a7db6e49cbd'
        API_URL     = 'https://api.themoviedb.org/3/'
        API_HOST    = 'api.themoviedb.org'
        
        import function
        
        ret = function.sendRequest(API_URL, 'find/' + imdbid, get={'api_key': API_KEY, 'external_source': 'imdb_id'})
        return ret
    
    