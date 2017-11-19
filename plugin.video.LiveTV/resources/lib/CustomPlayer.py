# -*- coding: utf-8 -*-
import xbmc


class MyXBMCPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        self.is_active = True
        self.urlplayed = False
        self.tempo = 0
        self.tempoTotal = 0
        self.pdialogue=None
        self.content = 'movie'
		
    def onPlayBackStarted( self ):
        try:
            print "#Im playing :: " 
        except:
            print "#I failed get what Im playing#"
        if (self.pdialogue):
            self.pdialogue.close()
        self.urlplayed = True
            
    def onPlayBackEnded( self ):
        self.onPlayBackStopped()
        
    def onPlayBackStopped( self ):
        self.playing = False
        self.is_active = False

