#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import xbmcgui
import xbmc
import xbmcvfs
import time
import urllib
import urllib2
import re
import sys 
import traceback
import json

class Player(xbmc.Player):
    def __init__(self, url, idFilme, pastaData, season, episode, nome, ano, logo, serieNome):
        xbmc.Player.__init__(self)
        self.url=url
        self.season=season
        self.episode=episode
        self.playing = True
        self.tempo = 0
        self.tempoTotal = 0
        self.idFilme = idFilme
        self.pastaData = xbmc.translatePath(pastaData)
        self.nome = nome
        self.ano = ano
        self.logo = logo
        self.serieNome = serieNome

        if not xbmcvfs.exists(os.path.join(pastaData,'tracker')):
            xbmcvfs.mkdirs(os.path.join(pastaData,'tracker'))


        if self.season != 0 and self.episode != 0:
            self.pastaVideo = os.path.join(self.pastaData,'tracker',str(self.idFilme)+'S'+str(self.season)+'x'+str(self.episode)+'.checkmovie')
            self.content = 'episode'
        else:
            self.pastaVideo = os.path.join(self.pastaData,'tracker',str(self.idFilme)+'.checkmovie')
            self.content = 'movie'

       

    def onPlayBackStarted(self):
        print '=======> player Start'
        self.tempoTotal = self.getTotalTime()
        print '==========> total time'+str(self.tempoTotal)

        

    def onPlayBackStopped(self):
        print 'player Stop'
        self.playing = False
        tempo = int(self.tempo)
        print 'self.time/self.totalTime='+str(self.tempo/self.tempoTotal)
        if (self.tempo/self.tempoTotal > 0.90):

            #self.adicionarVistoBiblioteca()
            #self.adicionarVistoSite()

            try:
                xbmcvfs.delete(self.pastaVideo)
            except:
                print "Não apagou"
                pass

    def adicionarVistoSite(self):
        return True
        


    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    def adicionarVistoBiblioteca(self):
        pastaVisto=os.path.join(self.pastaData,'vistos')
        
        try: 
            os.makedirs(pastaVisto)
        except: 
            pass

        if int(self.season) != 0 and int(self.episode) != 0:
            ficheiro = os.path.join(pastaVisto, str(self.idFilme)+'S'+str(self.season)+'x'+str(self.episode)+'.checkmovie')
        else:
            ficheiro = os.path.join(pastaVisto, str(self.idFilme)+'.checkmovie')

        if not os.path.exists(ficheiro):
            f = open(ficheiro, 'w')
            f.write('')
            f.close()

            try:

                if int(self.season) != 0 and int(self.episode) != 0:
                
                    #if xbmc.getCondVisibility('Library.HasContent(TVShows)'):
                    print "Check if tvshow episode exists in library when marking as watched\n\n"
                    titulo = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  self.nome)
                    dados = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["imdbnumber", "title", "year"]}, "id": 1}' % (self.season, self.episode))
                    dados = unicode(dados, 'utf-8', erros='ignore')
                    dados = json.loads(dados)
                    dados = dados['result']['episodes']
                    dados = [i for i in dados if titulo in i['file']][0]
                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(dados['episodeid']))
                    
                    """metaget = metahandlers.MetaData(preparezip=False)
                    metaget.get_meta('tvshow', self.serieNome, imdb_id=self.idFilme)
                    metaget.get_episode_meta(self.serieNome, self.idFilme, self.season, self.episode)
                    metaget.change_watched(self.content, '', self.idFilme, season=self.season, episode=self.episode, year='', watched=7)"""
                else:

                    #if xbmc.getCondVisibility('Library.HasContent(Movies)'):
                    print "Check if movie exists in library when marking as watched\n\n" 
                    titulo = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  self.nome)
                
                    dados = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber", "originaltitle", "year"]}, "id": 1}' % (self.ano, str(int(self.ano)+1), str(int(self.ano)-1)))
                    dados = unicode(dados, 'utf-8', errors='ignore')
                    dados = json.loads(dados)
                    print dados
                    dados = dados['result']['movies']
                    print dados
                    dados = [i for i in dados if self.idFilme in i['file']][0]
                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(dados['movieid']))

                    """metaget = metahandlers.MetaData(preparezip=False)
                    metaget.get_meta('movie', self.nome ,year=self.ano)
                    metaget.change_watched(self.content, '', self.idFilme, season='', episode='', year='', watched=7)"""
            except:
                pass

            xbmc.executebuiltin("XBMC.Notification(SemBilhete.tv,"+"Marcado como visto"+","+"6000"+","+ self.logo+")")
            xbmc.executebuiltin("XBMC.Container.Refresh")

        else:
            print "Já foi colocado antes"


