#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"

'''*
	Copyright (C) 2015 DudeHere

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

*'''

import sys
import re
import xbmc
import xbmcaddon
import xbmcgui
from resources.constants import *
from resources.i18n_strings import STRINGS as STRINGS_MAP
from dudehere.routines import *
from dudehere.routines.constants import WINDOW_ACTIONS
from dudehere.routines.i18nlib import i18n, LANGUAGE_PATH
from dudehere.routines.vfs import VFSClass
from dudehere.routines.plugin import Plugin, TextBox, ProgressBar, ContextMenu
plugin =  Plugin(default_views=VIEWS)

STRINGS = STRINGS_MAP()
'''*  	Validation functions 
		
		These functions are passed to some of the menu or context menu entries
		where needed. Trakt authorization dependent functions are passed validate_trakt
		for example, which simply checks to see if trakt as been authorized.
		A dependent menu would then be visible or hidden based on the result.
		This could be more complicated in the future. 

*'''


def validate_trakt():
	return ADDON.get_setting('trakt_authorized') == "true"

def validate_advanced():
	return ADDON.get_setting('advanced_mode') == "true"

def validate_watched():
	if ADDON.get_setting('trakt_authorized') == "false" or ADDON.get_setting('advanced_mode') == "false":
		return False
	return ADDON.get_setting('hide_watched_episodes') == "true"

def validate_transmogrifier():
	installed = xbmc.getCondVisibility('System.HasAddon(service.transmogrifier)') == 1
	if installed:
		return ADDON.get_setting('enable_transmogrifier') == "true"
	else:
		return False

def validate_transmogrifier_streaming():
	if validate_transmogrifier() and ADDON.get_setting('enable_transmogrifier_streaming') == "true":
		return True
	else:
		return False

def validate_source_filter():
	return validate_advanced() and ADDON.get_setting('enable_result_filters') == 'true'

'''*	I want the context menu to be empty by default except for the items defined in this array
		Plugin.replace_context_menu_by_default is False by default and so any default or menu dependent
		context menu items would be added to the system default.
*'''

plugin.replace_context_menu_by_default = ADDON.get_setting('enable_full_context') == 'false'
plugin.set_default_context_menu([
	('Enable/Disable Scrapers', {"mode": "scraper_list"}, True),
	('Set Result Filters', {'mode': 'set_source_filter'}, True, validate_source_filter),
	('Hide Watched', {'mode': 'toggle_hide_watched'}, True, (validate_watched()==False and validate_trakt())),
	('Show Watched', {'mode': 'toggle_hide_watched'}, True, validate_watched),
	('Enable Transmogrifier Streaming', {'mode': 'toggle_transmogrifier_streaming'}, True, (validate_transmogrifier() and validate_transmogrifier_streaming()==False)),
	('Disable Transmogrifier Streaming', {'mode': 'toggle_transmogrifier_streaming'}, True, validate_transmogrifier_streaming),
	('Transmogrifier Queue', {'mode': 'manage_transmogrifier'}, True, validate_transmogrifier)
])

def update_run():
	if plugin.check_version(ADDON.get_setting('version'), '0.8.0'):
		ADDON.set_setting('database_sqlite_init', "false")
		ADDON.set_setting('database_sqlite_init.cache', "false")
		ADDON.set_setting('database_mysql_init', "false")
		ADDON.set_setting('database_mysql_init.cache', "false")
		ADDON.set_setting('database_mysql_version', "1")
		ADDON.set_setting('database_mysql_version.cache', "1")
		first_run(True)
plugin.update_run = update_run

'''* 	Initial Run routine
		Plugin.first_run method
		This is called after every mode function is loaded prior to the final dispatch call.
		By default it does nothing, however here It is used to launch a setup wizard to walk
		through some basic settings.
		
		Plugin.run first check is the setting `setup_run` is false, if so the first_run method is called
		This must be added to the addon settings.xml file otherwise it won't be updated to true at the finalization
		of the first_run method.
*'''

def first_run(update=False):
	'''* 	We want to make sure the settings.xml file is generated, otherwise the guide does not save its output.
			For some reason it may not get created prior to the setup running and the it needs to run twice.
			plugin.initialize_settings reads the defaults settings and writes them to the settings.xml file.
	*'''
	plugin.initialize_settings(update)
	vfs = VFSClass()
	from dudehere.routines.window import Window
	from dudehere.routines.manager import Manager
	class FirstPage(Window):
		def set_info_controls(self):
			content = '''Welcome to back to The Royal We\nI've missed you!\n\nThis brief setup will get TRW up and running.\n\nFor support go to:\n[COLOR blue]http://tvaddons.ag[/COLOR]'''
			self.add_label(self.create_label(content), 0, 0, columnspan=4, rowspan=5, pad_x=15, pad_y=10)
	
	class SecondPage(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title, width=800, height=450, columns=4, rows=6)
			self.overide_strings = {"next_button": "ACCEPT"}
			
		def set_info_controls(self):	
			path = vfs.join(LANGUAGE_PATH, 'disclosure.txt', True)
			content  = vfs.read_file(path)
			self.add_label(self.create_label(content), 0, 0, columnspan=4, rowspan=5, pad_x=15, pad_y=10)
			
			self.create_button("decline", "I Decline")
			self.add_object("decline", 5, 2)
			def decline():
				self.close()
				plugin.exit()
			self.set_object_event("action", "decline", decline)
			
	class ThirdPage(Window):	
		def set_info_controls(self):
			content = '''The Royal We can be used in Basic or Advanced Mode.\nTRW is intended to require minimal configuration.\nIf that is what you want, just leave it.\nAdvanced Mode enables some setting and customization.'''
			self.add_label(self.create_label(content), 0, 0, columnspan=4, rowspan=3, pad_x=15, pad_y=10)
			
			self.create_list('usage')
			self.add_object('usage', 2,0,3,4)
			self.add_list_items('usage', ["Basic Mode", "Advanced Mode"], 0, allow_multiple=False, allow_toggle=False)
	
	class FourthPage(Window):
		def authorize(self):
			pin = self.get_value('pin')
			from dudehere.routines.trakt import TraktAPI
			trakt = TraktAPI()
			response = trakt.authorize(pin)
			if response:
				settings = trakt.get_settings()
				if settings:
					ADDON.set_setting('trakt_account', settings['user']['username'])
				plugin.notify("Trakt Authorization", "Success", image=ARTWORK + "trakt.png")	
			else:
				ADDON.set_setting('trakt_account', '')
				plugin.notify("Trakt Authorization", "Failed", image=ARTWORK + "trakt.png")

		def set_info_controls(self):
			self.create_image('trakt', ARTWORK + 'trakt.png', aspectRatio=1)
			self.add_object('trakt', 0, 0, columnspan=3, rowspan=3)
			
			content = '''[B]The Royal We is even better with a Trakt.TV account.\nIf you have one, you may authorize it now.\nOtherwise you can use TRW without trakt.\nYou can always authorize or re-authorize TRW.\nJust look in the Settings Menu.[/B]'''
			self.add_label(self.create_label(content), 0, 0, columnspan=3, rowspan=3, pad_x=15, pad_y=10)
			
			content = "Open a browser and navigate to:\n[B][COLOR red]%s[/COLOR][/B]" % ADDON.get_setting('trakt_pin_url')
			self.add_label(self.create_label(content), 3, 0, columnspan=3, rowspan=2, pad_x=15, pad_y=10)
			
			self.create_input('pin', _alignment=2)
			self.add_object('pin', 4, 0, columnspan=3)
			
			self.create_image('qr_code', ARTWORK + 'pin.png', aspectRatio=2)
			self.add_object('qr_code', 0, 3, columnspan=1, rowspan=2)
			
			self.create_button('authorize', 'Authorize')
			self.add_object('authorize', 4, 3)
			self.set_object_event('action', "authorize", self.authorize)	
	
	class FifthPage(Window):
		def set_info_controls(self):
			from dudehere.routines.scrapers import CommonScraper
			Scraper = CommonScraper(load='all')
			items = []
			services = {}
			for index in xrange(len(Scraper.supported_scrapers)):
				if Scraper.get_scraper_by_index(index) is None: continue
				name = Scraper.get_scraper_by_index(index).name
				services[name] = Scraper.get_scraper_by_index(index).service
				if Scraper.get_scraper_by_index(index).require_auth: items.append(name)
			
			content = '''Some scrapers require accounts to enable.\nIf you have an account for any of the following, you can enter it now.'''
			self.add_label(self.create_label(content), 0, 0, columnspan=4, rowspan=2, pad_x=15, pad_y=10)
			def set_account():
				from dudehere.routines.window import TEXTURES
				name = self.get_object("scrapers").getSelectedItem().getLabel()
				service = services[name]
				success = scraper_account(name, service)
				if success: self.get_object("scrapers").getSelectedItem().setIconImage(TEXTURES + 'checked.png')
			
			self.create_list('scrapers')
			self.add_object('scrapers', 2,0,3,4)
			self.add_list_items('scrapers', items, selectable=False, call_back=set_account)
	
	class SixthPage(Window):
		def set_info_controls(self):
			content = '''Using TRW should be pretty easy.\nThere are several lists and ways to search or find TV Shows and Movies.\nJust as before, TRW searches a bunch of sites for sources, but now no caching.\nTRW now uses several public indexes for its content.\nIf a site isn't working or down/responding slowly, disable if from the settings.\nSome sites require accounts, TRW works fine without them.'''
			self.add_label(self.create_label(content), 0, 0, columnspan=4, rowspan=3, pad_x=15, pad_y=10)
			
			self.create_button('finalize', 'Finish Setup')
			self.add_object('finalize', 5, 3)
			
	class ConfirmationPage(Window):	
		def set_info_controls(self):
			bg = vfs.join(ROOT_PATH, 'resources/artwork/confirmation.gif')
			self.create_image('background', bg, aspectRatio=0)
			self.add_object('background', 0, 0, rowspan=6, columnspan=3, pad_x=0, pad_y=0)
			content = '''You did it!\nFor support go to tvaddons.ag'''
			self.add_label(self.create_label(content, alignment=0, font="font18", textColor="0xFFF266CF"), 0, 0, columnspan=3, rowspan=5, pad_x=15, pad_y=15)		
			
	WM = Manager()
	WM.add_page(FirstPage('Welcome to The Royal We: v%s!' % VERSION))
	WM.add_page(SecondPage('Disclosures: v%s!' % VERSION))
	WM.add_page(ThirdPage('Usage Mode: v%s!' % VERSION))
	WM.add_page(FourthPage('Trakt.TV: v%s!' % VERSION))
	WM.add_page(FifthPage('Scraper Accounts: v%s!' % VERSION))
	WM.add_page(SixthPage('Basic Usage: v%s!' % VERSION))
	WM.add_confirmation(ConfirmationPage('Setup Complete!'))
	WM.build()
	
	WM.set_object_event(0, 'focus', 'next_button')
	WM.set_object_event(1, 'focus', 'decline')
	WM.set_object_event(1, 'left', 'next_button', 'decline')
	WM.set_object_event(1, 'left', 'decline', 'previous_button')
	WM.set_object_event(1, 'right', 'previous_button', 'decline')
	WM.set_object_event(1, 'right', 'decline', 'next_button')
	WM.set_object_event(2, 'focus', 'next_button')
	WM.set_object_event(2, 'left', 'next_button', 'previous_button')
	WM.set_object_event(2, 'right', 'previous_button', 'next_button')
	WM.set_object_event(2, 'up', 'next_button', 'usage')
	WM.set_object_event(2, 'up', 'previous_button', 'usage')
	WM.set_object_event(2, 'down', 'usage', 'next_button')
	WM.set_object_event(3, 'focus', 'next_button')
	WM.set_object_event(3, 'left', 'next_button', 'previous_button')
	WM.set_object_event(3, 'right', 'previous_button', 'next_button')
	WM.set_object_event(3, 'up', 'next_button', 'pin')
	WM.set_object_event(3, 'up', 'previous_button', 'pin')
	WM.set_object_event(3, 'down', 'pin', 'next_button')
	WM.set_object_event(3, 'down', 'authorize', 'next_button')
	WM.set_object_event(3, 'right', 'pin', 'authorize')
	WM.set_object_event(3, 'left', 'authorize', 'pin')
	WM.set_object_event(4, 'focus', 'next_button')
	WM.set_object_event(4, 'left', 'next_button', 'previous_button')
	WM.set_object_event(4, 'right', 'previous_button', 'next_button')
	WM.set_object_event(4, 'up', 'next_button', 'scrapers')
	WM.set_object_event(4, 'up', 'previous_button', 'scrapers')
	WM.set_object_event(4, 'down', 'scrapers', 'next_button')
	WM.set_object_event(5, 'focus', 'finalize')
	WM.set_object_event(5, 'left', 'finalize', 'previous_button')
	WM.set_object_event(5, 'right', 'previous_button', 'finalize')
	def finalize():
		WM.show_confirmation()
		ADDON.set_setting('setup_run', 'true')
		ADDON.set_setting('version', VERSION)
		usage_mode = WM.get_value(2, 'usage')
		if usage_mode[1]:
			ADDON.set_setting('advanced_mode', 'true')
	WM.set_object_event(5, 'action', 'finalize', finalize)
	WM.show()
	
plugin.first_run = first_run	


'''* 	Menu Functions
		Plugin.register(mode, function)
		This maps mode to a specific function.
		Pretty straight forward if you 
*'''

def main():
	plugin.add_menu_item({'mode': 'tv_menu'}, {'title': STRINGS.map('tv_menu')}, image=ARTWORK + "tvshows.jpg")
	plugin.add_menu_item({'mode': 'movie_menu'}, {'title': STRINGS.map('movie_menu')}, image=ARTWORK + "movies.jpg")
	plugin.add_menu_item({'mode': 'settings_menu'}, {'title': STRINGS.map('settings_menu')}, image=ARTWORK + "settings.jpg")
	plugin.add_menu_item({'mode': 'show_about'}, {'title': STRINGS.map('show_about')}, image=ARTWORK + "about.jpg")
	plugin.add_menu_item({'mode': 'authorize_trakt'}, {'title': STRINGS.map('authorize_trakt')}, image=ARTWORK + "authorize.jpg", visible=validate_trakt()==False)
	plugin.eod(clear_search=True)
plugin.register('main', main)

def tvshow_menu():
	plugin.add_menu_item({'mode': 'tv_favorites'}, {'title': STRINGS.map('my_favorites')}, image=ARTWORK + "favorites.jpg", visible=validate_trakt()==False)
	plugin.add_menu_item({'mode': 'calendar'}, {'title': STRINGS.map('calendar')}, image=ARTWORK + "calendar.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'calendar_browser'}, {'title': STRINGS.map('calendar_browser')}, image=ARTWORK + "calendar_browser.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'tv_genres'}, {'title': STRINGS.map('genres')}, image=ARTWORK + "genres/genre.jpg")
	plugin.add_menu_item({'mode': 'tv_watchlist'}, {'title': STRINGS.map('tv_watchlist')}, image=ARTWORK + "trakt_watchlist.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'tv_collection'}, {'title': STRINGS.map('my_collection')}, image=ARTWORK + "my_collection.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'tv_custom_lists'}, {'title': STRINGS.map('custom_lists')}, image=ARTWORK + "trakt_custom_lists.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'tv_trending'}, {'title': STRINGS.map('tv_trending')}, image=ARTWORK + "trakt_trending.jpg")
	plugin.add_menu_item({'mode': 'tv_popular'}, {'title': STRINGS.map('tv_popular')}, image=ARTWORK + "trakt_popular.jpg")
	plugin.add_menu_item({'mode': 'tv_recommended'}, {'title': STRINGS.map('tv_recommended')}, image=ARTWORK + "trakt_recommended.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'tv_anticipated'}, {'title': STRINGS.map('tv_anticipated')}, image=ARTWORK + "trakt_anticipated.jpg")
	plugin.add_menu_item({'mode': 'tv_networks'}, {'title': "Networks"}, image=ARTWORK + "networks.jpg")
	plugin.add_menu_item({'mode': 'tv_search'}, {'title': STRINGS.map('search')}, image=ARTWORK + "search.jpg")
	plugin.eod(clear_search=True)
plugin.register('tv_menu', tvshow_menu)

def tv_genres():
	from dudehere.routines.tmdb import TV_GENRES as GENRES
	for id in sorted(GENRES.r_map.keys()):
		genre = GENRES.r_map[id].lower()
		plugin.add_menu_item({'mode': 'tv_genre', "id": id}, {'title': genre}, image=ARTWORK + "genres/%s.jpg" % genre)
	plugin.eod(VIEWS.LIST)
plugin.register("tv_genres", tv_genres)	

def tv_networks():
	vfs = VFSClass()
	from dudehere.routines.tmdb import TV_NETWORK_TABLE
	for network in sorted(TV_NETWORK_TABLE.keys()):
		id = TV_NETWORK_TABLE[network]
		image = "networks/%s.png" % re.sub(r'\W+', '', network.lower())
		image = vfs.join(ARTWORK, image)
		plugin.add_menu_item({'mode': 'tv_network', "id": id}, {'title': network}, image=image)
	plugin.eod(VIEWS.LIST)
plugin.register("tv_networks", tv_networks)	

def movie_menu():
	plugin.add_menu_item({'mode': 'movie_favorites'}, {'title': STRINGS.map('my_favorites')}, image=ARTWORK + "favorites.jpg", visible=validate_trakt()==False)
	plugin.add_menu_item({'mode': 'movie_watchlist'}, {'title': STRINGS.map('movie_watchlist')}, image=ARTWORK + "trakt_watchlist.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'movie_collection'}, {'title': STRINGS.map('my_collection')}, image=ARTWORK + "my_collection.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'movie_genres'}, {'title': STRINGS.map('genres')}, image=ARTWORK + "genres/genre.jpg")
	plugin.add_menu_item({'mode': 'movie_custom_lists'}, {'title': STRINGS.map('custom_lists')}, image=ARTWORK + "trakt_custom_lists.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'movie_trending'}, {'title': STRINGS.map('movie_trending')}, image=ARTWORK + "trakt_trending.jpg")
	plugin.add_menu_item({'mode': 'movie_popular'}, {'title': STRINGS.map('movie_popular')}, image=ARTWORK + "trakt_popular.jpg")
	plugin.add_menu_item({'mode': 'movie_recommended'}, {'title': STRINGS.map('movie_recommended')}, image=ARTWORK + "trakt_recommended.jpg", visible=validate_trakt)
	plugin.add_menu_item({'mode': 'movie_search'}, {'title': STRINGS.map('search')}, image=ARTWORK +"search.jpg")
	plugin.add_menu_item({'mode': 'movie_discover'}, {'title': STRINGS.map('movie_discover')}, image=ARTWORK +"discover.jpg")
	plugin.eod(clear_search=True)
plugin.register('movie_menu', movie_menu)

def movie_genres():
	from dudehere.routines.tmdb import MOVIE_GENRES as GENRES
	for id in sorted(GENRES.r_map.keys()):
		genre = GENRES.r_map[id].lower()
		plugin.add_menu_item({'mode': 'movie_genre', "id": id}, {'title': genre}, image=ARTWORK + "genres/%s.jpg" % genre)
	plugin.eod(VIEWS.LIST, 'tvshows', clear_search=True)
plugin.register("movie_genres", movie_genres)	

def settings_menu():
	plugin.add_menu_item({'mode': 'scraper_list'}, {'title': STRINGS.map('scraper_list')}, image=ARTWORK + "scraper_list.jpg")
	plugin.add_menu_item({'mode': 'scraper_accounts'}, {'title': STRINGS.map('scraper_accounts')}, image=ARTWORK + "none")
	plugin.add_menu_item({'mode': 'set_source_filter'}, {'title': 'Set Result Filters'}, image=ARTWORK + "none", visible=validate_source_filter)
	plugin.add_menu_item({'mode': 'manage_hosts'}, {'title': STRINGS.map('manage_hosts')}, image=ARTWORK + "none", visible=validate_advanced())
	plugin.add_menu_item({'mode': 'manage_transmogrifier'}, {'title': STRINGS.map('manage_transmogrifier')}, image=ARTWORK + "none", visible=validate_transmogrifier)
	plugin.add_menu_item({'mode': 'settings_transmogrifier'}, {'title': STRINGS.map('settings_transmogrifier')}, image=ARTWORK + "none", visible=validate_transmogrifier)
	plugin.add_menu_item({'mode': 'settings_urlresolver'}, {'title': STRINGS.map('settings_urlresolver')}, image=ARTWORK + "none")
	plugin.add_menu_item({'mode': 'settings_theroyalwe'}, {'title': STRINGS.map('settings_theroyalwe')}, image=ARTWORK + "none")
	plugin.add_menu_item({'mode': 'authorize_trakt'}, {'title': STRINGS.map('authorize_trakt')}, image=ARTWORK + "authorize.jpg")
	plugin.add_menu_item({'mode': 'advanced_mode'}, {'title': STRINGS.map('enable_basic_mode')}, image=ARTWORK + "none", visible=validate_advanced())
	plugin.add_menu_item({'mode': 'advanced_mode'}, {'title': STRINGS.map('enable_advanced_mode')}, image=ARTWORK + "none", visible=validate_advanced() is False)
	plugin.add_menu_item({'mode': 'reset_trw'}, {'title': STRINGS.map('reset_trw')}, image=ARTWORK + "reset.jpg")
	plugin.eod(VIEWS.LIST, clear_search=True)
plugin.register('settings_menu', settings_menu)

'''* 	Media Search and List Functions
*'''

def tv_discover():
	from dudehere.routines.tmdb import TMDB_API
	tmdb = TMDB_API()
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	if validate_trakt():
		watchlist = trakt.get_watchlist_tvshows(simple=True, id_type='tmdb')
	else:
		watchlist = []
	page = int(plugin.args['page']) if 'page' in plugin.args.keys() else 1
	if plugin.mode == "tv_genre":
		results = tmdb.list_tv_genre(plugin.args['id'], page=page)
	elif plugin.mode == 'tv_network':
		results = tmdb.list_tv_network(plugin.args['id'], page=page)
	count = len(results)
	total_pages = results['total_pages']
	for result in results['results']:
		record = tmdb.process_record(result, 'tvshow')
		menu = ContextMenu()
		menu.add('Find Similar Shows', {"mode": "tv_similar", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']})
		menu.add('Save as Favorite', {"mode": "add_to_favorites", "media": "tvshow",  "record": record}, script=True, visible=validate_trakt()==False)
		
		if record['tmdb_id'] in watchlist:
			record['title'] = '[COLOR %s]%s[/COLOR]' % (WATCHLIST_COLOR, record['title'])
			menu.add('Remove from Watchlist', {"mode": "tv_delete_from_watchlist", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "name": record['title']}, script=True, visible=validate_trakt)
		else:
			menu.add('Add to Watchlist', {"mode": "tv_add_to_watchlist", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']}, script=True, visible=validate_trakt)
		menu.add('Add to custom list', {"mode": "add_to_custom_list", "media": "tvshow", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']}, script=True, visible=validate_trakt)
		plugin.add_menu_item({'mode': 'season_list', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "fanart": record['backdrop_url']}, record, menu=menu, image=record['cover_url'], fanart=record['backdrop_url'])
	if total_pages > 1: plugin.add_menu_item({'mode': plugin.mode, "id": plugin.args['id'], "page": page+1}, {'title': '[COLOR blue]Next Page %s/%s >>[/COLOR]' % (page+1, total_pages)}, image=ARTWORK + "next_page.jpg")
	plugin.eod(VIEWS.LIST, 'tvshows')
plugin.register(["tv_genre", "tv_network"], tv_discover)

def tv_list():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	if plugin.mode == 	'tv_watchlist' or validate_trakt() == False:
		watchlist = []
	else:
		watchlist = trakt.get_watchlist_tvshows(simple=True)
	regex = re.compile("^(A )|(An )|(The )", re.IGNORECASE)
	def sort_results(title):
		title = regex.sub('', title['show']['title'], re.IGNORECASE)
		return title.lower()
	if plugin.mode == 		'tv_favorites':
		results = get_tv_favorites()	
	elif plugin.mode == 		'tv_watchlist':
		results = trakt.get_watchlist_tvshows()
		if not results: return
		results.sort(key=lambda k: sort_results(k))
	elif plugin.mode == 	'tv_trending':
		results = trakt.get_trending_tvshows()
	elif plugin.mode == 	'tv_anticipated':
		results = trakt.get_anticipated_tvshows()	
	elif plugin.mode == 	'tv_popular':
		results = trakt.get_popular_tvshows()
	elif plugin.mode ==		'tv_recommended':
		results = trakt.get_recommended_tvshows()
		if not results: return
	elif plugin.mode ==		'tv_collection':
		results = trakt.get_collected_tvshows()
		if not results: return
		results.sort(key=lambda k: sort_results(k))
	elif plugin.mode ==		'tv_custom_list':
		if 'username' in plugin.args:
			results = trakt.get_custom_list(plugin.args['slug'], 'tvshows', username=plugin.args['username'])
		else:
			results = trakt.get_custom_list(plugin.args['slug'], 'tvshows')
		if not results: return	
		results.sort(key=lambda k: sort_results(k))
	elif plugin.mode ==		'tv_search':
		query = plugin.get_property('search.query.refesh')
		if query:
			plugin.clear_property('search.query')
			plugin.clear_property('search.query.refesh')
		else:
			query = plugin.dialog_input('Search Shows')
		if query is None: 
			plugin.clear_property("search.query")
			return
		plugin.set_property('search.query', query)
		results = trakt.search(query, 'show')
	elif plugin.mode == 	'tv_similar':
		imdb_id = trakt.query_id('tmdb', plugin.args['tmdb_id']) if plugin.args['imdb_id'] == 'None' else plugin.args['imdb_id']
		results = trakt.get_similar_tvshows(imdb_id)
	if not results:
		return
	for record in results:
		if plugin.mode != 'tv_favorites':
			record = trakt.process_record(record, media='tvshow')
		else:
			record['cast'] = []
		menu = ContextMenu()
		menu.add('Find Similar Shows', {"mode": "tv_similar", "imdb_id": record['imdb_id']})
		if plugin.mode == 	'tv_watchlist':
			menu.add('Remove from Watchlist', {"mode": "tv_delete_from_watchlist", "imdb_id": record['imdb_id'], "name": record['title']}, script=True, visible=validate_trakt)
		else:
			if record['imdb_id'] in watchlist: 
				record['title'] = '[COLOR %s]%s[/COLOR]' % (WATCHLIST_COLOR, record['title'])
				menu.add('Remove from Watchlist', {"mode": "tv_delete_from_watchlist", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "trakt_id": record['trakt_id'], "name": record['title']}, script=True, visible=validate_trakt)
			else:
				menu.add('Add to Watchlist', {"mode": "tv_add_to_watchlist", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "trakt_id": record['trakt_id']}, script=True, visible=validate_trakt)
				
		if plugin.mode ==	'tv_custom_list':
			menu.add('Remove from custom list', {"mode": "delete_from_custom_list", "media": "tvshow", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "trakt_id": record['trakt_id'], "slug": plugin.args['slug'], "name": record['title']}, script=True, visible=validate_trakt)
		else:
			menu.add('Add to custom list', {"mode": "add_to_custom_list", "media": "tvshow", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "trakt_id": record['trakt_id']}, script=True, visible=validate_trakt)
		
		if plugin.mode ==	'tv_favorites':
			menu.add('Delete Favorite', {"mode": "delete_from_favorites", "media": "tvshow", "title": record['title'], "id": record['id']}, script=True, visible=validate_trakt()==False)
		else:
			menu.add('Save as Favorite', {"mode": "add_to_favorites", "media": "tvshow",  "record": record}, script=True, visible=validate_trakt()==False)
		query = {
			'mode': 'season_list',
			"trakt_id": record['trakt_id'], 
			"imdb_id": record['imdb_id'],
			"tmdb_id": record['tmdb_id'],
			"slug": record['slug'],
			"fanart": record['backdrop_url']
		}
		plugin.add_menu_item(query, record, menu=menu, replace_menu=True, image=record['cover_url'], fanart=record['backdrop_url'])
	ADDON.save_data('last_directory.qs', sys.argv[0]+sys.argv[2])
	plugin.eod(VIEWS.TV_DEFAULT, 'tvshows')	
plugin.register(['tv_watchlist', 'tv_trending', 'tv_popular', 'tv_recommended', 'tv_custom_list', 'tv_search', 'tv_similar', 'tv_anticipated', 'tv_collection', 'tv_favorites'], tv_list)

def season_list():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	imdb_id = trakt.query_id('tmdb', plugin.args['tmdb_id']) if 'tmdb_id' in plugin.args.keys() else plugin.args['imdb_id']
	if plugin.get_arg('slug'):
		results = trakt.get_show_seasons(plugin.args['slug'])
	else:
		results = trakt.get_show_seasons(imdb_id)
	if not results:
		return
	for record in results:
		if record['number'] > 0:
			menu = ContextMenu()
			season_id = record['ids']['trakt']
			image = record['images']['poster']['full']
			fanart = plugin.args['fanart']
			season = record['number']
			record = {"title": 'Season %s' % season}
			menu.add('Mark Season Watched', {"mode": "set_watched", "media": "season", "id": season, "imdb_id": imdb_id}, visible=validate_trakt)
			query = {
				'mode': 'episode_list', 
				"imdb_id": imdb_id, 
				"season": season, 
				"season_id": season_id, 
				"fanart": fanart,
				"trakt_id": plugin.get_arg('trakt_id'),
				"slug": plugin.get_arg('slug')
			}
			plugin.add_menu_item(query, record, menu=menu, image=image, fanart=fanart)
	plugin.eod(VIEWS.SEASON_DEFAULT, 'tvshows')
plugin.register('season_list', season_list)

def episode_list():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	if plugin.get_arg('slug') is not None:
		show = trakt.get_show_info(plugin.args['slug'])
		results = trakt.get_show_episodes(plugin.args['slug'], plugin.args['season'])
	else:
		show = trakt.get_show_info(plugin.args['imdb_id'])
		results = trakt.get_show_episodes(plugin.args['imdb_id'], plugin.args['season'])

	if validate_trakt():
		watched = trakt.get_watched_episodes(plugin.args['season_id'])
	else:
		watched = None
	if validate_transmogrifier():
		from dudehere.routines.transmogrifier import TransmogrifierAPI
		TM = TransmogrifierAPI()
		path, transmogrified = TM.get_videos('tv')
	else:
		transmogrified = []
		is_local = False
	if not results:
		return
	for record in results:
		record = trakt.process_record(record, media='episode', watched=watched, show=show)
		if record is False: continue
		if record['episode'] == 0: continue
		if validate_transmogrifier():
			filename = "%s %sx%s" % (utf8(show['title']), record['season'], record['episode'])
			is_local = any(filename in test for test in transmogrified)
		menu = ContextMenu()
		record['showtitle'] = show['title']
		record['year'] = show['year']
		pattern = "[COLOR "+HAS_TRANMOGRIFIED+"]%s. %s[TM][/COLOR]" if is_local else "%s. %s"
		record['title'] = pattern % (record['episode'], record['title'])
		record['imdb_id'] = plugin.args['imdb_id']
		if record['playcount'] == 0:
			menu.add('Mark Watched', {"mode": "set_watched", "media": "episode", "id": record['trakt_id'], "imdb_id": record['imdb_id']}, visible=validate_trakt)
		else:
			if ADDON.get_setting('hide_watched_episodes') == "true" : continue
			record['overlay'] = 7
			menu.add('Mark Unwatched', {"mode": "set_unwatched", "media": "episode", "id": record['trakt_id']}, visible=validate_trakt)
		if is_local:
			menu.add('Play Cache File', {'mode': 'play_tv_cache', "title": record['showtitle'], "season": record['season'], "episode": record['episode']}, visible=validate_transmogrifier)
			menu.add('Delete Cache File', {'mode': 'delete_tv_cache', "title": record['showtitle'], "season": record['season'], "episode": record['episode']}, visible=validate_transmogrifier)
		else:
			menu.add('Transmogrify', {'mode': 'tv_transmogrify', "display": record['title'], "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "showtitle": record['showtitle'], "season": record['season'], "episode": record['episode']}, visible=validate_transmogrifier)
		if ADDON.get_setting('source_selection_mode') == 'Directory':
			query = {
				'mode': 'get_episode_sources', 
				"display": record['title'], 
				"imdb_id": record['imdb_id'], 
				"tmdb_id": record['tmdb_id'], 
				"trakt_id": record['trakt_id'], 
				"year": record['year'], 
				"showtitle": record['showtitle'], 
				"season": record['season'], 
				"episode": record['episode']
			}
			plugin.add_menu_item(query, record, menu=menu, image=record['cover_url'], fanart=plugin.args['fanart'])
		else:
			query = {
				'mode': 'play_episode', 
				"display": record['title'], 
				"imdb_id": record['imdb_id'], 
				"tmdb_id": record['tmdb_id'], 
				"trakt_id": record['trakt_id'], 
				"year": record['year'], 
				"showtitle": record['showtitle'], 
				"season": record['season'], 
				"episode": record['episode']
			}
			plugin.add_video_item(query, record, menu=menu, image=record['cover_url'], fanart=plugin.args['fanart'])
	ADDON.save_data('last_directory.qs', sys.argv[0]+sys.argv[2])
	plugin.eod(VIEWS.EPISODE_DEFAULT, 'tvshows')	
plugin.register('episode_list', episode_list)
	
def calendar():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()	
	results = trakt.get_calendar_shows()
	if not results:
		return
	if validate_trakt():
		watched = trakt.get_watched_history('shows')
	count = len(results)
	if validate_transmogrifier():
		from dudehere.routines.transmogrifier import TransmogrifierAPI
		TM = TransmogrifierAPI()
		path, transmogrified = TM.get_videos('tv')
	else:
		transmogrified = []
		is_local = False
	if not results:
		return
	for record in results:
		record = trakt.process_record(record, media='episode')
		if record['season'] == 0 or record['episode'] == 0: continue
		if validate_trakt():
			if record['imdb_id'] in watched.keys():
				if record['season'] in watched[record['imdb_id']]:
					record['playcount'] = 1 if record['episode'] in watched[record['imdb_id']][record['season']] else 0
					if ADDON.get_setting('hide_watched_episodes') == "true" and record['playcount'] == 1: continue
		if validate_transmogrifier():
			filename = "%s %sx%s" % (utf8(record['showtitle']), record['season'], record['episode'])
			is_local = any(filename  in test for test in transmogrified)
		menu = ContextMenu()
		if record['playcount'] == 0:
			menu.add('Mark Watched', {"mode": "set_watched", "media": "episode", "imdb_id": record['imdb_id'], "id": record['trakt_id']})
		else:
			record['overlay'] = 7
			menu.add('Mark Unwatched', {"mode": "set_unwatched", "media": "episode", "id": record['trakt_id']})
		menu.add('Find Similar Shows', {"mode": "tv_similar", "imdb_id": record['imdb_id']})
		menu.add('Go to Seasons', {"mode": "season_list", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "slug": record['slug'], "trakt_id": record['trakt_id'],  "fanart": record['backdrop_url']})
		pattern = "[COLOR "+HAS_TRANMOGRIFIED+"]%sx%s. %s - %s [TM][/COLOR]" if is_local else "%sx%s. %s - %s"
		record['title'] = pattern % (record['season'], record['episode'], record['showtitle'], record['title'])
		if is_local:
			menu.add('Play Cache File', {'mode': 'play_tv_cache', "imdb_id": record['imdb_id'], "title": record['showtitle'], "season": record['season'], "episode": record['episode']}, visible=validate_transmogrifier, script=False)
			menu.add('Delete Cache File', {'mode': 'delete_tv_cache', "title": record['showtitle'], "season": record['season'], "episode": record['episode']}, visible=validate_transmogrifier)
		else:
			query = {'mode': 'tv_transmogrify', "display": record['title'], "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "showtitle": record['showtitle'], "season": record['season'], "episode": record['episode']}
			menu.add('Transmogrify', query, visible=validate_transmogrifier)
		if ADDON.get_setting('source_selection_mode') == 'Directory':
			query = {
				'mode': 'get_episode_sources', 
				"display": record['title'], 
				"imdb_id": record['imdb_id'], 
				"tmdb_id": record['tmdb_id'], 
				"trakt_id": record['trakt_id'], 
				"year": record['year'], 
				"showtitle": record['showtitle'], 
				"season": record['season'], 
				"episode": record['episode']
			}
			plugin.add_menu_item(query, record, total_items=count, image=record['cover_url'], fanart=record['backdrop_url'], menu=menu)
		else:
			query = {
				'mode': 'play_episode', 
				"display": record['title'], 
				"imdb_id": record['imdb_id'], 
				"tmdb_id": record['tmdb_id'], 
				"trakt_id": record['trakt_id'], 
				"year": record['year'], 
				"showtitle": record['showtitle'], 
				"season": record['season'], 
				"episode": record['episode']
			}

			plugin.add_video_item(query, record, total_items=count, image=record['cover_url'], fanart=record['backdrop_url'], menu=menu)
	ADDON.save_data('last_directory.qs', sys.argv[0]+sys.argv[2])
	plugin.eod(VIEWS.EPISODE_DEFAULT, 'tvshows')
plugin.register('calendar', calendar)

def calendar_browser():
	import datetime, json
	CONTROLS = enum(CLOSE=90003, NEXT=90005, PREVIOUS=90004, CALENDAR=90009, CALENDAR_UP=90007, CALENDAR_DOWN=90008)
	
	from dudehere.routines.trakt import TraktAPI
	from dudehere.routines.window import Window
	trakt = TraktAPI()
	if validate_trakt():
		watched = trakt.get_watched_history('shows')
	else:
		watched = {}
	class Calendar(xbmcgui.WindowXMLDialog):
		offset = 0
		last_id = 0
		calendar = "my/shows"
		calendars = ["my/shows", "my/shows/new", "my/shows/premieres", "all/shows", "all/shows/new", "all/shows/premieres"]
		calendars_display = ["My Shows", "My New Shows", "My Season Premieres", "All Shows", "All New Shows", "All Season Premieres"]
		def __init__(self, *args, **kwargs):
			xbmcgui.WindowXML.__init__(self)
			
		def onInit(self):
			if plugin.get_property('Calendar.Resume'):
				try:
					self.offset = int (plugin.get_property('Calendar.Offset'))
					self.calendar = plugin.get_property('Calendar.Calendar')
				except: pass
			plugin.clear_property('Calendar.Resume')
			plugin.clear_property('Calendar.Offset')
			plugin.clear_property('Calendar.Calendar')
			calendar = self.calendars_display[self.calendars.index(self.calendar)]
			self.getControl(CONTROLS.CALENDAR).setLabel(calendar)	
			self.load_calendar(self.offset)
		
		def show_context(self, controlID):
			show = json.loads(self.getControl(controlID).getSelectedItem().getLabel2())
			class ContextWindow(Window):
				_action = 'false'
				def __init__(self, title):
					super(self.__class__,self).__init__(title,width=300, height=220, columns=1, rows=4, quiet=True)
					
				def event(self):
					obj = self.getFocus()
					self._action = obj.getSelectedPosition()

					self.close()
				
				def set_info_controls(self):
					if show['show']['playcount'] == 1:
						items = ["Mark Unwatched", "Go to Seasons"]
					else:
						items = ["Mark Watched", "Go to Seasons"]
					if validate_transmogrifier():
						items.append("Transmogrify")
					self.create_list('dialog')
					self.add_object('dialog', 0,0,5,1)
					self.add_list_items('dialog', items, selectable=False, call_back=self.event)
					self.set_object_event('focus', 'dialog')
			CW = ContextWindow("The Royal We")
			CW.show()
			action = CW._action
			del CW
			if action == 0:
				if show['show']['playcount'] == 1:
					query = {"mode": "set_unwatched", "media": "episode", "id": show['episode']['ids']['trakt'], "imdb_id": show['show']['ids']['imdb']}
				else:
					query = {"mode": "set_watched", "media": "episode", "id": show['episode']['ids']['trakt'], "imdb_id": show['show']['ids']['imdb']}
				plugin.execute_query(query)
				self.load_calendar(self.offset)
			elif action == 1:
				query = {"mode": "season_list", "imdb_id": show['show']['ids']['imdb'],"slug": show['show']['ids']['slug'], "fanart": show['show']['images']['fanart']['full']}
				plugin.navigate_to(query)
				self.close()
			elif action == 2:
				imdb_id = show['show']['ids']['imdb']
				tmdb_id = show['show']['ids']['tmdb']
				season = show['episode']['season']
				episode = show['episode']['number']
				year = show['show']['year']
				showtitle = show['show']['title'].encode("utf-8", "ignore")
				title =  show['episode']['title'].encode("utf-8", "ignore")
				query = {'mode': 'tv_transmogrify', "display": title, "imdb_id": imdb_id, "tmdb_id": tmdb_id, "year": year, "showtitle": showtitle, "season": season, "episode": episode}
				plugin_url = plugin.build_plugin_url(query)
				plugin.execute_query(query)

		def load_calendar(self, offset=0):
			xbmc.executebuiltin( "ActivateWindow(busydialog)" )
			format = "%a %b, %d"
			
			date = datetime.date.today() - datetime.timedelta(days=offset)
			self.getControl(90013).setLabel(date.strftime(format))
			
			date = datetime.date.today() - datetime.timedelta(days=1 + offset)
			self.getControl(90012).setLabel(date.strftime(format))
			
			date = datetime.date.today() - datetime.timedelta(days=2 + offset)
			self.getControl(90011).setLabel(date.strftime(format))
			
			date = datetime.date.today() - datetime.timedelta(days=3 + offset)
			self.getControl(90010).setLabel(date.strftime(format))
			
			items = []
			shows = []

			for index in xrange(4):
				shows.append([])
				items.append( trakt.get_calendar(self.calendar, index + offset) )
				for show in items[index]:
					title = show['show']['title'].encode("utf-8", "ignore")
					if len(title)>1 and title != 'No Activity':
						w = 0
						imdb = show['show']['ids']['imdb']
						season = show['episode']['season']
						episode = show['episode']['number']
						if season == 0 or episode == 0: continue
						if imdb in watched.keys():
							if season in watched[imdb]:
								w = 1 if episode in watched[imdb][season] else 0
						show['show']['playcount'] = w
						title = "%s %sx%s" % (title, season, episode)
						icon = ARTWORK+"checked.png" if w else ''
						liz = xbmcgui.ListItem(title, iconImage=icon)
						liz.setLabel2(json.dumps(show))
						shows[index].append(liz)
			
			self.getControl(90053).reset()
			self.getControl(90052).reset()
			self.getControl(90051).reset()
			self.getControl(90050).reset()
					
			self.getControl(90053).addItems(shows[0])
			self.getControl(90052).addItems(shows[1])
			self.getControl(90051).addItems(shows[2])
			self.getControl(90050).addItems(shows[3])
			
			xbmc.executebuiltin( "Dialog.Close(busydialog)" )

		def onAction(self, action):
			action = action.getId()
			if action in [WINDOW_ACTIONS.ACTION_PREVIOUS_MENU, WINDOW_ACTIONS.ACTION_NAV_BACK]:
				self.close()
			
			try:
				if action in [WINDOW_ACTIONS.ACTION_MOUSE_RIGHT_CLICK, WINDOW_ACTIONS.ACTION_SHOW_INFO, WINDOW_ACTIONS.ACTION_CONTEXT_MENU]:
					controlID = self.getFocus().getId()
					if controlID in [90050, 90051, 90052, 90053]:
						self.show_context(controlID)	
			except:
				pass
			try:
				controlID = self.getFocus().getId()
				if controlID in [90050, 90051, 90052, 90053]:
					self.update_info(controlID)	
				else:
					self.clear_info()
			except:
				pass
				
		def onClick(self, controlID):
			if controlID == CONTROLS.CLOSE:
				self.close()
			if controlID == CONTROLS.PREVIOUS:
				self.offset += 4
				self.load_calendar(self.offset)
			if controlID == CONTROLS.NEXT:
				self.offset -= 4
				self.load_calendar(self.offset)
			
			if controlID in [CONTROLS.CALENDAR_UP, CONTROLS.CALENDAR_DOWN]:
				calendar = self.getControl(CONTROLS.CALENDAR).getLabel()
				index = self.calendars_display.index(calendar)
				if controlID == CONTROLS.CALENDAR_UP:
					index += 1
					index = 0 if index > 5 else index
				else:
					index -= 1
					index = 5 if index < 0 else index
				self.getControl(CONTROLS.CALENDAR).setLabel(self.calendars_display[index])
				self.calendar = self.calendars[index]
				self.load_calendar()
				
			
			if controlID in [90050, 90051, 90052, 90053]:
				obj = self.getFocus()
				show = json.loads(obj.getSelectedItem().getLabel2())
				imdb_id = show['show']['ids']['imdb']
				tmdb_id = show['show']['ids']['tmdb']
				season = show['episode']['season']
				episode = show['episode']['number']
				year = show['show']['year']
				showtitle = show['show']['title'].encode("utf-8", "ignore")
				title =  show['episode']['title'].encode("utf-8", "ignore")
				query = {'mode': 'play_episode', "display": title, "imdb_id": imdb_id, "tmdb_id": tmdb_id, "year": year, "showtitle": showtitle, "season": season, "episode": episode}
				plugin_url = plugin.build_plugin_url(query)
				plugin.play_url(plugin_url)
				plugin.set_property('Calendar.Resume', "true")
				plugin.set_property('Calendar.Offset', str(self.offset))
				plugin.set_property('Calendar.Offset', self.calendar)
				self.close()
		
		def update_info(self, controlID):
			try:
				show = json.loads(self.getControl(controlID).getSelectedItem().getLabel2())
				overview = show['episode']['overview'].encode("ascii", "ignore") if show['episode']['overview'] is not None else ''
				screenshot = show['episode']['images']['screenshot']['medium']
				screenshot = "" if screenshot is None else screenshot
				season = show['episode']['season']
				episode = show['episode']['number']
				showtitle = show['show']['title'].encode("utf-8", "ignore")
				title =  show['episode']['title'].encode("utf-8", "ignore") if show['episode']['title'] is not None else ''
				full_title = "%s %sx%s %s" % (showtitle, season, episode, title)
				rating = show['episode']['rating']
				width = int(round((rating / 10 * 135)))
				network = 'network_logos' + os.sep + re.sub(' +\(.+?\)$', '', show['show']['network'].lower()).replace(' ', '-') + '.png'
				self.getControl(90015).setText(overview)
				self.getControl(90016).setLabel(full_title)
				self.getControl(90017).setImage(screenshot)
				self.getControl(90018).setWidth(width)
				self.getControl(90018).setImage('rating.png')
				self.getControl(90020).setImage(network)
				
			except Exception, e:
				ADDON.log( e )
				self.clear_info()
				
		def clear_info(self):
			self.getControl(90015).setText("")
			self.getControl(90016).setLabel("")
			self.getControl(90017).setImage("")
			
			self.getControl(90018).setWidth(0)
			self.getControl(90018).setImage('')
		
		def onFocus(self, controlID):
			if controlID in [90050, 90051, 90052, 90053, 90007, 90008]:
				last_id = self.last_id
				self.last_id = controlID
				if controlID == 90053 and last_id == 90050:
					self.offset += 4
					self.load_calendar(self.offset)
				elif controlID == 90050 and last_id == 90053:
					self.offset -= 4
					self.load_calendar(self.offset)

	
	cal = Calendar("calendar.xml", ROOT_PATH)
	cal.doModal()
plugin.register('calendar_browser', calendar_browser)

def movie_genre():
	from dudehere.routines.tmdb import TMDB_API
	tmdb = TMDB_API()
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()	
	page = int(plugin.args['page']) if 'page' in plugin.args.keys() else 1
	results = tmdb.list_movie_genre(plugin.args['id'], page=page)
	total_pages = results['total_pages']
	count = len(results)
	if validate_trakt():
		watchlist = trakt.get_watchlist_movies(simple=True, id_type='tmdb')
	else:
		watchlist = []
	
	if validate_transmogrifier():
		from dudehere.routines.transmogrifier import TransmogrifierAPI
		TM = TransmogrifierAPI()
		path, transmogrified = TM.get_videos('movie')
	else:
		transmogrified = []
		is_local = False
	if not results:
		return
	for result in results['results']:
		record = tmdb.process_record(result, 'movie')
		movie_title = record['title']
		menu = ContextMenu()
		menu.add("Watch Trailer", {"mode": "movie_trailers", "tmdb_id": record['tmdb_id']}, script=True)
		menu.add('Find Similar Movies', {"mode": "movie_similar", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']})
		menu.add('Save as Favorite', {"mode": "add_to_favorites", "media": "movie",  "record": record}, script=True, visible=validate_trakt()==False)
		if int(record['tmdb_id']) in watchlist:
			record['title'] = '[COLOR %s]%s[/COLOR]'% (WATCHLIST_COLOR, record['title'])
			menu.add('Remove from Watchlist', {"mode": "movie_delete_from_watchlist", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "name": movie_title}, script=True, visible=validate_trakt)
		else:
			menu.add('Add to Watchlist', {"mode": "movie_add_to_watchlist", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']}, script=True, visible=validate_trakt)
		menu.add('Add to custom list', {"mode": "add_to_custom_list", "media": "movie", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']}, script=True, visible=validate_trakt)	
		
		if validate_transmogrifier():
			filename = "%s (%s)" % (utf8(movie_title), record['year'])	
			is_local = any(filename  in test for test in transmogrified)
		
		if is_local:
			menu.add('Play Cache File', {'mode': 'play_movie_cache', "title": movie_title, "year": record['year']}, visible=validate_transmogrifier)
			menu.add('Delete Cache File', {'mode': 'delete_movie_cache', "title": movie_title, "year": record['year']}, visible=validate_transmogrifier)
			record['title'] = record['title'] + ' [TM]'
		else:
			query = {'mode': 'movie_transmogrify', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}
			menu.add('Transmogrify', query, visible=validate_transmogrifier)
		if ADDON.get_setting('source_selection_mode') == 'Directory':
			plugin.add_menu_item({'mode': 'get_movie_sources', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}, record, menu=menu, total_items=count, image=record['cover_url'], fanart=record['backdrop_url'])
		else:
			plugin.add_video_item({'mode': 'play_movie', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}, record, menu=menu, total_items=count, image=record['cover_url'], fanart=record['backdrop_url'])
	if total_pages> 1: plugin.add_menu_item({'mode': 'movie_genre', "id": plugin.args['id'], "page": page+1}, {'title': '[COLOR blue]Next Page %s/%s >>[/COLOR]' % (page+1, total_pages)}, image=ARTWORK + "next_page.jpg")
	plugin.eod(VIEWS.MOVIE_DEFAULT, 'movies')
plugin.register("movie_genre", movie_genre)

def movie_list():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	if plugin.mode ==		'movie_watchlist' or validate_trakt() == False:
		watchlist = []
	else:
		watchlist = trakt.get_watchlist_movies(simple=True)
	
	if validate_transmogrifier():
		from dudehere.routines.transmogrifier import TransmogrifierAPI
		TM = TransmogrifierAPI()
		path, transmogrified = TM.get_videos('movie')
	else:
		transmogrified = []
		is_local = False
	regex = re.compile("^(A )|(An )|(The )", re.IGNORECASE)
	def sort_results(title):
		title = regex.sub('', title['movie']['title'], re.IGNORECASE)
		return title.lower()
	if plugin.mode ==		'movie_favorites':
		results = get_movie_favorites()
	elif plugin.mode ==		'movie_watchlist':
		results = trakt.get_watchlist_movies()
		if not results: return
		results = sorted(results, key=lambda x: x['movie']['title'])
	elif plugin.mode ==		'movie_trending':
		results = trakt.get_trending_movies()
	elif plugin.mode ==		'movie_popular':
		results = trakt.get_popular_movies()
	elif plugin.mode ==		'movie_recommended':
		results = trakt.get_recommended_movies()
		if not results: return
	elif plugin.mode ==		'movie_collection':
		results = trakt.get_collected_movies()
		if not results: return
		results.sort(key=lambda k: sort_results(k))	
	elif plugin.mode ==		'movie_custom_list':
		if 'username' in plugin.args:
			results = trakt.get_custom_list(plugin.args['slug'], 'movie', username=plugin.args['username'])
		else:
			results = trakt.get_custom_list(plugin.args['slug'], 'movie')
			if not results: return
	elif plugin.mode == 	'movie_search':
		query = plugin.get_property('search.query.refesh')
		if query:
			plugin.clear_property('search.query')
			plugin.clear_property('search.query.refesh')
		else:
			query = plugin.dialog_input('Search Movies')
		if query is None: 
			plugin.clear_property("search.query")
			return
		plugin.set_property('search.query', query)
		results = trakt.search(query, 'movie')
	elif plugin.mode == 	'movie_similar':
		imdb_id = trakt.query_id('tmdb', plugin.args['tmdb_id']) if plugin.args['imdb_id'] == 'None' else plugin.args['imdb_id']
		results = trakt.get_similar_movies(imdb_id)
	count = len(results)
	if validate_trakt(): watched = trakt.get_watched_history('movies')
	if not results:
		return	
	for record in results:
		if plugin.mode  != 'movie_favorites':
			record = trakt.process_record(record, media='movie')
		else:
			record['cast'] = []
		menu = ContextMenu()
		menu.add("Watch Trailer", {"mode": "movie_trailers", "tmdb_id": record['tmdb_id']}, script=True)
		menu.add('Find Similar Movies', {"mode": "movie_similar", "imdb_id": record['imdb_id']})
		movie_title = record['title']
		if validate_trakt():
			if record['imdb_id'] in watched['imdb']:
				record['playcount'] = 1
				record['overlay'] = 7
				menu.add('Mark Unwatched', {"mode": "set_unwatched", "media": "movie", "id": record['imdb_id']})
			else:
				menu.add('Mark Watched', {"mode": "set_watched", "media": "movie", "id": record['imdb_id']})
					
		if plugin.args['mode']=='movie_watchlist':
			menu.add('Remove from Watchlist', {"mode": "movie_delete_from_watchlist", "imdb_id": record['imdb_id'], "name": movie_title}, script=True, visible=validate_trakt)
		else:
			if record['imdb_id'] in watchlist:
				record['title'] = '[COLOR %s]%s[/COLOR]' % (WATCHLIST_COLOR, record['title'])
				menu.add('Remove from Watchlist', {"mode": "movie_delete_from_watchlist", "imdb_id": record['imdb_id'], "name": movie_title}, script=True, visible=validate_trakt)
			else:
				menu.add('Add to Watchlist', {"mode": "movie_add_to_watchlist", "imdb_id": record['imdb_id']}, script=True, visible=validate_trakt)
			
		if plugin.args['mode']=='movie_custom_list':
			menu.add('Remove from custom list', {"mode": "delete_from_custom_list", "media": "movie", "imdb_id": record['imdb_id'], "slug": plugin.args['slug'], "name": record['title']}, script=True, visible=validate_trakt)
		else:
			menu.add('Add to custom list', {"mode": "add_to_custom_list", "media": "movie", "imdb_id": record['imdb_id']}, script=True, visible=validate_trakt)	
		
		if plugin.mode ==	'movie_favorites':
			menu.add('Delete Favorite', {"mode": "delete_from_favorites", "media": "movie", "title": record['title'], "id": record['id']}, script=True, visible=validate_trakt()==False)
		else:
			menu.add('Save as Favorite', {"mode": "add_to_favorites", "media": "movie",  "record": record}, script=True, visible=validate_trakt()==False)
	
		
		if validate_transmogrifier():
			filename = "%s (%s)" % (utf8(movie_title), record['year'])
			is_local = any(filename  in test for test in transmogrified)
		
		if is_local:
			menu.add('Play Cache File', {'mode': 'play_movie_cache', "title": movie_title, "year": record['year']}, visible=validate_transmogrifier)
			menu.add('Delete Cache File', {'mode': 'delete_movie_cache', "title": movie_title, "year": record['year']}, visible=validate_transmogrifier)
			record['title'] = record['title'] + ' [TM]'
		else:
			query = {'mode': 'movie_transmogrify', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}
			menu.add('Transmogrify', query, visible=validate_transmogrifier)

		if ADDON.get_setting('source_selection_mode') == 'Directory':
			plugin.add_menu_item({'mode': 'get_movie_sources', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}, record, menu=menu, total_items=count, image=record['cover_url'], fanart=record['backdrop_url'])
		else:
			plugin.add_video_item({'mode': 'play_movie', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}, record, menu=menu, total_items=count, image=record['cover_url'], fanart=record['backdrop_url'])
	ADDON.save_data('last_directory.qs', sys.argv[0]+sys.argv[2])
	plugin.eod(VIEWS.MOVIE_DEFAULT, 'movies')
plugin.register(['movie_watchlist', 'movie_trending', 'movie_popular', 'movie_recommended', 'movie_custom_list', 'movie_similar', 'movie_search', 'movie_collection', 'movie_favorites'], movie_list)

def discover_results():
	from dudehere.routines.tmdb import TMDB_API
	tmdb = TMDB_API()
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	if validate_trakt():
		watchlist = trakt.get_watchlist_movies(simple=True, id_type='tmdb')
	else:
		watchlist = []
	if validate_transmogrifier():
		from dudehere.routines.transmogrifier import TransmogrifierAPI
		TM = TransmogrifierAPI()
		path, transmogrified = TM.get_videos('movie')
	else:
		transmogrified = []
		is_local = False
	query = ADDON.load_data('movie.discover.qs')
	page = int(plugin.args['page']) if 'page' in plugin.args.keys() else query['page']
	query['page'] = page
	results = tmdb.discover_movies(query)
	total_pages = results['total_pages']
	count = len(results)
	#if page >1: plugin.add_menu_item({'mode': 'discover_results', "page": page - 1}, {'title': '[COLOR blue]<< Previous Page %s/%s[/COLOR]' % (page - 1, total_pages)}, image=ARTWORK +"discover.jpg")
	if not results:
		return
	for result in results['results']:
		record = tmdb.process_record(result, 'movie')
		movie_title = record['title']
		menu = ContextMenu()
		menu.add("Watch Trailer", {"mode": "movie_trailers", "tmdb_id": record['tmdb_id']}, script=True)
		menu.add('Find Similar Movies', {"mode": "movie_similar", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']})
		menu.add('Save as Favorite', {"mode": "add_to_favorites", "media": "movie",  "record": record}, script=True, visible=validate_trakt()==False)
		if int(record['tmdb_id']) in watchlist:
			record['title'] = '[COLOR %s]%s[/COLOR]' % (WATCHLIST_COLOR, record['title'])
			menu.add('Remove from Watchlist', {"mode": "movie_delete_from_watchlist", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "name": movie_title}, script=True, visible=validate_trakt)
		else:
			menu.add('Add to Watchlist', {"mode": "movie_add_to_watchlist", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']}, script=True, visible=validate_trakt)
		menu.add('Add to custom list', {"mode": "add_to_custom_list", "media": "movie", "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id']}, script=True, visible=validate_trakt)
		if validate_transmogrifier():
			filename = "%s (%s)" % (utf8(movie_title), record['year'])
			is_local = any(filename  in test for test in transmogrified)
		
		if is_local:
			menu.add('Play Cache File', {'mode': 'play_movie_cache', "title": movie_title, "year": record['year']}, visible=validate_transmogrifier)
			menu.add('Delete Cache File', {'mode': 'delete_movie_cache', "title": movie_title, "year": record['year']}, visible=validate_transmogrifier)
			record['title'] = record['title'] + ' [TM]'
		else:
			query = {'mode': 'movie_transmogrify', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}
			menu.add('Transmogrify', query, visible=validate_transmogrifier)
			
		if ADDON.get_setting('source_selection_mode') == 'Directory':
			plugin.add_menu_item({'mode': 'get_movie_sources', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}, record, menu=menu, total_items=count, image=record['cover_url'], fanart=record['backdrop_url'])
		else:
			plugin.add_video_item({'mode': 'play_movie', "imdb_id": record['imdb_id'], "tmdb_id": record['tmdb_id'], "year": record['year'], "title": movie_title}, record, menu=menu, total_items=count, image=record['cover_url'], fanart=record['backdrop_url'])
	if total_pages > 1: plugin.add_menu_item({'mode': 'discover_results', "page": page+1}, {'title': '[COLOR blue]Next Page %s/%s >>[/COLOR]' % (page+1, total_pages)}, image=ARTWORK +"discover.jpg")
	ADDON.save_data('last_directory.qs', sys.argv[0]+sys.argv[2])
	plugin.eod(VIEWS.MOVIE_DEFAULT, 'movies')
plugin.register('discover_results', discover_results)
	
def movie_discover():
	from dudehere.routines.window import Window
	from dudehere.routines.tmdb import TMDB_API, MOVIE_GENRES as GENRES
	tmdb = TMDB_API()
	
	class DiscoverWindow(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title,width=750, height=525, columns=4, rows=9)
			self.draw()
		
		def set_info_controls(self):
			self.add_label(self.create_label('Rating: ', textColor="0xFF0088FF"), 0, 2,  pad_x=42, pad_y=30)
			items = ["G", "PG", "PG-13", "R", "NC-17"]
			self.create_list('rating')
			self.add_object('rating', 1,2,6,1)
			self.add_list_items('rating', items, allow_multiple=False, allow_toggle=True)
			
			
			self.add_label(self.create_label('Genre: ', textColor="0xFF0088FF"), 0, 3,  pad_x=42, pad_y=30)
			items = [GENRES.r_map[id].lower() for id in GENRES.r_map.keys()]
			self.create_list('genre')
			self.add_object('genre', 1,3,7,1)
			self.add_list_items('genre', items, allow_multiple=True, allow_toggle=True)
			
			self.add_label(self.create_label('Keyword: ', textColor="0xFF0088FF"), 0, 0, pad_x=15, pad_y=30)
			self.create_input('keyword')
			self.add_object('keyword', 1, 0, columnspan=2, pad_x=15)
			
			self.add_label(self.create_label('Actor: ', textColor="0xFF0088FF"), 2, 0,  pad_x=15, pad_y=30)
			self.create_input('actor')
			self.add_object('actor', 3, 0, columnspan=2, pad_x=15)
			
			self.add_label(self.create_label('Sorting: ', textColor="0xFF0088FF"), 4, 0, pad_x=15, pad_y=30)
			items = ["Popularity", "Release Date", "User Rating", "Revenue"]
			self.create_list('sorting')
			self.add_object('sorting', 5,0,3,2)
			self.add_list_items('sorting', items, 0, allow_multiple=False, allow_toggle=False)
			
			self.create_button('cancel', 'Cancel')
			self.add_object('cancel',  8, 1)
			
			self.create_button('discover', 'Discover')
			self.add_object('discover',  8, 2)
	
	def discover():
		actor = w.get_value('actor')
		keyword = w.get_value('keyword')
		genre = w.get_value('genre', return_text=True)
		rating = w.get_value('rating', return_text=True)
		sorting = w.get_value('sorting', return_index=True)
		sorting = ["popularity.desc", "release_date.desc", "vote_average.desc", "revenue.desc"][sorting[0]]
		query = {"sort_by": sorting, "page": 1}
		if keyword:
			keyword_ids = tmdb.query_keyword_id(keyword)
			if len(keyword_ids) > 0:
				query['with_keywords'] = "|".join(keyword_ids)
		if actor:
			actor_ids = tmdb.query_person_id(actor)
			if len(actor_ids) > 0:
				query['with_cast'] = "|".join(actor_ids)
		if len(rating) > 0:
			query['certification_country'] = 'US'
			query['certification.lte'] = rating[0]
		genres = []	
		for text in genre:
			id = GENRES.f_map[text.upper()]
			genres.append(str(id))
		if len(genres) > 0:
			query['with_genres'] = "|".join(genres)	
		w.close()
		query = ADDON.save_data('movie.discover.qs', query)
		plugin.navigate_to({"mode": "discover_results"})
		
	w = DiscoverWindow('Discover Movies')
	w.set_object_event('action', 'cancel', w.close)
	w.set_object_event('action', 'discover', discover)
	w.set_object_event('focus', 'keyword')
	w.set_object_event('down', 'keyword', 'actor')
	w.set_object_event('down', 'actor', 'sorting')
	w.set_object_event('down', 'sorting', 'discover')
	w.set_object_event('down', 'rating', 'discover')
	w.set_object_event('down', 'genre', 'discover')
	w.set_object_event('right', 'keyword', 'rating')
	w.set_object_event('right', 'actor', 'rating')
	w.set_object_event('right', 'rating', 'genre')
	w.set_object_event('right', 'sorting', 'rating')
	w.set_object_event('left', 'genre', 'rating')
	w.set_object_event('left', 'rating', 'keyword')
	
	w.set_object_event('left', 'discover', 'cancel')
	w.set_object_event('up', 'actor', 'keyword')
	w.set_object_event('up', 'sorting', 'actor')
	w.set_object_event('up', 'cancel', 'sorting')
	w.set_object_event('up', 'discover', 'sorting')
	w.show()
plugin.register('movie_discover', movie_discover)


'''*	Miscellaneous Functions
*'''

def advanced_mode():
	mode = 'false' if validate_advanced() else 'true'
	ADDON.set_setting('advanced_mode', mode)
	plugin.refresh()
plugin.register('advanced_mode', advanced_mode)

def toggle_hide_watched():
	flag = 'false' if ADDON.get_setting('hide_watched_episodes') == 'true' else 'true'
	ADDON.set_setting('hide_watched_episodes', flag)
	plugin.refresh()
plugin.register('toggle_hide_watched', toggle_hide_watched)

def show_about():
	vfs = VFSClass()
	content = vfs.read_file(vfs.join(LANGUAGE_PATH, 'about.txt'))
	plugin.show_textbox('About', content)
plugin.register('show_about', show_about)

def scraper_accounts():
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(load='all')
	for index in xrange(len(Scraper.supported_scrapers)):
		if Scraper.get_scraper_by_index(index) is None: continue
		name = Scraper.get_scraper_by_index(index).name
		service = Scraper.get_scraper_by_index(index).service
		if Scraper.get_scraper_by_index(index).require_auth:
			plugin.add_menu_item({'mode': 'scraper_account', "service": service, "name": name}, {'title': name}, image=ARTWORK + "about.jpg")
	plugin.eod()
plugin.register('scraper_accounts', scraper_accounts)

def scraper_account(name=None, service=None):
	return_val = False
	from dudehere.routines.window import Window
	from dudehere.routines.scrapers import CommonScraper
	if name is None and service is None:
		name = plugin.args['name']
		service = plugin.args['service']
	class AccountWindow(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title,width=650, height=200, columns=4, rows=3)
			self.return_val = False
		def update(self):
			valid = True
			login = self.get_value('login')
			password = self.get_value('password')
			Scraper = CommonScraper(load=[service])
			if 'check_authentication' in dir(Scraper.get_scraper_by_index(0)):
				valid = Scraper.get_scraper_by_index(0).check_authentication(login, password)
				if not valid:
					plugin.dialog_ok('Login Error!', 'Please verify your account information.')
			if valid:
				ADDON.set_setting(service + '_username', login)
				ADDON.set_setting(service + '_password', password)
				self.return_val = True
				self.close()
		
		def set_info_controls(self):
			label = self.create_label("Login:")
			self.add_label(label, 0, 0, pad_x=15, pad_y=10)
			self.create_input('login')
			self.add_object('login', 0, 1, columnspan=3)
			self.set_value('login', ADDON.get_setting(service + '_username'))
			
			label = self.create_label("Password:")
			self.add_label(label, 1, 0, pad_x=15, pad_y=10)
			self.create_input('password', isPassword=True)
			self.add_object('password', 1, 1, columnspan=3)
			self.set_value('password', ADDON.get_setting(service + '_password'))
			
			self.create_button('cancel', 'Cancel')
			self.add_object('cancel', 2, 1)
			self.set_object_event('action', 'cancel', self.close)
		
			self.create_button('update', 'Update')
			self.add_object('update', 2, 2)
			self.set_object_event('action', 'update', self.update)
			
			self.set_object_event('focus', 'login')
			self.set_object_event('down', 'login', 'password')
			self.set_object_event('down', 'password', 'update')
			self.set_object_event('up', 'password', 'login')
			self.set_object_event('up', 'update', 'password')
			self.set_object_event('up', 'cancel', 'password')
			self.set_object_event('right', 'cancel', 'update')
			self.set_object_event('left', 'update', 'cancel')
	
	A = AccountWindow('Set Login/Password for: %s' % name)
	A.show()
	return_val = A.return_val
	del A
	return return_val
plugin.register('scraper_account', scraper_account)	

def scraper_list():
	from dudehere.routines.window import Window
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(load='all')
	scrapers = Scraper.read_scraper_states()
	items = []
	enabled = []
	for scraper in scrapers: 
		try:
			broken = Scraper.get_scraper_by_name(scraper['name']).broken
		except:
			broken = False if 'transmogrifier' in scraper['name'] else True
		name = "[COLOR red]%s[/COLOR]" % scraper['name'] if broken else scraper['name']
		items.append(name)
		if scraper['enabled']: enabled.append(scrapers.index(scraper))
	class ScraperWindow(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title,width=650, height=470, columns=3, rows=8)
		
		def togglez(self):
			list_item = self.getFocus().getSelectedItem()
			name = list_item.getLabel()
			if name.startswith('['): 
				name = name.replace('[COLOR red]', '')
				name = name.replace('[/COLOR]', '')
			query = {'mode': 'toggle_scraper', "scraper": name}
			plugin.execute_query(query)
		
		def disable_all(self):
			for index in xrange(0, self.get_object('scrapers').size()):
				self.set_unselected('scrapers', index)
				name = self.get_object('scrapers').getListItem(index).getLabel()
				if name.startswith('['): 
					name = name.replace('[COLOR red]', '')
					name = name.replace('[/COLOR]', '')
				Scraper.set_scraper_state(name, False)
		
		def enable_all(self):
			for index in xrange(0, self.get_object('scrapers').size()):
				self.set_selected('scrapers', index)
				name = self.get_object('scrapers').getListItem(index).getLabel()
				if name.startswith('['): 
					name = name.replace('[COLOR red]', '')
					name = name.replace('[/COLOR]', '')
				Scraper.set_scraper_state(name, True)

		def set_info_controls(self):
			self.create_list('scrapers')
			self.add_object('scrapers', 0,0,7,3)
			self.add_list_items('scrapers', items, enabled, call_back=self.togglez, allow_multiple=True, allow_toggle=True)

			self.create_button('disable_all', 'Disable All')
			self.add_object('disable_all', 7,0)
			self.set_object_event('action', 'disable_all', self.disable_all)
			
			self.create_button('enable_all', 'Enable All')
			self.add_object('enable_all', 7,1)
			self.set_object_event('action', 'enable_all', self.enable_all)
			
			self.create_button('close', 'Close')
			self.add_object('close', 7,2)
			self.set_object_event('action', 'close', self.close)
			
			self.set_object_event('focus', 'scrapers')
			self.set_object_event('down', 'scrapers', 'close')
			self.set_object_event('right', 'scrapers', 'close')
			self.set_object_event('left', 'close', 'enable_all')
			self.set_object_event('left', 'enable_all', 'disable_all')
			self.set_object_event('right', 'enable_all', 'close')
			self.set_object_event('right', 'disable_all', 'enable_all')
			self.set_object_event('up', 'enable_all', 'scrapers')
			self.set_object_event('up', 'disable_all', 'scrapers')
			self.set_object_event('up', 'close', 'scrapers')
					
	s = ScraperWindow('Enable/Disable Available Scrapers')
	s.show()
	del s
plugin.register('scraper_list', scraper_list)	

def set_source_filter():
	from dudehere.routines.window import Window
	vfs = VFSClass()
	cache_file = vfs.join(DATA_PATH, "filters.cache")

	items = [QUALITY.r_map[i] for i in range(1,9)] + ["AllDebrid", "RealDebrid", "Premiumize.ME", "RPNET"]
	if vfs.exists(cache_file):
		temp = ADDON.load_data(cache_file)
		enabled = []
		for item in items:
			if item in temp:
				enabled.append(items.index(item))
	else:
		enabled = [i for i in xrange(len(items))]
		ADDON.save_data(cache_file, items)
	class FilterWindow(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title,width=650, height=470, columns=3, rows=8)
		
		def togglez(self):
			list_item = self.getFocus().getSelectedItem()
			name = list_item.getLabel()
			query = {'mode': 'toggle_filter', "filter": name}
			plugin.execute_query(query)

		def set_info_controls(self):
			self.create_list('filters')
			self.add_object('filters', 0,0,7,3)
			self.add_list_items('filters', items, enabled, call_back=self.togglez, allow_multiple=True, allow_toggle=True)
			
			self.create_button('close', 'Close')
			self.add_object('close', 7,1)
			self.set_object_event('action', 'close', self.close)
			self.set_object_event('focus', 'filters')
			self.set_object_event('down', 'filters', 'close')
			self.set_object_event('right', 'filters', 'close')
			self.set_object_event('up', 'close', 'filters')
					
	f = FilterWindow('Change Source List Filters')
	f.show()
	del f
plugin.register('set_source_filter', set_source_filter)	

	
def toggle_filter():
	vfs = VFSClass()
	cache_file = vfs.join(DATA_PATH, "filters.cache")
	temp = ADDON.load_data(cache_file)
	filter = plugin.args['filter']
	if filter in temp:
		temp.remove(filter)
	else:
		temp.append(filter)
	ADDON.save_data(cache_file, temp)

	
plugin.register('toggle_filter', toggle_filter)

def toggle_scraper():
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(load=False)
	Scraper.toggle_scraper_state(plugin.args['scraper'])
plugin.register('toggle_scraper', toggle_scraper)

def transmogrifier_queue():
	plugin.run_command('RunAddon("service.transmogrifier")')
plugin.register('manage_transmogrifier', transmogrifier_queue)

def authorize_trakt():
	vfs = VFSClass()
	from dudehere.routines.window import Window
	class AuthorizationWindow(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title,width=800, height=400, columns=4, rows=6)
			
		def authorize(self):
			pin = self.get_value('pin')
			from dudehere.routines.trakt import TraktAPI
			trakt = TraktAPI()
			response = trakt.authorize(pin)
			if response:
				settings = trakt.get_settings()
				if settings:
					ADDON.set_setting('trakt_account', settings['user']['username'])
				plugin.notify("Trakt Authorization", "Success", image=ARTWORK + "trakt.png")
				self.close()
			else:
				ADDON.set_setting('trakt_account', '')
				plugin.notify("Trakt Authorization", "Failed", image=ARTWORK + "trakt.png")

		def set_info_controls(self):
			self.create_image('trakt', ARTWORK + 'trakt.png', aspectRatio=1)
			self.add_object('trakt', 0, 0, columnspan=3, rowspan=3)
			
			content = '''[B]The Royal We is even better with a Trakt.TV account.\nIf you have one, you may authorize it now.\nOtherwise you can use TRW without trakt.\nYou can always authorize or re-authorize TRW.\nJust look in the Settings Menu.[/B]'''
			self.add_label(self.create_label(content), 0, 0, columnspan=3, rowspan=3, pad_x=15, pad_y=10)
			
			content = "Open a browser and navigate to:\n[B][COLOR red]%s[/COLOR][/B]" % ADDON.get_setting('trakt_pin_url')
			self.add_label(self.create_label(content), 3, 0, columnspan=3, rowspan=2, pad_x=15, pad_y=10)
			
			self.create_input('pin', _alignment=2)
			self.add_object('pin', 4, 0, columnspan=4)
			
			self.create_image('qr_code', ARTWORK + 'pin.png', aspectRatio=2)
			self.add_object('qr_code', 0, 3, columnspan=1, rowspan=2)
			
			self.create_button('later', 'Maybe Later')
			self.add_object('later', 5, 1)	
			
			self.create_button('authorize', 'Authorize')
			self.add_object('authorize', 5, 2)	
			self.set_object_event('action', "later", self.close)
			self.set_object_event('action', "authorize", self.authorize)
			self.set_object_event('focus', 'pin')
			self.set_object_event('left', 'authorize', 'later')
			self.set_object_event('left', 'later', 'authorize')
			self.set_object_event('up', 'authorize', 'pin')
			self.set_object_event('up', 'later', 'pin')
			self.set_object_event('down', 'pin', 'authorize')
	
	A = AuthorizationWindow('Enter Trakt.tv Pin')
	A.show()
	del A	
plugin.register('authorize_trakt', authorize_trakt)

def reset_trw():
	from dudehere.routines.window import Window
	class ResetWindow(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title,width=700, height=300, columns=4, rows=6)
			self.draw()
			
		def set_info_controls(self):
			label = self.create_label("If you are sure you want to reset your TRW setup:")
			self.add_label(label, 0, 0, columnspan=4, pad_x=15, pad_y=10)
			
			label = self.create_label("1) Type 'RESET' in the field below")
			self.add_label(label, 1, 0, columnspan=4, pad_x=15, pad_y=10)
			
			label = self.create_label("2) Click the `Confirm Reset` button")
			self.add_label(label, 2, 0, columnspan=4, pad_x=15, pad_y=10)
			
			label = self.create_label("This will reset your database and settings to the default.")
			self.add_label(label, 3, 0, columnspan=4, pad_x=15, pad_y=10)
			
			label = self.create_label("Enter RESET")
			self.add_label(label, 4, 0, columnspan=2, pad_x=15, pad_y=10)
			
			self.create_input('reset')
			self.add_object('reset', 4, 1, columnspan=2)
			
			self.create_button('cancel', 'Cancel')
			self.add_object('cancel',  5, 1)
			
			self.create_button('confirm', 'Reset')
			self.add_object('confirm',  5, 2)
			
		def confirm(self):
			if self.get_value('reset') != 'RESET':
				plugin.notify('Confirmation Error', 'Please enter RESET to confirm')
				return
			ok = plugin.confirm("Final Confirmation", "Are you sure?", "This is your last change to cancel!")
			if ok:
				VFSClass().rm(DATA_PATH, quiet=True, recursive=True)
				self.close()
				plugin.exit()
			else:
				self.close()
			self.close()
		
	reset = ResetWindow('Reset The Royal We?')
	reset.set_object_event('focus', 'reset')
	reset.set_object_event('down', 'reset', 'confirm')
	reset.set_object_event('up', 'confirm', 'reset')
	reset.set_object_event('left', 'confirm', 'cancel')
	reset.set_object_event('right', 'cancel', 'confirm')
	reset.set_object_event('up', 'cancel', 'reset')
	reset.set_object_event('action', 'cancel', reset.close)
	reset.set_object_event('action', 'confirm', reset.confirm)
	reset.show()
plugin.register('reset_trw', reset_trw)

def host_manager():
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(load=False)
	hosts = Scraper.get_host_list()
	debrid_hosts = ADDON.load_data(VFSClass().join(DATA_PATH, 'debrid_hosts.cache'))
	debrid_color = ADDON.get_setting('custom_color_debrid_color') if ADDON.get_setting('custom_color_debrid_color') != '' else 'hotpink'
	for host in hosts:
		debrid = []
		if 'ad' in debrid_hosts:
			if host['host'] in debrid_hosts['ad']:
				debrid.append('AD')

		if 'rp' in debrid_hosts:
			if host['host'] in debrid_hosts['rp']:
				debrid.append('RPN')

		if 'rd' in debrid_hosts:
			if host['host'] in debrid_hosts['rd']:
				debrid.append('RD')

		if 'pm' in debrid_hosts:
			if host['host'] in debrid_hosts['pm']:
				debrid.append('PM')
		menu = ContextMenu()
		menu.add("Change priority", {"mode": "change_host_priority", "host": host['host'], "weight": host['weight']})
		color = 'white' if host['disabled'] == 0 else 'darkorange'
		if len(debrid):
			display = "%s | [COLOR %s]%s[/COLOR] |" % (host['host'], debrid_color, ' | '.join(debrid))
		else:
			display = "%s |" % host['host']
		display = "[COLOR %s]%s%s[/COLOR]" % (color, display, host['weight'])
		plugin.add_menu_item({"mode": "toggle_host", "host": host['host']}, {'title': display}, menu=menu)
	plugin.eod(VIEWS.LIST)	
plugin.register("manage_hosts", host_manager)

def toggle_host():
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(load=False)
	Scraper.toggle_host(plugin.args['host'])
	plugin.refresh()
plugin.register("toggle_host", toggle_host)	

def change_host_priority():
	weight = plugin.dialog_number('Enter new priority', default=plugin.args['weight'])
	if weight:
		from dudehere.routines.scrapers import CommonScraper
		Scraper = CommonScraper(load=False)
		Scraper.change_host_weight(plugin.args['host'], weight)
		plugin.refresh()
plugin.register("change_host_priority", change_host_priority)
	
def movie_trailers():
	from dudehere.routines.tmdb import TMDB_API
	tmdb = TMDB_API()
	trailers = tmdb.movie_trailers(plugin.args['tmdb_id'])
	options = [trailers[index]['name'] for index in xrange(len(trailers))]
	index = plugin.dialog_select('Select A Trailer', options)
	if index is not False:
		key = trailers[index]['key']
		plugin.play_url('plugin://plugin.video.youtube/play/?video_id=' + key)
plugin.register('movie_trailers', movie_trailers)

def toggle_watched():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()	
	re_watchlist = False
	if plugin.mode == 'set_watched':
		watched = True
		if plugin.args['media'] == 'episode' or plugin.args['media'] == 'season':
			watchlist = trakt.get_watchlist_tvshows(simple=True)
			re_watchlist = plugin.args['imdb_id'] in watchlist
	else:
		watched = False
	if plugin.args['media'] == 'season':
		trakt.set_watched_state(plugin.args['media'], plugin.args['imdb_id'], watched, plugin.args['id'])
	else:
		trakt.set_watched_state(plugin.args['media'], plugin.args['id'], watched)
	if re_watchlist: trakt.add_to_watchlist('shows', plugin.args['imdb_id'], id_type='imdb')
	plugin.notify('Success', "Watched" if watched == True else "Unwatched")
	plugin.refresh()
plugin.register(['set_watched', 'set_unwatched'], toggle_watched)

def set_watched(media, imdb_id, season=None, episode=None, refresh=True):
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	if media == 'episode':
		re_watchlist = False
		watchlist = trakt.get_watchlist_tvshows(simple=True)
		re_watchlist = imdb_id in watchlist
		episode =trakt.get_episode_details(imdb_id, season, episode, None)
		trakt_id = episode['trakt_id']
		trakt.set_watched_state(media, trakt_id, True)
		if re_watchlist: trakt.add_to_watchlist('shows', imdb_id, id_type='imdb')
	if refresh:
		plugin.refresh()

def custom_list_menu():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	lists = trakt.get_custom_lists()
	if not lists: return	
	media = 'tv' if plugin.mode == 'tv_custom_lists' else 'movie'
	plugin.add_menu_item({'mode': 'new_custom_list', "media": media}, {"title": '***New Custom List***'}, image=ARTWORK+'/create_trakt_list.jpg')
	for list in lists:
		menu = ContextMenu()
		menu.add('Delete Custom List', {"mode": "delete_custom_list", "slug": list['ids']['slug'], "name": list['name']}, script=True)
		plugin.add_menu_item({"mode": media + "_custom_list", 'slug': list['ids']['slug'], "media": media}, {"title": list['name']}, menu=menu)
	plugin.add_menu_item({"mode": "dummy"}, {"title": "--- Liked Lists ---"}, menu=menu)
	lists = trakt.get_liked_lists()
	for list in lists:
		plugin.add_menu_item({"mode": media + "_custom_list", 'username': list['list']['user']['username'], 'slug': list['list']['ids']['slug'], "media": media}, {"title": list['list']['name']})
	plugin.eod(VIEWS.LIST)
	
plugin.register(['tv_custom_lists', 'movie_custom_lists'], custom_list_menu)
def dummy():
	pass
plugin.register("dummy", dummy)


def get_tv_favorites():
	records = []
	plugin.DB.connect()
	results = plugin.DB.query_assoc("SELECT * FROM tvshow_favorites ORDER BY title ASC", force_double_array=True)
	plugin.DB.disconnect()
	if results:
		return results
	else:
		plugin.notify('Favorites is empty', 'Add something to the list!')
		return records
	
def get_movie_favorites():
	records = []
	plugin.DB.connect()
	results = plugin.DB.query_assoc("SELECT * FROM movie_favorites ORDER BY title ASC", force_double_array=True)
	plugin.DB.disconnect()
	if results:
		return results
	else:
		plugin.notify('Favorites is empty', 'Add something to the list!')
		return records

def add_to_favorites():
	import ast
	record = plugin.args['record']
	record = ast.literal_eval(record)
	if plugin.args['media'] == 'tvshow':
		SQL = """INSERT OR REPLACE INTO tvshow_favorites (
				imdb_id,
				tmdb_id,
				tvdb_id,
				trakt_id,
				slug,
				title,
				year,
				TVShowTitle,
				duration,
				rating,
				plot,
				mpaa,
				cover_url,
				banner_url,
				backdrop_url,
				trailer_url
				) VALUES(?,?,?,?,? ,?,?,?,?,?, ?,?,?,?,?, ?)
				"""
				
		values = [record[k] for k in ["imdb_id","tmdb_id","tvdb_id","trakt_id","slug","title","year","TVShowTitle","duration","rating","plot","mpaa","cover_url","banner_url","backdrop_url","trailer_url"]]
	else:
		SQL = """INSERT OR REPLACE INTO movie_favorites (
				imdb_id,
				tmdb_id,
				trakt_id,
				slug,
				title,
				year,
				tagline,
				duration,
				rating,
				votes,
				plot,
				mpaa,
				premiered,
				cover_url,
				thumb_url,
				backdrop_url,
				trailer_url
				) VALUES(?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?)
				"""
		values = [record[k] for k in ["imdb_id","tmdb_id","trakt_id","slug", "title","year","tagline","duration","rating","votes","plot","mpaa","premiered","cover_url","thumb_url","backdrop_url","trailer_url"]]
	plugin.DB.connect()
	plugin.DB.execute(SQL, values)
	plugin.DB.commit()
	plugin.DB.disconnect()	
	plugin.notify('Success', 'Added Favorite: %s' % record['title'])
	plugin.refresh()

plugin.register('add_to_favorites', add_to_favorites)

def delete_from_favorites():
	ok = plugin.confirm('Delete favorite', "click YES to continue", plugin.args['title'])
	if ok:
		plugin.DB.connect()
		SQL = "DELETE FROM %s_favorites WHERE id=?" % plugin.args['media']
		plugin.DB.execute(SQL, [plugin.args['id']])
		plugin.DB.commit()
		plugin.DB.disconnect()
		plugin.notify('Success', 'Favorite deleted: %s' % plugin.args['title'])
		plugin.refresh()

plugin.register('delete_from_favorites', delete_from_favorites)


def new_custom_list():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	name = plugin.dialog_input("List name:")
	if name:
		response = trakt.create_custom_list(name)
		if 'ids' in response.keys():
			plugin.notify('Success', 'Added custom list', image=ARTWORK + 'trakt.png')
		else:
			plugin.notify('Failed', 'Please check your log for details', image=ARTWORK + 'trakt.png')
		plugin.refresh()
plugin.register('new_custom_list', new_custom_list)

def delete_custom_list():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	ok = plugin.confirm('Delete custom list', "click YES to continue", plugin.args['name'])
	if ok:
		response = trakt.delete_custom_list(plugin.args['slug'])
		if response:
			plugin.refresh()
		else:
			plugin.notify('Failed', 'Please check your log for details', image=ARTWORK + 'trakt.png')
plugin.register('delete_custom_list', delete_custom_list)

def delete_from_custom_list():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	ok = plugin.confirm('Delete from custom list', "click YES to continue", plugin.args['name'])
	if plugin.args['media'] == 'movie':
		media = 'movies'
	else:
		media = 'shows'
	if ok:
		response = trakt.delete_from_custom_list(plugin.args['media'], plugin.args['slug'], plugin.args['imdb_id'])
		plugin.refresh()
		if response['deleted'][media]==1:
			plugin.notify('Success', 'Removed from custom list', image=ARTWORK + 'trakt.png')
		elif response['not_found'][media]==1:
			plugin.notify('Error', 'Not found in custom list', image=ARTWORK + 'trakt.png')
		else:
			plugin.notify('Failed', 'Please check your log for details', image=ARTWORK + 'trakt.png')
plugin.register('delete_from_custom_list', delete_from_custom_list)

def add_to_custom_list():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	lists = trakt.get_custom_lists()
	options = [lists[index]['name'] for index in xrange(len(lists))]
	index = plugin.dialog_select('Add to List', options)
	if plugin.args['media'] == 'movie':
		media = 'movies'
	else:
		media = 'shows'
	if index:
		slug = lists[index]['ids']['slug']
		if plugin.args['imdb_id'] == None or plugin.args['imdb_id'] == 'None':
			id = plugin.args['tmdb_id']
			id_type = 'tmdb'
		else:
			id = plugin.args['imdb_id']
			id_type = 'imdb'
		response = trakt.add_to_custom_list(plugin.args['media'], slug, id, id_type)
		if response['added'][media]==1:
			plugin.notify('Success', 'Added to custom List', image=ARTWORK + 'trakt.png')
		elif response['existing'][media]==1:
			plugin.notify('Error', 'Already exists in list', image=ARTWORK + 'trakt.png')
		else:
			plugin.notify('Failed', 'Please check your log for details', image=ARTWORK + 'trakt.png')
plugin.register('add_to_custom_list', add_to_custom_list)	

def add_watchlist():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	if plugin.mode == 'tv_add_to_watchlist':
		media = 'shows'
	else:
		media = 'movies'
	if plugin.args['imdb_id'] == None or plugin.args['imdb_id'] == 'None':
		id = plugin.args['tmdb_id']
		id_type = 'tmdb'
	else:
		id = plugin.args['imdb_id']
		id_type = 'imdb'
	response = trakt.add_to_watchlist(media, id, id_type=id_type)
	if response['added'][media]==1:
		plugin.refresh()
		plugin.notify('Success', 'Added to watchlist', image=ARTWORK + 'trakt.png')
	elif response['existing'][media]==1:
		plugin.notify('Error', 'Already exists in watchlist', image=ARTWORK + 'trakt.png')
	else:
		plugin.notify('Failed', 'Please check your log for details', image=ARTWORK + 'trakt.png')
plugin.register(['tv_add_to_watchlist', 'movie_add_to_watchlist'], add_watchlist)

def delete_from_watchlist():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	if plugin.args['mode'] == 'tv_delete_from_watchlist':
		media = 'shows'
	else:
		media = 'movies'
	ok = plugin.confirm('Delete from watchlist', "click YES to continue", plugin.args['name'])
	if ok:
		if plugin.args['imdb_id'] == None or plugin.args['imdb_id'] == 'None':
			id = plugin.args['tmdb_id']
			id_type = 'tmdb'
		else:
			id = plugin.args['imdb_id']
			id_type = 'imdb'
		response = trakt.delete_from_watchlist(media, id, id_type=id_type)

		if response['deleted'][media]==1:
			plugin.refresh()
			plugin.notify('Success', 'Removed from Watchlist', image=ARTWORK + 'trakt.png')
		elif response['not_found'][media]==1:
			plugin.notify('Error', 'Not found in Watchlist', image=ARTWORK + 'trakt.png')
		else:
			plugin.notify('Failed', 'Please check your log for details', image=ARTWORK + 'trakt.png')
		
plugin.register(['tv_delete_from_watchlist', 'movie_delete_from_watchlist'], delete_from_watchlist)


def toggle_transmogrifier_streaming():
	val = 'false' if ADDON.get_setting('enable_transmogrifier_streaming') == "true" else 'true'
	ADDON.set_setting('enable_transmogrifier_streaming', val)
	plugin.refresh()
	
plugin.register("toggle_transmogrifier_streaming", toggle_transmogrifier_streaming)

def open_settings():
	if plugin.mode == 'settings_transmogrifier':
		id = 'service.transmogrifier'
	elif  plugin.mode == 'settings_urlresolver':
		id = 'script.module.urlresolver'
	else:
		id = ADDON_ID
	xbmcaddon.Addon(id).openSettings()

plugin.register(['settings_transmogrifier', 'settings_urlresolver', 'settings_theroyalwe'], open_settings)


'''*	Streaming and Transmogrification functions
		There are separate definitions here for movies and tv shows
		Somewhat intentional, but not really necessary.
		The common scrpper class is initialized with the cache results set to false by default
		This option caches the results of each individual site scraper to a local sqllite db on
		a per scraper basis. If scraper a times out on attempt 1, but succeeds on attempt 2, the final
		result list is merged prior to sorting.
		The results a cached for a pre-defined decay period which will probably get moved to an overidable setting at some point
*'''


def get_meta_data():
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	metadata = None
	imdb_id = plugin.get_arg('imdb_id', '')
	tmdb_id = plugin.get_arg('tmdb_id', '')
	trakt_id = plugin.get_arg('trakt_id', '')
	season = plugin.get_arg('season', '')
	episode = plugin.get_arg('episode', '')
	if plugin.mode in ['play_episode', 'play_directory_episode']:
		metadata = trakt.get_metadata('episode', imdb_id, tmdb_id, trakt_id, season, episode)
	else:
		metadata = trakt.get_metadata('movie', imdb_id, tmdb_id, trakt_id)
	return metadata
	'''
	try:
		query_id = plugin.args['imdb_id'] if plugin.args['imdb_id'] != 'None' else plugin.args['trakt_id']
	except:
		query_id = plugin.args['tmdb_id']
	
	#if 'trakt_id' in plugin.args:
	#S	query_id = plugin.args['trakt_id']
		
	if plugin.mode in ['play_episode', 'play_directory_episode']:
		season = plugin.args['season']
		episode = plugin.args['episode']
		metadata = trakt.get_episode_details(query_id, season, episode)
	else:
		metadata = trakt.get_movie_details(query_id)
	return metadata'''

def on_playback_stop():
	data = plugin.get_stream_stop_times()
	media = 'episode' if plugin.mode in ['play_episode', 'play_directory_episode'] else 'movie'
	imdb_id = plugin.args['imdb_id']
	navigate_back = False
	refresh = False if ADDON.get_setting('source_selection_mode') == 'Directory' else True
	if data['percent'] >= WATCH_PERCENT:
		if media == 'episode':
			season = plugin.args['season']
			episode = plugin.args['episode']
			set_watched(media, imdb_id, season, episode, refresh=refresh)
		else:
			set_watched(media, imdb_id, refresh=refresh)
		if refresh is False:
			navigate_back = True
	else:
		if media == 'episode':
			season = plugin.args['season']
			episode = plugin.args['episode']
			plugin.set_resume_point(imdb_id, data['current'], season, episode)
		else:
			plugin.set_resume_point(imdb_id, data['current'])
			
	path = plugin.get_property('Path')
	if path:
		c = plugin.confirm('Confirm Delete', 'Do you want to delete the cached file?')
		if c: VFSClass().rm(path)
		plugin.clear_property('Path')
	
	if navigate_back:
		plugin_url  = ADDON.load_data('last_directory.qs')
		plugin.refresh(plugin_url)
	
	if plugin.get_property('Calendar.Resume'):
		calendar_browser()

plugin.on_playback_stop = on_playback_stop

def play_episode():
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(cache_results=ADDON.get_setting('enable_result_caching')=="true")
	Scraper.threadpool_size = int(ADDON.get_setting('threadpool_size'))
	imdb_id = plugin.args['imdb_id']
	title = plugin.args['showtitle']
	season = int(plugin.args['season'])
	episode = int(plugin.args['episode'])
	year = int(plugin.args['year'])
	resolved_url = Scraper.search_tvshow(title, season, episode, year, imdb_id)
	if not resolved_url: return
	if validate_transmogrifier_streaming():
		from dudehere.routines.transmogrifier import TransmogrifierAPI
		TM = TransmogrifierAPI()
		resolved_url = TM.get_streaming_url(resolved_url, host=Scraper.host_name)
	metadata=get_meta_data()
	plugin.play_stream(resolved_url, metadata=metadata)
plugin.register('play_episode', play_episode)

def get_episode_sources():
	vfs = VFSClass()
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(cache_results=ADDON.get_setting('enable_result_caching')=="true")
	Scraper.threadpool_size = int(ADDON.get_setting('threadpool_size'))
	imdb_id = plugin.args['imdb_id']
	tmdb_id = plugin.args['tmdb_id']
	trakt_id = plugin.args['trakt_id']
	title = plugin.args['showtitle']
	season = int(plugin.args['season'])
	episode = int(plugin.args['episode'])
	year = int(plugin.args['year'])
	sources, raw_urls, results = Scraper.search_tvshow(title, season, episode, year, imdb_id, return_sources=True)
	count = len(sources)
	if count == 0:
		plugin.error_message('Search Error', 'No results, consider changing scrapers.')
		return
	count = RESULT_LIMIT if count >= RESULT_LIMIT else count
	for source in sources:
		if sources.index(source) > RESULT_LIMIT: break
		menu = ContextMenu()
		raw_url = raw_urls[sources.index(source)]
		data = results[sources.index(source)]
		try:
			quality = data['quality']
			hostname = data['host']
		except:
			quality = data.quality
			hostname = data.hostname
		if quality < 6:
			image = vfs.join(ARTWORK, 'definition/480.png')
		else:
			image = vfs.join(ARTWORK, 'definition/720.png')
		menu.add('Transmogrify', {'mode': 'tv_directory_transmogrify', "url": raw_url, "display": title, "imdb_id": imdb_id,"tmdb_id": tmdb_id, "year": year, "showtitle": title, "season": season, "episode": episode}, visible=validate_transmogrifier)	
		
		query = {
			'mode': 'play_directory_episode', 
			"display": source, 
			"raw_url": raw_url, 
			"imdb_id": imdb_id, 
			"trakt_id": trakt_id,
			"year": year, 
			"showtitle": title, 
			"season": season, 
			"episode": episode,
			"hostname": hostname
		}
		plugin.add_video_item(query, {"title": source}, total_items=count, image=image, fanart='', menu=menu)
	plugin.eod(VIEWS.BIGLIST)
plugin.register('get_episode_sources', get_episode_sources)

def play_directory_episode():
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper()
	resolved_url = Scraper.resolve_url(plugin.args['raw_url'])
	if resolved_url:
		if validate_transmogrifier_streaming():
			from dudehere.routines.transmogrifier import TransmogrifierAPI
			TM = TransmogrifierAPI()
			resolved_url = TM.get_streaming_url(resolved_url, host=plugin.args['hostname'])
		metadata=get_meta_data()
		plugin.play_stream(resolved_url, metadata=metadata)
	
plugin.register('play_directory_episode', play_directory_episode)


def delete_transmogrified_file():
	from dudehere.routines.transmogrifier import TransmogrifierAPI
	TM = TransmogrifierAPI()
	if plugin.mode == 'delete_tv_cache':
		path = TM.get_cached_file(plugin.args['title'], plugin.args['season'], plugin.args['episode'])
	else:
		path = TM.get_cached_file(plugin.args['title'], plugin.args['year'])
	if path:
		c = plugin.confirm('Confirm Delete', 'Do you want to delete the cached file?')
		if c: VFSClass().rm(path)
		plugin.refresh()
plugin.register(['delete_tv_cache', 'delete_movie_cache'], delete_transmogrified_file)

def play_transmogrified_file():
	from dudehere.routines.transmogrifier import TransmogrifierAPI
	TM = TransmogrifierAPI()
	if plugin.mode == 'play_tv_cache':
		season = int(plugin.args['season'])
		episode = int(plugin.args['episode'])
		title = plugin.args['title']
		path = TM.get_cached_file(title, season=season, episode=episode)
	else:
		year = int(plugin.args['year'])
		title = plugin.args['title']
		path = TM.get_cached_file(title, year=year)
	if path:
		plugin.play_url(path)
plugin.register(['play_tv_cache', 'play_movie_cache'], play_transmogrified_file)

def play_movie():
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(cache_results=ADDON.get_setting('enable_result_caching')=="true")
	Scraper.threadpool_size = int(ADDON.get_setting('threadpool_size'))
	imdb_id = plugin.args['imdb_id']
	tmdb_id = plugin.args['tmdb_id']
	title = plugin.args['title']
	year = plugin.args['year']
	resolved_url = Scraper.search_movie(title, year, imdb_id=imdb_id)
	if not resolved_url: return
	if validate_transmogrifier_streaming():
		from dudehere.routines.transmogrifier import TransmogrifierAPI
		TM = TransmogrifierAPI()
		resolved_url = TM.get_streaming_url(resolved_url, host=Scraper.host_name)
	plugin.play_stream(resolved_url, metadata=get_meta_data())
plugin.register('play_movie', play_movie)	

def play_directory_movie():
	from dudehere.routines.scrapers import CommonScraper
	imdb_id = plugin.args['imdb_id']
	title = plugin.args['title']
	year = plugin.args['year']
	Scraper = CommonScraper()
	resolved_url = Scraper.resolve_url(plugin.args['raw_url'])
	if resolved_url:
		metadata=get_meta_data()
		plugin.play_stream(resolved_url, metadata=metadata)
plugin.register('play_directory_movie', play_directory_movie)

def get_movie_sources():
	vfs = VFSClass()
	from dudehere.routines.scrapers import CommonScraper
	Scraper = CommonScraper(cache_results=ADDON.get_setting('enable_result_caching')=="true")
	Scraper.threadpool_size = int(ADDON.get_setting('threadpool_size'))
	imdb_id = plugin.args['imdb_id']
	tmdb_id = plugin.args['tmdb_id']
	title = plugin.args['title']
	year = int(plugin.args['year'])
	sources, raw_urls, results = Scraper.search_movie(title, year, imdb_id, return_sources=True)
	count = len(sources)
	if count == 0:
		plugin.error_message('Search Error', 'No results, consider changing scrapers.')
		return
	count = RESULT_LIMIT if count > RESULT_LIMIT else count
	for source in sources:
		if sources.index(source) >= RESULT_LIMIT: break
		menu = ContextMenu()
		raw_url = raw_urls[sources.index(source)]
		data = results[sources.index(source)]
		try:
			quality = data['quality']
		except:
			quality = data.quality
		if quality < 6:
			image = vfs.join(ARTWORK, 'definition/480.png')
		else:
			image = vfs.join(ARTWORK, 'definition/720.png')
		menu.add('Transmogrify', {'mode': 'movie_directory_transmogrify', "url": raw_url, "display": title, "imdb_id": imdb_id, "tmdb_id": tmdb_id, "year": year, "title": title}, visible=validate_transmogrifier)	
		plugin.add_video_item({'mode': 'play_directory_movie', "display": source, "raw_url": raw_url, "imdb_id": imdb_id, "tmdb_id": tmdb_id, "year": year, "title": title}, {"title": source}, total_items=count, image=image, fanart='', menu=menu)
	plugin.eod(VIEWS.BIGLIST)
plugin.register('get_movie_sources', get_movie_sources)

def queue_to_transmogrifier():
	from dudehere.routines.scrapers import CommonScraper
	from dudehere.routines.transmogrifier import TransmogrifierAPI
	if plugin.mode.startswith('movie'):
		media='movie'
		imdb_id = plugin.args['imdb_id']
		tmdb_id = plugin.args['tmdb_id']
		if imdb_id == 'None':
			from dudehere.routines.trakt import TraktAPI
			trakt = TraktAPI()
			imdb_id = trakt.query_id('tmdb', tmdb_id)
		title = plugin.args['title']
		year = plugin.args['year']
		filename = "%s (%s)" %(title,year)
		Scraper = CommonScraper(cache_results=ADDON.get_setting('enable_result_caching')=="true")
		if plugin.mode == 'tv_transmogrify':
			Scraper.threadpool_size = int(ADDON.get_setting('threadpool_size'))
			resolved_url = Scraper.search_movie(title, year, imdb_id=imdb_id)
		else:
			raw_url = plugin.args['url']
			resolved_url = Scraper.resolve_url(raw_url)
		video = {
			"type": media,
			"filename": filename,
			"url": resolved_url,
			"raw_url": "",
			"imdb_id": imdb_id,
			"title": title,
			"save_dir": "",
			"addon": ADDON_ID
		}
	else:
		media='tvshow'
		imdb_id = plugin.args['imdb_id']
		title = plugin.args['showtitle']
		season = int(plugin.args['season'])
		episode = int(plugin.args['episode'])
		year = int(plugin.args['year'])
		if imdb_id == 'None':
			from dudehere.routines.trakt import TraktAPI
			trakt = TraktAPI()
			imdb_id = trakt.query_id('tmdb', tmdb_id)
		filename = "%s %sx%s" % (title, season, episode)
		Scraper = CommonScraper(cache_results=ADDON.get_setting('enable_result_caching')=="true")
		if plugin.mode == 'tv_transmogrify':
			Scraper.threadpool_size = int(ADDON.get_setting('threadpool_size'))
			resolved_url = Scraper.search_tvshow(title, season, episode, year, imdb_id)
		else:
			raw_url = plugin.args['url']
			resolved_url = Scraper.resolve_url(raw_url)

		'''*	Queue Object
				Transmogrifier takes an array of dictionaries with the following:
				
				required
					type = movie|tvshow
					filename
					url - the resolved url
				
				optional or '' if not provided
					raw_url
					title
					season
					episode
					save_dir
		*'''
		video = {
			"type": media,
			"filename": filename,
			"url": resolved_url,
			"raw_url": "",
			"imdb_id": imdb_id,
			"title": title,
			"season": season,
			"episode": episode,
			"save_dir": "",
			"addon": ADDON_ID
		}
	if not resolved_url: return
	TM = TransmogrifierAPI()
	response = TM.enqueue([video])
	'''if TM.use_remote_host:
		if 'status' in response and response['status'] == 200:
			plugin.notify("Enqueue Success", "Added to remote tranmogrifier queue")'''
	ADDON.log(response)
plugin.register(['tv_transmogrify', 'tv_directory_transmogrify', 'movie_transmogrify', 'movie_directory_transmogrify'], queue_to_transmogrifier)

if __name__ == '__main__':
	plugin.run()
