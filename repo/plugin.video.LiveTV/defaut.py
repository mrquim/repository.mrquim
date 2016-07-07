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
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,glob,threading,gzip,xbmcvfs,cookielib,pprint,datetime,thread,time
import xml.etree.ElementTree as ET
from datetime import date
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

####################################################### CONSTANTES #####################################################

global g_timer

__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo("id")
__ADDON__	= xbmcaddon.Addon(__ADDON_ID__)
__ADDONVERSION__ = __ADDON__.getAddonInfo('version')
__CWD__ = xbmc.translatePath( __ADDON__.getAddonInfo('path') ).decode("utf-8")
__ADDON_FOLDER__	= __ADDON__.getAddonInfo('path')
__SETTING__	= xbmcaddon.Addon().getSetting
__ART_FOLDER__	= __ADDON_FOLDER__ + '/resources/img/'
__FANART__ 		= os.path.join(__ADDON_FOLDER__,'fanart.jpg')
_ICON_ = __ADDON_FOLDER__ + '/icon.png'
__SKIN__ = 'v2'
__SITE__ = 'http://liveitkodi.com/PHP/'
__SITEAddon__ = 'http://liveitkodi.com/Addon/'
__EPG__ = 'http://liveitkodi.com/epg.gz'
__FOLDER_EPG__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.LiveTV/').decode('utf-8'), 'epglive')
__ALERTA__ = xbmcgui.Dialog().ok
__COOKIE_FILE__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.LiveTV/').decode('utf-8'), 'cookie.liveittv')
__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
debug = __ADDON__.getSetting('debug')
check_login = {}
__PASTA_DADOS__ = Addon(__ADDON_ID__).get_profile().decode("utf-8")
__PASTA_FILMES__ = xbmc.translatePath(__ADDON__.getSetting('bibliotecaFilmes'))
__PASTA_SERIES__ = xbmc.translatePath(__ADDON__.getSetting('bibliotecaSeries'))
__SITEFILMES__ = 'http://kodi.mrpiracy.club/'

###################################################################################
#                              Iniciar Addon		                                  #
###################################################################################
def addon_log(string):
	if debug == 'true':
		xbmc.log("[addon.live!t-tv-%s]: %s" %(__ADDONVERSION__, string))

def menu():
	if (not __ADDON__.getSetting('login_name') or not __ADDON__.getSetting('login_password')):
		__ALERTA__('Live!t TV', 'Precisa de definir o seu Utilizador e Senha')
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
				menus3['nome'] = "Pesquisa"
				menus3['logo'] = os.path.join(__ART_FOLDER__, __SKIN__, 'pesquisa.png')
				menus3['link'] = __SITEFILMES__
				menus3['tipo'] = "pesquisa"
				menus3['senha'] = ""
				check_login['menus'].append(menus3)
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
		
		vista_menu()
		#xbmc.executebuiltin("Container.SetViewMode(500)")

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

def login2():
	resultado = True
	try:
		net = Net()
		dados = {'email': __ADDON__.getSetting("email"), 'password': __ADDON__.getSetting("password"), 'lembrar_senha': 'lembrar'}
		codigo_fonte = net.http_POST(__SITEFILMES__+'login_bd.php',form_data=dados,headers=__HEADERS__).content.encode('utf-8')
		match = re.compile('class="myAccount">(.+?)<\/a>').findall(codigo_fonte)
	except:
		resultado = False
		match = ''
		return resultado

	if match == []:
		match = re.compile('class="myAccount">(.+?)<\/a>').findall(codigo_fonte)
		if match == []:
			resultado = False
			return resultado
		else:
			resultado = True
			return resultado
	else:
		net.save_cookies(__COOKIE_FILE__)
		resultado = True
		return resultado

###############################################################################################################
#                                                   Menus                                                     #
###############################################################################################################

def Menu_inicial(men):
	_tipouser = men['user']['tipo']
	_servuser = men['user']['servidor']
	_nomeuser = men['user']['nome']
	#_nomeuser = 'Live!t-TV ('+men['user']['nome']+')'
	for menu in men['menus']:
		nome = menu['nome']
		logo = menu['logo']
		link = menu['link']
		tipo = menu['tipo']
		senha = menu['senha']
		if tipo == 'Adulto' :
			addDir(nome,link,senha,3,'Miniatura',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif tipo == 'patrocinadores' or tipo == 'novidades':
			addDir(nome,link,None,1,'Lista',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif(tipo == 'Filme'):
			addDir(nome,link,None,21,'Miniatura',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif(tipo == 'Serie'):
			addDir(nome,link,None,20,'Miniatura',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif(tipo == 'estado'):
			addDir(nome,link,None,10,'Lista',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
		elif(tipo == 'pesquisa'):
			if _tipouser != 'Teste':
				addDir(nome,link,None,120,'Lista',logo,tipo,_tipouser,_servuser,'','','','')
		else:
			if _tipouser == 'Administrador' or _tipouser == 'Patrocinador' or _tipouser == 'PatrocinadorPagante':
				if nome == 'TVs':
					addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
					addDir('TVs-Free',link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
				else:
					addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
			else:
				addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servuser,'',men['info']['log'],men['info']['user'],men['info']['password'])
	
	#xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(_nomeuser, Versão do addon: '+_VERSAO_, 8000, _ICON_))
	thread.start_new_thread( obter_ficheiro_epg, () )
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%('Live!t-TV','Secção Iniciada: '+_nomeuser, 8000, _ICON_))
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
	if passa:
		if(__ADDON__.getSetting("login_adultos") == ''):
			__ALERTA__('Live!t TV', 'Preencha o campo senha para adultos.')
		elif(__ADDON__.getSetting("login_adultos") != senha):
			__ALERTA__('Live!t TV', 'Senha para adultos incorrecta. Verifique e tente de novo.')
		else:
			listar_grupos('',url,estilo,tipo,tipo_user,servidor_user,sserv,suser,spass)

def listar_grupos(nome_nov,url,estilo,tipo,tipo_user,servidor_user,sservee,suseree,spassee):
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
				paramss = estil.split('\n')
				if tipo_user == 'Administrador' or tipo_user == 'Pagante' or tipo_user == 'PatrocinadorPagante':
					if nome_nov == 'TVs-Free':
						addDir(nomee,urlll,None,2,'TesteServer',imag,tipo,tipo_user,servidor_user,'',sservee,suseree,spassee)
					elif servidor_user == 'Servidor1':
						addDir(nomee,urlllserv1,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
					elif servidor_user == 'Servidor2':
						addDir(nomee,urlllserv2,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
					else:
						addDir(nomee,urlllserv3,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'','','','')
				elif tipo_user == 'Patrocinador':
					if nome_nov == 'TVs-Free':
						addDir(nomee,urlll,None,2,'TesteServer',imag,tipo,tipo_user,servidor_user,'','','','')
				else:
					if tipo_user == 'Teste':
						if servidor_user == "Teste":
							addDir(nomee,urlll,None,2,'TesteServer',imag,tipo,tipo_user,servidor_user,'',sservee,suseree,spassee)
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
	
	vista_menu()
	#estiloSelect = returnestilo(estilo)
	#xbmc.executebuiltin(estiloSelect)	

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
						infoLabels = {'title':nomewp, 'plot':plot, 'writer': argumento, 'director':realizador, 'genre':detalhes1, 'year': detalhes2, 'aired':detalhes2, 'IMDBNumber':imdb, 'votes':votes, "credits": nomewp}
					else:
						infoLabels = {"title": nomewp, "genre": tipo, "credits": nomewp}
					
					if estilo == 'TesteServer':
						urlteste = rtmp.split('TSDOWNLOADER')
						tttot = len(urlteste)
						if tttot == 1:
							addLink(nomewp,rtmp,img,id_it,srt_f,descri,tipo,tipo_user,id_p,infoLabels,total)
						else:
							addLink(nomewp,'plugin://plugin.video.f4mTester/?url='+rtmp,img,id_it,srt_f,descri,tipo,tipo_user,id_p,infoLabels,total)
					else:
						addLink(nomewp,rtmp,img,id_it,srt_f,descri,tipo,tipo_user,id_p,infoLabels,total)
			except:
				pass
		
		if tipo == 'patrocinadores' or tipo == 'novidades' or tipo == 'Praia' or tipo == 'pesquisa' or tipo == 'estado' or tipo == 'ProgramasTV':
			estiloSelect = returnestilo(estilo)
			xbmc.executebuiltin(estiloSelect)
		else:
			vista_Canais()

###############################################################################################################
#                                                   EPG                                                     #
###############################################################################################################
def obter_ficheiro_epg():
	if not xbmcvfs.exists(__FOLDER_EPG__):
		xbmcvfs.mkdirs(__FOLDER_EPG__)

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
def menuFilmes():
	database = Database.isExists()
	addDir2('Filmes', __SITEFILMES__+'kodi_filmes.php', 111, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'filmes.png'))
	addDir2('', '', '', __FANART__, 0, poster=os.path.join(__ART_FOLDER__,'nada.png'))
	addDir2('Filmes por Ano', __SITEFILMES__+'kodi_filmes.php', 119, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'))
	addDir2('Filmes por Genero', __SITEFILMES__+'kodi_filmes.php', 118, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'genero.png'))

	vista_menu()

def menuSeries():
	database = Database.isExists()
	addDir2('Series', __SITEFILMES__+'kodi_series.php', 111, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'series.png'))
	addDir2('', '', '', __FANART__, 0, poster=os.path.join(__ART_FOLDER__,'nada.png'))
	addDir2('Series por Ano', __SITEFILMES__+'kodi_series.php', 119, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'))
	addDir2('Series por Genero', __SITEFILMES__+'kodi_series.php', 118, __FANART__, 1, poster=os.path.join(__ART_FOLDER__, __SKIN__, 'genero.png'))

	vista_menu()

def removerAcentos(txt, encoding='utf-8'):
	return normalize('NFKD', txt.decode(encoding)).encode('ASCII','ignore')

def getList(url, pagina):
	tipo = ''
	categoria = ''
	naovai = False
	net = Net()
	net.set_cookies(__COOKIE_FILE__)
	try:
		codigo_fonte = net.http_GET(url, headers=__HEADERS__).content.encode('utf8')
	except:
		naovai = True
	if naovai == False:
		if 'kodi_filmes.php' in url:
			tipo = 'kodi_filmes'
		elif 'kodi_series.php' in url:
			tipo = 'kodi_series'

		anoLink = ''
		if 'ano' in url:
			try:
				anoLink = re.compile('ano(.+?)&').findall(url)[0]
			except:
				anoLink = re.compile('&ano(.+?)').findall(url)[0]
			anoLink = '&ano'+anoLink

		if 'categoria=' in url:
			categoria = re.compile('categoria=(.+[0-9])').findall(url)[0]

		if tipo == 'kodi_filmes':
			match = re.compile('<div\s+class="movie-info">\s+<a\s+href="(.+?)"\s+class="movie-name">.+?<\/a>\s+<d.+?><\/div>\s+<d.+?>\s+<d.+?>\s+<span\s+class="genre">(.+?)<\/span>').findall(codigo_fonte)
		elif tipo == 'kodi_series':
			match = re.compile('<div\s+class="movie-info">\s+<a\s+href="(.+?)"\s+class="movie-name">.+?<\/a>\s+<d.+?><\/div>\s+<d.+?>\s+<d.+?>\s+<span\s+class="genre">(.+?)<\/span>').findall(codigo_fonte)
		database = Database.isExists()
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
				addVideo(nomeOriginal+' ('+ano+')', __SITEFILMES__+"kodi_"+link, 113, fanart, 'filme', 0, 0, infoLabels, poster)
		else:
			for link, cat in match:
				idIMDB = re.compile('imdb=(.+)').findall(link)[0]
				if not idIMDB.startswith('tt'):
					continue
				idIMDB = re.compile('imdb=(tt[0-9]{7})').findall(link)[0]
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
				addDir2(nomeOriginal, __SITEFILMES__+"kodi_"+link, 114, fanart, pagina, 'serie', infoLabels, poster)
		if categoria == '':
			addDir2('Proximo', __SITEFILMES__+tipo+'.php?pagina='+str(int(pagina)+1)+''+anoLink, 111, __FANART__, int(pagina)+1, poster= os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'))
		else:
			addDir2('Proximo', __SITEFILMES__+tipo+'.php?pagina='+str(int(pagina)+1)+'&categoria='+categoria+''+anoLink, 111, __FANART__, int(pagina)+1, poster= os.path.join(__ART_FOLDER__, __SKIN__, 'proximo.png'))
		vista_filmesSeries()
	else:
		__ALERTA__('Live!t-TV', 'Não foi possível abrir a página. Por favor tente novamente mais tarde.')

def getSeasons(url):
	net = Net()
	codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

	match = re.compile('<div\s+class="season"><a\s+href="(.+?)">(.+?)<\/a><\/div>').findall(codigo_fonte)
	match += re.compile('<div\s+class="season"><a\s+href="(.+?)" >(.+?)<\/a><\/div>').findall(codigo_fonte)

	for link, temporada in match:
		if '" class="slctd' in link:
			link = re.compile('(.+?)" class="slctd').findall(link)[0]
		addDir2Season("[B]Temporada[/B] "+temporada, __SITEFILMES__+"kodi_"+link, 115, os.path.join(__ART_FOLDER__, __SKIN__, 'temporadas', 'temporada'+temporada+'.png'), 1, temporada)
	vista_temporadas()

def getEpisodes(url):
	net = Net()
	net.set_cookies(__COOKIE_FILE__)
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
			infoEpis = json.loads(Trakt.getTVDBByEpSe(imdbid, temporada, episodio))

			Database.insertEpisodio(infoEpis["name"], infoEpis["plot"], infoEpis["imdb"], infoEpis["tvdb"], infoEpis["season"], infoEpis["episode"], infoEpis["fanart"], infoEpis["poster"], infoEpis["aired"], infoEpis["serie"], infoEpis["traktid"], actores=infoEpis['actors'])
			infoLabels = {'Title':infoEpis["name"], 'Actors':infoEpis['actors'], 'Plot':infoEpis["plot"], 'Season':infoEpis["season"], 'Episode':infoEpis["episode"], "Code":imdbid, 'Aired': infoEpis["aired"] }
			poster = infoEpis["poster"]
			fanart = infoEpis["fanart"]
			nomeEpisodio = infoEpis["name"]
			temporadaEpisodioDB = infoEpis["season"]
			numeroEpisodioDB = infoEpis["episode"]
			serieTitulo = infoEpis["serie"]
		else:
			infoLabels = {'Title':episodioInfo[0], 'Actors':episodioInfo[7], 'Plot':episodioInfo[1], 'Season':episodioInfo[2], 'Episode':episodioInfo[3], "Code":imdbid, 'Aired': episodioInfo[6] }
			poster = episodioInfo[5]
			fanart = episodioInfo[4]
			nomeEpisodio = episodioInfo[0]
			temporadaEpisodioDB = episodioInfo[2]
			numeroEpisodioDB = episodioInfo[3]
			serieTitulo = episodioInfo[11]

		addVideo('[B]Episodio '+episodioN+'[/B] | '+nomeEpisodio, __SITEFILMES__+"kodi_"+link, 113, fanart, 'episodio', temporadaEpisodioDB, numeroEpisodioDB, infoLabels, poster, serieTitulo)

	vista_episodios()

def getStreamLegenda(siteBase, codigo_fonte):
	stream = ''
	legenda = ''
	net = Net()
	servidor = ''
	titulos = []
	links = []
	legendas = []
	stuff = []
	i = 1
	if siteBase == 'serie.php':
		match = re.compile('<div\s+id="welele"\s+link="(.+?)"\s+legenda="(.+?)">').findall(codigo_fonte)
		match += re.compile('<div\s+id="welele2"\s+link="(.+?)"\s+legenda="(.+?)">').findall(codigo_fonte)
		for link, legenda in match:
			titulos.append('Servidor #%s' % i)
			links.append(link)
			if not '.srt' in legenda:
				legend = legenda+'.srt'
			legendas.append('http://mrpiracy.club/subs/%s' % legenda)
			i = i+1

	else:
		match = re.compile('<div\s+id="(.+?)"\s+link="(.+?)">').findall(codigo_fonte)
		legendaAux = ''
		for idS, link in match:
			if 'legenda' in idS:
				if not '.srt' in link:
					link = link+'.srt'
				legendaAux = 'http://mrpiracy.club/subs/%s' % link
				continue
			if 'videomega' in idS:
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
			legenda = legendaAux
		elif 'server.mrpiracy.club' in links[servidor]:
			stream = links[servidor]
			legenda = legendaAux
		elif 'openload' in links[servidor]:
			stream = URLResolverMedia.OpenLoad(links[servidor]).getMediaUrl()
			legenda = URLResolverMedia.OpenLoad(links[servidor]).getSubtitle()
		elif 'drive.google.com/' in links[servidor]:
			stream = URLResolverMedia.GoogleVideo(links[servidor]).getMediaUrl()
			legenda = legendaAux
	else:
		if 'server.mrpiracy.club' in links[0]:
			stream = links[0]
			legenda = legendas[0]
		elif 'uptostream.com' in links[0]:
			stream = URLResolverMedia.UpToStream(links[0]).getMediaUrl()
			legenda = legendas[0]
		elif 'drive.google.com/' in links[0]:
			stream = URLResolverMedia.GoogleVideo(links[0]).getMediaUrl()
			legenda = legendas[0]
		elif 'openload' in links[0]:
			stream = URLResolverMedia.OpenLoad(links[0]).getMediaUrl()
			legenda = URLResolverMedia.OpenLoad(links[0]).getSubtitle()

	return stream, legenda

def pesquisa(urlpa,tipp_uss,tipooo,servuss):
	codigo_fonte = ''
	dados = ''
	net = Net()
	net.set_cookies(__COOKIE_FILE__)
	
	dialog = xbmcgui.Dialog()
	server = dialog.select(u'Onde quer pesquisar?', ['Filmes', 'Series', 'Canais', 'Praias', 'Rádios'])
	
	if server == 0:
		site = urlpa+'kodi_procurarf.php'
	elif server == 1:
		site = urlpa+'kodi_procurars.php'
	elif server == 2 or  server == 3 or server == 4:
		site = __SITE__+'search.php'
	
	teclado = xbmc.Keyboard('', 'O que quer pesquisar?')
	teclado.doModal()
	
	if teclado.isConfirmed():
		strPesquisa = teclado.getText()
		if server == 2 or  server == 3 or server == 4:
			tabela = ''
			if server == 2:
				tabela = 'canais_kodi'
			elif server == 3:
				tabela = 'praias_kodi'
			elif server == 4:
				tabela = 'radios_kodi'
			else:
				tabela = 'programas_kodi'
			
			dados = {'searchBox': strPesquisa, 'tabela': tabela}
			codigo_fonte = net.http_POST(site, form_data=dados, headers=__HEADERS__).content
		else:
			dados = {'searchBox': strPesquisa}
		
		if server == 0 or server == 1:
			check_login = login2()
			net = Net()
			net.set_cookies(__COOKIE_FILE__)
			codigo_fonte = net.http_POST(site, form_data=dados, headers=__HEADERS__).content.encode('utf8')
			match = re.compile('<div\s+class="movie-info".+>\s+<a\s+href="(.+?)".+class="movie-name">.+?<\/a>\s+<d.+\s+<d.+\s+<d.+\s+<span\s+class="genre">(.+?)<\/span>').findall(codigo_fonte)
			if match != []:
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
						
						addVideo(nomeOriginal+' ('+ano+')', __SITEFILMES__+"kodi_"+link, 113, fanart, 'filme', 0, 0, infoLabels, poster)
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
						
						addDir2(nomeOriginal, __SITEFILMES__+"kodi_"+link, 114, fanart, pagina, 'serie', infoLabels, poster)
						
				vista_filmesSeries()
			else:
				addDir2('Voltar', 'url', None, os.path.join(__ART_FOLDER__, __SKIN__, 'retroceder.png'), 0)
				vista_filmesSeries()
		else:
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
					for g in child:
						adiciona = True
						if(g.tag == 'Nome'):
							canal['nome'] = g.text
						elif(g.tag == 'Imagem'):
							canal['logo'] = g.text
						elif(g.tag == 'Url'):
							urlchama = g.text.split(';')
							urlnoo = ''
							try:
								urlnoo = urlchama[2]
								if(servuss == 'Servidor1'):
									urlnoo = urlchama[0]
								elif(servuss == 'Servidor2'):
									urlnoo = urlchama[1]
								elif(servuss == 'Servidor3'):
									urlnoo = urlchama[2]
								
								if(urlnoo == 'nada'):
									adiciona = False
								else:
									canal['link'] = informa['servidor']['serv']+'/live/utilizadorliveit/senhaliveit/'+urlnoo
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
				addDir2('Voltar', 'url', None, os.path.join(__ART_FOLDER__, __SKIN__, 'retroceder.png'), 0)
				vista_filmesSeries()
	else:
		addDir2('Voltar', 'url', None, os.path.join(__ART_FOLDER__, __SKIN__, 'retroceder.png'), 0)
		vista_filmesSeries()

def download(url,name, temporada,episodio,serieNome):

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

    match = re.compile('<a id="(.+?)" class="btn(.+?)?" onclick=".+?"><img src="(.+?)"><\/a>').findall(codigo_fonte)

    if isFilme:
        linkOpenload = re.compile('<iframe id="reprodutor" src="(.+?)" scrolling="no"').findall(codigo_fonte)[0]
    else:
        linkOpenload = re.compile('<iframe src="(.+?)" scrolling="no"').findall(codigo_fonte)[0]

    idOpenLoad = URLResolverMedia.OpenLoad(linkOpenload).getId()

    legenda = URLResolverMedia.OpenLoad(linkOpenload).getSubtitle()
    stream = URLResolverMedia.OpenLoad('https://openload.co/f/'+idOpenLoad+'/').getDownloadUrl()

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
	net = Net()
	codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

	match = re.compile('<label for="genre1" id="genre1Label"><a style="font-family: Tahoma; color: #8D8D8D;font-size: 11px;padding-left: 5px;float: left;width: 142px;font-weight: normal;text-decoration: initial;" href="(.+?)">(.+?)<\/a><\/label>').findall(codigo_fonte)
	match += re.compile('<label for="genre1" id="genre1Label"><a style="font-family: Tahoma; color: #8D8D8D;font-size: 11px;padding-left: 5px;float: left;width: 142px;text-decoration: initial;" href="(.+?)">(.+?)<\/a><\/label>').findall(codigo_fonte)
	
	for link, nome in match:
		if 'kodi_filmes.php' in url:
			addDir2(nome.encode('utf8'), __SITEFILMES__+"kodi_"+link, 111, os.path.join(__ART_FOLDER__, __SKIN__, 'genero.png'), 1)
		else:
			addDir2(nome.encode('utf8'), url+link, 111, os.path.join(__ART_FOLDER__, __SKIN__, 'genero.png'), 1)

def getYears(url):
	net = Net()
	codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

	match = re.compile('<label for="(.+?)" id="(.+?)"><a style=\'font-family: Tahoma; color: #8D8D8D;\' class="active" href="(.+?)">(.+?)<\/a><\/label>').findall(codigo_fonte)
	for lixo1, lixo2, link, nome in match:
		addDir2(nome.encode('utf-8'), url+link, 111, os.path.join(__ART_FOLDER__, __SKIN__, 'ano.png'), 1)

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

def addDir2Season(name,url,mode,iconimage,pagina,temporada):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&pagina="+str(pagina)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&temporada="+str(temporada)
    ok=True
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    liz=xbmcgui.ListItem(name, iconImage="fanart.jpg", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', __FANART__)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

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

    xbmc.executebuiltin("XBMC.Notification(Live!t-TV,"+"Marcado como visto"+","+"6000"+","+ os.path.join(__ADDON_FOLDER__,'icon.png')+")")
    xbmc.executebuiltin("Container.Refresh")

def addVideo(name,url,mode,iconimage,tipo,temporada,episodio,infoLabels,poster,serieNome=False):
	menu = []

	try:
		name = name.encode('utf-8')
	except:
		name = name

	if tipo == 'filme':
		xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
		#visto = checkVisto(url)
		idIMDb = re.compile('imdb=(tt[0-9]{7})').findall(url)[0]
		if __ADDON__.getSetting('trailer-filmes') == 'true':
			linkTrailer = getTrailer(idIMDb)
		else:
			linkTrailer = ''
	elif tipo == 'serie':
		xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
		#visto = checkVisto(url, temporada, episodio)
		idIMDb = re.compile('imdb=(tt[0-9]{7})&').findall(url)[0]
		linkTrailer = ""
	elif tipo == 'episodio':
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		#visto = checkVisto(url, temporada, episodio)
		idIMDb = re.compile('imdb=(tt[0-9]{7})&').findall(url)[0]
		linkTrailer = ""
	else:
		xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
		linkTrailer = ""
	
	overlay = 6
	playcount = 0

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

	menu.append(('Download', 'XBMC.RunPlugin(%s?mode=117&name=%s&url=%s&iconimage=%s&serieNome=%s&temporada=%s&episodio=%s)'%(sys.argv[0],urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(serieNome), str(temporada), str(episodio))))
	liz.addContextMenuItems(menu, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def clean(text):
    command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def player(name,url,iconimage,temporada,episodio,serieNome):

	pastaData = ''
	stream = False
	net = Net()
	net.set_cookies(__COOKIE_FILE__)
	codigo_fonte = net.http_GET(url, headers=__HEADERS__).content

	infolabels = dict()

	if temporada == 0 and episodio == 0:
		pastaData = __PASTA_DADOS__
		idIMDb = re.compile('imdb=(tt[0-9]{7})').findall(url)[0]
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
	mensagemprogresso.create('Live!t-TV', u'Abrir emissão','Por favor aguarde...')
	mensagemprogresso.update(25, "", u'Obter video e legenda', "")

	try: stream, legenda = getStreamLegenda(siteBase, codigo_fonte)
	except: stream = False

	mensagemprogresso.update(50, "", u'Prepara-te, vai começar!', "")

	playlist = xbmc.PlayList(1)
	playlist.clear()
	listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)

	listitem.setInfo(type="Video", infoLabels=infolabels)
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	if stream != False:
		listitem.setPath(path=stream)
		playlist.add(stream, listitem)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
		mensagemprogresso.update(75, "", u'Boa Sessão!!!', "")

	if stream == False:
		__ALERTA__('Live!t-TV', 'O servidor escolhido não disponível, escolha outro ou tente novamente mais tarde.')
	else:
		player_mr = Player.Player(url=url, idFilme=idIMDb, pastaData=pastaData, temporada=temporada, episodio=episodio, nome=name, ano=ano, logo=os.path.join(__ADDON_FOLDER__,'icon.png'), serieNome=serieNome)

		mensagemprogresso.close()
		player_mr.play(playlist)
		player_mr.setSubtitles(legenda)

		while player_mr.playing:
			xbmc.sleep(5000)
			player_mr.trackerTempo()

###################################################################################
#                               FUNCOES JA FEITAS                                 #
###################################################################################
def abrirNada():
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
def addDir(name,url,senha,mode,estilo,iconimage,tipo,tipo_user,servidor_user,data_user,sserv,suser,spass,pasta=True,total=1):
	if(tipo == 'pesquisa'):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&tipologia="+str(tipo)+"&tipo_user="+str(tipo_user)+"&servidor_user="+str(servidor_user)
	else:
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&senha="+str(senha)+"&estilo="+urllib.quote_plus(estilo)+"&tipologia="+str(tipo)+"&tipo_user="+str(tipo_user)+"&servidor_user="+str(servidor_user)+"&data_user="+str(data_user)+"&lolserv="+sserv+"&loluser="+suser+"&lolpass="+spass
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	
	liz.setProperty('fanart_image', iconimage)
	liz.setArt({'fanart': os.path.join(__ART_FOLDER__, __SKIN__, 'fundo_addon.png')})

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def addFolder(name,url,mode,iconimage,folder):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
	return ok

def addLink(name,url,iconimage,idCanal,srtfilm,descricao,tipo,tipo_user,id_p,infoLabelssss,total=1):
	ok=True
	cm=[]
	if tipo != 'Praia' and tipo != 'ProgramasTV' and tipo != 'Filme' and tipo != 'Serie' and tipo != 'Adulto':
		cm.append(('Ver programação', 'XBMC.RunPlugin(%s?mode=31&name=%s&url=%s&iconimage=%s&idCanal=%s&idffCanal=%s)'%(sys.argv[0],urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), idCanal, id_p)))
	liz=xbmcgui.ListItem(label=str(name), iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo( type="Video", infoLabels=infoLabelssss)
	liz.addContextMenuItems(cm, replaceItems=False)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

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

def addLink2(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir2(name,url,mode,iconimage,pagina,tipo=None,infoLabels=None,poster=None):
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
	
def vista_Canais():
	opcao = __ADDON__.getSetting('canaisView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
	elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
	elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
	elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")

def abrirDefinincoes():
	__ADDON__.openSettings()
	addDir2('Entrar novamente', 'url', None, None, 'Lista Grande', __SITEAddon__+"Imagens/retroceder.png",'','','','','','','')
	xbmc.executebuiltin("Container.SetViewMode(51)")

def vista_menu():
	opcao = __ADDON__.getSetting('menuView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51")
	elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")

def vista_filmesSeries():
	opcao = __ADDON__.getSetting('filmesSeriesView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
	elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
	elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
	elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")


def vista_temporadas():
	opcao = __ADDON__.getSetting('temporadasView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")

def vista_episodios():
	opcao = __ADDON__.getSetting('episodiosView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(509)")
	elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(504)")
	elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(503)")
	elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(515)")

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
legenda=None
pagina=None
temporada=None
episodio=None
serieNome=None

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

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1:
	menu()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1: listar_grupos(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,s_serv,s_user,s_pass)
elif mode==2: listar_canais_url(str(name),str(url),estilo,tipologia,tipo_user,servidor_user,s_serv,s_user,s_pass)
elif mode==3: listar_grupos_adultos(str(url),str(senha),estilo,tipologia,tipo_user,servidor_user,s_serv,s_user,s_pass)
elif mode==10: minhaConta(str(name),estilo)
elif mode==20: menuSeries()
elif mode==21: menuFilmes()
elif mode==31: programacao_canal(idCanal)
elif mode==110: minhaConta2()
elif mode==111: getList(url, pagina)
elif mode==112: getSeries(url, pagina)
elif mode==113: player(name, url, iconimage, temporada, episodio, serieNome)
elif mode==114: getSeasons(url)
elif mode==115: getEpisodes(url)
elif mode==117: download(url, name, temporada, episodio, serieNome)
elif mode==118: getGeneros(url)
elif mode==119: getYears(url)
elif mode==120: pesquisa(url,tipo_user,tipologia,servidor_user)
elif mode==1000: abrirDefinincoes()
elif mode==2000: abrirNada()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
