#!/usr/bin/python
# coding=utf-8

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



import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,threading,xbmcvfs,cookielib,pprint,datetime,thread,time
from bs4 import BeautifulSoup
from resources.lib import Downloader #Enen92 class
from resources.lib import Player
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
from t0mm0.common.net import HttpResponse
from resources.lib import URLResolverMedia
from resources.lib import Trakt
from resources.lib import Database
from unicodedata import normalize


__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo("id")
__ADDON__   = xbmcaddon.Addon(__ADDON_ID__)
__ADDON_FOLDER__    = __ADDON__.getAddonInfo('path')
__SETTING__ = xbmcaddon.Addon().getSetting
__ART_FOLDER__  = os.path.join(__ADDON_FOLDER__,'resources','img')
__FANART__      = os.path.join(__ADDON_FOLDER__,'fanart.jpg')


__PASTA_DADOS__ = Addon(__ADDON_ID__).get_profile().decode("utf-8")
__PASTA_FILMES__ = xbmc.translatePath(__ADDON__.getSetting('bibliotecaFilmes'))
__PASTA_SERIES__ = xbmc.translatePath(__ADDON__.getSetting('bibliotecaSeries'))

__SKIN__ = 'v1'
__SITE__ = 'http://mrpiracy.top/'

__ALERTA__ = xbmcgui.Dialog().ok

__COOKIE_FILE__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.mrpiracy/').decode('utf8'), 'cookie.mrpiracy')
__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'} #ISO-8859-1,


def menu():

    check_login = login()
    database = Database.isExists()

    if check_login:
        addDir('Filmes', __SITE__+'kodi_filmes.php', 1, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'filmes.png'))
        addDir('Series', __SITE__+'kodi_series.php', 1, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'series.png'))
        addDir('Animes', __SITE__+'kodi_animes.php', 1, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'animes.png'))
        addDir('Pesquisa', __SITE__, 6, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'procurar.png'))
        addDir('', '', '', __FANART__, 0, poster=os.path.join(__ART_FOLDER__,'nada.png'))
        addDir('Filmes por Ano', __SITE__+'kodi_filmes.php', 9, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'))
        addDir('Filmes por Genero', __SITE__+'kodi_filmes.php', 8, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'generos.png'))
        addDir('Series por Ano', __SITE__+'kodi_series.php', 9, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'))
        addDir('Series por Genero', __SITE__+'kodi_series.php', 8, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'generos.png'))

        if Trakt.loggedIn():
            dp = xbmcgui.DialogProgress()
            dp.create('MrPiracy.top Trakt')
            dp.update(0, "A Carregar os Filmes vistos no Trakt")
            filmesTraktVistos()
            dp.update(50, "A Carregar as Series vistas no Trakt")
            seriesTraktVistos()

            dp.close()

            addDir('Trakt', __SITE__, 701, __FANART__, 0, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'trakt.png'))

        addDir('A Minha Conta '+getNumNotificacoes(), 'url', 10, __FANART__, 0, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'definicoes.png'))
        addDir('Definições', 'url', 1000, __FANART__, 0, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'definicoes.png'))

        vista_menu()
    else:
        addDir('Alterar Definições', 'url', 1000, __FANART__, 0, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'definicoes.png'))
        addDir('Entrar novamente', 'url', None, __FANART__, 0, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'retroceder.png'))
        vista_menu()


def minhaConta():
    addDir('Favoritos', __SITE__+'favoritos.php', 11, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'favoritos.png'))
    addDir('Agendados', __SITE__+'agendados.php', 11, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'agendados.png'))
    addDir('Últimos Filmes Vistos', __SITE__+'vistos.php', 11, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'ultimos.png'))
    addDir('Notificações', __SITE__+'notificacao.php', 14, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'notificacoes.png'))

    vista_menu()

def loginTrakt():
    Trakt.traktAuth()

def menuTrakt():
    addDir('Progresso', __SITE__, 702, __FANART__, 0, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'trakt.png'))
    addDir('Watchlist Filmes', 'https://api-v2launch.trakt.tv/sync/watchlist/movies', 703, __FANART__, 0, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'trakt.png'))
    addDir('Watchlist Series', 'https://api-v2launch.trakt.tv/sync/watchlist/shows', 703, __FANART__, 0, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'trakt.png'))
    vista_menu()

def removerAcentos(txt, encoding='utf-8'):
    return normalize('NFKD', txt.decode(encoding)).encode('ASCII','ignore')

def login():
    ap()
    if __ADDON__.getSetting("email") == '' or __ADDON__.getSetting('password') == '':
        __ALERTA__('MrPiracy.top', 'Precisa de definir o seu email e password')
        return False
    else:
        try:

            net = Net()

            dados = {'email': __ADDON__.getSetting("email"), 'password': __ADDON__.getSetting("password"), 'lembrar_senha': 'lembrar'}

            codigo_fonte = net.http_POST(__SITE__+'login_bd.php',form_data=dados,headers=__HEADERS__).content.encode('utf-8')

            match = re.compile('class="myAccount">(.+?)<\/a>').findall(codigo_fonte)

        except:
            resultado = False
            __ALERTA__('MrPiracy.top', 'Não foi possível abrir a página. Por favor tente novamente')
            match = ''
            return resultado

        if match == []:
            match = re.compile('class="myAccount">(.+?)<\/a>').findall(codigo_fonte)

            if match == []:
                resultado = False
                __ALERTA__('MrPiracy.top', 'Email e/ou Password incorretos')
                return resultado
            else:
                resultado = True
                xbmc.executebuiltin("XBMC.Notification(MrPiracy.top, Sessão iniciada: "+__ADDON__.getSetting("email") +", '10000', "+__ADDON_FOLDER__+"/icon.png)")
                return resultado
        else:
            net.save_cookies(__COOKIE_FILE__)
            resultado = True
            xbmc.executebuiltin("XBMC.Notification(MrPiracy.top, Sessão iniciada: "+__ADDON__.getSetting("email") +", '10000', "+__ADDON_FOLDER__+"/icon.png)")
            return resultado

def getList(url, pagina):
    ap()
    tipo = ''
    categoria = ''

    net = Net()
    net.set_cookies(__COOKIE_FILE__)
    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content.encode('utf8')

    if 'kodi_filmes.php' in url:
        tipo = 'kodi_filmes'
    elif 'kodi_series.php' in url:
        tipo = 'kodi_series'
    elif 'kodi_animes.php' in url:
        tipo = 'kodi_animes'

    anoLink = ''
    if 'ano' in url:
        try:
            anoLink = re.compile('ano(.+?)&').findall(url)[0]
        except:
            anoLink = re.compile('&ano(.+?)').findall(url)[0]
        anoLink = '&ano'+anoLink

    if 'categoria=' in url:
        categoria = re.compile('categoria=(.+[0-9])').findall(url)[0]

    #print codigo_fonte

    if tipo == 'kodi_filmes':
        match = re.compile('<div\s+class="movie-info">\s+<a\s+href="(.+?)"\s+class="movie-name">.+?<\/a>\s+<d.+?><\/div>\s+<d.+?>\s+<d.+?>\s+<span\s+class="genre">(.+?)<\/span>').findall(codigo_fonte)
        #match = re.compile('<img src="(.+?)" alt=".+?">\s+<\/a>\s+<\/div>\s+<\/div>\s+<div class="movie-info">\s+<a href="(.+?)" class="movie-name">.+?<\/a>\s+<div class="clear"><\/div>\s+<div class="movie-detailed-info">\s+<div class="detailed-aux" style="height\: inherit\;line-height\: 20px\;">\s+<span class="genre">(.+?)<\/span>\s+<span class="year">\s+<span>\(<\/span>(.+?)<span>\)<\/span><\/span>\s+<span class="original-name">\s+-\s+"(.+?)"<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Realizador:\s+<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Elenco:<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>\s+<\/div>\s+').findall(codigo_fonte)

    elif tipo == 'kodi_series':
        #match = re.compile('<img src="(.+?)" alt=".+?">\s+<div class="thumb-effect" title=".+?"><\/div>\s+<\/a>\s+<\/div>\s+<\/div>\s+<div class="movie-info">\s+<a href="(.+?)" class="movie-name">.+?<\/a>\s+<div class="clear"><\/div>\s+<div class="movie-detailed-info">\s+<div class="detailed-aux" style="height\: 20px\; line-height\: 20px\;">\s+<span class="genre">(.+?)<\/span>\s+<span class="year">\s+<span>\(<\/span>(.+?)<span>\)<\/span><\/span>\s+<span class="original-name">\s+-\s+"(.+?)"<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Criador:\s+<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Elenco:<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>\s+<\/div>\s+').findall(codigo_fonte)
        match = re.compile('<div\s+class="movie-info">\s+<a\s+href="(.+?)"\s+class="movie-name">.+?<\/a>\s+<d.+?><\/div>\s+<d.+?>\s+<d.+?>\s+<span\s+class="genre">(.+?)<\/span>').findall(codigo_fonte)
    elif tipo == 'kodi_animes':
        #match = re.compile('<img src="(.+?)" alt=".+?">\s+<div class="thumb-effect" title=".+?"><\/div>\s+<\/a>\s+<\/div>\s+<\/div>\s+<div class="movie-info">\s+<a href="(.+?)" class="movie-name">.+?<\/a>\s+<div class="clear"><\/div>\s+<div class="movie-detailed-info">\s+<div class="detailed-aux" style="height\: 20px\; line-height\: 20px\;">\s+<span class="genre">(.+?)<\/span>\s+<span class="year">\s+<span>\(<\/span>(.+?)<span>\)<\/span><\/span>\s+<span class="original-name">\s+-\s+"(.+?)"<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Criador:\s+<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Elenco:<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>\s+<\/div>\s+').findall(codigo_fonte)
        match = re.compile('<div\s+class="movie-info">\s+<a\s+href="(.+?)"\s+class="movie-name">.+?<\/a>\s+<d.+?><\/div>\s+<d.+?>\s+<d.+?>\s+<span\s+class="genre">(.+?)<\/span>').findall(codigo_fonte)

    if tipo == 'kodi_filmes':

        for link, cat in match:
            idIMDB = re.compile('imdb=(.+)').findall(link)[0]
            if not idIMDB.startswith('tt'):
                continue

            idIMDB = re.compile('imdb=(tt[0-9]{7})').findall(link)[0]

            dados = Database.selectFilmeDB(idIMDB)
            if dados is None:
                try:
                    infoFilme = json.loads(Trakt.getFilme(idIMDB, cat.decode('utf8')))
                except ValueError:
                    continue
                poster = infoFilme["poster"]
                fanart = infoFilme["fanart"]
                nomeOriginal = infoFilme["nome"]
                ano = infoFilme["ano"]
                infoLabels = {'Title': infoFilme["nome"], 'Year': infoFilme["ano"], 'Genre': cat.decode('utf8'), 'Plot': infoFilme["plot"], 'Code': idIMDB}
            else:
                infoLabels = {'Title': dados[1], 'Year': dados[8], 'Genre': dados[3], 'Plot': dados[2], 'Code': dados[0] }
                poster = dados[6]
                fanart = dados[5]
                nomeOriginal = dados[1]
                ano = dados[8]

            try:
                nomeOriginal = unicode(nomeOriginal, 'utf-8')
            except:
                nomeOriginal = nomeOriginal

            addVideo(nomeOriginal+' ('+ano+')', __SITE__+"kodi_"+link, 3, fanart, 'filme', 0, 0, infoLabels, poster)
    else:

        for link, cat in match:
            idIMDB = re.compile('imdb=(.+)').findall(link)[0]
            if not idIMDB.startswith('tt'):
                continue

            idIMDB = re.compile('imdb=(tt[0-9]{7})').findall(link)[0]
            print idIMDB
            dados = Database.selectSerieDB(idIMDB)
            if dados is None:
                try:
                    infoSerie = json.loads(Trakt.getSerie(idIMDB, cat.decode('utf8')))
                except:
                    infoSerie = ''
                    continue
                poster = infoSerie["poster"]
                fanart = infoSerie["fanart"]
                nomeOriginal = infoSerie["nome"]
                ano = infoSerie["ano"]

                infoLabels = {"Title": infoSerie["nome"], 'Aired':infoSerie['aired'], 'Plot':infoSerie['plot'], 'Year':infoSerie['ano'], 'Genre':infoSerie['categoria'], 'Code': infoSerie["imdb"]}
            else:
                infoLabels = {"Title": dados[0], 'Aired':dados[8], 'Plot':dados[1], 'Genre':dados[5], 'Code':dados[2], 'Year': dados[9]}
                poster = dados[7]
                fanart = dados[6]
                nomeOriginal = dados[0]
                ano = dados[9]

            try:
                nomeOriginal = unicode(nomeOriginal, 'utf-8')
            except:
                nomeOriginal = nomeOriginal

            addDir(nomeOriginal, __SITE__+"kodi_"+link, 4, fanart, pagina, 'serie', infoLabels, poster)

    """else:
        for imagem, link, genero, ano, nomeOriginal, realizador, elenco in match:
            #try:
            infoLabels = {'Title':nomeOriginal.decode('utf8'), 'Aired':ano, 'Plot': ''}
            addDir(nomeOriginal+ ' ('+ano+')', __SITE__+"kodi_"+link, 4, imagem, pagina, 'serie', infoLabels, imagem)
    #        except:
    #            pass"""

    if categoria == '':
        addDir('Proximo', __SITE__+tipo+'.php?pagina='+str(int(pagina)+1)+''+anoLink, 1, __FANART__, int(pagina)+1, poster= os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'))
    else:
        addDir('Proximo', __SITE__+tipo+'.php?pagina='+str(int(pagina)+1)+'&categoria='+categoria+''+anoLink, 1, __FANART__, int(pagina)+1, poster= os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'))

    vista_filmesSeries()


def getSeasons(url):
    ap()
    net = Net()
    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

    match = re.compile('<div\s+class="season"><a\s+href="(.+?)">(.+?)<\/a><\/div>').findall(codigo_fonte)
    match += re.compile('<div\s+class="season"><a\s+href="(.+?)" >(.+?)<\/a><\/div>').findall(codigo_fonte)


    for link, temporada in match:

        if '" class="slctd' in link:
            link = re.compile('(.+?)" class="slctd').findall(link)[0]

        addDirSeason("[B]Temporada[/B] "+temporada, __SITE__+"kodi_"+link, 5, os.path.join(__ART_FOLDER__, __SKIN__, 'temporadas', 'temporada'+temporada+'.png'), 1, temporada)

    vista_temporadas()

def getEpisodes(url):
    ap()
    net = Net()
    net.set_cookies(__COOKIE_FILE__)
    """if "kodi_anime" in url:
        try:
            codigo_fonte = net.http_GET(url, headers=__HEADERS__).content.encode('utf8')
        except:
            codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

        match = re.compile('<div id="(.+?)" class="item">\s+<div class="thumb(.+?)?">\s+<a name=\'.+?\' href="(.+?)">\s+<img style="(.+?)" src="(.+?)" onError="this\.onerror=null;this\.src=\'(.+?)\';"\s+alt="(.+?)?">\s+<div class="thumb-shadow" alt="(.+?)?"><\/div>\s+<div class="thumb-effect" alt="(.+?)?"><\/div>\s+<div class="episode-number">(.+?)<\/div>').findall(codigo_fonte)

        temporadaNumero = re.compile('<div\s+class="season"><a\s+href="(.+?)"\s+class="slctd">(.+?)<\/a>').findall(codigo_fonte)[0][1]
        #actors = re.compile('<span class="director-caption">Elenco:<\/span>\s+<span class="director">(.+?)<\/span>').findall(codigo_fonte)[0]
        try:
            plot = re.compile(u'Descrição:<\/span>(.+\s.+)<\/span>\s+<\/div>').findall(codigo_fonte)[0]
        except:
            plot = "-"

        #criador = re.compile('<span class="director-caption">Criador: <\/span>\s+<span class="director">\s+(.+?)<\/span>').findall(codigo_fonte)[0]
        serieTitulo = re.compile('<span class="original-name">- "(.+?)"<\/span>').findall(codigo_fonte)[0]

        for lixo, lixo1, link, lixo2, imagem, imagemExterna, nome, nome1, nome2, episodioNumero in match:
            imdb = re.compile('imdb=(.+?)&').findall(link)[0]
            #infoLabels = {'Title':nome.decode('utf8'), 'Actors':actors.decode('utf8'), 'Plot':plot.decode('utf8'), 'Season':temporadaNumero, 'Episode':episodioNumero, 'Writer': criador.decode('utf8'), "Code":imdb }
            try:
                infoLabels = {'Title': nome, 'Season':temporadaNumero, 'Episode': episodioNumero, "Code": imdb}
            except:
                infoLabels = {'Title':nome.decode('utf8'), 'Actors':actors.decode('utf8'), 'Plot':plot.decode('utf8'), 'Season':temporadaNumero, 'Episode':episodioNumero, 'Writer': criador.decode('utf8'), "Code":imdb }
            if 'e' in episodioNumero:
                episodioNumeroReal = re.compile('(.+)e').findall(episodioNumero)[0]
            else:
                episodioNumeroReal = episodioNumero

            if '/' in episodioNumeroReal:
                episodioNumeroReal = episodioNumeroReal.split('/')[0]

            try:
                addVideo('[B]Episodio '+episodioNumero+'[/B] | '+nome, __SITE__+"kodi_"+link, 3, __SITE__+imagem, 'episodio', temporadaNumero, episodioNumeroReal, infoLabels, imagemExterna, serieTitulo)
            except:
                addVideo('[B]Episodio '+episodioNumero+'[/B] | '+nome.decode('utf8'), __SITE__+"kodi_"+link, 3, __SITE__+imagem, 'episodio', temporadaNumero, episodioNumeroReal, infoLabels, imagemExterna, serieTitulo)
    else:"""

    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

    match = re.compile('<div id=".+?" class="item">\s+<div.+>\s+<a.+href="(.+?)">\s+').findall(codigo_fonte)

    temporadaNumero = re.compile('<div\s+class="season"><a\s+href="(.+?)"\s+class="slctd">(.+?)<\/a>').findall(codigo_fonte)[0][1]

    for link in match:
        imdbid = re.compile('imdb=(.+?)&').findall(link)[0]

        imdbid = re.compile('imdb=(tt[0-9]{7})').findall(link)[0]

        episodioN = re.compile('e=(.+?)&').findall(link)[0]

        if 'e' in episodioN:
            episodioN = re.compile('(.+)e').findall(episodioN)[0]

        if '/' in episodioN:
            episodioN = episodioN.split('/')[0]

        episodioInfo = Database.selectEpisodioDB(imdbid, temporadaNumero, episodioN)
        if episodioInfo is None:
            infoEpis = json.loads(Trakt.getTVDBByEpSe(imdbid, temporadaNumero, episodioN))
            Database.insertEpisodio(infoEpis["name"], infoEpis["plot"], infoEpis["imdb"], infoEpis["tvdb"], infoEpis["season"], infoEpis["episode"], infoEpis["fanart"], infoEpis["poster"], infoEpis["aired"], infoEpis["serie"], infoEpis["traktid"], actores=infoEpis['actors'])
            infoLabels = {'Title':infoEpis["name"], 'Actors':infoEpis['actors'], 'Plot':infoEpis["plot"], 'Season':infoEpis["season"], 'Episode':infoEpis["episode"], "Code":imdbid, 'Aired': infoEpis["aired"] }
            poster = infoEpis["poster"]
            fanart = infoEpis["fanart"]
            nomeEpisodio = infoEpis["name"]
            temporadaEpisodioDB = infoEpis["season"]
            numeroEpisodioDB = infoEpis["episode"]
            serieTitulo = infoEpis["serie"]
        else:
            """if int(episodioInfo[3]) is not int(episodioN):
                infoEpis = json.loads(Trakt.getTVDBByEpSe(imdbid, temporadaNumero, episodioN))
                Database.updateEpisodioDB(infoEpis["name"], infoEpis["plot"], infoEpis["imdb"], infoEpis["tvdb"], infoEpis["season"], infoEpis["episode"], infoEpis["fanart"], infoEpis["poster"], infoEpis["aired"], infoEpis["serie"], infoEpis["traktid"], actores=infoEpis['actors'])
                infoLabels = {'Title':infoEpis["name"], 'Actors':infoEpis['actors'], 'Plot':infoEpis["plot"], 'Season':infoEpis["season"], 'Episode':infoEpis["episode"], "Code":imdbid, 'Aired': infoEpis["aired"] }
                poster = infoEpis["poster"]
                fanart = infoEpis["fanart"]
                nomeEpisodio = infoEpis["name"]
                temporadaEpisodioDB = infoEpis["season"]
                numeroEpisodioDB = infoEpis["episode"]
                serieTitulo = infoEpis["serie"]
            else:"""
            infoLabels = {'Title':episodioInfo[0], 'Actors':episodioInfo[7], 'Plot':episodioInfo[1], 'Season':episodioInfo[2], 'Episode':episodioInfo[3], "Code":imdbid, 'Aired': episodioInfo[6] }
            poster = episodioInfo[5]
            fanart = episodioInfo[4]
            nomeEpisodio = episodioInfo[0]
            temporadaEpisodioDB = episodioInfo[2]
            numeroEpisodioDB = episodioInfo[3]
            serieTitulo = episodioInfo[11]

        addVideo('[B]Episodio '+episodioN+'[/B] | '+nomeEpisodio, __SITE__+"kodi_"+link, 3, fanart, 'episodio', temporadaEpisodioDB, numeroEpisodioDB, infoLabels, poster, serieTitulo)

    vista_episodios()

def getStreamLegenda(siteBase, codigo_fonte):
    ap()
    stream = ''
    legenda = ''

    net = Net()

    ext_g = ''

    servidor = ''
    titulos = []
    links = []
    legendas = []
    stuff = []
    i = 1
    legendaAux = ''
    if siteBase == 'serie.php':
        match = re.compile('<div\s+id="welele"\s+link="(.+?)"\s+legenda="(.+?)">').findall(codigo_fonte)
        match += re.compile('<div\s+id="welele2"\s+link="(.+?)"\s+legenda="(.+?)">').findall(codigo_fonte)

        for link, legenda in match:
            titulos.append('Servidor #%s' % i)
            links.append(link)
            if not '.srt' in legenda:
                legend = legenda+'.srt'
            legendas.append('http://mrpiracy.top/subs/%s' % legenda)
            i = i+1

    else:
        match = re.compile('<div\s+id="(.+?)"\s+link="(.+?)">').findall(codigo_fonte)
        for idS, link in match:
            if 'legenda' in idS:
                if not '.srt' in link:
                    link = link+'.srt'
                legendaAux = 'http://mrpiracy.top/subs/%s' % link
                continue
            if 'videomega' in idS and 'videomega' in link:
                continue

            titulos.append('Servidor #%s' % i)
            links.append(link)
            i = i+1

    if len(titulos) > 1:
        servidor = xbmcgui.Dialog().select('Escolha o servidor', titulos)

        if 'vidzi' in links[servidor]:
            vidzi = URLResolverMedia.Vidzi(links[servidor])
            stream = vidzi.getMediaUrl()
            legenda = vidzi.getSubtitle()
        elif 'uptostream.com' in links[servidor]:
            stream = URLResolverMedia.UpToStream(links[servidor]).getMediaUrl()
            if legendaAux != '':
                legenda = legendaAux
            else:
                legenda = legendas[0]
        elif 'server.mrpiracy.top' in links[servidor]:
            stream = links[servidor]
            if legendaAux != '':
                legenda = legendaAux
            else:
                legenda = legendas[0]
        elif 'openload' in links[servidor]:
            stream = URLResolverMedia.OpenLoad(links[servidor]).getMediaUrl()
            legenda = URLResolverMedia.OpenLoad(links[servidor]).getSubtitle()
        elif 'drive.google.com/' in links[servidor]:
            stream, ext_g = URLResolverMedia.GoogleVideo(links[servidor]).getMediaUrl()
            if legendaAux != '':
                legenda = legendaAux
            else:
                legenda = legendas[0]

    else:

        if 'server.mrpiracy.top' in links[0]:
            stream = links[0]
            if legendaAux != '':
                legenda = legendaAux
            else:
                legenda = legendas[0]
        elif 'uptostream.com' in links[0]:
            stream = URLResolverMedia.UpToStream(links[0]).getMediaUrl()
            if legendaAux != '':
                legenda = legendaAux
            else:
                legenda = legendas[0]
        elif 'drive.google.com/' in links[0]:
            stream, ext_g = URLResolverMedia.GoogleVideo(links[0]).getMediaUrl()
            if legendaAux != '':
                legenda = legendaAux
            else:
                legenda = legendas[0]
        elif 'openload' in links[0]:
            stream = URLResolverMedia.OpenLoad(links[0]).getMediaUrl()
            legenda = URLResolverMedia.OpenLoad(links[0]).getSubtitle()


    """if match != []:

        servidores = re.compile('document\.getElementById\(\"banner-box box-header servidores\"\)\.innerHTML = \'(.+?)\'\;').findall(codigo_fonte)

        #pprint.pprint(servidores)



        #if len(match) == 1:
        servidor = dialog.select(u'Escolha o servidor', ['OpenLoad', 'VidZi', 'Antigo OpenLoad'])
        elif len(match) == 2:
            servidor = dialog.select(u'Escolha o servidor', ['Servidor #1', 'Servidor #2', 'Servidor #3'])
        elif len(match) == 3:
            servidor = dialog.select(u'Escolha o servidor', ['Servidor #1', 'Servidor #2', 'Servidor #3'])
        elif len(match) == 4:
            servidor = dialog.select(u'Escolha o servidor', ['Servidor #1', 'Servidor #2', 'Servidor #3', 'Servidor #4', 'Servidor #5'])

        if servidor == 0:
            linkOpenload = re.compile('<iframe id="reprodutor" src="(.+?)" scrolling="no"').findall(codigo_fonte)[0]
            stream = URLResolverMedia.OpenLoad(linkOpenload).getMediaUrl()
            legenda = legendas[0]
            legenda = URLResolverMedia.OpenLoad(linkOpenload).getSubtitle()

        elif servidor == 3:
            linkVideoMega = re.compile('<iframe id="reprodutor" src="(.+?)" scrolling="no"').findall(servidores[1])[0]
            stream = URLResolverMedia.VideoMega(linkVideoMega).getMediaUrl()
            linkOpenload = re.compile('<iframe id="reprodutor" src="(.+?)" scrolling="no"').findall(codigo_fonte)[0]
            legenda = URLResolverMedia.OpenLoad(linkOpenload).getSubtitle()

        elif servidor == 1:
            linkVidzi = re.compile('<iframe id="reprodutor" src="(.+?)" scrolling="no"').findall(servidores[2])[0]
            vidzi = URLResolverMedia.Vidzi(linkVidzi)
            stream = vidzi.getMediaUrl()
            #legenda = vidzi.getSubtitle()
            linkOpenload = re.compile('<iframe id="reprodutor" src="(.+?)" scrolling="no"').findall(codigo_fonte)[0]
            legenda = URLResolverMedia.OpenLoad(linkOpenload).getSubtitle()

        elif servidor == 2:
            linkOpenload = re.compile('<iframe id="reprodutor" src="(.+?)" scrolling="no"').findall(codigo_fonte)[0]
            stream = URLResolverMedia.OpenLoad(linkOpenload).getMediaUrlOld()
            legenda = URLResolverMedia.OpenLoad(linkOpenload).getSubtitle()

    else:

        if 'serie' in siteBase:
            linkOpenload = re.compile('<iframe src="(.+?)" scrolling="no"').findall(codigo_fonte)[0]
        else:
            linkOpenload = re.compile('<iframe id="reprodutor" src="(.+?)" scrolling="no"').findall(codigo_fonte)[0]

        servidor = dialog.select(u'Escolha o servidor', ['OpenLoad', 'Antigo OpenLoad'])

        if servidor == 0:
            stream = URLResolverMedia.OpenLoad(linkOpenload).getMediaUrl()
            legenda = URLResolverMedia.OpenLoad(linkOpenload).getSubtitle()
        elif servidor == 1:
            stream = URLResolverMedia.OpenLoad(linkOpenload).getMediaUrlOld()
            legenda = URLResolverMedia.OpenLoad(linkOpenload).getSubtitle()

    """

    return stream, legenda

def pesquisa():
    ap()
    net = Net()
    net.set_cookies(__COOKIE_FILE__)

    dialog = xbmcgui.Dialog()
    server = dialog.select(u'Onde quer pesquisar?', ['Filmes', 'Series', 'Animes'])

    if server == 0:
        site = __SITE__+'kodi_procurarf.php'
    elif server == 1:
        site = __SITE__+'kodi_procurars.php'
    elif server == 2:
        site = __SITE__+'kodi_procuraranime.php'

    teclado = xbmc.Keyboard('', 'O que quer pesquisar?')
    teclado.doModal()

    if teclado.isConfirmed():
        strPesquisa = teclado.getText()
        dados = {'searchBox': strPesquisa}
        codigo_fonte = net.http_POST(site, form_data=dados, headers=__HEADERS__).content.encode('utf8')

        """if server == 2:
            match = re.compile('<img src="(.+?)" alt="(.+?)">\s+<div class="thumb-effect" title="(.+?)"><\/div>\s+<\/a>\s+<\/div>\s+<\/div>\s+<div class="movie-info" style="width\: 80\%\;">\s+<a href="(.+?)" class="movie-name">(.+?)<\/a>\s+<div class="clear"><\/div>\s+<div class="movie-detailed-info">\s+<div class="detailed-aux" style="height\: 20px\; line-height\: 20px\;">\s+<span class="genre">(.+?)<\/span>\s+<span class="year">\s+<span>\(<\/span>(.+?)<span>\)<\/span><\/span>\s+<span class="original-name">\s+-\s+"(.+?)"<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Escritor:\s+<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Elenco:<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>').findall(codigo_fonte)
        elif server == 1 or server == 0:"""
            #match = re.compile('<img src="(.+?)" alt="(.+?)">\s+<div class="thumb-effect" title="(.+?)"><\/div>\s+<\/a>\s+<\/div>\s+<\/div>\s+<div class="movie-info" style="width\: 80\%\;">\s+<a href="(.+?)" class="movie-name">(.+?)<\/a>\s+<div class="clear"><\/div>\s+<div class="movie-detailed-info" style="width\: initial\;">\s+<div class="detailed-aux" style="height\: 20px\; line-height\: 20px\;">\s+<span class="genre">(.+?)<\/span>\s+<span class="year">\s+<span>\(<\/span>(.+?)<span>\)<\/span><\/span>\s+<span class="original-name">\s+-\s+"(.+?)"<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Realizador:\s+<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>\s+<div class="detailed-aux">\s+<span class="director-caption">Elenco:<\/span>\s+<span class="director">(.+?)<\/span>\s+<\/div>').findall(codigo_fonte)
        match = re.compile('<div\s+class="movie-info".+>\s+<a\s+href="(.+?)".+class="movie-name">.+?<\/a>\s+<d.+\s+<d.+\s+<d.+\s+<span\s+class="genre">(.+?)<\/span>').findall(codigo_fonte)

        if match != []:
            #if server == 0 or server == 1:
            for link, cat in match:
                if server == 0:
                    idIMDB = re.compile('imdb=(.+)').findall(link)[0]
                    if not idIMDB.startswith('tt'):
                        continue

                    idIMDB = re.compile('imdb=(tt[0-9]{7})').findall(link)[0]
                    dados = Database.selectFilmeDB(idIMDB)
                    if dados is None:
                        infoFilme = json.loads(Trakt.getFilme(idIMDB, cat.decode('utf8')))
                        poster = infoFilme["poster"]
                        fanart = infoFilme["fanart"]
                        nomeOriginal = infoFilme["nome"]
                        ano = infoFilme["ano"]
                        infoLabels = {'Title': infoFilme["nome"], 'Year': infoFilme["ano"], 'Genre': cat.decode('utf8'), 'Plot': infoFilme["plot"], 'Code': idIMDB}
                    else:
                        infoLabels = {'Title': dados[1], 'Year': dados[8], 'Genre': dados[3], 'Plot': dados[2], 'Code': dados[0] }
                        poster = dados[6]
                        fanart = dados[5]
                        nomeOriginal = dados[1]
                        ano = dados[8]

                    try:
                        nomeOriginal = unicode(nomeOriginal, 'utf-8')
                    except:
                        nomeOriginal = nomeOriginal

                    addVideo(nomeOriginal+' ('+ano+')', __SITE__+"kodi_"+link, 3, fanart, 'filme', 0, 0, infoLabels, poster)
                #elif server == 1:
                else:
                    idIMDB = re.compile('imdb=(.+)').findall(link)[0]
                    if not idIMDB.startswith('tt'):
                        continue

                    idIMDB = re.compile('imdb=(tt[0-9]{7})').findall(link)[0]

                    dados = Database.selectSerieDB(idIMDB)
                    if dados is None:
                        infoSerie = json.loads(Trakt.getSerie(idIMDB, cat.decode('utf8')))
                        poster = infoSerie["poster"]
                        fanart = infoSerie["fanart"]
                        nomeOriginal = infoSerie["nome"]
                        ano = infoSerie["ano"]

                        infoLabels = {"Title": infoSerie["nome"], 'Aired':infoSerie['aired'], 'Plot':infoSerie['plot'], 'Year':infoSerie['ano'], 'Genre':infoSerie['categoria'], 'Code': infoSerie["imdb"]}
                    else:
                        infoLabels = {"Title": dados[0], 'Aired':dados[8], 'Plot':dados[1], 'Genre':dados[5], 'Code':dados[2], 'Year': dados[9]}
                        poster = dados[7]
                        fanart = dados[6]
                        nomeOriginal = dados[0]
                        ano = dados[9]

                    try:
                        nomeOriginal = unicode(nomeOriginal, 'utf-8')
                    except:
                        nomeOriginal = nomeOriginal

                    addDir(nomeOriginal, __SITE__+"kodi_"+link, 4, fanart, pagina, 'serie', infoLabels, poster)


            """if server == 2:
                for imagem, nome1, nome2, link, nome3, genero, ano, nomeOriginal, realizador, elenco in match:
                    infoLabels = {'Title':nomeOriginal.decode('utf8'), 'Aired':ano, 'Plot': '-'}
                    addDir(nomeOriginal+ ' ('+ano+')', __SITE__+"kodi_"+link, 4, imagem, pagina, 'serie', infoLabels, imagem)"""

        else:
            addDir('Voltar', 'url', None, os.path.join(__ART_FOLDER__, __SKIN__, 'retroceder.png'), 0)

    vista_filmesSeries()

def download(url,name, temporada,episodio,serieNome):
    ap()
    legendasOn = False
    isFilme = False

    if 'serie.php' in url:
        siteBase = 'serie.php'
        isFilme = False
    elif 'filme.php' in url:
        siteBase = 'filme.php'
        isFilme = True

    net = Net()
    net.set_cookies(__COOKIE_FILE__)
    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content
    ap()
    stream = ''
    legenda = ''
    servidor = ''
    ext_g = ''
    titulos = []
    links = []
    legendas = []
    stuff = []
    i = 1
    legendaAux = ''
    if siteBase == 'serie.php':
        match = re.compile('<div\s+id="welele"\s+link="(.+?)"\s+legenda="(.+?)">').findall(codigo_fonte)
        match += re.compile('<div\s+id="welele2"\s+link="(.+?)"\s+legenda="(.+?)">').findall(codigo_fonte)

        for link, legenda in match:
            titulos.append('Servidor #%s' % i)
            links.append(link)
            if not '.srt' in legenda:
                legend = legenda+'.srt'
            legendas.append('http://mrpiracy.top/subs/%s' % legenda)
            i = i+1

    else:
        match = re.compile('<div\s+id="(.+?)"\s+link="(.+?)">').findall(codigo_fonte)
        for idS, link in match:
            if 'vidzi' in link or 'uptostream' in link:
                continue
            if 'legenda' in idS:
                if not '.srt' in link:
                    link = link+'.srt'
                legendaAux = 'http://mrpiracy.top/subs/%s' % link
                continue

            titulos.append('Servidor #%s' % i)
            links.append(link)
            i = i+1
    if len(titulos) > 1:
        servidor = xbmcgui.Dialog().select('Escolha o servidor', titulos)
        if 'openload' in links[servidor]:
            stream = URLResolverMedia.OpenLoad(links[servidor]).getMediaUrl()
            legenda = URLResolverMedia.OpenLoad(links[servidor]).getSubtitle()
        elif 'drive.google.com/' in links[servidor]:
            stream, ext_g = URLResolverMedia.GoogleVideo(links[servidor]).getMediaUrl()
            if legendaAux != '':
                legenda = legendaAux
            else:
                legenda = legendas[0]
    else:
        if 'openload' in links[0]:
            stream = URLResolverMedia.OpenLoad(links[0]).getMediaUrl()
            legenda = URLResolverMedia.OpenLoad(links[0]).getSubtitle()
        elif 'drive.google.com/' in links[servidor]:
            stream, ext_g = URLResolverMedia.GoogleVideo(links[0]).getMediaUrl()
            if legendaAux != '':
                legenda = legendaAux
            else:
                legenda = legendas[0]

    folder = xbmc.translatePath(__ADDON__.getSetting('pastaDownloads'))

    if temporada and episodio:
        if not xbmcvfs.exists(os.path.join(folder,'series')):
            xbmcvfs.mkdirs(os.path.join(folder,'series'))
        if not xbmcvfs.exists(os.path.join(folder,'series',serieNome)):
            xbmcvfs.mkdirs(os.path.join(folder,'series',serieNome))
        if not xbmcvfs.exists(os.path.join(folder,'series',serieNome,"Temporada "+str(temporada))):
            xbmcvfs.mkdirs(os.path.join(folder,'series',serieNome,"Temporada "+str(temporada)))

        folder = os.path.join(folder,'series',serieNome,"Temporada "+str(temporada))
        name = "e"+str(episodio)+" - "+clean(name.split('|')[-1])
    else:
        if not xbmcvfs.exists(os.path.join(folder,'filmes')):
            xbmcvfs.mkdirs(os.path.join(folder,'filmes'))
        folder = os.path.join(folder,'filmes')

    streamAux = clean(stream.split('/')[-1])
    extensaoStream = clean(streamAux.split('.')[-1])

    if '?mim' in extensaoStream:
        extensaoStream = re.compile('(.+?)\?mime=').findall(extensaoStream)[0]

    if ext_g != '':
        extensaoStream = ext_g

    nomeStream = name+'.'+extensaoStream

    if '.vtt' in legenda:
        legendaAux = clean(legenda.split('/')[-1])
        extensaoLegenda = clean(legendaAux.split('.')[1])
        nomeLegenda = name+'.'+extensaoLegenda
        legendasOn = True


    Downloader.Downloader().download(os.path.join(folder.decode("utf-8"),nomeStream), stream, name)

    if legendasOn:
        download_legendas(legenda, os.path.join(folder,nomeLegenda))

def download_legendas(url,path):
    contents = abrir_url(url)
    if contents:
        fh = open(path, 'w')
        fh.write(contents)
        fh.close()
    return

def getGeneros(url):
    ap()
    net = Net()
    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

    #match = re.compile('<div id="item1" class="item">\s+<label for="genre1" id="genre1Label"><a style="font-family: Tahoma; color: #8D8D8D;font-size: 11px;padding-left: 5px;float: left;width: 142px;font-weight: normal;text-decoration: initial;" href="(.+?)">(.+?)<\/a><\/label>\s+<\/div>').findall(codigo_fonte)
    match = re.compile('<label for="genre1" id="genre1Label"><a style="font-family: Tahoma; color: #8D8D8D;font-size: 11px;padding-left: 5px;float: left;width: 142px;font-weight: normal;text-decoration: initial;" href="(.+?)">(.+?)<\/a><\/label>').findall(codigo_fonte)
    match += re.compile('<label for="genre1" id="genre1Label"><a style="font-family: Tahoma; color: #8D8D8D;font-size: 11px;padding-left: 5px;float: left;width: 142px;text-decoration: initial;" href="(.+?)">(.+?)<\/a><\/label>').findall(codigo_fonte)



    for link, nome in match:
        if 'kodi_filmes.php' in url:
            addDir(nome.encode('utf8'), __SITE__+"kodi_"+link, 1, os.path.join(__ART_FOLDER__, __SKIN__, 'generos.png'), 1)
        else:
            addDir(nome.encode('utf8'), url+link, 1, os.path.join(__ART_FOLDER__, __SKIN__, 'generos.png'), 1)

def getYears(url):
    ap()
    net = Net()
    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

    match = re.compile('<label for="(.+?)" id="(.+?)"><a style=\'font-family: Tahoma; color: #8D8D8D;\' class="active" href="(.+?)">(.+?)<\/a><\/label>').findall(codigo_fonte)
    #match += re.compile('<div id="(.+?)" class="item">\s+<label for="(.+?)" id="(.+?)"><a style=\'font-family: Tahoma; color: #8D8D8D;\' class="active" href="(.+?)">(.+?)<\/a><\/label>\s+<\/div>').findall(codigo_fonte)

    for lixo1, lixo2, link, nome in match:
        addDir(nome.encode('utf-8'), url+link, 1, os.path.join(__ART_FOLDER__, __SKIN__, 'generos.png'), 1)

def getNumNotificacoes():
    ap()
    net = Net()
    net.set_cookies(__COOKIE_FILE__)
    codigo_fonte = net.http_GET(__SITE__, headers=__HEADERS__).content

    match = re.compile('<a href="(.+)" class=".+" style=".+?">(.+?) .+<\/a>').findall(codigo_fonte)

    #pprint.pprint(match)
    try:
        if int(match[0][1]) >= 1:
            devolve = '[B][COLOR red]'+match[0][1]+' alertas[/COLOR][/B]'
        else:
            devolve = '[B]'+match[0][1]+' alertas[/B]'
    except:
        devolve = ''

    return devolve


def getListOfMyAccount(url, pagina):
    ap()
    net = Net()
    net.set_cookies(__COOKIE_FILE__)
    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content


    match = re.compile('<div id=".+" class="item">\s+<a href="(.+?)">').findall(codigo_fonte)

    if 'favoritos.php' in url:
        tipo = 'kodi_favoritos'
    elif 'agendados.php' in url:
        tipo = 'agendados'
    elif 'vistos.php' in url:
        tipo = 'vistos'

    #pprint.pprint(match)

    for link in match:
        if 'filme.php' in link:
            idIMDB = re.compile('imdb=(.+)').findall(link)[0]
            if not idIMDB.startswith('tt'):
                continue

            idIMDB = re.compile('imdb=(tt[0-9]{7})').findall(link)[0]
            dados = Database.selectFilmeDB(idIMDB)
            if dados is None:
                infoFilme = json.loads(Trakt.getFilme(idIMDB, ''))
                poster = infoFilme["poster"]
                fanart = infoFilme["fanart"]
                nomeOriginal = infoFilme["nome"]
                ano = infoFilme["ano"]
                infoLabels = {'Title': infoFilme["nome"], 'Year': infoFilme["ano"], 'Genre': infoFilme["categoria"], 'Plot': infoFilme["plot"], 'Code': idIMDB}
            else:
                infoLabels = {'Title': dados[1], 'Year': dados[8], 'Genre': dados[3], 'Plot': dados[2], 'Code': dados[0] }
                poster = dados[6]
                fanart = dados[5]
                nomeOriginal = dados[1]
                ano = dados[8]

            try:
                nomeOriginal = unicode(nomeOriginal, 'utf-8')
            except:
                nomeOriginal = nomeOriginal

            addVideo(nomeOriginal+' ('+ano+')', __SITE__+"kodi_"+link, 3, fanart, 'filme', 0, 0, infoLabels, poster)
        elif 'serie.php' in link:
            idIMDB = re.compile('imdb=(.+)').findall(link)[0]
            if not idIMDB.startswith('tt'):
                continue

            idIMDB = re.compile('imdb=(tt[0-9]{7})').findall(link)[0]

            dados = Database.selectSerieDB(idIMDB)
            if dados is None:
                infoSerie = json.loads(Trakt.getSerie(idIMDB, ''))
                poster = infoSerie["poster"]
                fanart = infoSerie["fanart"]
                nomeOriginal = infoSerie["nome"]
                ano = infoSerie["ano"]

                infoLabels = {"Title": infoSerie["nome"], 'Aired':infoSerie['aired'], 'Plot':infoSerie['plot'], 'Year':infoSerie['ano'], 'Genre':infoSerie['categoria'], 'Code': infoSerie["imdb"]}
            else:
                infoLabels = {"Title": dados[0], 'Aired':dados[8], 'Plot':dados[1], 'Genre':dados[5], 'Code':dados[2], 'Year': dados[9]}
                poster = dados[7]
                fanart = dados[6]
                nomeOriginal = dados[0]
                ano = dados[9]

            try:
                nomeOriginal = unicode(nomeOriginal, 'utf-8')
            except:
                nomeOriginal = nomeOriginal

            addDir(nomeOriginal, __SITE__+"kodi_"+link, 4, fanart, pagina, 'serie', infoLabels, poster)
            """infoLabels = {'Title': nome.encode('utf8') }
            addVideo(nome.encode('utf8'), __SITE__+"kodi_"+link, 3, imagem, 'filme', 0, 0, infoLabels, imagem)"""
        #elif 'serie.php' in link:
            """infoLabels = {'Title': nome.encode('utf8')}
            addDir(nome.encode('utf8'), __SITE__+"kodi_"+link, 4, imagem, pagina, 'serie', infoLabels, imagem)"""


    addDir('Proximo', __SITE__+tipo+'.php?pagina='+str(int(pagina)+1), 11, os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'), int(pagina)+1)

    vista_filmesSeries()

def getNotificacoes(url, pagina):
    ap()
    net = Net()
    net.set_cookies(__COOKIE_FILE__)
    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content.encode('utf8')

    matchAvisos = re.compile('<img src="..(.+?)" style=".+?">\s+<div class="thumb-effect" style=".+?"><\/div>\s+<\/a>\s+<\/div>\s+<\/div>\s+<div class="movie-info" style=".+?">\s+<div class="movie-actions">\s+<a id="watched" href=".+?">Marcar como lido<span class="watch"><\/span><\/a><br>\s+<\/div>\s+<br>\s+<span id="movie-synopsis" class="movie-synopsis" style=".+?">(.+?)<\/span>').findall(codigo_fonte)

    for imagem, aviso in matchAvisos:
        addDir(aviso, 'url', None, __SITE__+imagem, pagina, 0)

    addDir('', '', '', os.path.join(__ART_FOLDER__,'nada.png'), 0)

    #matchNotificacoesSerie = re.compile('<div class="thumb-and-episodes" name="(.+?)">\s+<div class=".+?" title=".+?" style=".+?">\s+<a style=".+?">\s+<img src="(.+?)" alt=".+?" style=".+?">\s+<div class="thumb-effect" title=".+?" style=".+?"><\/div>\s+<\/a>\s+<\/div>\s+<\/div>\s+<div class="movie-info" style=".+?">\s+<a class="movie-name">(.+?)<\/a> > <a class="movie-name" href="(.+?)" style=".+?">(.+?)<\/a> <div class="clear"><\/div>\s+<div class="movie-actions">\s+<a id="watched" href="(.+?)">.+?<span class=".+?"><\/span><\/a><br>\s+<a id=".+?" href=".+?" class=".+?"><\/span><\/a><br>\s+<\/div>\s+<br>\s+<span id="movie-synopsis" class=".+?" style=".+?">(.+?)<a href="(.+?)">(.+?)<\/a><\/span>').findall(codigo_fonte)
    matchNotificacoes = re.compile('<div class="thumb-and-episodes" name="(.+?)">\s+<div class=".+?" title=".+?" style=".+?">\s+<a style=".+?">\s+<img src="(.+?)" alt=".+?" style=".+?">\s+<div class="thumb-effect" title=".+?" style=".+?"><\/div>\s+<\/a>\s+<\/div>\s+<\/div>\s+<div class="movie-info" style=".+?">\s+<a class="movie-name">(.+?)<\/a> > <a class="movie-name" href="(.+?)" style=".+?">(.+?)<\/a> <div class="clear"><\/div>\s+<div class="movie-actions">\s+<a id="watched" href="(.+?)">.+?<span class=".+?"><\/span><\/a><br>\s+<a id=".+?" href=".+?" class=".+?"><\/span><\/a><br>\s+<\/div>\s+<br>\s+<span id="movie-synopsis" class=".+?" style=".+?">(.+?)<').findall(codigo_fonte)

    for idIMDB, imagem, nome, linkMarcarVisto, filmeSerie, linkMarcarVisto1, aviso in matchNotificacoes:
        if 'Filme' in filmeSerie:
            infoLabels = {'Title': nome.decode('utf8'), 'Plot': '' }

            addVideo(nome+": "+aviso, __SITE__+"kodi_filme.php?imdb="+idIMDB, 3, imagem, 'filme', 0, 0, infoLabels, imagem)
        else:
            infoLabels = {'Title':nome.decode('utf8'), 'Plot': ''}
            addDir(nome+": "+aviso, __SITE__+"kodi_serie.php?imdb="+idIMDB, 4, imagem, pagina, 'serie', infoLabels, imagem)


def getTrailer(idIMDB):

    net = Net()
    url = 'http://api.themoviedb.org/3/movie/'+idIMDB+'/videos?api_key=3421e679385f33e2438463e286e5c918'

    try:
        codigo_fonte = net.http_GET(url, headers=__HEADERS__).content
        match = json.loads(codigo_fonte)

    except:
        match = ''
        urlTrailer = ''
    try:
        idYoutube = match["results"][0]["key"]
        urlTrailer = 'plugin://plugin.video.youtube/?action=play_video&videoid='+idYoutube
    except:
        urlTrailer = ''

    return urlTrailer

def seriesTraktVistos():
    url = 'https://api-v2launch.trakt.tv/users/%s/watched/shows' % __ADDON__.getSetting('utilizadorTrakt')

    vistos = Trakt.getTrakt(url, login=False)
    vistos = json.loads(vistos)

    for v in vistos:
        if v["show"]["ids"]["imdb"] is None:
            continue

        for s in v["seasons"]:
            if s['number'] == 0:
                continue

            temporadaNumero = s["number"]

            for e in s["episodes"]:
                episodioN = e["number"]

                episodioInfo = Database.selectEpisodioDB(v["show"]["ids"]["imdb"], temporadaNumero, episodioN)
                if episodioInfo is None:
                    if Database.selectSerieDB(v["show"]["ids"]["imdb"]) is None:
                        lixo = Trakt.getSerie(v["show"]["ids"]["imdb"])
                        Database.markwatchedEpisodioDB(v["show"]["ids"]["imdb"], temporadaNumero, episodioN)
                    else:
                        infoEpis = json.loads(Trakt.getTVDBByEpSe(v["show"]["ids"]["imdb"], temporadaNumero, episodioN))
                        Database.insertEpisodio(infoEpis["name"], infoEpis["plot"], infoEpis["imdb"], infoEpis["tvdb"], infoEpis["season"], infoEpis["episode"], infoEpis["fanart"], infoEpis["poster"], infoEpis["aired"], infoEpis["serie"], infoEpis["traktid"], actores=infoEpis['actors'])
                        Database.markwatchedEpisodioDB(v["show"]["ids"]["imdb"], temporadaNumero, episodioN)
                else:
                    if Database.isWatchedSerieDB(v["show"]["ids"]["imdb"], temporadaNumero, episodioN):
                        continue
                    Database.markwatchedEpisodioDB(v["show"]["ids"]["imdb"], temporadaNumero, episodioN)


def filmesTraktVistos():
    url = 'https://api-v2launch.trakt.tv/users/%s/watched/movies' % __ADDON__.getSetting('utilizadorTrakt')

    vistos = Trakt.getTrakt(url, login=False)
    vistos = json.loads(vistos)


    for v in vistos:
        if v["movie"]["ids"]["imdb"] is None:
            continue
        filme = Database.selectFilmeDB(v["movie"]["ids"]["imdb"])
        if filme is None:
            infoFilme = json.loads(Trakt.getFilme(v["movie"]["ids"]["imdb"], ''))
            Database.markwatchedFilmeDB(v["movie"]["ids"]["imdb"])
        else:
            Database.markwatchedFilmeDB(v["movie"]["ids"]["imdb"])

def watchlistTrakt(url):

    if 'shows' in url:
        tipo = 'series'
    elif 'movies' in url:
        tipo = 'filmes'

    dados = Trakt.getTrakt(url)
    dados = json.loads(dados)

    if tipo == 'filmes':
        for f in dados:
            if f["movie"]["ids"]["imdb"] is None:
                continue

            imdb = f["movie"]["ids"]["imdb"]
            filme = Database.selectFilmeDB(imdb)
            if filme is None:
                infoFilme = json.loads(Trakt.getFilme(imdb, ''))
                poster = infoFilme["poster"]
                fanart = infoFilme["fanart"]
                nomeOriginal = infoFilme["nome"]
                ano = infoFilme["ano"]
                infoLabels = {'Title': infoFilme["nome"], 'Year': infoFilme["ano"], 'Genre': infoFilme["categoria"], 'Plot': infoFilme["plot"], 'Code': imdb}
            else:
                infoLabels = {'Title': filme[1], 'Year': filme[8], 'Genre': filme[3], 'Plot': filme[2], 'Code': filme[0] }
                poster = filme[6]
                fanart = filme[5]
                nomeOriginal = filme[1]
                ano = filme[8]

            try:
                nomeOriginal = unicode(nomeOriginal, 'utf-8')
            except:
                nomeOriginal = nomeOriginal

            addVideo(nomeOriginal+' ('+ano+')', __SITE__+'kodi_filme.php?imdb='+imdb, 3, fanart, 'filme', 0, 0, infoLabels, poster)
    elif tipo == 'series':

        for s in dados:

            if s["show"]["ids"]["imdb"] is None:
                continue

            imdb = s["show"]["ids"]["imdb"]

            serie = Database.selectSerieDB(imdb)
            if serie is None:
                infoSerie = json.loads(Trakt.getSerie(imdb, ''))
                poster = infoSerie["poster"]
                fanart = infoSerie["fanart"]
                nomeOriginal = infoSerie["nome"]
                ano = infoSerie["ano"]

                infoLabels = {"Title": infoSerie["nome"], 'Aired':infoSerie['aired'], 'Plot':infoSerie['plot'], 'Year':infoSerie['ano'], 'Genre':infoSerie['categoria'], 'Code': infoSerie["imdb"]}
            else:
                infoLabels = {"Title": serie[0], 'Aired':serie[8], 'Plot':serie[1], 'Genre':serie[5], 'Code':serie[2], 'Year': serie[9]}
                poster = serie[7]
                fanart = serie[6]
                nomeOriginal = serie[0]
                ano = serie[9]

            try:
                nomeOriginal = unicode(nomeOriginal, 'utf-8')
            except:
                nomeOriginal = nomeOriginal

            addDir(nomeOriginal, __SITE__+"kodi_serie.php?imdb="+imdb, 4, fanart, pagina, 'serie', infoLabels, poster)

def progressoTrakt():
    url = 'http://api-v2launch.trakt.tv/users/%s/watched/shows?extended=full,images' % __ADDON__.getSetting('utilizadorTrakt')

    progresso = Trakt.getTrakt(url, login=False)
    progresso = json.loads(progresso)

    dataAgora = datetime.datetime.now()
    for serie in progresso:
        url = 'https://api-v2launch.trakt.tv/shows/%s/progress/watched?hidden=false&specials=false' % serie["show"]["ids"]["slug"]

        data = Trakt.getTrakt(url)

        #pprint.pprint(data)
        if data == "asd":
            continue
        data = json.loads(data)
        series = {}
        imdbid = serie["show"]["ids"]["imdb"]
        fanart = serie["show"]["images"]["fanart"]["full"]
        poster = serie["show"]["images"]["poster"]["full"]
        slug = serie["show"]["ids"]["imdb"]
        try:
            episodioN = str(data["next_episode"]["number"])
            temporadaNumero = str(data["next_episode"]["season"])
        except:
            continue
        url = 'https://api-v2launch.trakt.tv/shows/%s/seasons/%s/episodes/%s?extended=full' % (imdbid, temporadaNumero, episodioN)
        airedData = json.loads(Trakt.getTrakt(url))

        airedData = airedData["first_aired"].split("T")[0]
        airedData = airedData.split("-")

        if datetime.datetime(int(airedData[0]), int(airedData[1]), int(airedData[2])) > dataAgora:
            continue

        episodioInfo = Database.selectEpisodioDB(imdbid, temporadaNumero, episodioN)
        if episodioInfo is None:
            if Database.selectSerieDB(imdbid) is None:
                lixo = Trakt.getSerie(imdbid)

                infoEpis = Database.selectEpisodioDB(imdbid, temporadaNumero, episodioN)

                infoLabels = {'Title':infoEpis[0], 'Actors':infoEpis[7], 'Plot':infoEpis[1], 'Season':infoEpis[2], 'Episode':infoEpis[3], "Code":imdbid, 'Aired': infoEpis[6] }
                poster = infoEpis[5]
                fanart = infoEpis[4]
                nomeEpisodio = infoEpis[0]
                temporadaEpisodioDB = infoEpis[2]
                numeroEpisodioDB = infoEpis[3]
                serieTitulo = infoEpis[11]

        else:
            infoLabels = {'Title':episodioInfo[0], 'Actors':episodioInfo[7], 'Plot':episodioInfo[1], 'Season':episodioInfo[2], 'Episode':episodioInfo[3], "Code":imdbid, 'Aired': episodioInfo[6] }
            poster = episodioInfo[5]
            fanart = episodioInfo[4]
            nomeEpisodio = episodioInfo[0]
            temporadaEpisodioDB = episodioInfo[2]
            numeroEpisodioDB = episodioInfo[3]
            serieTitulo = episodioInfo[11]

        urlmr = '%skodi_serie.php?t=%s&imdb=%s&e=%s#%s' % (__SITE__, temporadaEpisodioDB, imdbid, numeroEpisodioDB, numeroEpisodioDB)
        addVideo("[B]"+serieTitulo+"[/B] "+temporadaNumero+'x'+episodioN+' . '+nomeEpisodio, urlmr, 3, fanart, 'episodio', temporadaEpisodioDB, numeroEpisodioDB, infoLabels, poster, serieTitulo)

        #thread.start_new_thread(infoSerieProgressoTraktWorker, (imdbid, temporadaNumero, episodioN,))

def infoSerieProgressoTraktWorker(imdbid, temporadaNumero, episodioN):
    episodioInfo = Database.selectEpisodioDB(imdbid, temporadaNumero, episodioN)
    if episodioInfo is None:
        if Database.selectSerieDB(imdbid) is None:
            lixo = Trakt.getSerie(imdbid)

            infoEpis = Database.selectEpisodioDB(imdbid, temporadaNumero, episodioN)

            infoLabels = {'Title':infoEpis[0], 'Actors':infoEpis[7], 'Plot':infoEpis[1], 'Season':infoEpis[2], 'Episode':infoEpis[3], "Code":imdbid, 'Aired': infoEpis[6] }
            poster = infoEpis[5]
            fanart = infoEpis[4]
            nomeEpisodio = infoEpis[0]
            temporadaEpisodioDB = infoEpis[2]
            numeroEpisodioDB = infoEpis[3]
            serieTitulo = infoEpis[11]

    else:
        infoLabels = {'Title':episodioInfo[0], 'Actors':episodioInfo[7], 'Plot':episodioInfo[1], 'Season':episodioInfo[2], 'Episode':episodioInfo[3], "Code":imdbid, 'Aired': episodioInfo[6] }
        poster = episodioInfo[5]
        fanart = episodioInfo[4]
        nomeEpisodio = episodioInfo[0]
        temporadaEpisodioDB = episodioInfo[2]
        numeroEpisodioDB = episodioInfo[3]
        serieTitulo = episodioInfo[11]

    urlmr = '%skodi_serie.php?t=%s&imdb=%s&e=%s#%s' % (__SITE__, temporadaEpisodioDB, imdbid, numeroEpisodioDB, numeroEpisodioDB)
    addVideo("[B]"+serieTitulo+"[/B] "+temporadaNumero+'x'+episodioN+' . '+nomeEpisodio, urlmr, 3, fanart, 'episodio', temporadaEpisodioDB, numeroEpisodioDB, infoLabels, poster, serieTitulo)



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

def vista_filmesSeries():
    opcao = __ADDON__.getSetting('filmesSeriesView')
    if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
    elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
    elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
    elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
    elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
    elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
    elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
    elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")


def vista_temporadas():
    opcao = __ADDON__.getSetting('temporadasView')
    if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
    elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
    elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")

def vista_episodios():
    opcao = __ADDON__.getSetting('episodiosView')
    if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
    elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
    elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")

###################################################################################
#                               FUNCOES JA FEITAS                                 #
###################################################################################


def abrir_url(url,pesquisa=False):

    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection': 'keep-alive'}

    if pesquisa:
        data = urllib.urlencode({'searchBox' : pesquisa})
        req = urllib2.Request(url,data, headers=header)
    else:
        req = urllib2.Request(url, headers=header)

    response = urllib2.urlopen(req)
    link=response.read()
    return link

def addLink(name,url,iconimage):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage,pagina,tipo=None,infoLabels=None,poster=None):
    if infoLabels: infoLabelsAux = infoLabels
    else: infoLabelsAux = {'Title': name}

    if poster: posterAux = poster
    else: posterAux = iconimage

    try:
        name = name.encode('utf-8')
    except:
        name = name


    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&pagina="+str(pagina)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True

    fanart = __FANART__

    if tipo == 'filme':
        fanart = posterAux
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    elif tipo == 'serie':
        fanart = posterAux
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    elif tipo == 'episodio':
        fanart = posterAux
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    else:
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

    liz=xbmcgui.ListItem(name, iconImage=posterAux, thumbnailImage=posterAux)
    liz.setProperty('fanart_image', iconimage)
    liz.setInfo( type="Video", infoLabels=infoLabelsAux )

    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addFolder(name,url,mode,iconimage,folder):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="fanart.jpg", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', iconimage)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
    return ok

def addDirSeason(name,url,mode,iconimage,pagina,temporada):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&pagina="+str(pagina)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&temporada="+str(temporada)
    ok=True
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    liz=xbmcgui.ListItem(name, iconImage="fanart.jpg", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', __FANART__)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def checkVisto(url, temporada=None, episodio=None):

    visto = False

    if temporada and episodio:
        pastaData = __PASTA_DADOS__
        idIMDb = re.compile('imdb=(tt[0-9]{7})&').findall(url)[0]
        visto = Database.isWatchedSerieDB(idIMDb, temporada, episodio)
    else:
        pastaData = __PASTA_DADOS__
        idIMDb = re.compile('imdb=(tt[0-9]{7})').findall(url)[0]
        visto = Database.isWatchedFilmeDB(idIMDb)

    if visto == True:
        return True

    pastaVisto = os.path.join(pastaData,'vistos')

    if temporada and episodio:
        ficheiroVisto = os.path.join(pastaVisto,idIMDb+'_S'+str(temporada)+'x'+str(episodio)+'.mrpiracy')
    else:
        ficheiroVisto = os.path.join(pastaVisto,idIMDb+'.mrpiracy')

    if os.path.exists(ficheiroVisto):
        if temporada and episodio:
            Database.markwatchedEpisodioDB(idIMDb, temporada, episodio)
            if Trakt.loggedIn():
                Trakt.markwatchedEpisodioTrakt(idIMDb, temporada, episodio)
        else:
            Database.markwatchedFilmeDB(idIMDb)
            if Trakt.loggedIn():
                Trakt.markwatchedFilmeTrakt(idIMDb)

        return True
    else:
        return False


def removerVisto(url, temporada=None, episodio=None):

    pastaData = __PASTA_DADOS__
    pastaVisto = os.path.join(pastaData,'vistos')
    if temporada and episodio:
        idIMDb = re.compile('imdb=(tt[0-9]{7})&').findall(url)[0]
        ficheiroVisto = os.path.join(pastaVisto,idIMDb+'_S'+str(temporada)+'x'+str(episodio)+'.mrpiracy')

        Database.markwatchedEpisodioDB(idIMDb, temporada, episodio, naoVisto=True)
        if Trakt.loggedIn():
            Trakt.marknotwatchedEpisodioTrakt(idIMDb, temporada, episodio)
    else:
        idIMDb = re.compile('imdb=(tt[0-9]{7})').findall(url)[0]
        ficheiroVisto = os.path.join(pastaVisto,idIMDb+'.mrpiracy')

        Database.markwatchedFilmeDB(idIMDb, naoVisto=True)
        if Trakt.loggedIn():
            Trakt.marknotwatchedFilmeTrakt(idIMDb)

    try:
        os.remove(ficheiroVisto)
    except:
        pass

    xbmc.executebuiltin("XBMC.Notification(MrPiracy.top,"+"Marcado como não visto"+","+"6000"+","+ os.path.join(__ADDON_FOLDER__,'icon.png')+")")
    xbmc.executebuiltin("XBMC.Container.Refresh")

"""
    if temporada and episodio:
        pastaData = __PASTA_DADOS__
        idIMDb = re.compile('imdb=(.+?)&').findall(url)[0]
    else:
        pastaData = __PASTA_DADOS__
        idIMDb = re.compile('imdb=(.+)').findall(url)[0]

    pastaVisto = os.path.join(pastaData,'vistos')

    if temporada and episodio:
        ficheiroVisto = os.path.join(pastaVisto,idIMDb+'_S'+str(temporada)+'x'+str(episodio)+'.mrpiracy')
    else:
        ficheiroVisto = os.path.join(pastaVisto,idIMDb+'.mrpiracy')

    try:
        os.remove(ficheiroVisto)
    except:
        __ALERTA__('MrPiracy.top', 'Não foi possível marcar como não visto.')

    xbmc.executebuiltin("XBMC.Notification(MrPiracy.top,"+"Marcado como não visto"+","+"6000"+","+ os.path.join(__ADDON_FOLDER__,'icon.png')+")")
    xbmc.executebuiltin("XBMC.Container.Refresh")"""

def marcarVistoSite(url, temporada=None, episodio=None):
    net = Net()
    net.set_cookies(__COOKIE_FILE__)

    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

    if temporada and episodio:
        visto = re.compile('<div class="episode-actions">\s+<a href="(.+?)" class="marcar">Marcar como visto<\/a><a').findall(codigo_fonte)[0]
        siteVisto = __SITE__+visto
    else:
        visto = re.compile('xmlhttp\.open\(\"GET\"\,\"getvisto\.php\?id\=(.+?)\"\,true\)\;').findall(codigo_fonte)[0]
        siteVisto = __SITE__+'getvisto.php?id='+visto
        #visto = re.compile('<a id="watched" href="(.+?)" class="watched ">Marcar como visto<span class="watch"><\/span><\/a>').findall(codigo_fonte)[0]

    if visto != '':
        marcar = net.http_GET(siteVisto, headers=__HEADERS__).content

        xbmc.executebuiltin("XBMC.Notification(MrPiracy.top,"+"Marcado como visto (Site)"+","+"6000"+","+ os.path.join(__ADDON_FOLDER__,'icon.png')+")")
        xbmc.executebuiltin("Container.Refresh")

def ap():
    url = 'http://go.ad2up.com/afu.php?id=366078'
    abrir_url(url)

def marcarVisto(url, temporada=None, episodio=None):


    if temporada and episodio:
        idIMDb = re.compile('imdb=(tt[0-9]{7})&').findall(url)[0]
        Database.markwatchedEpisodioDB(idIMDb, temporada, episodio)
        if Trakt.loggedIn():
            Trakt.markwatchedEpisodioTrakt(idIMDb, temporada, episodio)
    else:
        idIMDb = re.compile('imdb=(tt[0-9]{7})').findall(url)[0]
        Database.markwatchedFilmeDB(idIMDb)
        if Trakt.loggedIn():
            Trakt.markwatchedFilmeTrakt(idIMDb)

    xbmc.executebuiltin("XBMC.Notification(MrPiracy.top,"+"Marcado como visto"+","+"6000"+","+ os.path.join(__ADDON_FOLDER__,'icon.png')+")")
    xbmc.executebuiltin("Container.Refresh")


    """if temporada and episodio:
        pastaData = __PASTA_DADOS__
        idIMDb = re.compile('imdb=(.+?)&').findall(url)[0]
    else:
        pastaData = __PASTA_DADOS__
        idIMDb = re.compile('imdb=(.+)').findall(url)[0]

    pastaVisto = os.path.join(pastaData,'vistos')

    try:
        os.makedirs(pastaVisto)
    except:
        pass

    if temporada and episodio:
        ficheiroVisto = os.path.join(pastaVisto,idIMDb+'_S'+str(temporada)+'x'+str(episodio)+'.mrpiracy')
    else:
        ficheiroVisto = os.path.join(pastaVisto,idIMDb+'.mrpiracy')

    if not os.path.exists(ficheiroVisto):
        f = open(ficheiroVisto, 'w')
        f.write('')
        f.close()
        xbmc.executebuiltin("XBMC.Notification(MrPiracy.top,"+"Marcado como visto"+","+"6000"+","+ os.path.join(__ADDON_FOLDER__,'icon.png')+")")
        xbmc.executebuiltin("Container.Refresh")
    else:
        __ALERTA__('MrPiracy.top', 'Já foi marcado como visto anteriormente.')"""



def addVideo(name,url,mode,iconimage,tipo,temporada,episodio,infoLabels,poster,serieNome=False):

    menu = []

    try:
        name = name.encode('utf-8')
    except:
        name = name

    try:
        serieNome = serieNome.encode('utf-8')
    except:
        serieNome = serieNome
    else:
        pass

    if tipo == 'filme':
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        visto = checkVisto(url)
        idIMDb = re.compile('imdb=(tt[0-9]{7})').findall(url)[0]
        #visto = Database.isWatchedFilmeDB(idIMDb)

        if __ADDON__.getSetting('trailer-filmes') == 'true':
            linkTrailer = getTrailer(idIMDb)
        else:
            linkTrailer = ''
    elif tipo == 'serie':
        print(""+str(temporada))
        print(""+str(episodio))
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        visto = checkVisto(url, temporada, episodio)

        idIMDb = re.compile('imdb=(tt[0-9]{7})&').findall(url)[0]

        linkTrailer = ""
    elif tipo == 'episodio':
        print temporada
        print episodio
        print(""+str(temporada))
        print(""+str(episodio))
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        visto = checkVisto(url, temporada, episodio)
        idIMDb = re.compile('imdb=(tt[0-9]{7})&').findall(url)[0]
        #visto = Database.isWatchedSerieDB(idIMDb, temporada, episodio)
        linkTrailer = ""



    overlay = 6
    playcount = 0

    if visto == True:
        if tipo != 'filme':
            #url += "&temporada="+str(temporada)+"&episodio="+str(episodio)
            menu.append(('Marcar como não visto', 'XBMC.RunPlugin(%s?url=%s&mode=13&temporada=%s&episodio=%s)' % (sys.argv[0], urllib.quote_plus(url), str(temporada), str(episodio))))
        else:
            menu.append(('Marcar como não visto', 'XBMC.RunPlugin(%s?mode=13&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        overlay = 7
        playcount = 1
    elif visto == False:
        if tipo != 'filme':
            #url += "&temporada="+str(temporada)+"&episodio="+str(episodio)
            menu.append(('Marcar como visto', 'XBMC.RunPlugin(%s?url=%s&mode=12&temporada=%s&episodio=%s)' % (sys.argv[0], urllib.quote_plus(url), str(temporada), str(episodio))))
        else:
            menu.append(('Marcar como visto', 'XBMC.RunPlugin(%s?mode=12&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))

    if tipo != 'filme':
        menu.append(('Marcar como visto (Site)', 'XBMC.RunPlugin(%s?url=%s&mode=16&temporada=%s&episodio=%s)' % (sys.argv[0], urllib.quote_plus(url), str(temporada), str(episodio))))
    else:
        menu.append(('Marcar como visto (Site)', 'XBMC.RunPlugin(%s?url=%s&mode=16)' % (sys.argv[0], urllib.quote_plus(url))))

    infoLabels["overlay"] = overlay
    infoLabels["playcount"] = playcount

    liz=xbmcgui.ListItem(name, iconImage=poster, thumbnailImage=poster)
    liz.setProperty('fanart_image', iconimage)
    liz.setInfo( type="Video", infoLabels=infoLabels )

    if not serieNome:
        serieNome = ''

    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&temporada="+str(temporada)+"&episodio="+str(episodio)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&serieNome="+urllib.quote_plus(serieNome)
    ok=True



    if linkTrailer != "":
        menu.append(('Ver trailer', 'XBMC.PlayMedia(%s)' % (linkTrailer)))

    menu.append(('Download', 'XBMC.RunPlugin(%s?mode=7&name=%s&url=%s&iconimage=%s&serieNome=%s&temporada=%s&episodio=%s)'%(sys.argv[0],urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(serieNome), str(temporada), str(episodio))))
    liz.addContextMenuItems(menu, replaceItems=True)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def clean(text):
    command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def player(name,url,iconimage,temporada,episodio,serieNome):

    pastaData = ''

    net = Net()
    net.set_cookies(__COOKIE_FILE__)
    codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

    infolabels = dict()


    if temporada == 0 and episodio == 0:
        pastaData = __PASTA_DADOS__
        idIMDb = re.compile('imdb=(tt[0-9]{7})').findall(url)[0]
        #ano = str(re.compile('\((.+?)\)').findall(name)[0])
        ano = str(re.compile('<span class="year"><span>\s+-\s+\(<\/span>(.+?)<span>\)').findall(codigo_fonte)[0])
        siteBase = 'filme.php'
    else:
        pastaData = __PASTA_DADOS__
        ano = str(re.compile('<span class="year"><span>\s+-\s+\(<\/span>(.+?)<span>\)').findall(codigo_fonte)[0])
        idIMDb = re.compile('imdb=(tt[0-9]{7})&').findall(url)[0]
        siteBase = 'serie.php'
        infolabels['TVShowTitle'] = serieNome

    infolabels['Code'] = idIMDb
    infolabels['Year'] = ano

    mensagemprogresso = xbmcgui.DialogProgress()
    mensagemprogresso.create('MrPiracy.top', u'Abrir emissão','Por favor aguarde...')
    mensagemprogresso.update(25, "", u'Obter video e legenda', "")

    #match = re.compile('<a id="(.+?)" class="btn(.+?)?" onclick=".+?"><img src="(.+?)"><\/a>').findall(codigo_fonte)

    stream, legenda = getStreamLegenda(siteBase, codigo_fonte)

    mensagemprogresso.update(50, "", u'Prepara-te, vai começar!', "")

    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)

    #liz.setInfo( type="Video", infoLabels=infolabels )
    listitem.setInfo(type="Video", infoLabels=infolabels)
    #listitem.setInfo("Video", {"title":name})
    listitem.setProperty('mimetype', 'video/x-msvideo')
    listitem.setProperty('IsPlayable', 'true')
    listitem.setPath(path=stream)
    playlist.add(stream, listitem)

    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

    mensagemprogresso.update(75, "", u'Boa Sessão!!!', "")
    #print "url: "+url+" idIMDb: "+idIMDb+" pastaData: "+pastaData+"\n temporada: "+str(temporada)+" episodio: "+str(episodio)+" \nnome: "+name+" ano:"+str(ano)+"\nstream: "+stream+" legenda: "+legenda

    if stream == False:
        __ALERTA__('MrPiracy.top', 'O servidor escolhido não disponível, escolha outro ou tente novamente mais tarde.')
    else:

        player_mr = Player.Player(url=url, idFilme=idIMDb, pastaData=pastaData, temporada=temporada, episodio=episodio, nome=name, ano=ano, logo=os.path.join(__ADDON_FOLDER__,'icon.png'), serieNome=serieNome)

        mensagemprogresso.close()
        player_mr.play(playlist)
        player_mr.setSubtitles(legenda)

        while player_mr.playing:
            xbmc.sleep(5000)
            player_mr.trackerTempo()


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
legenda=None
pagina=None
temporada=None
episodio=None
serieNome=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: link=urllib.unquote_plus(params["link"])
except: pass
try: legenda=urllib.unquote_plus(params["legenda"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: temporada=int(params["temporada"])
except: pass
try: episodio=int(params["episodio"])
except: pass
try: mode=int(params["mode"])
except: pass
try: pagina=int(params["pagina"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try : serieNome=urllib.unquote_plus(params["serieNome"])
except: pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "LINK. "+str(link)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "PAGINA: "+str(pagina)
print "Temporada: "+str(temporada)
print "Episodio: "+str(episodio)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################
if mode==None or url==None or len(url)<1:
    menu()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1: getList(url, pagina)
elif mode==2: getSeries(url, pagina)
elif mode==3: player(name, url, iconimage, temporada, episodio, serieNome)
elif mode==4: getSeasons(url)
elif mode==5: getEpisodes(url)
elif mode==6: pesquisa()
elif mode==7: download(url, name, temporada, episodio, serieNome)
elif mode==8: getGeneros(url)
elif mode==9: getYears(url)
elif mode==10: minhaConta()
elif mode==11: getListOfMyAccount(url, pagina)
elif mode==12: marcarVisto(url, temporada, episodio)
elif mode==13: removerVisto(url, temporada, episodio)
elif mode==14: getNotificacoes(url, pagina)
elif mode==15: marcarNotificacaoVisto(url)
elif mode==16: marcarVistoSite(url, temporada, episodio)
elif mode==700: loginTrakt()
elif mode==701: menuTrakt()
elif mode==702: progressoTrakt()
elif mode==703: watchlistTrakt(url)
elif mode==1000: abrirDefinincoes()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
