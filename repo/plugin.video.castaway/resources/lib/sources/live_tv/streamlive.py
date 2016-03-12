from __future__ import unicode_literals
from resources.lib.modules import client, webutils
import re, urllib, requests


class info():
    def __init__(self):
    	self.mode = 'streamlive'
        self.name = 'Streamlive.to'
        self.icon = 'streamlive.png'
        self.paginated = True
        self.categorized = True
        self.multilink= False


class main():
	def __init__(self, url = 'http://www.streamlive.to/channels/?sort=1'):
		self.base = 'http://www.streamlive.to/'
		self.url = url
		self.session = self.start_session()


	def categories(self):
		html = self.session.get(self.url).text
		soup = webutils.bs(html)
		items = soup.find('select', {'name':'category'}).findAll('option')
		cats = []
		ic = info().icon
		for item in items:
			name = item['value']
			url = self.base + name
			if name =='': name = 'All'
			cats.append((url, name, ic))
		return cats



	def channels(self, url):
		self.url = url
		html = self.session.get(url).text

		regex='<a href="(.+?)" title=".+?" class="clist-thumb">\s*<img .+? src="(.+?)" src=".+?" alt="(.+?)" '
		reg=re.compile(regex)
		channels = re.findall(regex,html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			url = channel[0]
			img = 'http:' + channel[1]
			title = channel[2].encode('utf-8')
			new.append((url,title,img))
		return new

	def next_page(self):
		print(self.url)
		html = self.session.get(self.url, headers={'referer':self.base}).text
		try: 
			next = re.compile('>\s\d+\s<a href="(.+?)">').findall(html)[0]
			return next
		except:
			return


	def start_session(self):
		s = requests.Session()
		html = s.get(self.url, headers={'referer':self.base, 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to'}).text
		if 'captcha' in html:
			try:
				answer = re.findall('Question\:.+?\:(.+?)<',html)[0].strip()
			except:
				answer = eval(re.findall('Question\:(.+?)<',html)[0].replace('=?',''))
			
			post = urllib.urlencode({"captcha":answer})
			html = s.post(self.url, data=post, headers={'referer':self.base, 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to'}).text
			
		return s
