#!/usr/bin/python
# -*- coding: utf-8 -*-

import urlparse,json,zlib,hashlib,urllib2,time,re,os,sys,xbmc,xbmcgui,xbmcplugin,xbmcvfs,pprint, base64
import unicodedata
import URLResolverMedia
reload(sys)  
sys.setdefaultencoding('utf8')

global arrgrupos
global arrlinks

arrgrupos = []
arrlinks = []

class TVArchive:
	def __init__(self):
		self.arrgrupos = []
		self.arrlinks = []
		self.API = base64.urlsafe_b64decode('aHR0cDovL21wYXBpLm1sLw==')
		self.API_SITE = base64.urlsafe_b64decode('aHR0cDovL21wYXBpLm1sL2FwaS8=')
		self.SITE = base64.urlsafe_b64decode('aHR0cDovL21ycGlyYWN5LmdxLw==')
		
	def getInfo(self, url, username, password):
		urllis = 'http://mikkm.xyz/android/androidApi.php?mode=timeshift&url='+url+'&username='+username+'&password='+password
		page_with_xml = urllib2.urlopen(urllis).readlines()
		num = 0
		groupant = ''
		grouicon = ''
		menus_Grupos = []
		menus_Link = []
		logo2 = ''
		menulk = {
			'nome': '',
			'logo': '',
			'link': ''
		}
		data_nn = ''
		namechann = ''
		logoicon = ''
		
		if(page_with_xml != ''):
			for line in page_with_xml:
				objecto = line.decode('latin-1').encode("utf-8")
				if(num == 0):
					app2 = objecto.split(' group-title="')
					app22 = app2[1].split('" tvg-logo=')
					app3 = objecto.split(' tvg-logo="')
					app33 = app3[1].split('",')
					grouppp = app22[0]
					if(groupant != grouppp):
						groupant = app22[0]
						grouicon = app33[0]
						menugr = {
								'nome': '',
								'logo': '',
								'menu_data': []
							}
						menugr['nome'] = groupant
						menugr['logo'] = grouicon
						menus_Grupos.append(menugr)
						arrgrupos.append(menugr)
					
					for menu1 in menus_Grupos:
						logo1 = menu1['logo']
						if(grouppp == menu1['nome']):
							app4 = objecto.split(',')
							app5 = app4[1].split('(')
							data_nn = app5[0].split(') ')
							
							menudt = {
								'nome': '',
								'logo': ''
							}
							menudt['nome'] = data_nn
							menudt['logo'] = logo1
							menu1['menu_data'].append(menudt)
							break
					
					for menu2 in menus_Grupos:
						logo2 = menu2['logo']
						if(grouppp == menu2['nome']):
							app4 = objecto.split(',')
							app5 = app4[1].split('(')
							data_nn = app5[0].split(') ')
							for menu3 in menu2['menu_data']:
								if(data_nn == menu3['nome']):
									namechann = app4[1]
									logoicon = logo2
									break
					
					num = 1	
				else:
					num = 0
					if(namechann != ''):
						menulk = {
							'nome': '',
							'logo': '',
							'data_nova': '',
							'link': ''
						}
						menulk['nome'] = namechann
						menulk['logo'] = logo2
						menulk['data_nova'] = data_nn
						menulk['link'] = objecto
						arrlinks.append(menulk)
						
						namechann = ''
						logoicon = ''
						logo2 = ''
			
			self.arrgrupos = arrgrupos
			self.arrlinks = arrlinks
			return arrgrupos
		else:
			__ALERTA__('Live!t-TV', 'Não tem canais em gravação.')
			return None
	
	def __ALERTA__(text1="",text2="",text3=""):
		if text3=="": xbmcgui.Dialog().ok(text1,text2)
		elif text2=="": xbmcgui.Dialog().ok("",text1)
		else: xbmcgui.Dialog().ok(text1,text2,text3)
	
	def buscarArrGrupos(self):
		return arrgrupos

	def buscarLinks(self):
		return arrlinks