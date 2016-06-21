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
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,HTMLParser,xmltosrt,os,json,threading,xbmcvfs,sys,platform,time,gzip,glob,datetime,thread
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from t0mm0.common.net import Net
from datetime import date
import xml.etree.ElementTree as ET
import urlresolver
import jsunpack
import mechanize, cookielib
from bs4 import BeautifulSoup

try:
    import json
except:
    import simplejson as json
h = HTMLParser.HTMLParser()

import re, htmlentitydefs
reload(sys)
sys.setdefaultencoding('utf-8')

####################################################### CONSTANTES #####################################################

global g_timer

__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo("id")
__ADDON__	= xbmcaddon.Addon(__ADDON_ID__)
__CWD__ = xbmc.translatePath( __ADDON__.getAddonInfo('path') ).decode("utf-8")
__ADDON_FOLDER__	= __ADDON__.getAddonInfo('path')
__SETTING__	= xbmcaddon.Addon().getSetting
__ART_FOLDER__	= __ADDON_FOLDER__ + '/resources/img/'
__FANART__ 		= os.path.join(__ADDON_FOLDER__,'fanart.jpg')
_ICON_ = __ADDON_FOLDER__ + '/icon.png'
__SKIN__ = 'v1'
__SITE__ = 'http://www.pcteckserv.com/GrupoKodi/PHP/'
__SITEAddon__ = 'http://www.pcteckserv.com/GrupoKodi/Addon/'
__EPG__ = 'http://www.pcteckserv.com/GrupoKodi/epg.gz'
__FOLDER_EPG__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.LiveTV/').decode('utf-8'), 'epg')
__ALERTA__ = xbmcgui.Dialog().ok
__COOKIE_FILE__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.LiveTV/').decode('utf-8'), 'addon_cookies_liveit')
__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

xml = BeautifulSOAP(open(__ADDON_FOLDER__+'/addon.xml','r'), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
_VERSAO_ = str(xml.addon['version'])
_NOMEADDON_ = str(xml.addon['name'])
check_login = {}

#reload(sys)
#sys.setdefaultencoding('utf-8')

###################################################################################
#                              Iniciar Addon		                                  #
###################################################################################
  
def menu():
	if (not __ADDON__.getSetting('login_name') or not __ADDON__.getSetting('login_password')):
		__ALERTA__('Live!t TV', 'Precisa de definir o seu Utilizador e Senha')
		abrirDefinincoes()
	else:
		check_login = login()
		if check_login['user']['nome'] != '':
			if check_login['sucesso']['resultado'] == 'yes':
				#xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%('Live!t TV - Sessão: '+check_login['user']['nome']+', Versão do addon: '+_VERSAO_, '8000, _ICON_))
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
				if check_login['datafim']['data'] != "Membro Ativo Sem Doacao!":
					if check_login['user']['dias'] == '5' or check_login['user']['dias'] == '4' or check_login['user']['dias'] == '3' or check_login['user']['dias'] == '2' or check_login['user']['dias'] == '1':
						__ALERTA__('Live!t TV', 'Faltam '+check_login['user']['dias']+' dias para o serviço expirar.')
					if check_login['user']['dias'] == '0':
						__ALERTA__('Live!t TV', 'É hoje que o seu serviço expira. Faça a sua Renovação. Caso não faça irá ficar Inactivo Hoje.')
				if check_login['datafim']['data'] != "Membro Ativo Sem Doacao!":
					menus2 = {
					'nome': '',
					'logo': '',
					'link': '',
					'tipo': '',
					'senha': ''
					}
					menus2['nome'] = check_login['datafim']['data']
					menus2['logo'] = __SITEAddon__+"Imagens/estadomembro.png"
					menus2['link'] = 'url'
					menus2['tipo'] = "estado"
					menus2['senha'] = ""
					check_login['menus'].append(menus2)
				menus['nome'] = "Participacoes"
				menus['logo'] = check_login['info']['logo']
				menus['link'] = check_login['info']['link']
				menus['tipo'] = "patrocinadores"
				menus['senha'] = ""
				check_login['menus'].append(menus)
				menus1['nome'] = "Novidades"
				menus1['logo'] = check_login['info']['logo2']
				menus1['link'] = check_login['info']['link2']
				menus1['tipo'] = "novidades"
				menus1['senha'] = ""
				check_login['menus'].append(menus1)
				Menu_inicial(check_login)
			elif check_login['sucesso']['resultado'] == 'utilizador':
				__ALERTA__('Live!t TV', 'Utilizador incorreto.')
				addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','','','','')
				addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','','','','')
			elif check_login['sucesso']['resultado'] == 'senha':
				__ALERTA__('Live!t TV', 'Senha incorreta.')
				addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','','','','')
				addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','','','','')
			elif check_login['sucesso']['resultado'] == 'ativo':
				__ALERTA__('Live!t TV', 'O estado do seu Utilizador encontra-se Inactivo. Para saber mais informações entre em contacto pelo email registoliveit@pcteckserv.com.')
			else:
				__ALERTA__('Live!t TV', 'Não foi possível abrir a página. Por favor tente novamente.')
		else:
			addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','','','','')
			addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','','','','')

		xbmc.executebuiltin("Container.SetViewMode(500)")
	
def abrir_cookie(usser, seenha, service, url, New=False):
	import mechanize
	import cookielib

	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	if not New:
		cj.load(os.path.join(xbmc.translatePath("special://temp"),"addon_cookies_liveit"), ignore_discard=False, ignore_expires=False)
		br.set_handle_equiv(True)
		br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	if New:
		br.open(service + 'admin/')
		br.select_form(nr=0)
		br.form['password']= seenha
		br.form['username']= usser
		br.submit()
		cj.save(os.path.join(xbmc.translatePath("special://temp"),"addon_cookies_liveit"))
		try:
			br.open(url,timeout=50000000)
		except:
			br.open(url)
		return br.response().read()

def getSoup(url):
	data = abrir_cookie('','','',url).decode('utf8')
	return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)

###################################################################################
#                              Login Addon		                                  #
###################################################################################
def minhaConta(data_user,estilo):
	addDir(data_user, 'url', None, None, estilo, __SITEAddon__+"Imagens/estadomembro.png",'','','','','','','')
	addDir('Definições', 'url', None, 1000, estilo, __SITEAddon__+"Imagens/definicoes.png",'','','','','','','')

def login():
	informacoes = {
		'user' : {
			'nome': '',
			'nome': '',
			'email': '',
			'tipo': '',
			'dias': '',
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
		codigo_fonte = net.http_POST(__SITE__+'LoginAddon2.php',form_data=dados,headers=__HEADERS__).content
		elems = ET.fromstring(codigo_fonte)
		for child in elems:
			if(child.tag == 'sucesso'):
				informacoes['sucesso']['resultado'] = child.text
			elif(child.tag == 'user'):
				for d in child:
					if(d.tag == 'Nome'):
						informacoes['user']['nome'] = d.text
					elif(d.tag == 'Email'):
						informacoes['user']['email'] = d.text
					elif(d.tag == 'Servidor'):
						informacoes['user']['servidor'] = d.text
					elif(d.tag == 'Tipo'):
						informacoes['user']['tipo'] = d.text
					elif(d.tag == 'dias'):
						informacoes['user']['dias'] = d.text
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
						'senha': ''
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
					elif(g.tag == 'senha'):
						menu['senha'] = informacoes['user']['senhaadulto']
				if informacoes['datafim']['data'] == "Membro Ativo Sem Doacao!":
					if menu['nome'] != 'Adultos':
						informacoes['menus'].append(menu)
				else:
					informacoes['menus'].append(menu)
			else: 
				print "Não sei o que estou a ler"
	except:
		__ALERTA__('Live!t TV', 'Não foi possível abrir a página. Por favor tente novamente.')
		return informacoes

	return informacoes

###############################################################################################################
#                                                   Menus                                                     #
###############################################################################################################

def Menu_inicial(men):
	_tipouser = men['user']['tipo']
	_nomeuser = 'Live!t-TV ('+men['user']['nome']+')'
	for menu in men['menus']:
		nome = menu['nome']
		logo = menu['logo']
		link = menu['link']
		tipo = menu['tipo']
		senha = menu['senha']
		if tipo == 'Adulto' :
			addDir(nome,link,senha,3,'Miniatura',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif tipo == 'patrocinadores' or tipo == 'novidades':
			addDir(nome,link,None,1,'Lista',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif(tipo == 'Filme'):
			addDir(nome,link,None,21,'Miniatura',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif(tipo == 'Serie'):
			addDir(nome,link,None,20,'Miniatura',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif(tipo == 'estado'):
			addDir(nome,link,None,10,'Lista',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
		else:
			if _tipouser == 'Administrador' or _tipouser == 'Patrocinador' or _tipouser == 'PatrocinadorPagante':
				if nome == 'TVs':
					addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
					addDir('TVs-Free',link,None,1,'Miniatura',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
				else:
					addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
			else:
				addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,men['user']['servidor'],'',men['info']['log'],men['info']['user'],men['info']['password'])
	
	#xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(_nomeuser, Versão do addon: '+_VERSAO_, 8000, _ICON_))
	thread.start_new_thread( obter_ficheiro_epg, () )
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(_nomeuser,'Versão do addon: '+_VERSAO_, 8000, _ICON_))
	#check_version()
###############################################################################################################
#                                                   Listar Grupos                                             #
###############################################################################################################
def listar_grupos_adultos(url,senha,estilo,tipo,tipo_user,servidor_user,sserv,suser,spass):
	passa = True
	if tipo_user == 'Teste':
		if servidor_user == "Teste":
			passa = False
			__ALERTA__('Live!t TV', 'Não tem acesso a este menu. Faça a sua doação.')
		else:
			if servidor_user == 'Teste':
				passa = False
				__ALERTA__('Live!t TV', 'Não tem acesso a este menu. Faça a sua doação.')	
	if passa == True:
		if(__ADDON__.getSetting("login_adultos") == ''):
			__ALERTA__('Live!t TV', 'Preencha o campo senha para adultos.')
		elif(__ADDON__.getSetting("login_adultos") != senha):
			__ALERTA__('Live!t TV', 'Senha para adultos incorrecta. Verifique e tente de novo.')
		else:
			listar_grupos('',url,estilo,tipo,tipo_user,servidor_user,sserv,suser,spass)

def listar_grupos(nome_nov,url,estilo,tipo,tipo_user,servidor_user,sservee,suseree,spassee):
	if url != 'url':
		if tipo == 'Filme':
			xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(_NOMEADDON_,'A verificar os seus dados de acesso.', 2000, _ICON_))
			estado = abrir_cookie(suseree, spassee, sservee, sservee + 'canais/liberar/', True)
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
				paramss = estil.split('\n')
				if tipo_user == 'Administrador' or tipo_user == 'Pagante' or tipo_user == 'PatrocinadorPagante':
					if nome_nov == 'TVs-Free':
						addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
					elif servidor_user == 'Servidor1':
						addDir(nomee,urlllserv1,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
					elif servidor_user == 'Servidor2':
						addDir(nomee,urlllserv2,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
					else:
						addDir(nomee,urlllserv3,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
				elif tipo_user == 'Patrocinador':
					if nome_nov == 'TVs-Free':
						addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
				else:
					if tipo_user == 'Teste':
						if servidor_user == "Teste":
							addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
						else:
							if servidor_user != '':
								if servidor_user == 'Servidor1':
									addDir(nomee,urlllserv1,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
								elif servidor_user == 'Servidor2':
									addDir(nomee,urlllserv2,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
								else:
									addDir(nomee,urlllserv3,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
							else:
								addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
					else:
						addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
			except:
				pass
	estiloSelect = returnestilo(estilo)
	xbmc.executebuiltin(estiloSelect)	
	
###############################################################################################################
#                                                   Listar Canais                                             #
###############################################################################################################
def listar_canais_url(nome,url,estilo,tipo,tipo_user,servidor_user,sservee,suseree,spassee):
	if url != 'nada':
		page_with_xml = urllib2.urlopen(url).readlines()
		f = open(os.path.join(__FOLDER_EPG__, 'epg'), mode="r")
		codigo = f.read()
		f.close()
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
				if tipo == 'ProgramasTV':
					urlchama = params[2].split(';;;')
					total2 = len(urlchama)
					urlcorrecto = ''
					if total2 == 1:
						urlcorrecto = params[2].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').replace('utilizadorliveit',__ADDON__.getSetting("login_name")).replace('senhaliveit',__ADDON__.getSetting("login_password"))
					else:
						net = Net()
						net.set_cookies(__COOKIE_FILE__)
						dados = {'url': urlchama[1], 'canal': urlchama[0]}
						codigo_fonte = net.http_POST(__SITE__+'searchurl.php',form_data=dados,headers=__HEADERS__).content
						elems = ET.fromstring(codigo_fonte)
						for child in elems:
							if(child.tag == 'info'):
								for d in child:
									if(d.tag == 'url'):
										urlcorrecto = d.text
					
					rtmp = urlcorrecto;
				else:
					rtmp = params[2].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').replace('utilizadorliveit',__ADDON__.getSetting("login_name")).replace('senhaliveit',__ADDON__.getSetting("login_password"))
				
				img = params[1].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http')
				grup = params[3]
				id_it = params[4].rstrip()
				id_p = params[5]
				srt_f = ''
				descri = ''
				if grup == nome:
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
						argumento = 'Live!t-TV'
						plot = 'Enredo: '+descri
						detalhes2 = ano
						imdb = '4510398'
						votes = '5 estrelas'
						infoLabels = {'Title':nomewp, 'Plot':plot, 'Writer': argumento, 'Director':realizador, 'Genre':detalhes1, 'Year': detalhes2, 'Aired':detalhes2, 'IMDBNumber':imdb, 'Votes':votes}
					else:
						infoLabels = {'Title':nomewp}
						
					addLink(nomewp,rtmp,img,id_it,srt_f,descri,tipo,tipo_user,id_p,infoLabels,total)
			except:
				pass
		estiloSelect = returnestilo(estilo)
		xbmc.executebuiltin(estiloSelect)

def play_mult_canal(arg, icon, nome, tipouser):
	#playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist = xbmc.PlayList(1)
	playlist.clear()
	#__ALERTA__('Live!t TV', 'Zequinha')
	listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setInfo("Video", {"title":name})
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	playlist.add(url, listitem)
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
	player = xbmc.Player()		
	try:
		player.play(playlist)
	except:
		if tipouser == 'Teste':
			__ALERTA__('Live!t TV', 'Sendo Free tem estas paragens ou falhas. Adquire agora o premium vai ao grupo e fala com o Administrador.')
		else:
			__ALERTA__('Live!t TV', 'Faça Retroceder 3 vezes no comando e tente novamente.')

###############################################################################################################
#                                                   EPG                                                     #
###############################################################################################################
def obter_ficheiro_epg():

	if not xbmcvfs.exists(__FOLDER_EPG__):
		xbmcvfs.mkdirs(__FOLDER_EPG__)

	"""horaAtual = time.strftime("%d/%m/%Y")
	
	ficheiroData = os.path.join(__FOLDER_EPG__, 'ultima.txt')

	if not xbmcvfs.exists(ficheiroData):
		f = open(ficheiroData, mode="w")
		f.write("")
		f.close()

	f = open(ficheiroData, mode="r")
	dataAntiga = f.read()
	f.close()

	if (time.strptime(dataAntiga, "%d/%m/%Y")) < horaAtual or not dataAntiga:
		f = open(ficheiroData, mode="w")
		f.write(str(horaAtual))
		f.close()"""

	urllib.urlretrieve(__EPG__, os.path.join(__FOLDER_EPG__, 'epg.gz'))		

	for gzip_path in glob.glob(__FOLDER_EPG__ + "/*.gz"):
		inf = gzip.open(gzip_path, 'rb')
		s = inf.read()
		inf.close()

		gzip_fname = os.path.basename(gzip_path)
		fname = gzip_fname[:-3]
		uncompressed_path = os.path.join(__FOLDER_EPG__, fname)

		open(uncompressed_path, 'w').write(s)


def getProgramacaoDiaria(idCanal, diahora, codigo):
	source = re.compile('<programme channel="'+idCanal+'" start="(.+?) \+0100" stop="(.+?) \+0100">\s+<title lang="pt">(.+?)<\/title>').findall(codigo)

	programa = ''

	for start, stop, programa1  in source:

		if(int(start) < diahora and int(stop) > diahora):
			programa = programa1
	return programa

			
def programacao_canal(idCanal):

	f = open(os.path.join(__FOLDER_EPG__, 'epg'), mode="r")
	codigo = f.read()
	f.close()

	ts = time.time()
	st = int(datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d'))

	diahora = int(str(st)+'060000')
	diaamanha = int(str(st+1)+'060000')

	source = re.compile('<programme channel="'+idCanal+'" start="(.+?) \+0100" stop="(.+?) \+0100">\s+<title lang="pt">(.+?)<\/title>').findall(codigo)

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
		window.getControl(1).setLabel('Live!t TV')
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
#                                               Addon Filmes e Series                                      #
############################################################################################################ 

def listamenusseries(nome_nov,url,estilo,tipo,tipo_user,servidor_user,iconimage,sserv,suser,spass):
	addDir('Series Live!t',url,None,1,'Miniatura',iconimage,tipo,tipo_user,servidor_user,'',sserv,suser,spass)
	addDir('Series Web','-',None,22,estilo,iconimage,'','','','','','','')
	estiloSelect = returnestilo(estilo)
	xbmc.executebuiltin(estiloSelect)

def listamenusfilmes(nome_nov,url,estilo,tipo,tipo_user,servidor_user,iconimage,sserv,suser,spass):
	addDir('Filmes Live!t',url,None,1,estilo,iconimage,tipo,tipo_user,servidor_user,'',sserv,suser,spass)
	addDir('Filmes Web','-',None,23,estilo,iconimage,'','','','',sserv,suser,spass)
	estiloSelect = returnestilo(estilo)
	xbmc.executebuiltin(estiloSelect)

def listaseries(estilo):
	addDir('Pesquisar Series','-',estilo,8,'',__ART_FOLDER__ + 'pesquisa.png','','','','','','','')
	listar_series('http://www.armagedomfilmes.biz/?cat=21|1')
	estiloSelect = returnestilo(estilo)
	xbmc.executebuiltin(estiloSelect)

def listafilmes(estilo):
	addDir('Pesquisar Filmes','-',estilo,14,'',__ART_FOLDER__ + 'pesquisa.png','','','','','','','')
	addDir('Lançamentos','http://www.armagedomfilmes.biz/?cat=3236',estilo,13,'',__ART_FOLDER__ + 'upfolder.png','','','','','','','')
	categorias(estilo)
	estiloSelect = returnestilo(estilo)
	xbmc.executebuiltin(estiloSelect)

def categorias(estilo):
	addDir('BLURAY','http://www.armagedomfilmes.biz/?cat=5529',None,13,estilo,__ART_FOLDER__ + 'bluray.png','','','','','','','')
	addDir('LEGENDADOS','http://www.armagedomfilmes.biz/?s=legendado',None,13,estilo,__ART_FOLDER__ + 'legendados.png','','','','','','','')
	addDir('ACAO','http://www.armagedomfilmes.biz/?cat=3227',None,13,estilo,__ART_FOLDER__ + 'action.png','','','','','','','')
	addDir('ANIMACAO','http://www.armagedomfilmes.biz/?cat=3228',None,13,estilo,__ART_FOLDER__ + 'cartoons.png','','','','','','','')
	addDir('AVENTURA','http://www.armagedomfilmes.biz/?cat=3230',None,13,estilo,__ART_FOLDER__ + 'adventure.png','','','','','','','')
	addDir('COMEDIA ','http://www.armagedomfilmes.biz/?cat=3229',None,13,estilo,__ART_FOLDER__ + 'comedy.png','','','','','','','')
	addDir('COMEDIA ROMANTICA','http://www.armagedomfilmes.biz/?cat=3231',None,13,estilo,__ART_FOLDER__ + 'romance.png','','','','','','','')
	addDir('DRAMA','http://www.armagedomfilmes.biz/?cat=3233',None,13,estilo,__ART_FOLDER__ + 'drama.png','','','','','','','')
	addDir('FAROESTE','http://www.armagedomfilmes.biz/?cat=18',None,13,estilo,__ART_FOLDER__ + 'faroeste.png','','','','','','','')
	addDir('FICCAO CIENTIFICA','http://www.armagedomfilmes.biz/?cat=3235',None,13,estilo,__ART_FOLDER__ + 'scifi.png','','','','','','','')
	addDir('LUTAS UFC','http://www.armagedomfilmes.biz/?cat=3394',None,13,estilo,__ART_FOLDER__ + 'sports.png','','','','','','','')
	addDir('NACIONAL','http://www.armagedomfilmes.biz/?cat=3226',None,13,estilo,__ART_FOLDER__ + 'homemovies.png','','','','','','','')
	addDir('POLICIAL','http://www.armagedomfilmes.biz/?cat=72',None,13,estilo,__ART_FOLDER__ + 'war.png','','','','','','','')
	addDir('RELIGIOSO','http://www.armagedomfilmes.biz/?cat=20',None,13,estilo,__ART_FOLDER__ + 'classics.png','','','','','','','')
	addDir('ROMANCE','http://www.armagedomfilmes.biz/?cat=3232',None,13,estilo,__ART_FOLDER__ + 'romance.png','','','','','','','')
	addDir('SHOWS','http://www.armagedomfilmes.biz/?cat=30',None,13,estilo,__ART_FOLDER__ + 'musicals.png','','','','','','','')
	addDir('SUSPENSE','http://www.armagedomfilmes.biz/?cat=3239',None,13,estilo,__ART_FOLDER__ + 'mystery.png','','','','','','','')
	addDir('TERROR','http://www.armagedomfilmes.biz/?cat=3238',None,13,estilo,__ART_FOLDER__ + 'horror.png','','','','','','','')
	addDir('THRILLER','http://www.armagedomfilmes.biz/?cat=30',None,13,estilo,__ART_FOLDER__ + 'thriller.png','','','','','','','')

def listar_videos(url):
	codigo_fonte = abrir_url(url)
	soup = BeautifulSoup(abrir_url(url))
	content = BeautifulSoup(soup.find("div", { "class" : "bic-miniaturas" }).prettify())
	filmes = content("div", { "class" : "bic-miniatura" })
	for filme in filmes:
		titulo = filme.a["title"].replace('Assistir ','')
		url = filme.a["href"]
		img = filme.img["src"]
		addDir(titulo.encode('utf8'),url,None,4,'Lista',img,'','','','','','','',False,len(filmes))
		
	pagenavi = BeautifulSoup(soup.find('div', { "class" : "wp-pagenavi" }).prettify())("a", { "class" : "nextpostslink" })[0]["href"]
	addDir('Página Seguinte >>',pagenavi,None,13,'',__ART_FOLDER__ + 'prox.png','','','','','','','')

	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	estiloSelect = returnestilo('Lista')
	xbmc.executebuiltin(estiloSelect)
	
def listar_series(url):
	pagina = str(int(url.split('|')[1])+1)
	url = url.split('|')[0]

	soup = BeautifulSoup(abrir_url(url))
	content = BeautifulSoup(soup.find("div", { "class" : "bic-miniaturas" }).prettify())
	series = content("div", { "class" : "bic-miniatura" })
	codigo_fonte = abrir_url(url)
	
	total = len(series)
	for serie in series:
		titulo = serie.a['title']
		titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'").replace('Assistir ','')
		try:
			addDir(titulo.encode('utf-8'),serie.a['href'],None,12,'Lista',serie.img['src'],'','','','','','','',True,total)
		except:
			pass

	addDir('Página Seguinte >>','http://www.armagedomfilmes.biz/?cat=21&paged='+pagina+'|'+pagina,None,6,'',__ART_FOLDER__ + 'prox.png','','','','','','','')
	estiloSelect = returnestilo('Lista')
	xbmc.executebuiltin(estiloSelect)

def listar_temporadas(url):
	codigo_fonte = abrir_url(url)
	soup = BeautifulSoup(abrir_url(url))
	conteudo = BeautifulSoup(soup.find("ul", { "class" : "bp-series" }).prettify())
	temporadas = conteudo("li")
	total = len(temporadas)
	i=1
	#print total
	
	while i <= total:
		temporada = conteudo("li", { "class" : "serie"+str(i)+"-code"})
		for temp in temporada:
			img = temp.img["src"]
			titulo = str(i)+" temporada"
			try:
				addDir(titulo,url,None,7,'',img,'','','','','','','',True,total)
			except:
				pass
		i=i+1
	
	estiloSelect = returnestilo('Lista')
	xbmc.executebuiltin(estiloSelect)

def listar_series_f2(name,url):
	n = name.replace(' temporada','')
	soup = BeautifulSoup(abrir_url(url))
	content = BeautifulSoup(soup.find("li", { "class" : "serie"+n+"-code" }).prettify())
	episodios = content.findAll("a")
	#print episodios[0]
	a = [] # url titulo img
	for episodio in episodios:
		try:
			xml = BeautifulSoup(abrir_url(episodio["href"]+'/feed'))
			title = xml.title.string.encode('utf-8').replace('Comentários sobre: Assistir ','')
			try:
				if "html" in os.path.basename(episodio["href"]):
					temp = [episodio["href"],title]
					a.append(temp)
			except:
				pass
		except:
			pass

	total = len(a)
	for url2, titulo, in a:
		titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'").replace('Assistir ','')
		addDir(titulo,url2,None,4,'','','','','','','','','',False,total) 

	estiloSelect = returnestilo('Lista')
	xbmc.executebuiltin(estiloSelect)

def obtem_url_dropvideo(url):
	codigo_fonte = abrir_url(url)
	try:
		soup = BeautifulSoup(codigo_fonte)
		lista = soup.findAll('script')
		js = str(lista[9]).replace('<script>',"").replace('</script>',"")
		sUnpacked = jsunpack.unpack(js)
		#print sUnpacked
		url_video = re.findall(r'var vurl2="(.*?)";', sUnpacked)
		url_video = str(url_video).replace("['","").replace("']","")
		return [url_video,"-"]
	except:
		pass	
	
def obtem_videobis(url):
	codigo_fonte = abrir_url(url)
	try:
		url_video = re.findall(r'file: "(.*?)"',codigo_fonte)[1]
		return [url_video,"-"]
	except:
		return ["-","-"]
		
def obtem_neodrive(url):
	codigo_fonte = abrir_url(url)
	try:
		url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_videopw(url):
	codigo_fonte = abrir_url(url)
	try:
		url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]		
	
def obtem_cloudzilla(url):
	codigo_fonte = abrir_url(url)
	try:
		url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def player1(name,url,iconimage):
	try:
		dropvideo = r'src="(.*?dropvideo.*?/embed.*?)"'
		dropmega = r'src=".*?drop.*?id=(.*?)"'
		neodrive = r'src="(.*?neodrive.*?/embed.*?)"'
		neomega = r'src=".*?neodrive.*?id=(.*?)"'
		videobis = r'SRC="(.*?videobis.*?/embed.*?)"'
		videopw = r'src=".*?videopw.*?id=(.*?)"'
		cloudzilla = r'cloudzilla.php.id=(.*?)"'
		cloudzilla_f = r'http://www.cloudzilla.to/share/file/(.*?)"'
		
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('Live!t-TV', 'A resolver link','Por favor aguarde...')
		mensagemprogresso.update(33)
		links = []
		hosts = []
		matriz = []
		codigo_fonte = abrir_url(url)
		
		try:
			links.append(re.findall(dropvideo, codigo_fonte)[0])
			hosts.append('Dropvideo')
		except:
			pass
		
		try:
			links.append('http://www.dropvideo.com/embed/'+re.findall(dropmega, codigo_fonte)[0])
			hosts.append('Dropvideo')
		except:
			pass
		
		try:
			links.append('http://videopw.com/e/'+re.findall(videopw, codigo_fonte)[0])
			hosts.append('Videopw')
		except:
			pass
			
		try:
			links.append(re.findall(videobis, codigo_fonte)[0])
			hosts.append('Videobis')
		except:
			pass
		
		try:
			links.append(re.findall(neodrive, codigo_fonte)[0])
			hosts.append('Neodrive')
		except:
			pass
		
		try:
			links.append('http://neodrive.co/embed/'+re.findall(neomega, codigo_fonte)[0])
			hosts.append('Neodrive')
		except:
			pass	
			
		try:
			links.append('http://www.cloudzilla.to/embed/'+re.findall(cloudzilla,codigo_fonte)[0])
			hosts.append('CloudZilla')
		except:
			pass
		
		try:
			links.append('http://www.cloudzilla.to/embed/'+re.findall(cloudzilla_t,codigo_fonte)[0])
			hosts.append('CloudZilla(Legendado)')
		except:
			pass
			
		if not hosts:
			return
		
		index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)
		
		if index == -1:
			return
		
		url_video = links[index]
		mensagemprogresso.update(66)
		
		#print 'Player url: %s' % url_video
		if 'dropvideo.com/embed' in url_video:
			matriz = obtem_url_dropvideo(url_video)  
		elif 'cloudzilla' in url_video:
			matriz = obtem_cloudzilla(url_video)
		elif 'videobis' in url_video:
			matriz = obtem_videobis(url_video)
		elif 'neodrive' in url_video:
			matriz = obtem_neodrive(url_video)
		elif 'videopw' in url_video:
			matriz = obtem_videopw(url_video)			
		else:
			print "Falha: " + str(url_video)
		#print matriz
		url = matriz[0]
		#print url
		if url=='-': return
		legendas = matriz[1]
		#print "Url do gdrive: " + str(url_video)
		#print "Legendas: " + str(legendas)
		
		mensagemprogresso.update(100)
		mensagemprogresso.close()
		
		listitem = xbmcgui.ListItem() # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
		listitem.setPath(url)
		listitem.setProperty('mimetype','video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		#try:
		player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		player.play(url)
		if legendas != '-':
			if 'timedtext' in legendas:
				#legenda = xmltosrt.convert(legendas)
				#try:
					import os.path
					sfile = os.path.join(xbmc.translatePath("special://temp"),'sub.srt')
					sfile_xml = os.path.join(xbmc.translatePath("special://temp"),'sub.xml')#timedtext
					sub_file_xml = open(sfile_xml,'w')
					sub_file_xml.write(urllib2.urlopen(legendas).read())
					sub_file_xml.close()
					#print "Sfile.srt : " + sfile_xml
					xmltosrt.main(sfile_xml)
					xbmcPlayer.setSubtitles(sfile)
				#except:
				#	pass
			else:
				xbmcPlayer.setSubtitles(legendas)
		#except:
			dialog = xbmcgui.Dialog()
			dialog.ok("Live!t-TV Erro:", " Impossível abrir vídeo! ")
		#	pass
	except:
		#print "erro ao abrir o video"
		#print url_video
		pass
	
def pesquisa_filme():
	keyb = xbmc.Keyboard('', 'faca a procura') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto Ã©, escapa os parametros necessarios para ser incorporado num endereÃ§o url
		url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa) #nova definicao de url. str forÃ§a o parametro de pesquisa a ser uma string
		#print url
		soup = BeautifulSoup(abrir_url(url))
		content = BeautifulSoup(soup.find("div", { "class" : "bic-miniaturas" }).prettify())
		filmes = content("div", { "class" : "bic-miniatura" })
		#print filmes[0]
		for filme in filmes:
			titulo = filme.a["title"].replace('Assistir ','')
			url = filme.a["href"]
			img = filme.img["src"]
			addDir(titulo.encode('utf8'),url,None,4,'',img,'','','','','','','',False,len(filmes))

	estiloSelect = returnestilo('Lista')
	xbmc.executebuiltin(estiloSelect)

def pesquisa_serie():
	keyb = xbmc.Keyboard('', 'faca a procura') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search)
		url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa)
		soup = BeautifulSoup(abrir_url(url))
		content = BeautifulSoup(soup.find("div", { "class" : "bic-miniaturas" }).prettify())
		series = content("div", { "class" : "bic-miniatura" })
		codigo_fonte = abrir_url(url)

		total = len(series)
		for serie in series:
			titulo = serie.a['title']
			titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'").replace('Assistir ','')
			try:
				addDir(titulo.encode('utf-8'),serie.a['href'],None,12,'',serie.img['src'],'','','','','','','',True,total)
			except:
				pass
	
	estiloSelect = returnestilo('Lista')
	xbmc.executebuiltin(estiloSelect)

###################################################################################
#                              DEFININCOES		                                  #
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
	return __estilagem__

def abrirDefinincoes():
	__ADDON__.openSettings()
	addDir('Entrar novamente', 'url', None, None, 'Lista Grande', __SITEAddon__+"Imagens/retroceder.png",'','','','','','','')
	xbmc.executebuiltin("Container.SetViewMode(51)")

def abrirNada():
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
def addDir(name,url,senha,mode,estilo,iconimage,tipo,tipo_user,servidor_user,data_user,sserv,suser,spass,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&senha="+str(senha)+"&estilo="+urllib.quote_plus(estilo)+"&tipologia="+str(tipo)+"&tipo_user="+str(tipo_user)+"&servidor_user="+str(servidor_user)+"&data_user="+str(data_user)+"&lolserv="+sserv+"&loluser="+suser+"&lolpass="+spass
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def addFolder(name,url,mode,iconimage,folder):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
	return ok
	
def addLink(name,url,iconimage,idCanal,srtfilm,descricao,tipo,tipo_user,id_p,infoLabels,total=1):
	cm=[]
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	if tipo == 'Filme' or tipo == 'Serie':
		u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=333&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)+ "&srtfilm=" + urllib.quote_plus(srtfilm)+"&tipo_user="+str(tipo_user)
	else:
		u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=105&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)+"&tipo_user="+str(tipo_user)
		if tipo != 'Praia' and tipo != 'ProgramasTV':
			cm.append(('Ver programação', 'XBMC.RunPlugin(%s?mode=31&name=%s&url=%s&iconimage=%s&idCanal=%s&idffCanal=%s)'%(sys.argv[0],urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), idCanal, id_p)))
	liz.setInfo( type="Video", infoLabels=infoLabels)
	if tipo == 'Filme':	
		xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	elif tipo == 'Serie':
		xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

	if tipo == 'Filme' or tipo == 'Serie':
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	else:
		liz.addContextMenuItems(cm, replaceItems=False)
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok

def play_srt(name,url,iconimage,legendas):
	playlist = xbmc.PlayList(1)
	playlist.clear()
	listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setInfo("Video", {"title":name})
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	playlist.add(url, listitem)
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
	player = xbmc.Player()
	player.play(playlist)
	while not (player.isPlaying()):
		xbmc.sleep(80)
		time.sleep(80)
	if legendas != '':
		player.setSubtitles(legendas)

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

############################################################################################################
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

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        estilo=urllib.unquote_plus(params["estilo"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        senha=urllib.unquote_plus(params["senha"])
except:
        pass
try:
		idCanal=urllib.unquote_plus(params["idCanal"])
except:
		pass
try:
		idffCanal=params["idffCanal"]
except:
		pass
try:
		srtfilm=urllib.unquote_plus(params["srtfilm"])
except:
		pass
try:
		tipologia=urllib.unquote_plus(params["tipologia"])
except:
		pass
try:
        descricao=urllib.unquote_plus(params["descricao"])
except:
        pass
try:
		tipo_user=urllib.unquote_plus(params["tipo_user"])
except:
		pass
try:
		servidor_user=urllib.unquote_plus(params["servidor_user"])
except:
		pass
try:
		s_serv=urllib.unquote_plus(params["lolserv"])
except:
		pass
try:
		s_user=urllib.unquote_plus(params["loluser"])
except:
		pass
try:
		s_pass=urllib.unquote_plus(params["lolpass"])
except:
		pass

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1: menu()
elif mode==1: listar_grupos(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,s_serv,s_user,s_pass)
elif mode==2: listar_canais_url(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,s_serv,s_user,s_pass)
elif mode==3: listar_grupos_adultos(str(url),str(senha),estilo,tipologia,tipo_user,servidor_user,s_serv,s_user,s_pass)
elif mode==4: player1(name,url,iconimage)
elif mode==5: listar_videos_M18(url)
elif mode==6: listar_series(url)
elif mode==7: listar_series_f2(name,url)	
elif mode==8: pesquisa_serie()
elif mode==9: listar_animes(url)
elif mode==10: minhaConta(str(name),estilo)
elif mode==11: categorias()
elif mode==12: listar_temporadas(url)
elif mode==13: listar_videos(url)
elif mode==14: pesquisa_filme()
elif mode==20: listamenusseries(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,iconimage,s_serv,s_user,s_pass)
elif mode==21: listamenusfilmes(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,iconimage,s_serv,s_user,s_pass)
elif mode==22: listaseries(estilo)
elif mode==23: listafilmes(estilo)
elif mode==31: programacao_canal(idCanal)
elif mode==105: play_mult_canal(url, iconimage, name, tipo_user)
elif mode==1000: abrirDefinincoes()
elif mode==2000: abrirNada()
elif mode==333: play_srt(str(name),str(url),iconimage,srtfilm)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
