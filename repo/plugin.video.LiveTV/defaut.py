#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,glob,threading,gzip,xbmcvfs,cookielib,pprint,datetime,thread,time,urlparse,base64,plugintools,calendar
import xml.etree.ElementTree as ET
import fileUtils as fu

from resources.lib import common
from urllib2 import Request, urlopen
from datetime import date
from bs4 import BeautifulSoup
from resources.lib import Downloader #Enen92 class
from resources.lib import Player
from resources.lib import TVArchive
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
from t0mm0.common.net import HttpResponse
from resources.lib import URLResolverMedia
from resources.lib import Trakt
from resources.lib import Database
from unicodedata import normalize

####################################################### CONSTANTES #####################################################

global g_timer
global televisioonilink
global filmilink
global andmelink
global uuenduslink
global lehekylg
global uuendused
global vanemalukk
global version
global mode

AddonTitle = "Live!t TV"
mode = 3333
version = ""
kasutajanimi = ""
salasona = ""
lehekylg = ""
vanemakood = ""
vanemalukk = ""
televisioonilink = ""
filmilink = ""
andmelink = ""

__ADDON_ID__	= xbmcaddon.Addon().getAddonInfo("id")
__ADDON__	= xbmcaddon.Addon(__ADDON_ID__)
__ADDONVERSION__ = __ADDON__.getAddonInfo('version')
__ADDON_FOLDER__	= __ADDON__.getAddonInfo('path')
__SETTING__	= xbmcaddon.Addon().getSetting
__ART_FOLDER__	= __ADDON_FOLDER__ + '/resources/img/'
__FANART__ 		= os.path.join(__ADDON_FOLDER__,'fanart.jpg')
_ICON_ = __ADDON_FOLDER__ + '/icon.png'
__SKIN__ = 'v2'
__SITEBD__ = base64.urlsafe_b64decode('aHR0cDovL3d3dy5wY3RlY2tzZXJ2LmNvbS9HcnVwb0tvZGkvUEhQLw==')
__SITEAddon__ = base64.urlsafe_b64decode('aHR0cDovL3d3dy5wY3RlY2tzZXJ2LmNvbS9HcnVwb0tvZGkvQWRkb24v')
__EPG__ = __ADDON__.getSetting("lista_epg")
__Qualidade__ = __ADDON__.getSetting('qualidadeFilmes')
__FOLDER_EPG__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.LiveTV/').decode('utf-8'), 'epgliveit')
__COOKIE_FILE__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.LiveTV/').decode('utf-8'), 'cookie.liveittv')
__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
check_login = {}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.7', 'Content-Type': 'application/json'}
__PASTA_DADOS__ = Addon(__ADDON_ID__).get_profile().decode("utf-8")
__PASTA_FILMES__ = xbmc.translatePath(__ADDON__.getSetting('bibliotecaFilmes'))
__PASTA_SERIES__ = xbmc.translatePath(__ADDON__.getSetting('bibliotecaSeries'))
__API__ = base64.urlsafe_b64decode('aHR0cDovL21wYXBpLm1sLw==')
__API_SITE__ = base64.urlsafe_b64decode('aHR0cDovL21wYXBpLm1sL2FwaS8=')
__SITE__ = base64.urlsafe_b64decode('aHR0cDovL21ycGlyYWN5LmdxLw==')

###################################################################################
#							  Iniciar Addon										  #
###################################################################################

def __ALERTA__(text1="",text2="",text3=""):
	if text3=="": xbmcgui.Dialog().ok(text1,text2)
	elif text2=="": xbmcgui.Dialog().ok("",text1)
	else: xbmcgui.Dialog().ok(text1,text2,text3)

def menu():
	if (not __ADDON__.getSetting('login_name') or not __ADDON__.getSetting('login_password')):
		__ALERTA__(AddonTitle, 'Precisa de definir o seu Utilizador e Senha')
		abrirDefinincoes()
		
	else:
		check_login = login()
		database = Database.isExists()
		if check_login['user']['nome'] != '':
			if check_login['sucesso']['resultado'] == 'yes':
				menus = {
					'nome': '',
					'logo': '',
					'link': '',
					'tipo': '',
					'senha': ''
					}
				menus1 = {
					'nome': '',
					'logo': '',
					'link': '',
					'tipo': '',
					'senha': ''
					}
				menus3 = {
					'nome': '',
					'logo': '',
					'link': '',
					'tipo': '',
					'senha': ''
					}
				menus4 = {
					'nome': '',
					'logo': '',
					'link': '',
					'tipo': '',
					'senha': ''
					}
				menus5 = {
					'nome': '',
					'logo': '',
					'link': '',
					'tipo': '',
					'senha': ''
					}
				if check_login['datafim']['data'] != "Membro Ativo Sem Doacao!":
					if check_login['user']['dias'] == '5' or check_login['user']['dias'] == '4' or check_login['user']['dias'] == '3' or check_login['user']['dias'] == '2' or check_login['user']['dias'] == '1':
						__ALERTA__(AddonTitle, 'Faltam '+check_login['user']['dias']+' dias para o servico expirar.')
					if check_login['user']['dias'] == '0':
						__ALERTA__(AddonTitle, 'É hoje que o seu serviço expira. Faça a sua Renovação. Caso não faça irá ficar Inactivo Hoje.')
				if check_login['datafim']['data'] != "Membro Ativo Sem Doacao!":
					menus2 = {
					'nome': '',
					'logo': '',
					'link': '',
					'tipo': '',
					'senha': ''
					}
					#_listauser = check_login['user']['lista']
					#andmelink = _listauser+'panel_api.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")
					#menus2['nome'] = "Ver Informacao da Conta"
					#menus2['logo'] = __SITEAddon__+"Imagens/estadomembro.png"
					#menus2['link'] = andmelink
					#menus2['tipo'] = "estado"
					#menus2['senha'] = ""
					#menus2['fanart'] = __SITEAddon__+"Imagens/estado_fanart.png"
					#check_login['menus'].append(menus2)
				
				
				#menus4['nome'] = "Limpar Cache"
				#menus4['logo'] = __SITEAddon__+"Imagens/estadomembro.png"
				#menus4['link'] = 'adsfsdfsd'
				#menus4['tipo'] = "limparcache"
				#menus4['senha'] = ""
				#menus4['fanart'] = __SITEAddon__+"Imagens/estado_fanart.png"
				#check_login['menus'].append(menus4)
				#menus5['nome'] = "Limpar Tudo Gravado"
				#menus5['logo'] = __SITEAddon__+"Imagens/estadomembro.png"
				#menus5['link'] = 'sdfsdfsd'
				#menus5['tipo'] = "limpartudo"
				#menus5['senha'] = ""
				#menus5['fanart'] = __SITEAddon__+"Imagens/estado_fanart.png"
				#check_login['menus'].append(menus5)
				
				menus5['nome'] = "Definições"
				menus5['logo'] = __SITEAddon__+"Imagens/definicoes.png"
				menus5['link'] = 'sdfsdfsd'
				menus5['tipo'] = "definicoes"
				menus5['senha'] = ""
				menus5['fanart'] = __SITEAddon__+"Imagens/definicoes_fanart.png"
				check_login['menus'].append(menus5)
				
				#menus3['nome'] = "Pesquisa"
				#menus3['logo'] = os.path.join(__ART_FOLDER__, __SKIN__, 'pesquisa.png')
				#menus3['link'] = __API_SITE__
				#menus3['tipo'] = "pesquisa"
				#menus3['senha'] = ""
				#menus3['fanart'] = os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png')
				#check_login['menus'].append(menus3)
				
				menus1['nome'] = "Novidades"
				menus1['logo'] = check_login['info']['logo2']
				menus1['link'] = check_login['info']['link2']
				menus1['tipo'] = "novidades"
				menus1['senha'] = ""
				menus1['fanart'] = __SITEAddon__+"Imagens/novidades_fanart.png"
				check_login['menus'].append(menus1)
				
				Menu_inicial(check_login,False,'')
			elif check_login['sucesso']['resultado'] == 'utilizador':
				__ALERTA__(AddonTitle, 'Utilizador incorreto.')
				addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','',__SITEAddon__+"Imagens/definicoes_fanart.png")
				addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
				vista_menu()
			elif check_login['sucesso']['resultado'] == 'senha':
				__ALERTA__(AddonTitle, 'Senha incorreta.')
				addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','',__SITEAddon__+"Imagens/definicoes_fanart.png")
				addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
				vista_menu()
			elif check_login['sucesso']['resultado'] == 'ativo':
				__ALERTA__(AddonTitle, 'O estado do seu Utilizador encontra-se Inactivo. Para saber mais informações entre em contacto pelo email liveitkodi@gmail.com.')
				vista_menu()
			else:
				__ALERTA__(AddonTitle, 'Não foi possível abrir a página. Por favor tente novamente.')
				vista_menu()
		else:
			addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','',__SITEAddon__+"Imagens/definicoes_fanart.png")
			addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
			vista_menu()

###################################################################################
#							  Login Addon										  #
###################################################################################
def minhaConta(data_user,estilo):
	addDir(data_user, 'url', None, None, estilo, __SITEAddon__+"Imagens/estadomembro.png",'','','','',__SITEAddon__+"Imagens/estado_fanart.png")
	addDir('Definições', 'url', None, 1000, estilo, __SITEAddon__+"Imagens/definicoes.png",'','','','',__SITEAddon__+"Imagens/definicoes_fanart.png")
	vista_menu()

def login():
	informacoes = {
		'user' : {
			'nome': '',
			'nome': '',
			'email': '',
			'tipo': '',
			'dias': '',
			'lista': '',
			'listanova': '',
			'epg': '',
			'tipologia': '',
			'servidor': '',
			'senhaadulto': ''
		},
		'sucesso' :{
			'resultado': ''
		},
		'mac' :{
			'tem': ''
		},
		'macestado' :{
			'mac': ''
		},
		'datafim' :{
			'data': ''
		},
		'info' : {
			'epg': '',
			'logo': '',
			'logo2': '',
			'log': '',
			'user': '',
			'password': '',
			'link2': '',
			'link': ''
		},
		'menus': []
	} # 
	
	try:
		net = Net()
		net.set_cookies(__COOKIE_FILE__)
		dados = {'username': __ADDON__.getSetting("login_name"), 'password': __ADDON__.getSetting("login_password")}
		
		codigo_fonte = net.http_POST(__SITEBD__+'LoginAddon2.php',form_data=dados,headers=__HEADERS__).content
		elems = ET.fromstring(codigo_fonte)
		for child in elems:
			if(child.tag == 'sucesso'):
				informacoes['sucesso']['resultado'] = child.text
			elif(child.tag == 'user'):
				for d in child:
					if(d.tag == 'Nome'):
						informacoes['user']['nome'] = d.text
					elif(d.tag == 'EPG'):
						informacoes['user']['epg'] = d.text
					elif(d.tag == 'Tipologia'):
						informacoes['user']['tipologia'] = d.text
					elif(d.tag == 'Email'):
						informacoes['user']['email'] = d.text
					elif(d.tag == 'Servidor'):
						informacoes['user']['servidor'] = d.text
					elif(d.tag == 'Tipo'):
						informacoes['user']['tipo'] = d.text
					elif(d.tag == 'dias'):
						informacoes['user']['dias'] = d.text
					elif(d.tag == 'Lista'):
						informacoes['user']['lista'] = d.text
					elif(d.tag == 'ListaNova'):
						informacoes['user']['listanova'] = d.text
					elif(d.tag == 'DataFim'):
						try:
							informacoes['datafim']['data'] = "Membro Ativo até "+ d.text
						except:
							informacoes['datafim']['data'] = "Membro Ativo Sem Doacao!"
					elif(d.tag == 'SenhaAdultos'):
						informacoes['user']['senhaadulto'] = d.text		
			elif(child.tag == 'info'):
				for e in child:
					if(e.tag == 'epg'):
						informacoes['info']['epg'] = e.text
					elif(e.tag == 'logo'):
						informacoes['info']['logo'] = e.text
					elif(e.tag == 'link'):
						informacoes['info']['link'] = e.text
					elif(e.tag == 'logo2'):
						informacoes['info']['logo2'] = e.text
					elif(e.tag == 'link2'):
						informacoes['info']['link2'] = e.text
					elif(e.tag == 'log'):
						informacoes['info']['log'] = e.text
					elif(e.tag == 'user'):
						informacoes['info']['user'] = e.text
					elif(e.tag == 'password'):
						informacoes['info']['password'] = e.text
			elif(child.tag == 'menus'):
				menu = {
						'nome': '',
						'logo': '',
						'link': '',
						'tipo': '',
						'senha': '',
						'fanart': ''
					}
				for g in child:
					if(g.tag == 'nome'):
						menu['nome'] = g.text	
					elif(g.tag == 'logo'):
						menu['logo'] = g.text
					elif(g.tag == 'link'):
						menu['link'] = g.text
					elif(g.tag == 'tipo'):
						menu['tipo'] = g.text	
					elif(g.tag == 'fanart'):
						menu['fanart'] = g.text
					elif(g.tag == 'senha'):
						menu['senha'] = informacoes['user']['senhaadulto']
				if informacoes['datafim']['data'] == "Membro Ativo Sem Doacao!":
					if menu['nome'] != 'Adultos' and menu['nome'] != 'TV Archive':
						informacoes['menus'].append(menu)
				else:
					if menu['nome'] == 'TV Archive':
						menu['nome'] = menu['nome']+" (Ver o que passou)"
						menu['tipo'] = "tvarchive"
						
					informacoes['menus'].append(menu)		
			else:
				__ALERTA__(AddonTitle, 'Não sei o que estou a ler.')
	except:
		__ALERTA__(AddonTitle, 'Não foi possível abrir a página. Por favor tente novamente.')
		return informacoes

	return informacoes

def definicoes(url,tipouser,servuser):
	if tipouser != 'Teste' and servuser != 'Teste':
		andmelink = url+'panel_api.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")
		addDir('Ver Informacao da Conta', andmelink, None, 3335, 'Lista',__SITEAddon__+"Imagens/estadomembro.png",'','','','',__SITEAddon__+"Imagens/estado_fanart.png")
	else:
		addDir('Conta de Teste', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
	addDir('Limpar Cache', 'ytyty', None, 5000, 'Lista',__SITEAddon__+"Imagens/definicoes.png",'','','','',__SITEAddon__+"Imagens/definicoes_fanart.png")
	addDir('Limpar Toda a Cache', 'sdfsdf', None, 6000, 'Lista',__SITEAddon__+"Imagens/definicoes.png",'','','','',__SITEAddon__+"Imagens/definicoes_fanart.png")
	addDir('Definições Addon', 'sdfsdf', None, 3000, 'Lista',__SITEAddon__+"Imagens/definicoes.png",'','','','',__SITEAddon__+"Imagens/definicoes_fanart.png")

def login2():
	resultado = False
	try:
		post = {'username': __ADDON__.getSetting('email'), 'password': __ADDON__.getSetting('password'),'grant_type': 'password', 'client_id': 'kodi', 'client_secret':'pyRmmKK3cbjouoDMLXNtt2eGkyTTAG' }
		
		resultado = abrir_url(__API_SITE__+'login', post=json.dumps(post), header=headers)
		
		if resultado == 'DNS':
			__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
			return False
		resultado = json.loads(resultado)
		#colocar o loggedin
		token = resultado['access_token']
		refresh = resultado['refresh_token']
		headersN = headers
		headersN['Authorization'] = 'Bearer %s' % token
		
		resultado = abrir_url(__API_SITE__+'me', header=headersN)
		resultado = json.loads(resultado)
		try:
			username = resultado['username'].decode('utf-8')
		except:
			username = resultado['username'].encode('utf-8')
		
		if resultado['email'] == __ADDON__.getSetting('email'):
			__ADDON__.setSetting('tokenMrpiracy', token)
			__ADDON__.setSetting('refreshMrpiracy', refresh)
			__ADDON__.setSetting('loggedin', username)
			return True
	except:
		__ALERTA__(AddonTitle, 'Não foi possível abrir a página. Por favor tente novamente.')
		return False

def minhaContabuild():
	if (not __ADDON__.getSetting('login_name') or not __ADDON__.getSetting('login_password')):
		__ALERTA__(AddonTitle, 'Precisa de definir o seu Utilizador e Senha')
		abrirDefinincoesMesmo()
	else:
		check_login = login()
		if check_login['datafim']['data'] == '':
			abrirDefinincoesMesmo()
		else:
			_listauser = check_login['user']['lista']
			andmelink = _listauser+'panel_api.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")
			execute_ainfo(andmelink)

def loginPesquisa():
	if (not __ADDON__.getSetting('login_name') or not __ADDON__.getSetting('login_password')):
		__ALERTA__(AddonTitle, 'Precisa de definir o seu Utilizador e Senha')
		abrirDefinincoesMesmo()
	else:
		check_login = login()
		if check_login['datafim']['data'] == '':
			abrirDefinincoesMesmo()
		else:
			_tipouser = check_login['user']['tipo']
			_servuser = check_login['user']['servidor']
			_nomeuser = check_login['user']['nome']
			pesquisa('',_servuser)

def buildLiveit(tipologia):
	if (not __ADDON__.getSetting('login_name') or not __ADDON__.getSetting('login_password')):
		__ALERTA__(AddonTitle, 'Precisa de definir o seu Utilizador e Senha')
		abrirDefinincoesMesmo()
	else:
		if(tipologia == 'FilmesLive') or (tipologia == 'SeriesLive') or (tipologia == 'AnimesLive'):
			check_login = login2()
			if check_login == True:
				check_login2 = login()
				if(tipologia == 'FilmesLive'):
					_listauser = check_login2['user']['lista']
					if tipo_user != 'Teste':
						filmilink = _listauser+'enigma2.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")+'&type=get_vod_categories'
						addDir('Filmes da Lista',filmilink,None,3337,'Miniatura',os.path.join(__ART_FOLDER__, __SKIN__, 'filmes.png'),'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
					menuFilmes(os.path.join(__ART_FOLDER__, __SKIN__, 'filmes.png'),__SITEAddon__+'Imagens/filmes_fanart.png')
				elif(tipologia == 'SeriesLive'):
					menuSeries(os.path.join(__ART_FOLDER__, __SKIN__, 'series.png'),__SITEAddon__+'Imagens/series_fanart.png')
				elif(tipologia == 'AnimesLive'):
					menuAnimes(os.path.join(__ART_FOLDER__, __SKIN__, 'animes.png'),__SITEAddon__+'Imagens/series_fanart.png')
		else:
			check_login = login()
			if check_login['user']['nome'] != '':
				if check_login['sucesso']['resultado'] == 'yes':
					Menu_inicial(check_login,True,tipologia)
				elif check_login['sucesso']['resultado'] == 'utilizador':
					__ALERTA__(AddonTitle, 'Utilizador incorreto.')
				elif check_login['sucesso']['resultado'] == 'senha':
					__ALERTA__(AddonTitle, 'Senha incorreta.')
				elif check_login['sucesso']['resultado'] == 'ativo':
					__ALERTA__(AddonTitle, 'O estado do seu Utilizador encontra-se Inactivo. Para saber mais informações entre em contacto pelo email liveitkodi@gmail.com')
				else:
					__ALERTA__(AddonTitle, 'Não foi possível abrir a página. Por favor tente novamente.')
			else:
				__ALERTA__(AddonTitle, 'Não foi possível abrir a página. Por favor tente novamente.')

def abrirVideoClube(url,_tipouser):
	addDir('Filmes',url,None,21,'Miniatura',__SITEAddon__+'Imagens/filme2.png','Filme','','','',__SITEAddon__+'Imagens/filmes_fanart.png')					
	addDir('Séries',url,None,20,'Miniatura',__SITEAddon__+'Imagens/serie1.png','Serie','','','',__SITEAddon__+'Imagens/series_fanart.png')
	addDir('Animes',url,None,24,'Miniatura',__SITEAddon__+'Imagens/anime.png','Filme','','','',__SITEAddon__+'Imagens/series_fanart.png')
	
	if _tipouser != 'Teste':
		addDir('Pesquisa',__API_SITE__,None,120,'Lista',os.path.join(__ART_FOLDER__, __SKIN__, 'pesquisa.png'),'pesquisa','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))

def Menu_inicial(men,build,tipo):
	_tipouser = men['user']['tipo']
	_servuser = men['user']['servidor']
	_nomeuser = men['user']['nome']
	_listauser = men['user']['lista']
	_listausernova = men['user']['listanova']
	_datauser = men['datafim']['data']
	_epguser = men['user']['epg']
	tiposelect = men['user']['tipologia']
	
	_senhaadultos = __ADDON__.getSetting("login_adultos")
	_fanart = ''
	
	passanovo = True
	if _tipouser == 'Teste' and _servuser == 'Teste':
		passanovo = False
	
	if build == True and passanovo == False:
		__ALERTA__(AddonTitle, 'É um utilizador Free logo não tem acesso á nossa build a funcionar.')
	elif(build == True):
		tipocan = ''
		urlbuild = ''
		nomebuild = ''
		senhaadu = men['user']['senhaadulto']
		if tipo == 'Praia':
			urlbuild = __SITEAddon__+"Ficheiros/praiasaddongr.txt"
			_fanart = __SITEAddon__+"Imagens/novidades_fanart.png"
			tipocan = 'Praia'
			nomebuild = 'Praia'
		if tipo == 'ProgramasTV':
			urlbuild = __SITEAddon__+"Ficheiros/proteleaddongr.txt"
			_fanart = __SITEAddon__+"Imagens/novidades_fanart.png"
			tipocan = 'ProgramasTV'
			nomebuild = 'ProgramasTV'
		#if _servuser == 'Teste':
		#	urlbuild = __SITEAddon__+"Ficheiros/praiasaddongr.txt"
		#elif(_servuser == 'Servidor1'):
		#	urlbuild = __SITEAddon__+"Ficheiros/canaisaddonservidor1.txt"
		if(tipo == 'Canal'):
			tipocan = 'Normal'
			nomebuild = 'Canais PT'
			_fanart = __SITEAddon__+"Imagens/tv_fanart.png"
		elif(tipo == 'Novidades'):
			tipocan = 'novidades'
			nomebuild = 'Novidades'
			_fanart = __SITEAddon__+"Imagens/novidadestv.png"
			urlbuild = __SITEAddon__+"Ficheiros/novidades_fanart.txt"
		elif(tipo == 'Patrocinadores'):
			tipocan = 'patrocinadores'
			nomebuild = 'Patrocinadores'
			_fanart = __SITEAddon__+"Imagens/participa.jpg"
			urlbuild = __SITEAddon__+"Ficheiros/patrocinadores.txt"
		
		if(tipo == 'Novidades') or (tipo == 'Patrocinadores'):
			listar_grupos('',urlbuild,'Lista',tipocan,_tipouser,_servuser,_fanart)
		else:
			if(tipo == 'Praia') or (tipo == 'ProgramasTV'):
				listar_grupos('',urlbuild,'Miniatura',tipocan,_tipouser,_servuser,_fanart)
				xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
			else:
				#urlbuild = _listauser+'get.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")+'&type=m3u_plus&output='+tiposelect	
				abrim3u2(_listauser,tiposelect)
				xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
	else:
		for menu in men['menus']:
			nome = menu['nome']
			logo = menu['logo']
			link = menu['link']
			tipo = menu['tipo']
			senha = menu['senha']
			fanart = menu['fanart']
			if tipo != 'Filme' and tipo != 'Serie':
				if tipo == 'patrocinadores' or tipo == 'novidades':
					addDir(nome,link,None,1,'Lista',logo,tipo,_tipouser,_servuser,'',fanart)
				elif tipo == 'Anime':
					addDir(nome,_listauser,None,28,'Miniatura',logo,tipo,_tipouser,_servuser,'',fanart)
				elif tipo == 'tvarchive':
					if _tipouser != 'Teste' and _servuser != 'Teste':
						addDir(nome,_listauser,None,25,'Miniatura',logo,'','','','',fanart)
				elif tipo == 'definicoes':
					addDir(nome,_listauser,None,27,'Miniatura',logo,tipo,_tipouser,_servuser,'',fanart)
				elif(tipo == 'pesquisa' and _tipouser != 'Teste'):
					if _tipouser != 'Teste':
						addDir(nome,link,None,120,'Lista',logo,tipo,_tipouser,_servuser,'',fanart)
				else:
					if _tipouser == 'Administrador' or _tipouser == 'Patrocinador' or _tipouser == 'PatrocinadorPagante':
						if nome == 'TVs':
							#urllis = _listauser+'get.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")+'&type=m3u_plus&output='+tiposelect
							addDir(nome,_listauser,tiposelect,3333,'Miniatura',logo,tipo,_tipouser,_servuser,_datauser,fanart)
							addDir('TVs-Free',link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,'',fanart)
						else:
							addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,nome,fanart)
					else:
						if (nome == 'TVs' and _tipouser != 'Teste') or (nome == 'TVs' and _tipouser == 'Teste' and _servuser != 'Teste'):
							#urllis = _listauser+'get.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")+'&type=m3u_plus&output='+tiposelect
							addDir(nome,_listauser,tiposelect,3333,'Miniatura',logo,tipo,_tipouser,_servuser,_datauser,fanart)
						else:
							if tipo != 'Adulto' or nome != 'Radios':
								if _servuser == 'Teste':
									addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,nome,fanart)
								else:
									addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,_datauser,fanart)
							else:
								if _servuser == 'Teste':
									addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,nome,fanart)	
		
		#xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(_nomeuser, Versão do addon: '+_VERSAO_, 8000, _ICON_))
		thread.start_new_thread( obter_ficheiro_epg, () )
		xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(AddonTitle,'Secção Iniciada: '+_nomeuser, 8000, _ICON_))
		vista_Canais_Lista()
		xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
	#check_version()

################################
###		Clear Cache		###
################################

def CLEARCACHE():
	xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
	if os.path.exists(xbmc_cache_path)==True:	
		for root, dirs, files in os.walk(xbmc_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
	
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Apagar Cache no XBMC.", str(file_count) + " ficheiros encontrados.", "Quer apagar todos os ficheiros em cache?"):
				
					for f in files:
						try:
							os.unlink(os.path.join(root, f))
						except:
							pass
					for d in dirs:
						try:
							shutil.rmtree(os.path.join(root, d))
						except:
							pass
						
			else:
				pass
	if xbmc.getCondVisibility('system.platform.ATV2'):
		atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
		
		for root, dirs, files in os.walk(atv2_cache_a):
			file_count = 0
			file_count += len(files)
		
			if file_count > 0:

				dialog = xbmcgui.Dialog()
				if dialog.yesno("Apagar ficheiros ATV2.", str(file_count) + " ficheiros encontrados em 'Outros'", "Quer apagar todos os ficheiros em cache?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass
		atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
		
		for root, dirs, files in os.walk(atv2_cache_b):
			file_count = 0
			file_count += len(files)
		
			if file_count > 0:

				dialog = xbmcgui.Dialog()
				if dialog.yesno("Apagar ficheiros ATV2.", str(file_count) + " ficheiros encontrados em 'Local'", "Quer apagar todos os ficheiros em cache?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass
			  # Set path to Cydia Archives cache files
							 

	# Set path to What th Furk cache files
	wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
	if os.path.exists(wtf_cache_path)==True:	
		for root, dirs, files in os.walk(wtf_cache_path):
			file_count = 0
			file_count += len(files)
		
		# Count files and give option to delete
			if file_count > 0:
	
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Apagar a cache WTF.", str(file_count) + " ficheiros encontrados.", "Quer apagar todos os ficheiros em cache?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass
				
				# Set path to 4oD cache files
	channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
	if os.path.exists(channel4_cache_path)==True:	
		for root, dirs, files in os.walk(channel4_cache_path):
			file_count = 0
			file_count += len(files)
		
		# Count files and give option to delete
			if file_count > 0:
	
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Apagar ficheiros 4oD em cache.", str(file_count) + " ficheiros encontrados.", "Quer apagar todos os ficheiros em cache?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass
				
				# Set path to BBC iPlayer cache files
	iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
	if os.path.exists(iplayer_cache_path)==True:	
		for root, dirs, files in os.walk(iplayer_cache_path):
			file_count = 0
			file_count += len(files)
		
		# Count files and give option to delete
			if file_count > 0:
	
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Apagar ficheiros BBC iPlayer em cache.", str(file_count) + " ficheiros encontrados.", "Quer apagar todos os ficheiros em cache?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass
				
				
				# Set path to Simple Downloader cache files
	downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
	if os.path.exists(downloader_cache_path)==True:	
		for root, dirs, files in os.walk(downloader_cache_path):
			file_count = 0
			file_count += len(files)
		
		# Count files and give option to delete
			if file_count > 0:
	
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Apagar ficheiros Simple Downloader em cache.", str(file_count) + " ficheiros encontrados.", "Quer apagar todos os ficheiros em cache?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass
	
	itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
	if os.path.exists(itv_cache_path)==True:	
		for root, dirs, files in os.walk(itv_cache_path):
			file_count = 0
			file_count += len(files)
			
			if file_count > 0:
	
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Apagar items em cache", str(file_count) + " ficheiros encontrados.", "Quer apagar todos os ficheiros em cache?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass
	dialog = xbmcgui.Dialog()
	dialog.ok(AddonTitle, "		Cache apagada com sucesso!")


################################
###	 Purge Packages		###
################################

def PURGEPACKAGES():
	packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
	try:	
		for root, dirs, files in os.walk(packages_cache_path):
			file_count = 0
			file_count += len(files)
			
			if file_count > 0:
	
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Excluir informação em Cache.", str(file_count) + " ficheiros encontrados.", "Quer apagar todos os ficheiros?"):
							
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
					dialog = xbmcgui.Dialog()
					dialog.ok(AddonTitle, "		Kodi limpo com sucesso.")
				else:
						pass
			else:
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, "		Não foram encontrados ficheiros a apagar.")
	except: 
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle, "Erro ao tentar apagar ficheiros em cache.")

###############################################################################################################
#													Menus													 #
###############################################################################################################

def abrim3u(url, datauser):
	tmpList = []
	list = common.m3u2list(url)
	addDir('Atualizar Lista',url,None,3333,'Miniatura',os.path.join(__ART_FOLDER__, __SKIN__, 'retroceder.png'),'','','',datauser,os.path.join(__ART_FOLDER__, __SKIN__, 'retroceder.png'))
	addLinkCanal('Vídeo Instalação Build','plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=PulxztcAHks&t','','','')
	addLinkCanal('Dúvidas: liveitkodi@gmail.com ','','','','')
	addLinkCanal(datauser,'','','','')
	for channel in list:
		name = common.GetEncodeString(channel["display_name"])
		image = channel.get("tvg_logo", "")
		url = common.GetEncodeString(channel["url"])
		id_ip = channel.get("tvg-ID", "")
		
		addLinkCanal(name,url,image,id_ip,'')
	
	vista_Canais_Lista()
	
def abrim3u2(url,tipose):
	version = __ADDONVERSION__
	kasutajanimi=__ADDON__.getSetting("login_name")
	salasona=__ADDON__.getSetting("login_password")
	lehekylg=url
	vanemakood=__ADDON__.getSetting("login_adultos")
	vanemalukk=__ADDON__.getSetting("login_adultos_sim")
	
	televisioonilink = url+'enigma2.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")+'&type=get_live_categories'

	addDir('Atualizar Lista',url,tipose,3333,'Miniatura',os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
	security_check(televisioonilink,tipose)

def security_check(url,tipose):
	request = urllib2.Request(url, headers={"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ET.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall("channel"):
		kanalinimi = channel.find("title").text
		kanalinimi = base64.b64decode(kanalinimi)
		kategoorialink = channel.find("playlist_url").text
		
		addDir(kanalinimi,kategoorialink,tipose,3338,'Miniatura',os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
	vista_Canais_Lista()

def detect_modification(url):
	request = urllib2.Request(url, headers={"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ET.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall("channel"):
		filminimi = channel.find("title").text
		filminimi = base64.b64decode(filminimi)
		kategoorialink = channel.find("playlist_url").text
		
		addDir(filminimi,kategoorialink,None,3339,'Miniatura',os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
	vista_Canais_Lista()

def stream_video(name,url,image,tiposelect):
	vanemalukk=__ADDON__.getSetting("login_adultos_sim")
	if vanemalukk == "true":
		vanema_lukk(name)
	request = urllib2.Request(url, headers={"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ET.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
		kanalinimi = channel.find(get_live("dGl0bGU=")).text
		kanalinimi = base64.b64decode(kanalinimi)
		kanalinimi = kanalinimi.partition("[")
		striimilink = channel.find(get_live("c3RyZWFtX3VybA==")).text
		striimilink = striimilink.replace('.ts','.'+tiposelect)
		pilt = channel.find("desc_image").text
		kava = kanalinimi[1]+kanalinimi[2]
		kava = kava.partition("]")
		kava = kava[2]
		kava = kava.partition("	")
		kava = kava[2]
		shou = get_live("W0NPTE9SIHdoaXRlXSVzIFsvQ09MT1Jd")%(kanalinimi[0])+kava
		kirjeldus = channel.find("description").text
		if kirjeldus:
			kirjeldus = base64.b64decode(kirjeldus)
			nyyd = kirjeldus.partition("(")
			nyyd = "Agora: "+nyyd[0]
			jargmine = kirjeldus.partition(")\n")
			jargmine = jargmine[2].partition("(")
			jargmine = "A seguir: "+jargmine[0]
			kokku = nyyd+jargmine
		else:
			kokku = ""
		if pilt:
			addLinkCanalLista(shou,striimilink,pilt,kokku,os.path.join(__ART_FOLDER__, __SKIN__, 'hometheater.png'))
		else:
			addLinkCanalLista(shou,striimilink,os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),kokku,os.path.join(__ART_FOLDER__, __SKIN__, 'hometheater.png'))
	
	xbmcplugin.setContent(int(sys.argv[1]) ,"episodes")
	xbmc.executebuiltin("Container.SetViewMode(55)")

def get_myaccount(name,url,image):
	vanemalukk=__ADDON__.getSetting("login_adultos_sim")
	if vanemalukk == "true":
		vanema_lukk(name)
	
	request = urllib2.Request(url, headers={"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ET.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall("channel"):
		pealkiri = channel.find("title").text
		pealkiri = base64.b64decode(pealkiri)
		pealkiri = pealkiri.encode("utf-8")
		striimilink = channel.find("stream_url").text
		pilt = channel.find("desc_image").text 
		kirjeldus = channel.find("description").text
		if kirjeldus:
			kirjeldus = base64.b64decode(kirjeldus)
		if pilt:
			addLinkCanalLista(pealkiri,striimilink,pilt,kirjeldus,os.path.join(__ART_FOLDER__, __SKIN__, 'theater.png'))
		else:
			addLinkCanalLista(pealkiri,striimilink,os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),kirjeldus,os.path.join(__ART_FOLDER__, __SKIN__, 'theater.png'))
	
	xbmcplugin.setContent( int(sys.argv[1]) ,"movies" )
	xbmc.executebuiltin('Container.SetViewMode(55)')

def addLinkCanalLista(title,url,thumbnail,plot,fanart, isPlayable=True, folder=False):
	ok=True
	
	listitem=xbmcgui.ListItem(title,iconImage=thumbnail,thumbnailImage=thumbnail)
	info_labels={"Title":title,"FileName":title,"Plot":plot}
	listitem.setInfo( "video", info_labels )
	if fanart!="": 
		listitem.setProperty('fanart_image',fanart)
		xbmcplugin.setPluginFanart(int(sys.argv[1]),fanart)
	if url.startswith("plugin://"): 
		itemurl=url
		listitem.setProperty('IsPlayable','true')
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=itemurl,listitem=listitem,isFolder=folder)
	elif isPlayable: 
		listitem.setProperty("Video","true")
	
	u = sys.argv[0] + "?url=" + str(url) + "&mode=3340&name=" + str(name) + "&iconimage="+str(iconimage)+"&fanart="+str(fanart)+"&plot="+str(plot)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=listitem,isFolder=folder)
	return ok

def run_cronjob(title,url,image,plot,fanart):
	vanemalukk=__ADDON__.getSetting("login_adultos_sim")
	if vanemalukk == "true":
		vanema_lukk(name)
	
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	
	info_labels={"Title":title,"FileName":title,"Plot":plot}
	listitem=xbmcgui.ListItem(title,iconImage=image,thumbnailImage=image)
	listitem.setInfo( "video", info_labels )
	playlist.add(url=url, listitem=listitem, index=1)
	xbmc.Player().play(playlist)

def sync_data(channel):
	video = base64.b64decode(channel)
	return video

def restart_service(params):
	vanemalukk=__ADDON__.getSetting("login_adultos_sim")
	if vanemalukk == "true":
		pealkiri = params.get(sync_data("dGl0bGU="))
		vanema_lukk(pealkiri)
	lopplink = params.get(vod_channels("dXJs"))
	
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def grab_epg(url):
	req = urllib2.Request(url)
	req.add_header(sync_data("VXNlci1BZ2VudA==") , vod_channels("S29kaSBwbHVnaW4gYnkgTGl2ZSF0"))
	response = urllib2.urlopen(req)
	link=response.read()
	jdata = json.loads(link.decode('utf8'))
	response.close()
	if jdata:
		return jdata
def kontroll(url):
	randomstring = grab_epg(url)
	kasutajainfo = randomstring[sync_data("dXNlcl9pbmZv")]
	kontroll = kasutajainfo[get_live("YXV0aA==")]
	return kontroll
def get_live(channel):
	video = base64.b64decode(channel)
	return video
def execute_ainfo(url):
	andmed = grab_epg(url)
	kasutajaAndmed = andmed[sync_data("dXNlcl9pbmZv")]
	seis = kasutajaAndmed[get_live("c3RhdHVz")]
	aegub = kasutajaAndmed[sync_data("ZXhwX2RhdGU=")]
	if aegub:
		aegub = datetime.datetime.fromtimestamp(int(aegub)).strftime('%H:%M %d.%m.%Y')
	else:
		aegub = vod_channels("TmV2ZXI=") 
	rabbits = kasutajaAndmed[vod_channels("aXNfdHJpYWw=")]
	if rabbits == "0":
		rabbits = sync_data("Tm8=")
	else:
		rabbits = sync_data("WWVz")
	leavemealone = kasutajaAndmed[get_live("bWF4X2Nvbm5lY3Rpb25z")]
	polarbears = kasutajaAndmed[sync_data("dXNlcm5hbWU=")]
	
	addLinkCanalLista("[COLOR = white]Utilizador: [/COLOR]"+polarbears,"",os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'theater.png'))
	
	addLinkCanalLista("[COLOR = white]Estado: [/COLOR]"+seis,"",os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'theater.png'))
	
	addLinkCanalLista("[COLOR = white]Expira: [/COLOR]"+aegub,"",os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'theater.png'))
	
	addLinkCanalLista("[COLOR = white]Conta de Teste: [/COLOR]"+rabbits,"",os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'theater.png'))
	
	addLinkCanalLista("[COLOR = white]Maximo de Connec: [/COLOR]"+leavemealone,"",os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'icon.png'),os.path.join(__ART_FOLDER__, __SKIN__, 'theater.png'))
	
	vista_Canais_Lista()

def vanema_lukk(name):
	a = 'XXX', 'Adult', 'Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx'
	if any(s in name for s in a):
		xbmc.executebuiltin((u'XBMC.Notification("Controlo Parental", "O canal contem conteudo adulto", 2000)'))
		text = plugintools.keyboard_input(default_text="", title="Codigo para controlo parental")
		if text==plugintools.get_setting(sync_data("bG9naW5fYWR1bHRvcw==")):
		  return
		else:
		  exit()
	else:
		name = ""

def DownloaderClass(url,dest):
	dp = xbmcgui.DialogProgress()
	dp.create(sync_data("R2V0dGluZyB1cGRhdGU="),get_live("RG93bmxvYWRpbmc="))
	urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
	try:
		percent = min((numblocks*blocksize*100)/filesize, 100)
		__ALERTA__(AddonTitle, ''+percent)
		dp.update(percent)
	except:
		percent = 100
		dp.update(percent)
	if dp.iscanceled():
		__ALERTA__(AddonTitle, 'O download foi cancelado.')
		dp.close()

def vod_channels(channel):
	video = base64.b64decode(channel)
	return video



def PlayUrl(name, url, iconimage=None):
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

###############################################################################################################
#													Listar Grupos											 #
###############################################################################################################
def listar_grupos_adultos(url,senha,estilo,tipo,tipo_user,servidor_user,fanart):
	passa = True
	if tipo_user == 'Teste':
		if servidor_user == "Teste":
			passa = False
			__ALERTA__(AddonTitle, 'Não tem acesso a este menu. Faça a sua doação.')
		else:
			if servidor_user == 'Teste':
				passa = False
				__ALERTA__(AddonTitle, 'Não tem acesso a este menu. Faça a sua doação.')	
	if passa:
		if(__ADDON__.getSetting("login_adultos") == ''):
			__ALERTA__(AddonTitle, 'Preencha o campo senha para adultos.')
		elif(__ADDON__.getSetting("login_adultos") != senha):
			__ALERTA__(AddonTitle, 'Senha para adultos incorrecta. Verifique e tente de novo.')
		else:
			listar_grupos('',url,estilo,tipo,tipo_user,servidor_user,fanart)

def listar_grupos(nome_nov,url,estilo,tipo,tipo_user,servidor_user,fanart):
	if url != 'url':
		page_with_xml = urllib2.urlopen(url).readlines()
		for line in page_with_xml:
			objecto = line.decode('latin-1').encode("utf-8")
			params = objecto.split(',')
			try:
				nomee = params[0]
				imag = params[1]
				urlll = params[2]
				estil = params[3]
				urlllserv1 = params[4]
				urlllserv2 = params[5]
				urlllserv3 = params[6]
				urlllserv4 = params[7]
				urlllserv5 = params[8]
				urlllserv6 = params[9]
				urlllserv7 = params[10]
				urlllserv8 = params[10]
				paramss = estil.split('\n')
				if tipo_user == 'Administrador' or tipo_user == 'Pagante' or tipo_user == 'PatrocinadorPagante' or tipo_user == 'Desporto':
					if nome_nov == 'TVs-Free':
						addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
					elif servidor_user == 'Servidor1':
						addDir(nomee,urlllserv1,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
					elif servidor_user == 'Servidor2':
						addDir(nomee,urlllserv2,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
					elif servidor_user == 'Servidor3':
						addDir(nomee,urlllserv3,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
					elif servidor_user == 'Servidor4':
						addDir(nomee,urlllserv4,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
					elif servidor_user == 'Servidor5':
						addDir(nomee,urlllserv5,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
					elif servidor_user == 'Servidor6':
						addDir(nomee,urlllserv6,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
					elif servidor_user == 'Servidor7':
						addDir(nomee,urlllserv7,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
					else:
						addDir(nomee,urlllserv8,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
				elif tipo_user == 'Patrocinador':
					if nome_nov == 'TVs-Free':
						addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
				else:
					if tipo_user == 'Teste':
						if servidor_user == "Teste":
							addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
						else:
							if servidor_user != '':
								if servidor_user == 'Servidor1':
									addDir(nomee,urlllserv1,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
								elif servidor_user == 'Servidor2':
									addDir(nomee,urlllserv2,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
								elif servidor_user == 'Servidor3':
									addDir(nomee,urlllserv3,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
								elif servidor_user == 'Servidor4':
									addDir(nomee,urlllserv4,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
								elif servidor_user == 'Servidor5':
									addDir(nomee,urlllserv5,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
								elif servidor_user == 'Servidor6':
									addDir(nomee,urlllserv6,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
								elif servidor_user == 'Servidor7':
									addDir(nomee,urlllserv7,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
								else:
									addDir(nomee,urlllserv8,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
							else:
								addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'',fanart)
					else:
						addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,nome_nov,fanart)
			except:
				pass
	
	if tipo == 'patrocinadores' or tipo == 'novidades' or tipo == 'Praia' or tipo == 'pesquisa' or tipo == 'estado' or tipo == 'ProgramasTV' or nome_nov == 'Eventos Diários':
		estiloSelect = returnestilo(estilo)
		xbmc.executebuiltin(estiloSelect)
	else:
		if tipo == 'Filme' or tipo == 'Serie':
			vista_filmesSeries()
		else:
			vista_Canais()	
	xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)

###############################################################################################################
#													Menu TV Arquivo											 #
###############################################################################################################

def listatvarchive(url):
	endereco = url+"/panel_api.php?username="+__ADDON__.getSetting('login_name')+"&password="+__ADDON__.getSetting('login_password')+"&action=get_live_streams"
	iIiIIIi = urllib2.urlopen(endereco)
	ooo00OOOooO	= json.load(iIiIIIi)
	O00OOOoOoo0O = ooo00OOOooO['available_channels']
	for	O000OOo00oo	in	O00OOOoOoo0O.values():
		oo0OOo = O000OOo00oo['tv_archive']
		if(oo0OOo == 1):
			nametv=O000OOo00oo['name']
			stream_id=O000OOo00oo['stream_id']
			logo_tv=O000OOo00oo['stream_icon']
			duration = O000OOo00oo['tv_archive_duration']
			
			addLinkGrupo(nametv,logo_tv,stream_id,url,duration,os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'),1)

def listatvarchivecanais(name,stream_id,url,duration,iconimage,fanart):
	endereco = url+"/panel_api.php?username="+__ADDON__.getSetting('login_name')+"&password="+__ADDON__.getSetting('login_password')+"&action=get_epg&stream_id="+stream_id
	iIiIIIi	=	urllib2	.urlopen(endereco)
	iiiI11	=	json.load(iIiIIIi)
	iiIiI	=	datetime.datetime.utcnow() - datetime.timedelta(days=int(duration))
	o00oooO0Oo	=calendar.timegm(iiIiI.timetuple())
	o00oooO0Oo	=int(o00oooO0Oo)
	o0O0OOO0Ooo	=time.time()
	o0O0OOO0Ooo	=int(o0O0OOO0Ooo)
	
	for	iiIiII1	in	iiiI11	:
		title_tv = iiIiII1['title']
		title_tv=base64.b64decode(title_tv)
		start	= int(iiIiII1['start'])
		end	= int(iiIiII1['end'])
		segundo = 0.0166666667
		
		duracao = int((end-start)*segundo)
		
		if(start > o00oooO0Oo and start < o0O0OOO0Ooo):
			if 90 - 90:	Ooo0	%	Oo0ooO0oo0oO	/	Oo0oO0ooo
			IIi = datetime.datetime.fromtimestamp(int(start)).strftime('%d.%m %H:%M')
			i1Iii1i1I = datetime.datetime.fromtimestamp(int(start)).strftime('%Y-%m-%d:%H:%M')
			title_tv = IIi + " " + title_tv
			endereco = url+"/streaming/timeshift.php?username="+__ADDON__.getSetting('login_name')+"&password="+__ADDON__.getSetting('login_password')+"&stream="+stream_id+"&start="+i1Iii1i1I+"&duration="+str(duracao)
			
			addLinkCanal(title_tv,endereco,iconimage,'0001','')

def addLinkGrupo(title,thumbnail,stream_id,url,duration,fanart,type):
	ok=True
	
	listitem=xbmcgui.ListItem(title,iconImage=thumbnail,thumbnailImage=thumbnail)
	info_labels={"Title":title,"FileName":title}
	listitem.setInfo( "video", info_labels )
	listitem.setProperty('fanart_image',fanart)
	xbmcplugin.setPluginFanart(int(sys.argv[1]),fanart)
	
	u = sys.argv[0] + "?url=" + str(url) + "&mode=26&name=" + str(title) + "&iconimage="+str(thumbnail)+"&fanart="+str(fanart)+"&stream_id="+str(stream_id)+"&duration="+duration
	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=listitem,isFolder=True)
	
	return ok

###############################################################################################################
#													Listar Canais											 #
###############################################################################################################
def listar_canais_url(nome,url,estilo,tipo,tipo_user,servidor_user,fanart,tippoo,adultos=False):
	if url != 'nada':
		page_with_xml = urllib2.urlopen(url).readlines()
		passaepg = True
		if tippoo == 'Desporto' or tippoo == 'Crianca' or tippoo == 'Canal' or tippoo == 'Documentario' or tippoo == 'Musica' or tippoo == 'Filme' or tippoo == 'Noticia' or tippoo == 'TVs':
			if(__EPG__ != ''):
				urlqqq = urllib.urlopen(__EPG__)
				codigo = urlqqq.read()
				urlqqq.close
			else:
				passaepg = False
	
		ts = time.time()
		st = int(datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S'))
		if tipo == 'Filme' or tipo == 'Serie':
			refres = '**'
		else:
			refres = ','
		for line in page_with_xml:
			total = len(line)
			objecto = line.decode('latin-1').encode("utf-8")
			params = objecto.split(refres)	
			try:
				nomee = params[0]
				rtmp = params[2].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').replace('utilizadorliveit',__ADDON__.getSetting("login_name")).replace('senhaliveit',__ADDON__.getSetting("login_password"))
				img = params[1].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http')
				grup = params[3]
				id_it = params[4].rstrip()
				id_p = params[5]
				srt_f = ''
				descri = ''
				_fanart = ''
				
				pesqyo = rtmp.split('https://www.youtube.com/watch?v=')
				total2 = len(pesqyo)
				if total2 > 1:
					rtmp = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+pesqyo[1]
				
				if grup == nome:
					programa = ''
					if tippoo == 'Desporto' or tippoo == 'Crianca' or tippoo == 'Canal' or tippoo == 'Documentario' or tippoo == 'Musica' or tippoo == 'Filme' or tippoo == 'Noticia' or tippoo == 'TVs':
						if id_it != '':
							if passaepg:
								twrv = ThreadWithReturnValue(target=getProgramacaoDiaria, args=(id_it, st,codigo))
								twrv.start()
								programa = twrv.join()
					
					if programa != '':
						nomewp = nomee + " | "+ programa
					else:
						nomewp = nomee
					
					if	tipo == 'Filme' or tipo == 'Serie':
						srt_f = params[6]
						ano = params[7]
						realizador = 'Director: '+params[8]
						descri = params[9]
						detalhes1 = grup
						argumento = AddonTitle
						plot = 'Enredo: '+descri
						detalhes2 = ano
						imdb = '4510398'
						votes = '5 estrelas'
						infoLabels = {'title':nomewp, 'plot':plot, 'writer': argumento, 'director':realizador, 'genre':detalhes1, 'year': detalhes2, 'aired':detalhes2, 'IMDBNumber':imdb, 'votes':votes, "credits": nomewp}
					else:
						infoLabels = {"title": nomewp, "genre": tipo, "credits": nomewp}
					
					
					addLink(nomewp,rtmp,img,id_it,srt_f,descri,tipo,tipo_user,id_p,infoLabels,fanart,tippoo,adultos,total)				
			except:
				pass
		
		#__ALERTA__(AddonTitle, 'Tipo: '+tipo)
		if tipo == 'patrocinadores' or tipo == 'novidades' or tipo == 'Praia' or tipo == 'pesquisa' or tipo == 'estado' or tipo == 'ProgramasTV' or nome == 'Eventos Diários':
			estiloSelect = returnestilo(estilo)
			xbmc.executebuiltin(estiloSelect)
		else:
			if tipo == 'Filme' or tipo == 'Serie':
				vista_filmesSeries()
			else:
				vista_Canais()
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)

###############################################################################################################
#													EPG													 #
###############################################################################################################
def obter_ficheiro_epg():
	if not xbmcvfs.exists(__FOLDER_EPG__):
		xbmcvfs.mkdirs(__FOLDER_EPG__)

	uncompressed_path = os.path.join(__FOLDER_EPG__, 'epg.xml')
	url = urllib.urlopen(__EPG__)
	codigo = url.read()
	url.close
	
	open(uncompressed_path, 'w').write(codigo)

def getProgramacaoDiaria(idCanal, diahora, codigo):
	source = re.compile('<programme start="(.+?) \+0100" stop="(.+?) \+0100" channel="'+idCanal+'">\s+<title lang="pt">(.+?)<\/title>').findall(codigo)

	programa = ''

	for start, stop, programa1  in source:

		if(int(start) < diahora and int(stop) > diahora):
			programa = programa1
	return programa


def programacao_canal(idCanal):
	url = urllib.urlopen(__EPG__)
	codigo = url.read()
	url.close
	
	ts = time.time()
	st = int(datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d'))

	diahora = int(str(st)+'060000')
	diaamanha = int(str(st+1)+'060000')

	source = re.compile('<programme start="(.+?) \+0100" stop="(.+?) \+0100" channel="'+idCanal+'">\s+<title lang="pt">(.+?)<\/title>').findall(codigo)

	programa = ''

	titles=['[B][COLOR white]Programação:[/COLOR][/B]']

	
	for start, stop, programa1 in source:

		start1 = re.compile('([0-9]{4}[0-1][0-9][0-3][0-9])([0-9]{2})([0-9]{2})([0-9]{2})').findall(start)
		stop1 = re.compile('([0-9]{4}[0-1][0-9][0-3][0-9])([0-9]{2})([0-9]{2})([0-9]{2})').findall(stop)

		if(int(start) > diahora and int(start) < diaamanha ):
			titles.append('\n[B]%s:%s -> %s:%s[/B] - %s' % (start1[0][1], start1[0][2], stop1[0][1], stop1[0][2], programa1))


	programacao = '\n'.join(titles)
	try:
		xbmc.executebuiltin("ActivateWindow(10147)")
		window = xbmcgui.Window(10147)
		xbmc.sleep(100)
		window.getControl(1).setLabel(AddonTitle)
		window.getControl(5).setText(programacao)
	except:
		pass


####################### THREADS ######################

from threading import Thread

class ThreadWithReturnValue(Thread):
	def __init__(self, group=None, target=None, name=None,
				 args=(), kwargs={}, Verbose=None):
		Thread.__init__(self, group, target, name, args, kwargs, Verbose)
		self._return = None
	def run(self):
		if self._Thread__target is not None:
			self._return = self._Thread__target(*self._Thread__args,
												**self._Thread__kwargs)
	def join(self):
		Thread.join(self)
		return self._return

############################################################################################################
#												Addon Filmes e Series									  #
############################################################################################################

def listamenusseries(nome_nov,url,estilo,tipo,tipo_user,servidor_user,iconimage,fanart):
	check_login = login2()
	if check_login == True:
		menuSeries(os.path.join(__ART_FOLDER__, __SKIN__, 'series.png'),__SITEAddon__+'Imagens/series_fanart.png')
	else:
		__ALERTA__(AddonTitle, 'Erro a fazer login nesta parte. Tente novamente mais tarde.')

def listamenusfilmes(nome_nov,url,estilo,tipo,tipo_user,servidor_user,iconimage,fanart):
	check_login = login2()
	if check_login == True:
		database = Database.isExists()
		if tipo_user != 'Teste':
			filmilink = url+'enigma2.php?username='+__ADDON__.getSetting("login_name")+'&password='+__ADDON__.getSetting("login_password")+'&type=get_vod_categories'
			addDir('Filmes da Lista',filmilink,None,3337,'Miniatura',os.path.join(__ART_FOLDER__, __SKIN__, 'filmes.png'),'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
		menuFilmes(os.path.join(__ART_FOLDER__, __SKIN__, 'filmes.png'),__SITEAddon__+'Imagens/filmes_fanart.png')
	else:
		__ALERTA__(AddonTitle, 'Erro a fazer login nesta parte. Tente novamente mais tarde.')

def listamenusanimes(nome_nov,url,estilo,tipo,tipo_user,servidor_user,iconimage,fanart):
	check_login = login2()
	if check_login == True:
		menuAnimes(os.path.join(__ART_FOLDER__, __SKIN__, 'animes.png'),__SITEAddon__+'Imagens/series_fanart.png')
	else:
		__ALERTA__(AddonTitle, 'Erro a fazer login nesta parte. Tente novamente mais tarde.')

def menuFilmes(iconimage,fanart):
	evento = getEventos()
	if evento:
		addDir2('[B]'+evento+'[/B]', __API_SITE__+'evento/1', 111, 'filmes', iconimage, 1, None, None, fanart)
		addDir2(' ', '', 0, '', os.path.join(__ART_FOLDER__, __SKIN__, 'nada.png'), 1, None, None, fanart)
	addDir2('Todos os Filmes', __API_SITE__+'filmes', 111, 'filmes', iconimage, 1, None, None, fanart)
	addDir2('Filmes em Destaque',  __API_SITE__+'filmes/destaque', 111, 'filmes', iconimage, 1, None, None, fanart)
	addDir2('Filmes por Ano', __API_SITE__+'filmes/ano', 119, 'listagemAnos', os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'), 1, None, None, fanart)
	addDir2('Filmes por Genero', __API_SITE__+'filmes/categoria', 118, 'listagemGeneros', os.path.join(__ART_FOLDER__, __SKIN__, 'genero.png'), 1, None, None, fanart)

	vista_menu()

def menuSeries(iconimage,fanart):
	database = Database.isExists()
	addDir2('Todas as Series', __API_SITE__+'series', 123, 'series', iconimage, 1, None, None, fanart)
	addDir2('Series em Destaque',  __API_SITE__+'series/destaque', 123, 'series', iconimage, 1, None, None, fanart)
	addDir2('Series por Ano', __API_SITE__+'series/ano', 119, 'listagemAnos', os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'), 1, None, None, fanart)
	addDir2('Series por Genero', __API_SITE__+'series/categoria', 118, 'listagemGeneros', os.path.join(__ART_FOLDER__, __SKIN__, 'genero.png'), 1, None, None, fanart)

	vista_menu()

def menuAnimes(iconimage,fanart):
	database = Database.isExists()
	addDir2('Todos os Animes', __API_SITE__+'animes', 123, 'animes', iconimage, 1, None, None, fanart)
	addDir2('Animes em Destaque',  __API_SITE__+'animes/destaque', 123, 'animes', iconimage, 1, None, None, fanart)
	addDir2('Animes por Ano', __API_SITE__+'animes/ano', 119, 'listagemAnos', os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'), 1, None, None, fanart)
	addDir2('Animes por Genero', __API_SITE__+'animes/categoria', 118, 'listagemGeneros', os.path.join(__ART_FOLDER__, __SKIN__, 'genero.png'), 1, None, None, fanart)

	vista_menu()

def removerAcentos(txt, encoding='utf-8'):
	return normalize('NFKD', txt.decode(encoding)).encode('ASCII','ignore')

def filmes(url, pagina):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultado = abrir_url(url, header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	resultado = json.loads(resultado)
	for i in resultado['data']:
		categoria = i['categoria1']
		if i['categoria2'] != '':
			categoria += ','+i['categoria2']
		if i['categoria3'] != '':
			categoria += ','+i['categoria3']
		visto = False
		pt = ''
		cor = "white"
		br = ''
		if 'Brasileiro' in categoria:
			br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
		if 'Portu' in categoria:
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		if 'PT' in i['IMBD']:
			i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		if i['visto'] == 1:
			visto = True

		infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'IMDBNumber': i['IMBD'] }
		
		try:
			nome = i['nome_ingles'].decode('utf-8')
		except:
			nome = i['nome_ingles'].encode('utf-8')
		if 'http' not in i['foto']:
			i['foto'] = __API__+'images/capas/'+i['foto'].split('/')[-1]
			#i['foto'] = i['foto'].replace('PT','')
		
		nomeee = '[COLOR '+cor+']'+pt+br+removerAcentos(nome)+' ('+i['ano']+')[/COLOR]'
		urlnoo = __API_SITE__+'filme/'+str(i['id_video'])
		fotooo = i['foto']
		#i['background'] = i['background'].replace('PT','')
		i['background'] = 'images/background/'+i['IMBD']+'.jpg'
		fanarttt = __API__+i['background']
		addVideo(nomeee, urlnoo, 113, fotooo,visto, 'filme', 0, 0, infoLabels, fanarttt, trailer=i['trailer'])
		
	current = resultado['meta']['pagination']['current_page']
	total = resultado['meta']['pagination']['total_pages']
	try: proximo = resultado['meta']['pagination']['links']['next']
	except: pass 
	if current < total:
		addDir2('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 111, 'filmes', os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'),1)
	vista_filmesSeries()

def series(url):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultado = abrir_url(url, header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	resultado = json.loads(resultado)
	if 'serie' in url:
		tipo = 'serie'
	elif 'anime' in url:
		tipo = 'anime'
	for i in resultado['data']:
		categoria = i['categoria1']
		if i['categoria2'] != '':
			categoria += ','+i['categoria2']
		if i['categoria3'] != '':
			categoria += ','+i['categoria3']
		br = ''
		pt = ''
		if 'Brasileiro' in categoria:
			br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
		if 'Portu' in categoria:
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		if 'PT' in i['IMBD']:
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'Code': i['IMBD'] }
	
		try:
			nome = i['nome_ingles'].decode('utf-8')
		except:
			nome = i['nome_ingles'].encode('utf-8')
		if 'http' not in i['foto']:
			i['foto'] = __API__+'images/capas/'+i['foto'].split('/')[-1]
			#i['foto'] = i['foto'].replace('PT','')
		if i['visto'] == 1:
			visto=True
		else:
			visto=False
		
		
		nomeee = pt+br+removerAcentos(nome)+' ('+i['ano']+')'
		fotooo = i['foto']
		#i['background'] = i['background'].replace('PT','')
		i['background'] = 'images/background/'+i['IMBD']+'.jpg'
		fanarttt = __API__+i['background']
		addDir2(nomeee, __API_SITE__+tipo+'/'+str(i['id_video']), 114, 'temporadas', fotooo, tipo='serie', infoLabels=infoLabels,poster=fanarttt,visto=visto)
	
	current = resultado['meta']['pagination']['current_page']
	total = resultado['meta']['pagination']['total_pages']
	try: proximo = resultado['meta']['pagination']['links']['next']
	except: pass 
	if current < total:
		addDir2('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 123, 'series', os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'))
	
	vista_filmesSeries()

def getSeasons(url):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultado = abrir_url(url, header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	resultado = json.loads(resultado)
	j=1
	while j <= resultado['temporadas']:
		addDir2("[B]Temporada[/B] "+str(j), url+'/temporada/'+str(j), 115, 'episodios', os.path.join(__ART_FOLDER__, __SKIN__,'temporadas', 'temporada'+str(j)+'.png'),poster=__API__+resultado['background'])
		j+=1
	
	vista_temporadas()

def getEpisodes(url):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultado = abrir_url(url, header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	resultado = json.loads(resultado)
	if 'serie' in url:
		tipo = 'serie'
	elif 'anime' in url:
		tipo = 'anime'
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultadoS = abrir_url(__API_SITE__+tipo+'/'+url.split('/')[5], header=headers)
	resultadoS = json.loads(resultadoS)
	for i in resultado['data']:
		if i['URL'] == '' and i['URL2'] == '':
			continue
		pt = ''
		categoria = resultadoS['categoria1']
		if resultadoS['categoria2'] != '':
			categoria += ','+resultadoS['categoria2']
		if resultadoS['categoria3'] != '':
			categoria += ','+resultadoS['categoria3']
		infoLabels = {'Title': i['nome_episodio'], 'Code': i['IMBD'], 'Episode': i['episodio'], 'Season': i['temporada'] }
		try:
			nome = i['nome_episodio'].decode('utf-8')
		except:
			nome = i['nome_episodio'].encode('utf-8')
		br = ''
		final = ''
		semLegenda = ''
		if i['fimtemporada'] == 1:
			final = '[B]Final da Temporada [/B]'
		if i['semlegenda'] == 1:
			semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
		if 'Brasileiro' in categoria:
			br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
		if 'Portu' in categoria:
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		if 'PT' in i['IMBD']:
			i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		visto = False
		cor = 'white'
		if i['visto'] == 1:
			visto = True	
		
		imagem = ''
		if i['imagem'] == 1:
			imagem = __API__+'images/series/'+i['IMBD']+'.jpg'
		elif i['imagem'] == 0:
			imagem = __API__+'images/capas/'+i['imdbSerie']+'.jpg'
		
		#imagem = imagem.replace('PT','')
		#i['background'] = i['background'].replace('PT','')
		i['background'] = 'images/background/'+i['IMBD']+'.jpg'
		fanarttt = __API__+i['background']
		
		nomeee = pt+br+final+semLegenda+'[COLOR '+cor+'][B]Episodio '+str(i['episodio'])+'[/B][/COLOR] '+removerAcentos(nome)
		
		addVideo(nomeee, __API_SITE__+tipo+'/'+str(i['id_serie'])+'/episodio/'+str(i['id_episodio']), 113, imagem, visto, 'episodio', i['temporada'], i['episodio'], infoLabels, fanarttt)
	
	vista_episodios()

def getGeneros(url):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultado = abrir_url(__API_SITE__+'categorias', header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	resultado = json.loads(resultado)

	for i in resultado:
		if i['id_categoria'] == 0:
			continue
		if 'filme' not in url and i['tipo'] == 1:
			continue
		addDir2(i['categorias'], url+'/'+str(i['id_categoria']), 122, 'categorias', os.path.join(__ART_FOLDER__, __SKIN__, 'genero.png'))
	
	vista_menu()

def categorias(url):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultado = abrir_url(url, header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	resultadoa = json.loads(resultado)
	
	for i in resultadoa["data"]:
		if 'filme' in url:
			resultado = abrir_url(__API_SITE__+'filme/'+str(i['id_video']), header=headers)
			resultado = json.loads(resultado)
			categoria = resultado['categoria1']
			if resultado['categoria2'] != '':
				categoria += ','+resultado['categoria2']
			if resultado['categoria3'] != '':
				categoria += ','+resultado['categoria3']
			
			try:
				nome = resultado['nome_ingles'].decode('utf-8')
			except:
				nome = resultado['nome_ingles'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = __API__+'images/capas/'+resultado['foto'].split('/')[-1]
			pt = ''
			br = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			cor = "white"
			if 'PT' in resultado['IMBD']:
				resultado['IMBD'] = re.compile('(.+?)PT').findall(resultado['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			visto = False
			
			infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot':resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['IMBD'] }
			nomeee = '[COLOR '+cor+']'+pt+br+removerAcentos(nome)+' ('+resultado['ano']+')[/COLOR]'
			urlnoo = __API_SITE__+'filme/'+str(resultado['id_video'])
			
			fotooo = resultado['foto']
			#fotooo = fotooo.replace('PT','')
			#resultado['background'] = resultado['background'].replace('PT','')
			resultado['background'] = 'images/background/'+resultado['IMBD']+'.jpg'
			fanarttt = __API__+resultado['background']
			
			addVideo(nomeee, urlnoo, 113, fotooo,visto, 'player', 0, 0, infoLabels, fanarttt, trailer=resultado['trailer'])
		elif 'serie' in url or 'anime' in url:
			cor = "white"
			if 'serie' in url:
				tipo = 'serie'
			elif 'anime' in url:
				tipo = 'anime'
			resultado = abrir_url(__API_SITE__+tipo+'/'+str(i['id_video']), header=headers)
			resultado = json.loads(resultado)
			categoria = resultado['categoria1']
			if resultado['categoria2'] != '':
				categoria += ','+resultado['categoria2']
			if resultado['categoria3'] != '':
				categoria += ','+resultado['categoria3']
			pt = ''
			br = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if 'PT' in resultado['IMBD']:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			try:
				nome = resultado['nome_ingles'].decode('utf-8')
			except:
				nome = resultado['nome_ingles'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = __API_SITE__+'images/capas/'+resultado['foto'].split('/')[-1]
			visto = False
			if resultado['visto'] == 1:
				visto=True
			
			infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['IMBD'] }
			
			fotooo = resultado['foto']
			#fotooo = fotooo.replace('PT','')
			#resultado['background'] = resultado['background'].replace('PT','')
			resultado['background'] = 'images/background/'+resultado['IMBD']+'.jpg'
			fanarttt = __API__+resultado['background']
			
			nomeee = pt+br+removerAcentos(nome)+' ('+resultado['ano']+')'
			addDir2(nomeee, __API_SITE__+tipo+'/'+str(resultado['id_video']), 114, 'temporadas', fotooo, tipo='serie', infoLabels=infoLabels,poster=fanarttt,visto=visto)
	
	current = resultadoa['meta']['pagination']['current_page']
	total = resultadoa['meta']['pagination']['total_pages']
	try: proximo = resultadoa['meta']['pagination']['links']['next']
	except: pass 
	if current < total:
		addDir2('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 121, 'anos', os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'),1)
	
	vista_filmesSeries()

def getYears(url):
	anos = [
			'2017',
			'2016',
			'2015',
			'2014',
			'2013',
			'2012',
			'2011',
			'2010',
			'2009',
			'2008',
			'2007',
			'2006',
			'2000-2005',
			'1990-1999',
			'1980-1989',
			'1970-1979',
			'1960-1969',
			'1950-1959',
			'1900-1949'
		]
	for i in anos:
		addDir2(i, url+'/'+i, 121, 'anos', os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'))
		
	vista_menu()

def anos(url):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultado = abrir_url(url, header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	resultadoa = json.loads(resultado)
	
	for i in resultadoa["data"]:
		if 'filme' in url:
			resultado = abrir_url(__API_SITE__+'filme/'+str(i['id_video']), header=headers)
			resultado = json.loads(resultado)
			categoria = resultado['categoria1']
			if resultado['categoria2'] != '':
				categoria += ','+resultado['categoria2']
			if resultado['categoria3'] != '':
				categoria += ','+resultado['categoria3']
			
			visto = False
			pt = ''
			br = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			cor = "white"
			if 'PT' in i['IMBD']:
				i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if i['visto'] == 1:
				visto = True
			
			try:
				nome = resultado['nome_ingles'].decode('utf-8')
			except:
				nome = resultado['nome_ingles'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = __API__+'images/capas/'+resultado['foto'].split('/')[-1]
	
			infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot':resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['IMBD'] }
			nomeee = '[COLOR '+cor+']'+pt+br+removerAcentos(nome)+' ('+i['ano']+')[/COLOR]'
			urlnoo = __API_SITE__+'filme/'+str(resultado['id_video'])
			
			fotooo = resultado['foto']
			fotooo = fotooo.replace('PT','')
			resultado['background'] = resultado['background'].replace('PT','')
			fanarttt = __API__+resultado['background']
			
			addVideo(nomeee, urlnoo, 113, fotooo,visto, 'player', 0, 0, infoLabels, fanarttt, trailer=resultado['trailer'])
		elif 'serie' in url or 'anime' in url:
			cor = "white"
			if 'serie' in url:
				tipo = 'serie'
			elif 'anime' in url:
				tipo = 'anime'
			resultado = abrir_url(__API_SITE__+tipo+'/'+str(i['id_video']), header=headers)
			resultado = json.loads(resultado)
			categoria = resultado['categoria1']
			if resultado['categoria2'] != '':
				categoria += ','+resultado['categoria2']
			if resultado['categoria3'] != '':
				categoria += ','+resultado['categoria3']
			pt=''
			br = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if 'PT' in resultado['IMBD']:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			try:
				nome = resultado['nome_ingles'].decode('utf-8')
			except:
				nome = resultado['nome_ingles'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = __API__+'images/capas/'+resultado['foto'].split('/')[-1]
			if resultado['visto'] == 1:
				visto=True
			else:
				visto=False
			infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['IMBD'] }
			
			fotooo = resultado['foto']
			fotooo = fotooo.replace('PT','')
			resultado['background'] = resultado['background'].replace('PT','')
			fanarttt = __API__+resultado['background']
			
			nomeee = pt+br+removerAcentos(nome)+' ('+i['ano']+')'
			addDir2(nomeee, __API_SITE__+tipo+'/'+str(resultado['id_video']), 114, 'temporadas', fotooo, tipo='serie', infoLabels=infoLabels,poster=fanarttt,visto=visto)
	
	current = resultadoa['meta']['pagination']['current_page']
	total = resultadoa['meta']['pagination']['total_pages']
	try: proximo = resultadoa['meta']['pagination']['links']['next']
	except: pass 
	if current < total:
		addDir2('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 121, 'anos', os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'),1)
	
	vista_filmesSeries()

def getEventos():
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	
	resultado = abrir_url(__API_SITE__+'eventos', header=headers)
	resultado = json.loads(resultado)
	try:
		if resultado['codigo'] == 204:
			return False
	except:
		pass
	return resultado['data']['nome']
		
		
def player(name,url,iconimage,temporada,episodio,serieNome):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	resultado = abrir_url(url, header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	
	resultado = json.loads(resultado)
	infolabels = dict()
	coiso = ''
	pastaData = ''
	if 'filme' in url:
		infolabels['Code'] = resultado['IMBD']
		infolabels['Year'] = resultado['ano']
		idVideo = resultado['id_video']
		nome = resultado['nome_ingles']
		temporada = 0
		episodio = 0
		coiso = 'filme'
	else:
		idVideo = resultado['id_serie']
		nome = resultado['nome_episodio']
		temporada = resultado['temporada']
		episodio = resultado['episodio']
		coiso = 'outro'

	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create(AddonTitle, u'Abrir emissão','Por favor aguarde...')
	mensagemprogresso.update(25, "", u'Obter video e legenda', "")

	stream, legenda, ext_g = getStreamLegenda(resultado, coiso=coiso)

	mensagemprogresso.update(50, "", u'Prepara-te, vai começar!', "")

	playlist = xbmc.PlayList(1)
	playlist.clear()
	listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)

	listitem.setInfo(type="Video", infoLabels=infolabels)
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	
	listitem.setPath(path=stream)
	playlist.add(stream, listitem)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	mensagemprogresso.update(75, "", u'Boa Sessão!!!', "")

	if stream == False:
		__ALERTA__(AddonTitle, 'O servidor escolhido não disponível, escolha outro ou tente novamente mais tarde.')
	else:
		#__ALERTA__(AddonTitle, 'Stream: '+stream)
		player_mr = Player.Player(url=url, idFilme=idVideo, pastaData=__PASTA_DADOS__, temporada=temporada, episodio=episodio, nome=name, logo=os.path.join(__ADDON_FOLDER__,'icon.png'))
		
		mensagemprogresso.close()
		player_mr.play(playlist)
		player_mr.setSubtitles(legenda)

		while player_mr.playing:
			xbmc.sleep(5000)
			#player_mr.trackerTempo()

def getStreamLegenda(resultado, coiso=None):
	i = 0
	servidores = []
	titulos = []
	nome = ''
	if resultado['URL'] != '':
		i+=1
		servidores.append(resultado['URL'])
		if 'openload' in resultado['URL']:
			nome = "OpenLoad"
		elif 'vidzi' in resultado['URL']:
			nome = 'Vidzi'
		elif 'google' in resultado['URL'] or 'cloud.mail.ru' in resultado['URL']:
			nome = AddonTitle
		elif 'uptostream.com' in resultado['URL']:
			nome = 'UpToStream'
		elif 'rapidvideo.com' in resultado['URL'] or 'raptu' in resultado['URL']:
			nome = 'RapidVideo'
		titulos.append('Servidor #%s: %s' % (i, nome))
	if resultado['URL2'] != '':
		i+=1
		servidores.append(resultado['URL2'])
		if 'openload' in resultado['URL2']:
			nome = "OpenLoad"
		elif 'vidzi' in resultado['URL2']:
			nome = 'Vidzi'
		elif 'google' in resultado['URL2'] or 'cloud.mail.ru' in resultado['URL2']:
			nome = AddonTitle
		elif 'uptostream.com' in resultado['URL2']:
			nome = 'UpToStream'
		elif 'rapidvideo.com' in resultado['URL2'] or 'raptu' in resultado['URL2']:
			nome = 'RapidVideo'
		titulos.append('Servidor #%s: %s' % (i, nome))
	try:
		if resultado['URL3'] != '':
			i+=1
			servidores.append(resultado['URL3'])
			if 'openload' in resultado['URL3']:
				nome = "OpenLoad"
			elif 'vidzi' in resultado['URL3']:
				nome = 'Vidzi'
			elif 'google' in resultado['URL3'] or 'cloud.mail.ru' in resultado['URL3']:
				nome = AddonTitle
			elif 'uptostream.com' in resultado['URL3']:
				nome = 'UpToStream'
			elif 'rapidvideo.com' in resultado['URL3'] or 'raptu' in resultado['URL3']:
				nome = 'RapidVideo'
			titulos.append('Servidor #%s: %s' % (i, nome))
	except:
		pass
	try:
		if resultado['URL4'] != '':
			i+=1
			servidores.append(resultado['URL4'])
			if 'openload' in resultado['URL4']:
				nome = "OpenLoad"
			elif 'vidzi' in resultado['URL4']:
				nome = 'Vidzi'
			elif 'google' in resultado['URL4'] or 'cloud.mail.ru' in resultado['URL4']:
				nome = AddonTitle
			elif 'uptostream.com' in resultado['URL4']:
				nome = 'UpToStream'
			elif 'rapidvideo.com' in resultado['URL4'] or 'raptu' in resultado['URL4']:
				nome = 'RapidVideo'
			titulos.append('Servidor #%s: %s' % (i, nome))
	except:
		pass
	legenda = ''
	stream = ''
	if '://' in resultado['legenda'] or resultado['legenda'] == '':
		legenda = __API__+'subs/%s.srt' % resultado['IMBD']
	elif resultado['legenda'] != '':
		if not '.srt' in resultado['legenda']:
			resultado['legenda'] = resultado['legenda']+'.srt'
		legenda = __API__+'subs/%s' % resultado['legenda']
	try:
		if resultado['semlegenda'] == 1:
			legenda = ''
	except:
		pass
	ext_g = 'coiso'
	legendaAux = legenda
	servidor = 0
	if len(titulos) > 1:
		servidor = xbmcgui.Dialog().select('Escolha o servidor', titulos)
	else:
		servidor = 0
	
	if 'vidzi' in servidores[servidor]:
		vidzi = URLResolverMedia.Vidzi(servidores[servidor])
		stream = vidzi.getMediaUrl()
		legenda = vidzi.getSubtitle()
	elif 'uptostream.com' in servidores[servidor]:
		stream = URLResolverMedia.UpToStream(servidores[servidor]).getMediaUrl()
	elif 'server.mrpiracy.win' in servidores[servidor]:
		stream = servidores[servidor]
	elif 'openload' in servidores[servidor]:
		stream = URLResolverMedia.OpenLoad(servidores[servidor]).getMediaUrl()
		legenda = URLResolverMedia.OpenLoad(servidores[servidor]).getSubtitle()
		if not '.vtt' in legenda:
			legenda = legendaAux
	elif 'drive.google.com/' in servidores[servidor]:
		stream, ext_g = URLResolverMedia.GoogleVideo(servidores[servidor]).getMediaUrl()
	elif 'cloud.mail.ru' in servidores[servidor]:
		stream, ext_g = URLResolverMedia.CloudMailRu(servidores[servidor]).getMediaUrl()
	elif 'rapidvideo.com' in servidores[servidor] or 'raptu' in servidores[servidor]:
		rapid = URLResolverMedia.RapidVideo(servidores[servidor])
		stream = rapid.getMediaUrl()
		legenda = rapid.getLegenda()
	
	if coiso == 'filme':
		legenda = legendaAux
		if resultado['IMBD'] not in legenda:
			legenda = self.API+'subs/%s.srt' % resultado['IMBD']
		if legenda == '':
			legenda = legendaAux
	return stream, legenda, ext_g


def pesquisa(url,servuss):
	codigo_fonte = ''
	dados = ''
	net = Net()
	net.set_cookies(__COOKIE_FILE__)
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	tabela = ''
	strPesquisa = ''
	ficheiro = ''
	if 'filmes' in url:
		ficheiro = os.path.join(__PASTA_DADOS__,'filmes_pesquisa.liveit')
		tipo = 0
	elif 'series' in url:
		ficheiro = os.path.join(__PASTA_DADOS__,'series_pesquisa.liveit')
		tipo = 1
	elif 'animes' in url:
		ficheiro = os.path.join(__PASTA_DADOS__,'animes_pesquisa.liveit')
		tipo = 2
	
	if 'page' not in url:
		#tipo = xbmcgui.Dialog().select(u'Onde quer pesquisar?', ['Filmes', 'Series', 'Animes', 'Canais', 'Praias', 'Rádios'])
		tipo = xbmcgui.Dialog().select(u'Onde quer pesquisar?', ['Filmes', 'Series', 'Animes'])
		teclado = xbmc.Keyboard('', 'O que quer pesquisar?')
		if tipo == 0:
			url = __API_SITE__+'filmes/pesquisa'
			ficheiro = os.path.join(__PASTA_DADOS__,'filmes_pesquisa.liveit')
		elif tipo == 1:
			url = __API_SITE__+'series/pesquisa'
			ficheiro = os.path.join(__PASTA_DADOS__,'series_pesquisa.liveit')
		elif tipo == 2:
			url = __API_SITE__+'animes/pesquisa'
			ficheiro = os.path.join(__PASTA_DADOS__,'animes_pesquisa.liveit')
		elif tipo == 3 or  tipo == 4 or tipo == 5:
			url = __SITEBD__+'search.php'
			if tipo == 3:
				tabela = 'canais_kodi'
				ficheiro = os.path.join(__PASTA_DADOS__,'canais.liveit')
			elif tipo == 4:
				tabela = 'praias_kodi'
				ficheiro = os.path.join(__PASTA_DADOS__,'praias.liveit')
			elif tipo == 5:
				tabela = 'radios_kodi'
				ficheiro = os.path.join(__PASTA_DADOS__,'radios.liveit')
			else:
				tabela = 'programas_kodi'
				ficheiro = os.path.join(__PASTA_DADOS__,'programas.liveit')
		
		if ficheiro != '':
			if xbmcvfs.exists(ficheiro):
				f = open(ficheiro, "r")
				texto = f.read()
				teclado.setDefault(texto)
			teclado.doModal()

		if teclado.isConfirmed():
			strPesquisa = teclado.getText()
			dados = {'pesquisa': strPesquisa, 'qualidade': __Qualidade__}
			try:
				f = open(ficheiro, mode="w")
				f.write(strPesquisa)
				f.close()
			except:
				traceback.print_exc()
				__ALERTA__(AddonTitle, 'Não gravou o conteudo em '+ficheiro)
			
			if strPesquisa == '':
				__ALERTA__(AddonTitle, 'Insira algo na pesquisa.')
				addDir2('Alterar Pesquisa', 'url', 7000, '', os.path.join(__ART_FOLDER__, __SKIN__, 'pesquisa.png'), 0)
			else:
				resultado = abrir_url(url,post=json.dumps(dados), header=headers)
	else:
		if ficheiro != '':
			if xbmcvfs.exists(ficheiro):
				f = open(ficheiro, "r")
				texto = f.read()
			dados = {'pesquisa': texto, 'qualidade': __Qualidade__}
			resultado = abrir_url(url,post=json.dumps(dados), header=headers)
	
	if strPesquisa != '':
		if resultado == 'DNS':
			__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
			return False
		
		if tipo == 3 or  tipo == 4 or tipo == 5:
			xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
			if strPesquisa == '':
				__ALERTA__(AddonTitle, 'Insira algo na pesquisa.')
				addDir2('Alterar Pesquisa', 'url', 7000, '', os.path.join(__ART_FOLDER__, __SKIN__, 'pesquisa.png'), 0)
			else:
				dados = {'searchBox': strPesquisa, 'tabela': tabela}
				codigo_fonte = net.http_POST(url, form_data=dados, headers=__HEADERS__).content.decode('latin-1').encode("utf-8")
				informa = {
						'servidor' : {
							'nome': '',
							'serv': ''
						},
						'servidores': [],
						'canais': []
					}
				sucesso = 'no'
				elems = ET.fromstring(codigo_fonte)
				
				for childee in elems:
					if(childee.tag == 'servidores'):
						servidor = {
							'nome': '',
							'link': ''
						}
						for gg in childee:	
							if(gg.tag == 'Nome'):
								servidor['nome'] = gg.text	
							elif(gg.tag == 'Servidor'):
								servidor['link'] = gg.text		
							informa['servidores'].append(servidor)
					
				for servvvv in informa['servidores']:
					if(servvvv['nome'] == servuss):
						informa['servidor']['nome'] = servvvv['nome']
						informa['servidor']['serv'] = servvvv['link']			
				
				for child in elems:
					if(child.tag == 'sucesso'):
						sucesso = child.text
					elif(child.tag == 'canais'):
						canal = {
							'nome': '',
							'logo': '',
							'link': '',
							'grupo': '',
							'nomeid': '',
							'idnovo': ''
						}
						adiciona = True
						pagante = False
						for g in child:
							adiciona = True
							if(g.tag == 'Nome'):
								canal['nome'] = g.text
							elif(g.tag == 'Imagem'):
								canal['logo'] = g.text
							elif(g.tag == 'Pagante'):
								if(g.text == 'true'):
									pagante = True
							elif(g.tag == 'Url'):
								urlchama = g.text.split(';')
								urlnoo = g.text
								try:
									if(servuss == 'Servidor1'):
										urlnoo = urlchama[0]
									elif(servuss == 'Servidor2'):
										urlnoo = urlchama[1]
									elif(servuss == 'Servidor3'):
										urlnoo = urlchama[2]
									elif(servuss == 'Servidor4'):
										urlnoo = urlchama[3]
									elif(servuss == 'Servidor5'):
										urlnoo = urlchama[4]
									elif(servuss == 'Servidor6'):
										urlnoo = urlchama[5]
									elif(servuss == 'Servidor7'):
										urlnoo = urlchama[6]
									elif(servuss == 'Servidor8'):
										urlnoo = urlchama[7]
									
									if(urlnoo == 'nada'):
										adiciona = False
									else:
										if pagante:
											canal['link'] = informa['servidor']['serv']+'live/utilizadorliveit/senhaliveit/'+urlnoo
										else:
											canal['link'] = urlnoo
								except:
									canal['link'] = g.text
							elif(g.tag == 'Grupo'):
								canal['grupo'] = g.text
							elif(g.tag == 'NomeID'):
								canal['nomeid'] = g.text
							elif(g.tag == 'ID'):
								canal['idnovo'] = g.text
						if adiciona:
							informa['canais'].append(canal)

				if sucesso == 'yes':
					addDir2('Alterar Pesquisa', 'url', 7000, '', os.path.join(__ART_FOLDER__, __SKIN__, 'pesquisa.png'), 0)
					for cann in informa['canais']:
						nomee = cann['nome']
						img = cann['logo']
						rtmp = cann['link'].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').replace('utilizadorliveit',__ADDON__.getSetting("login_name")).replace('senhaliveit',__ADDON__.getSetting("login_password"))
						grup = cann['grupo']
						id_it = cann['nomeid']
						id_p = cann['idnovo']
						srt_f = ''
						descri = ''
						
						addLink2(nomee,rtmp,'http://liveitkodi.com/Logos/'+img)
					
					vista_Canais()
				
		else:
			resultado = json.loads(resultado)
			if resultado['data'] != '':
				if tipo == 0:
					for i in resultado['data']:
						categoria = i['categoria1']
						if i['categoria2'] != '':
							categoria += ','+i['categoria2']
						if i['categoria3'] != '':
							categoria += ','+i['categoria3']
						infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'IMDBNumber': i['IMBD'] }				
						try:
							nome = i['nome_ingles'].decode('utf-8')
						except:
							nome = i['nome_ingles'].encode('utf-8')
						pt = ''
						br = ''
						if 'Brasileiro' in categoria:
							br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
						if 'Portu' in categoria:
							pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
						cor = "white"
						if 'http' not in i['foto']:
							i['foto'] = __API__+'images/capas/'+i['foto'].split('/')[-1]
						if 'PT' in i['IMBD']:
							i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
							pt = '[B]PT: [/B]'
						visto = False
						
						nomeee = pt+removerAcentos(nome)+' ('+i['ano']+')'
						urlnoo = __API_SITE__+'filme/'+str(i['id_video'])
						fotooo = i['foto']
						fanarttt = __API__+i['background']
						addVideo(nomeee, urlnoo, 113, fotooo,visto, 'filme', 0, 0, infoLabels, fanarttt, trailer=i['trailer'])
				elif tipo == 1 or tipo == 2:
					for i in resultado['data']:
						categoria = i['categoria1']
						if i['categoria2'] != '':
							categoria += ','+i['categoria2']
						if i['categoria3'] != '':
							categoria += ','+i['categoria3']
						pt = ''
						br = ''
						if 'Brasileiro' in categoria:
							br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
						if 'Portu' in categoria:
							pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
						infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'Code': i['IMBD'] }
						cor = "white"
						if 'PT' in i['IMBD']:
							i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
							pt = '[B]PT: [/B]'
						try:
							nome = i['nome_ingles'].decode('utf-8')
						except:
							nome = i['nome_ingles'].encode('utf-8')
						if 'http' not in i['foto']:
							i['foto'] =__API__+'images/capas/'+i['foto'].split('/')[-1]
						if tipo == 1:
							link = 'serie'
						elif tipo == 2:
							link = 'anime'
						visto=False	
						nomeee = pt+removerAcentos(nome)+' ('+i['ano']+')'
						urlnoo = __API_SITE__+link+'/'+str(i['id_video'])
						fotooo = i['foto']
						fanarttt = __API__+i['background']
						addDir2(nomeee, urlnoo, 114, 'temporadas', fotooo, tipo='serie', infoLabels=infoLabels,poster=fanarttt,visto=visto)

				current = resultado['meta']['pagination']['current_page']
				total = resultado['meta']['pagination']['total_pages']
				try: proximo = resultado['meta']['pagination']['links']['next']
				except: pass 
				if current < total:
					addDir2('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 120, 'pesquisa', os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'))
				else:
					xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
				vista_filmesSeries()


def download(url,name, temporada,episodio,serieNome):
	headers['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenMrpiracy')
	links = url.split('/')
	if 'filme' in url:
		id_video = links[-1]
		tipo = 0
	elif 'serie' in url:
		id_video = links[5]
		temporada = links[7]
		episodio = links[-1]
		tipo = 1
	elif 'anime' in url:
		id_video = links[5]
		temporada = links[7]
		episodio = links[-1]
		tipo = 2

	resultado = abrir_url(url, header=headers)
	if resultado == 'DNS':
		__ALERTA__(AddonTitle, 'Tem de alterar os DNS para poder usufruir do addon.')
		return False
	
	resultado = json.loads(resultado)

	stream, legenda, ext_g = getStreamLegenda(resultado)

	folder = xbmc.translatePath(__ADDON__.getSetting('pastaDownloads'))
	if(folder == 'Escolha a pasta para Download'):
		__ALERTA__(AddonTitle, 'Seleccione uma pasta primeiro no submenu Credênciais ou nas Configurações do Addon.')
	else:
		if tipo > 0:
			if tipo == 1:
				resultadoa = abrir_url(__API_SITE__+'serie/'+id_video, header=headers)
			elif tipo == 2:
				resultadoa = abrir_url(__API_SITE__+'anime/'+id_video, header=headers)
			resultadoa = json.loads(resultadoa)
			if not xbmcvfs.exists(os.path.join(folder,'series')):
				xbmcvfs.mkdirs(os.path.join(folder,'series'))
			if not xbmcvfs.exists(os.path.join(folder,'series',resultadoa['nome_ingles'])):
				xbmcvfs.mkdirs(os.path.join(folder,'series',resultadoa['nome_ingles']))
			if not xbmcvfs.exists(os.path.join(folder,'series',resultadoa['nome_ingles'],"Temporada "+str(temporada))):
				xbmcvfs.mkdirs(os.path.join(folder,'series',resultadoa['nome_ingles'],"Temporada "+str(temporada)))
			folder = os.path.join(folder, 'series', resultadoa['nome_ingles'], "Temporada", str(temporada))
			name = "e"+str(episodio)+" - "+clean(resultado['nome_episodio'])
		else:
			if not xbmcvfs.exists(os.path.join(folder,'filmes')):
				xbmcvfs.mkdirs(os.path.join(folder,'filmes'))
			folder = os.path.join(folder,'filmes')
			name = resultado['nome_ingles']

		streamAux = clean(stream.split('/')[-1])
		extensaoStream = clean(streamAux.split('.')[-1])

		if '?mim' in extensaoStream:
			extensaoStream = re.compile('(.+?)\?mime=').findall(extensaoStream)[0]

		if ext_g != 'coiso':
			extensaoStream = ext_g

		nomeStream = name+'.'+extensaoStream
		nomelegenda = ''
		Downloader.Downloader().download(os.path.join(folder.decode("utf-8"), nomeStream), stream, name)
		
		if legendasOn:
			legendaAux = clean(legenda.split('/')[-1])
			extensaoLegenda = clean(legendaAux.split('.')[1])
			nomeLegenda = name+'.'+extensaoLegenda
			download_legendas(legenda, os.path.join(folder, nomeLegenda))

def download_legendas(url,path):
	contents = abrir_url(url)
	if contents:
		fh = open(path, 'w')
		fh.write(contents)
		fh.close()
	return

def clean(text):
	command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
	regex = re.compile("|".join(map(re.escape, command.keys())))
	return regex.sub(lambda mo: command[mo.group(0)], text)

def addVideo(name,url,mode,iconimage,visto,tipo,temporada,episodio,infoLabels,poster,trailer=False,serieNome=False):
	menu = []
	
	if infoLabels: infoLabelsAux = infoLabels
	else: infoLabelsAux = {'Title': name}

	if poster: posterAux = poster
	else: posterAux = iconimage
	
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

	fanart = __FANART__
	
	if tipo == 'filme':
		xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
		if __ADDON__.getSetting('trailer-filmes') == 'true':
			try:
				idYoutube = trailer.split('?v=')[-1].split('/')[-1].split('?')[0].split('&')[0]
				linkTrailer = 'plugin://plugin.video.youtube/play/?video_id='+idYoutube
				#idYoutube=trailer.split('=')
				#__ALERTA__(AddonTitle, 'ID: '+idYoutube[1])
				#linkTrailer = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+idYoutube[1]
				#linkTrailer = trailer
			except:
				linkTrailer = ''
		else:
			linkTrailer = ''
	elif tipo == 'serie':
		xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
		idIMDb = re.compile('imdb=(.+?)&').findall(url)[0]
		linkTrailer = ""
	elif tipo == 'episodio':
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		linkTrailer = ""
	else:
		xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
		linkTrailer = ""
	
	overlay = 6
	playcount = 0

	infoLabelsAux["overlay"] = overlay
	infoLabelsAux["playcount"] = playcount
	
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels=infoLabelsAux)
	liz.setProperty('fanart_image', poster)
	liz.setArt({'fanart': poster})
	
	
	if not serieNome:
		serieNome = ''

	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&temporada="+str(temporada)+"&episodio="+str(episodio)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&serieNome="+urllib.quote_plus(serieNome)
	ok=True
	
	if linkTrailer != "":
		menu.append(('Ver Trailer', 'XBMC.PlayMedia(%s)' % (linkTrailer)))
		#menu.append(('Ver Trailer', 'XBMC.RunPlugin(%s?mode=105&name=%s&url=%s&iconimage=%s)'%(sys.argv[0],urllib.quote_plus(name), linkTrailer, urllib.quote_plus(iconimage))))
	
	menu.append(('Download', 'XBMC.RunPlugin(%s?mode=117&name=%s&url=%s&iconimage=%s&serieNome=%s&temporada=%s&episodio=%s)'%(sys.argv[0],urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(serieNome), str(temporada), str(episodio))))
	liz.addContextMenuItems(menu, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

###################################################################################
#								FUNCOES JA FEITAS								 #
###################################################################################
def abrirNada():
	xbmc.executebuiltin("Container.SetViewMode(55)")
	
def addDir(name,url,senha,mode,estilo,iconimage,tipo,tipo_user,servidor_user,data_user,fanart,pasta=True,total=1):
	if(tipo == 'pesquisa' and tipo == 'limparcache' and tipo == 'limpartudo'):				
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&tipologia="+str(tipo)+"&tipo_user="+str(tipo_user)+"&servidor_user="+str(servidor_user)
	else:
		if mode == 3333 or mode == 3338:
			u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&tiposelect="+str(senha)+"&fanart="+str(fanart)
		else:
			if tipo_user == 'Teste' and servidor_user == 'Teste':
				u=sys.argv[0]+"?url="+str(url)+"&mode="+str(mode)+"&name="+str(name)+"&senha="+str(senha)+"&estilo="+str(estilo)+"&tipologia="+str(tipo)+"&tipo_user="+str(tipo_user)+"&servidor_user="+str(servidor_user)+"&data_user="+str(data_user)+"&fanart="+str(fanart)
			else:
				u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&senha="+str(senha)+"&estilo="+urllib.quote_plus(estilo)+"&tipologia="+str(tipo)+"&tipo_user="+str(tipo_user)+"&servidor_user="+str(servidor_user)+"&data_user="+str(data_user)+"&fanart="+str(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setArt({'fanart': fanart})
	#liz.setArt({'fanart': os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png')})
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def addFolder(name,url,mode,iconimage,folder):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
	return ok

def addLinkCanal(name,url,iconimage,idcanal,id_p):
	infoLabelssss = {"title": name, "genre": 'All'}
	ok=True
	cm=[]
	
	if(idcanal != '0001'):
		cm.append(('Ver programação', 'XBMC.RunPlugin(%s?mode=31&name=%s&url=%s&iconimage=%s&idCanal=%s&idffCanal=%s)'%(sys.argv[0],urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), idCanal, id_p)))
	
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	#liz.setProperty('fanart_image', fanart)
	#liz.setArt({'fanart': fanart})
	liz.setInfo( type="Video", infoLabels=infoLabelssss)
	liz.addContextMenuItems(cm, replaceItems=False)
	liz.setProperty('IsPlayable', 'true')
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=3334&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)+"&data_user="+str(idcanal)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok
	
def addLink(name,url,iconimage,idCanal,srtfilm,descricao,tipo,tipo_user,id_p,infoLabelssss,fanart,tipppp,adultos=False,total=1):
	ok=True
	cm=[]
	
	if tipo != 'Praia' and tipo != 'ProgramasTV' and tipo != 'Filme' and tipo != 'Serie':
		cm.append(('Ver programação', 'XBMC.RunPlugin(%s?mode=31&name=%s&url=%s&iconimage=%s&idCanal=%s&idffCanal=%s)'%(sys.argv[0],urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), idCanal, id_p)))
	
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setArt({'fanart': fanart})
	liz.setInfo( type="Video", infoLabels=infoLabelssss)
	liz.addContextMenuItems(cm, replaceItems=False)
	
	canaisproprios = False
	
	urlverifica = url.split('.ts')
	totalver = len(urlverifica)
	if totalver != 1:
		canaisproprios = True;
		
	if 'acestream://' in url:
		canaisproprios = True;
	
	if canaisproprios == False:
		urlverifica2 = url.split('.m3u8')
		totalver2 = len(urlverifica2)
		if totalver2 != 1:
			canaisproprios = True;
	
	if tipo == 'ProgramasTV' or tipo == 'Praia' or tipo == 'Filme' or tipo == 'Serie':
		u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=105&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	else:
		if canaisproprios == False:
			u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=105&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
		else:
			if 'acestream://' in url:
				reizinho = ''
			else:
				liz.setProperty('IsPlayable', 'true')
			
			u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=106&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok

def abrir_url(url, post=None, header=None, code=False, erro=False):
	if header == None:
		header = headers
	if post:
		req = urllib2.Request(url, data=post, headers=header)
	else:
		req = urllib2.Request(url, headers=header)
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError as response:
		if erro == True:
			return str(response.code), "asd"
	link=response.read()
	
	if 'judicial blblblblbl' in link:
		return 'DNS'
	if code:
		return str(response.code), link

	response.close()
	return link

def addLink2(name,url,iconimage):
	ok=True
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setArt({'fanart': iconimage})
	liz.setInfo( type="Video", infoLabels={ "Title": name })
	liz.setProperty('IsPlayable', 'true')
	u = sys.argv[0] + "?url=" + url + "&mode=106&name=" + name + "&iconimage=" + iconimage
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok

def play_mult_canal(arg, icon, nome):
	urlchama = arg.split(';;;')
	total2 = len(urlchama)
	urlcorrecto = ''
	if total2 == 1:
		urlcorrecto = arg.replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').replace('utilizadorliveit',__ADDON__.getSetting("login_name")).replace('senhaliveit',__ADDON__.getSetting("login_password"))
	else:
		net = Net()
		net.set_cookies(__COOKIE_FILE__)
		dados = {'url': urlchama[1], 'canal': urlchama[0]}
		codigo_fonte = net.http_POST(__SITEBD__+'searchurl.php',form_data=dados,headers=__HEADERS__).content
		elems = ET.fromstring(codigo_fonte)
		for child in elems:
			if(child.tag == 'info'):
				for d in child:
					if(d.tag == 'url'):
						urlcorrecto = d.text
	
	#__ALERTA__(AddonTitle, 'Url: '+urlcorrecto)
	
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	listitem = xbmcgui.ListItem(nome, thumbnailImage=iconimage)
	listitem.setInfo('video', {'Title': nome})
	playlist.add(url=urlcorrecto, listitem=listitem, index=1)
	xbmc.Player().play(playlist)

def play_canal(arg, icon, nome):
	listitem = xbmcgui.ListItem( label = str(nome), iconImage = icon, thumbnailImage = icon, path=arg )
	listitem.setProperty('fanart_image', icon)
	listitem.setArt({'fanart': icon})
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setInfo(type="Video", infoLabels={ "Title": nome })
	if 'acestream://' in arg:
		from resources.lib.acecore import TSengine as tsengine
		xbmc.executebuiltin('Action(Stop)')
		lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
		if xbmcvfs.exists(lock_file):
			xbmcvfs.delete(lock_file)
		aceport=62062
		chid=arg.replace('acestream://','').replace('ts://','')
		TSPlayer = tsengine()
		out = None
		if chid.find('http://') == -1 and chid.find('.torrent') == -1:
			out = TSPlayer.load_torrent(chid,'PID',port=aceport)
		elif chid.find('http://') == -1 and chid.find('.torrent') != -1:
			out = TSPlayer.load_torrent(chid,'TORRENT',port=aceport)
		else:
			out = TSPlayer.load_torrent(chid,'TORRENT',port=aceport)
		if out == 'Ok':
			TSPlayer.play_url_ind(0,nome + ' (' + chid + ')',icon,icon)
			TSPlayer.end()
			return
		else:	
			__ALERTA__(AddonTitle, 'Erro ao abrir o canal Acestream. ')
			TSPlayer.end()
			return	
	else:
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def addDir2(name,url,mode,mode2,iconimage,pagina=1,tipo=None,infoLabels=None,poster=None,visto=False):
	if infoLabels: infoLabelsAux = infoLabels
	else: infoLabelsAux = {'Title': name}
	fanart = ''
	if poster: fanart = poster
	else: fanart = iconimage
	
	try:
		name = name.encode('utf-8')
	except:
		name = name

	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&modo="+mode2+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	
	ok=True

	#fanart = __FANART__

	if tipo == 'filme':
		#fanart = posterAux
		xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	elif tipo == 'serie':
		#fanart = posterAux
		xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	elif tipo == 'episodio':
		#fanart = posterAux
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	else:
		if name != 'Refresh':
			xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	
	overlay = 6
	playcount = 0
	
	infoLabelsAux["overlay"] = overlay
	infoLabelsAux["playcount"] = playcount
	
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setArt({'fanart': fanart})
	liz.setInfo( type="Video", infoLabels=infoLabelsAux )

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

###################################################################################
#							  DEFININCOES										  #
###################################################################################	
def returnestilo(estilonovo):
	__estilagem__ = ""
	
	if estilonovo == "Lista":
		__estilagem__ ="Container.SetViewMode(50)"
	elif estilonovo == "Lista Grande":
		__estilagem__ = "Container.SetViewMode(51)"
	elif estilonovo == "Miniatura":
		__estilagem__ ="Container.SetViewMode(500)"
	elif estilonovo == "Posters":
		__estilagem__ ="Container.SetViewMode(501)"
	elif estilonovo == "Fanart":
		__estilagem__ = "Container.SetViewMode(508)"
	elif estilonovo == "Media Info 1":
		__estilagem__ = "Container.SetViewMode(504)"
	elif estilonovo == "Media Info 2":
		__estilagem__ = "Container.SetViewMode(503)"
	elif estilonovo == "Media Info 3":
		__estilagem__ = "Container.SetViewMode(515)"
		
	__estilagem__ ="Container.SetViewMode(55)"
	return __estilagem__
	
def vista_Canais():
	xbmc.executebuiltin("Container.SetViewMode(55)")
	opcao = __ADDON__.getSetting('canaisView')
	#if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	#elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	#elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(508)")
	#elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(504)")
	#elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(503)")
	#elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(515)")
	#elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(55)")

def vista_Canais_Lista():
	xbmc.executebuiltin("Container.SetViewMode(55)")
	opcao = __ADDON__.getSetting('canaisView2')
	#if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	#elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	#elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(508)")
	#elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(504)")
	#elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(503)")
	#elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(515)")
	#elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(55)")

def abrirDefinincoes():
	__ADDON__.openSettings()
	addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','',os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png'))
	vista_menu()

def abrirDefinincoesMesmo():
	__ADDON__.openSettings()
	vista_menu()

def vista_menu():
	xbmc.executebuiltin("Container.SetViewMode(55)")
	opcao = __ADDON__.getSetting('menuView')
	#if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	#elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	#elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(508)")
	#elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(504)")
	#elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(503)")
	#elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(515)")
	#elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(55)")

def vista_filmesSeries():
	xbmc.executebuiltin("Container.SetViewMode(55)")
	opcao = __ADDON__.getSetting('filmesSeriesView')
	#if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	#elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	#elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(508)")
	#elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(504)")
	#elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(503)")
	#elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(515)")
	#elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(55)")


def vista_temporadas():
	xbmc.executebuiltin("Container.SetViewMode(55)")
	opcao = __ADDON__.getSetting('temporadasView')
	#if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	#elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	#elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(508)")
	#elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(504)")
	#elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(503)")
	#elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(515)")
	#elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(55)")

def vista_episodios():
	xbmc.executebuiltin("Container.SetViewMode(55)")
	opcao = __ADDON__.getSetting('episodiosView')
	#if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	#elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	#elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	#elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(508)")
	#elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(504)")
	#elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(503)")
	#elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(515)")
	#elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(55)")

############################################################################################################
#												GET PARAMS												 #
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
buildtipo=None
name=None
mode=None
iconimage=None
link=None
senha=None
estilo=None
srtfilm=None
idCanal=None
idffCanal=None
tipologia=None
descricao=None
tipo_user=None
servidor_user=None
data_user=None
s_serv=None
s_user=None
s_pass=None
legenda=None
pagina=None
temporada=None
episodio=None
serieNome=None
fanart=None
thumbnail=None
stream_id=None
duration=None
tiposelect=None

try: duration=urllib.unquote_plus(params["duration"])
except: pass
try: stream_id=urllib.unquote_plus(params["stream_id"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: estilo=urllib.unquote_plus(params["estilo"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: senha=urllib.unquote_plus(params["senha"])
except: pass
try: idCanal=urllib.unquote_plus(params["idCanal"])
except: pass
try: idffCanal=params["idffCanal"]
except: pass
try: srtfilm=urllib.unquote_plus(params["srtfilm"])
except: pass
try: tipologia=urllib.unquote_plus(params["tipologia"])
except: pass
try: descricao=urllib.unquote_plus(params["descricao"])
except: pass
try: tipo_user=urllib.unquote_plus(params["tipo_user"])
except: pass
try: servidor_user=urllib.unquote_plus(params["servidor_user"])
except: pass
try: s_serv=urllib.unquote_plus(params["lolserv"])
except: pass
try: s_user=urllib.unquote_plus(params["loluser"])
except: pass
try: s_pass=urllib.unquote_plus(params["lolpass"])
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
try : buildtipo=urllib.unquote_plus(params["buildtipo"])
except: pass
try : fanart=urllib.unquote_plus(params["fanart"])
except: pass
try : thumbnail=urllib.unquote_plus(params["thumbnail"])
except: pass
try : data_user=urllib.unquote_plus(params["data_user"])
except: pass
try : tiposelect=urllib.unquote_plus(params["tiposelect"])
except: pass





###############################################################################################################
#													MODOS													 #
###############################################################################################################
if mode==None or url==None or len(url)<1: menu()
elif mode==1: listar_grupos(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,fanart)
elif mode==2: listar_canais_url(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,fanart,data_user)
elif mode==4: buildLiveit(buildtipo)
elif mode==3: listar_grupos_adultos(str(url),str(senha),estilo,tipologia,tipo_user,servidor_user,fanart)
elif mode==10: minhaConta(str(name),estilo)
elif mode==20: listamenusseries(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,iconimage,fanart)
elif mode==21: listamenusfilmes(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,iconimage,fanart)
elif mode==24: listamenusanimes(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,iconimage,fanart)
elif mode==25: listatvarchive(str(url))
elif mode==27: definicoes(str(url),tipo_user,servidor_user)
elif mode==28: abrirVideoClube(str(url),tipo_user)
elif mode==26: listatvarchivecanais(str(name),stream_id,str(url),duration,iconimage,fanart)
#elif mode==22: menuSeries()
#elif mode==23: menuFilmes()
elif mode==31: programacao_canal(idCanal)
elif mode==105: play_mult_canal(url, iconimage, name)
elif mode==106: play_canal(url, iconimage, name)
elif mode==110: minhaConta2()
elif mode==111: filmes(url, pagina)
elif mode==123: series(url)
elif mode==118: getGeneros(url)
elif mode==119: getYears(url)
elif mode==120: pesquisa(url,servidor_user)
elif mode==121: anos(url)
elif mode==122: categorias(url)
elif mode==113: player(name, url, iconimage, temporada, episodio, serieNome)
elif mode==114: getSeasons(url)
elif mode==115: getEpisodes(url)
elif mode==117: download(url, name, temporada, episodio, serieNome)
elif mode==1000: abrirDefinincoes()
elif mode==2000: abrirNada()
elif mode==3000: abrirDefinincoesMesmo()
elif mode==3333: abrim3u2(url,tiposelect)
#elif mode==3333: abrim3u2(url,data_user)
elif mode==3335: execute_ainfo(url)
elif mode==3336: security_check(url)
elif mode==3337: detect_modification(url)
elif mode==3338: stream_video(name,url,iconimage,tiposelect)
elif mode==3339: get_myaccount(name,url,iconimage)
elif mode==3340: run_cronjob(name,url,iconimage,thumbnail,fanart)
elif mode==3334: PlayUrl(name,url,iconimage)
elif mode==4000: minhaContabuild()
elif mode==5000: CLEARCACHE()
elif mode==6000: PURGEPACKAGES()
#elif mode==7000: loginPesquisa()
elif mode==8000: buildLiveit(url)

if mode==None or url==None or len(url)<1:
	xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
else:
	if mode !=7000 and  mode !=120 and mode !=3333 and mode !=26 and mode !=27: 
		xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
	elif mode == 120 or mode == 7000:
		pesquisa(url,servidor_user)
		#if mode = 120:
		#	pesquisa(url,servidor_user)
		#else:
		#	loginPesquisa()
	else: 
		xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)