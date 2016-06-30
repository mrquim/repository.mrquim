#!/usr/bin/python
# -*- coding: utf-8 -*-


try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

import xbmcvfs, os, sys, xbmc

__DB_FILE__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.mrpiracy/').decode('utf8'), 'cache.db')

def isExists():
    if not xbmcvfs.exists(__DB_FILE__):
        createDB()
        return "DB criada com sucesso!"
    else:
        return "DB nao criada"


def createDB():

    if not xbmcvfs.exists(__DB_FILE__):
        """f = open(__DB_FILE__, 'w')
        f.write('')
        f.close()"""

        con, dbcursor = connect()

        dbcursor.execute("CREATE TABLE IF NOT EXISTS episodios (id integer PRIMARY KEY NOT NULL,nome text,plot text,categoria text,actores text,temporada text,episodio text,visto text DEFAULT('nao'),fanart text,poster text,imdb text,tvdb text,aired text,serienome text,traktid text);")
        dbcursor.execute("CREATE TABLE IF NOT EXISTS filmes (id integer PRIMARY KEY NOT NULL,imdb text,nome text,plot text,actores text,categoria text,visto text DEFAULT('nao'),fanart text,poster text,trailer text,ano text,traktid text,slug text);")
        dbcursor.execute("CREATE TABLE IF NOT EXISTS series (id integer PRIMARY KEY NOT NULL,nome text,plot text,imdb text,tvdb text,actores text,categoria text,visto text DEFAULT('nao'),fanart text,poster text,aired text,ano text,traktid text,slug text);")
        dbcursor.execute("CREATE TABLE IF NOT EXISTS temporadas (id integer PRIMARY KEY NOT NULL,imdb text,tvdb text,fanart text,temporada text,poster text);")
        con.commit()

def connect():
    conn = database.connect(__DB_FILE__)
    cursor = conn.cursor()

    return conn, cursor

def close(conn):
    conn.close()


def insertFilmeDB(nome, plot, imdb, poster, fanart, trailer, ano, traktid, slug, categoria=None, actores=None):
    if categoria == None:
        categoria = ''
    if actores == None:
        actores = ''
    con, dbcursor = connect()
    dbcursor.execute("INSERT INTO filmes(imdb, nome, plot, categoria, actores, fanart, poster, trailer, ano, traktid, slug) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (imdb, nome, plot, categoria, actores, fanart, poster, trailer, ano, traktid, slug))
    con.commit()

def selectFilmeDB(imdb):
    con, dbcursor = connect()
    dbcursor.execute("SELECT imdb, nome, plot, categoria, actores, fanart, poster, trailer, ano, visto, traktid, slug FROM filmes WHERE imdb=?", (imdb,))
    return dbcursor.fetchone()

def markwatchedFilmeDB(imdb, naoVisto=None):
    conn, dbcursor = connect()

    dbcursor.execute("SELECT visto FROM filmes WHERE imdb=?", (imdb,))
    visto = dbcursor.fetchone()

    if visto[0] == "nao":
        dbcursor.execute("UPDATE filmes SET visto=? WHERE imdb=?", ("sim", imdb))
        conn.commit()
        return True
    elif visto[0] == "sim":
        if naoVisto:
            dbcursor.execute("UPDATE filmes SET visto=? WHERE imdb=?", ("nao", imdb))
            conn.commit()
            return True
        return False

def isWatchedFilmeDB(imdb):
    conn, dbcursor = connect()
    dbcursor.execute("SELECT visto FROM filmes WHERE imdb=?", (imdb,))
    visto = dbcursor.fetchone()

    if visto[0] == "nao":
        return False
    elif visto[0] == "sim":
        return True

def insertSerie(nome, plot, imdb, tvdb, poster, fanart, aired, ano, traktid, slug, categoria=None, actores=None):
    if categoria == None:
        categoria = ''
    if actores == None:
        actores = ''

    con, dbcursor = connect()
    dbcursor.execute("INSERT INTO series(nome, plot, imdb, tvdb, actores, categoria, fanart, poster, aired, ano, traktid, slug) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome, plot, imdb, tvdb, actores, categoria, fanart, poster, aired, ano, traktid, slug))
    con.commit()

def selectSerieDB(imdb):
    con, dbcursor = connect()
    dbcursor.execute("SELECT nome, plot, imdb, tvdb, actores, categoria, fanart, poster, aired, ano, traktid, slug FROM series WHERE imdb=?", (imdb,))
    return dbcursor.fetchone()

def getTVDBSerie(imdb):
    con, dbcursor = connect()
    dbcursor.execute("SELECT tvdb FROM series WHERE imdb=?", (imdb,))
    return dbcursor.fetchone()

def insertEpisodio(nome, plot, imdb, tvdb, temporada, episodio, fanart, poster, aired, serienome, traktid, categoria=None, actores=None):
    if categoria == None:
        categoria = ''
    if actores == None:
        actores = ''

    con, dbcursor = connect()
    dbcursor.execute("INSERT INTO episodios(nome, plot, temporada, episodio, fanart, poster, imdb, tvdb, aired, actores, categoria, serienome, traktid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome, plot, temporada, episodio, fanart, poster, imdb, tvdb, aired, actores, categoria, serienome, traktid))
    con.commit()

def selectEpisodioDB(imdb, temporada, episodio):
    con, dbcursor = connect()
    dbcursor.execute("SELECT nome, plot, temporada, episodio, fanart, poster, aired, actores, categoria, visto, imdb, serienome, traktid FROM episodios WHERE imdb=? AND temporada=? AND episodio=?", (imdb, temporada, episodio))
    return dbcursor.fetchone()

def selectTVDBEpisodioDB(imdb, temporada, episodio):
    conn, dbcursor = connect()
    dbcursor.execute("SELECT tvdb FROM episodios WHERE imdb=? AND temporada=? AND episodio=?", (imdb, temporada, episodio))
    return dbcursor.fetchone()

def markwatchedEpisodioDB(imdb, temporada, episodio, naoVisto=None):
    conn, dbcursor = connect()

    dbcursor.execute("SELECT visto FROM episodios WHERE imdb=? AND temporada=? AND episodio=?", (imdb, temporada, episodio))
    visto = dbcursor.fetchone()

    if visto[0] == "nao":
        dbcursor.execute("UPDATE episodios SET visto=? WHERE imdb=? AND temporada=? AND episodio=?", ("sim", imdb, temporada, episodio))
        conn.commit()
        return True
    elif visto[0] == "sim":
        if naoVisto:
            dbcursor.execute("UPDATE episodios SET visto=? WHERE imdb=? AND temporada=? AND episodio=?", ("nao", imdb, temporada, episodio))
            conn.commit()
            return True
        return False

def isWatchedSerieDB(imdb, temporada, episodio):
    conn, dbcursor = connect()
    dbcursor.execute("SELECT visto FROM episodios WHERE imdb=? AND temporada=? AND episodio=?", (imdb, temporada, episodio))
    visto = dbcursor.fetchone()

    if visto[0] == "nao":
        return False
    elif visto[0] == "sim":
        return True

def updateEpisodioDB(nome, plot, imdb, tvdb, temporada, episodio, fanart, poster, aired, serienome, traktid, categoria=None, actores=None):
    conn, dbcursor = connect()
    if categoria == None:
        categoria = ''
    if actores == None:
        actores = ''
    dbcursor.execute("DELETE FROM episodios WHERE imdb=? AND temporada=? AND episodio is NULL", (imdb, temporada))
    #dbcursor.execute("UPDATE episodios SET nome=?, plot=?, tvdb=?, episodio=?, fanart=?, poster=?, aired=?, serienome=?, traktid=?, categoria=?, actores=? WHERE imdb=? AND temporada=?", (nome, plot, tvdb, episodio, fanart, poster, aired, serienome, traktid, categoria, actores, imdb, temporada)")
    conn.commit()

    insertEpisodio(nome, plot, imdb, tvdb, temporada, episodio, fanart, poster, aired, serienome, traktid, categoria, actores)
