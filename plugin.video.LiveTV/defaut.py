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
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,threading,xbmcvfs,cookielib,sys,platform,time,gzip,glob,datetime,thread
from t0mm0.common.net import Net
import xml.etree.ElementTree as ET

####################################################### CONSTANTES #####################################################

global g_timer

macaddr = ''
_tipouser = ''
__estilagem__ = 'novo'
__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo("id")
__ADDON__	= xbmcaddon.Addon(__ADDON_ID__)
__CWD__ = xbmc.translatePath( __ADDON__.getAddonInfo('path') ).decode("utf-8")
__ADDON_FOLDER__	= __ADDON__.getAddonInfo('path')
__SETTING__	= xbmcaddon.Addon().getSetting
__ART_FOLDER__	= os.path.join(__ADDON_FOLDER__,'resources','img')
__FANART__ 		= os.path.join(__ADDON_FOLDER__,'fanart.jpg')
__SKIN__ = 'v1'
__SITE__ = 'http://www.pcteckserv.com/GrupoKodi/PHP/'
__SITEAddon__ = 'http://www.pcteckserv.com/GrupoKodi/Addon/'
__EPG__ = 'http://www.pcteckserv.com/GrupoKodi/epg.gz'
__FOLDER_EPG__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.LiveTV/').decode('utf-8'), 'epg')
__ALERTA__ = xbmcgui.Dialog().ok
__COOKIE_FILE__ = os.path.join(xbmc.translatePath('special://userdata/addon_data/plugin.video.LiveTV/').decode('utf-8'), 'cookie.livetv')
__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

#reload(sys)
#sys.setdefaultencoding('utf-8')

###################################################################################
#                              Iniciar Addon		                                  #
###################################################################################
  
def menu():
	check_login = login()
	if check_login['user']['nome'] != '':
		if check_login['sucesso']['resultado'] == 'yes':
			xbmc.executebuiltin("XBMC.Notification(Live!t TV, Sessão iniciada: "+ check_login['user']['nome'] +", '10000', "+__ADDON_FOLDER__+"/icon.png)")
			menus = {
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
			menus['nome'] = "Participacoes"
			menus['logo'] = check_login['info']['logo']
			menus['link'] = check_login['info']['link']
			menus['tipo'] = "patrocinadores"
			menus['senha'] = ""
			#check_login['menus'].append(menus)
			Menu_inicial(check_login)
			if check_login['datafim']['data'] != "Membro Ativo Sem Doacao!":
				#addDir('Favoritos', __SITE__+'favoritos.php', None, 11, 'Miniatura', __SITEAddon__+"Imagens/favoritos.png",'','','','')
				addDir(check_login['datafim']['data'], 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/estadomembro.png",'','','','')
				#thread.start_new_thread(obter_ficheiro_epg, ())
			#addDir('A Minha Conta', 'url', None, 10, 'Miniatura', __SITEAddon__+"Imagens/estadomembro.png",'','','',check_login['datafim']['data'])
			#addDir('Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','')
		elif check_login['sucesso']['resultado'] == 'utilizador':
			__ALERTA__('Live!t TV', 'Utilizador incorreto.')
			addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','')
			addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','')
		elif check_login['sucesso']['resultado'] == 'senha':
			__ALERTA__('Live!t TV', 'Senha incorreta.')
			addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','')
			addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','')
		elif check_login['sucesso']['resultado'] == 'ativo':
			__ALERTA__('Live!t TV', 'O estado do seu Utilizador encontra-se Inactivo. Para saber mais informações entre em contacto pelo email registoliveit@pcteckserv.com.')
		else:
			__ALERTA__('Live!t TV', 'Não foi possível abrir a página. Por favor tente novamente.')
	else:
		addDir('Alterar Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','')
		addDir('Entrar novamente', 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/retroceder.png",'','','','')

	xbmc.executebuiltin("Container.SetViewMode(500)")
###################################################################################
#                              Login Addon		                                  #
###################################################################################
def minhaConta(data_user):
	addDir(data_user, 'url', None, None, 'Miniatura', __SITEAddon__+"Imagens/estadomembro.png",'','','','')
	addDir('Definições', 'url', None, 1000, 'Miniatura', __SITEAddon__+"Imagens/definicoes.png",'','','','')

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
			'link': ''
		},
		'menus': []
	} # 
	
	if __ADDON__.getSetting("login_name") == '' or __ADDON__.getSetting('login_password') == '':
		__ALERTA__('Live!t TV', 'Precisa de definir o seu Utilizador e Senha')
		return informacoes
	else:
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
					print("Não sei o que estou a ler")
		except:
			__ALERTA__('Live!t TV', 'Não foi possível abrir a página. Por favor tente novamente.')
			return informacoes

		return informacoes

###############################################################################################################
#                                                   Menus                                                     #
###############################################################################################################

def Menu_inicial(men):
	_tipouser = men['user']['tipo']
	_servidoruser = men['user']['servidor']
	for menu in men['menus']:
		nome = menu['nome']
		logo = menu['logo']
		link = menu['link']
		tipo = menu['tipo']
		senha = menu['senha']
		if(tipo == 'Adulto'):		
			addDir(nome,link,senha,3,'Miniatura',logo,tipo,_tipouser,_servidoruser,'')
		elif(tipo == 'patrocinadores'):
			addDir(nome,link,None,1,'Lista',logo,tipo,_tipouser,_servidoruser,'')
		elif(tipo == 'Filme'):
			addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servidoruser,'')
		elif(tipo == 'Serie'):
			addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servidoruser,'')
		else:
			if _tipouser == 'Administrador' or _tipouser == 'Patrocinador' or _tipouser == 'PatrocinadorPagante':
				if nome == 'TVs':
					addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servidoruser,'')
					addDir('TVs-Free',link,None,1,'Miniatura',logo,tipo,_tipouser,_servidoruser,'')
				else:
					addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servidoruser,'')
			else:
				addDir(nome,link,None,1,'Miniatura',logo,tipo,_tipouser,_servidoruser,'')

	thread.start_new_thread( obter_ficheiro_epg, () )

def listar_grupos_adultos(url,senha,estilo,tipo,tipo_user,servidor_user):
	passa = True
	if tipo_user == 'Teste':
		passa = False
		__ALERTA__('Live!t TV', 'Não tem acesso a este menu. Faça a sua doação.')	
	if passa == True:
		if(__ADDON__.getSetting("login_adultos") == ''):
			__ALERTA__('Live!t TV', 'Preencha o campo senha para adultos.')
		elif(__ADDON__.getSetting("login_adultos") != senha):
			__ALERTA__('Live!t TV', 'Senha para adultos incorrecta. Verifique e tente de novo.')
		else:
			listar_grupos('',url,estilo,tipo,tipo_user,servidor_user)
	
def listar_grupos(nome_nov,url,estilo,tipo,tipo_user,servidor_user):
	passa = True
	if passa == True:
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
						addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'')
					elif servidor_user == 'Servidor1':
						addDir(nomee,urlllserv1,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'')
					elif servidor_user == 'Servidor2':
						addDir(nomee,urlllserv2,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'')
					else:
						addDir(nomee,urlllserv3,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'')
				elif tipo_user == 'Patrocinador':
					if nome_nov == 'TVs-Free':
						addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'')
				else:
					addDir(nomee,urlll,None,2,paramss[0],imag,tipo,tipo_user,servidor_user,'')
			except:
				pass
		estiloSelect = returnestilo(estilo)
		xbmc.executebuiltin(estiloSelect)
	
def listar_canais_url(nome,url,estilo,tipo,tipo_user,servidor_user):
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
				img = params[1].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http')
				rtmp = params[2].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').replace('utilizadorliveit',__ADDON__.getSetting("login_name")).replace('senhaliveit',__ADDON__.getSetting("login_password"))
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

					addLink(nomewp,rtmp,img,id_it,srt_f,descri,tipo,id_p,infoLabels,total)
			except:
				pass
		estiloSelect = returnestilo(estilo)
		xbmc.executebuiltin(estiloSelect)

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
	addDir('Entrar novamente', 'url', None, None, 'Lista Grande', __SITEAddon__+"Imagens/retroceder.png",'','','','')
	xbmc.executebuiltin("Container.SetViewMode(51)")

def abrirNada():
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
def addDir(name,url,senha,mode,estilo,iconimage,tipo,tipo_user,servidor_user,data_user,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&senha="+str(senha)+"&estilo="+urllib.quote_plus(estilo)+"&tipologia="+str(tipo)+"&tipo_user="+str(tipo_user)+"&servidor_user="+str(servidor_user)+"&data_user="+str(data_user)
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
	
def addLink(name,url,iconimage,idCanal,srtfilm,descricao,tipo,id_p,infoLabels,total=1):
	cm=[]
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	if tipo == 'Filme' or tipo == 'Serie':
		u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=333&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)+ "&srtfilm=" + urllib.quote_plus(srtfilm)
	else:
		if tipo != 'Praia':
			#cm.append(('Adicionar a Favoritos', 'XBMC.RunPlugin(%s?mode=55&name=%s&url=%s&iconimage=%s&idCanal=%s&idffCanal=%s)'%(sys.argv[0],urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), idCanal, id_p)))
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
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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
		data_user=urllib.unquote_plus(params["data_user"])
except:
		pass

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1: menu()
elif mode==1: listar_grupos(str(name),str(url),estilo,tipologia,tipo_user,servidor_user)
elif mode==2: listar_canais_url(str(name),str(url),estilo,tipologia,tipo_user,servidor_user)
elif mode==3: listar_grupos_adultos(str(url),str(senha),estilo,tipologia,tipo_user,servidor_user)
elif mode==10: minhaConta(data_user)
elif mode==1000: abrirDefinincoes()
elif mode==2000: abrirNada()
elif mode==31: programacao_canal(idCanal)
elif mode==333: play_srt(str(name),str(url),iconimage,srtfilm)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
