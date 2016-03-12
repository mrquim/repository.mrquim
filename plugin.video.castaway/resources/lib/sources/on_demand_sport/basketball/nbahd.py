from __future__ import unicode_literals
from resources.lib.modules import client,webutils
import re,urlparse



class info():
    def __init__(self):
    	self.mode = 'nbahd'
        self.name = 'nbahd.com (full replays)'
        self.icon = 'nbahd.png'
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://nbahd.com'):
		self.base = 'http://nbahd.com'
		self.url = url

	def items(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		items=soup.findAll('div',{'class':'thumb'})
		out=[]
		for item in items:
			url = item.find('a')['href']
			title=item.find('a')['title'].encode('utf-8')
			thumb=item.find('img')['src'].encode('utf-8')

			out+=[[title,url,thumb]]

		return out

	def links(self,url, img=' '):
		if 'nbahd.com' not in url:
			url = self.base + url
		html = client.request(url)
		soup = webutils.bs(html)
		tags=soup.find('div',{'class':'entry-content rich-content'}).findAll('p')
		tags.pop(0)
		out=[]
		tag=tags[0]
		parts=tag.findAll('a')
		i = 1
		for part in parts:
			url = part['href']
			title = 'Part %s'%i
			img = ' '
			i+=1
			out.append((title,url,img))

		if len(out)==0:
			links=re.findall('<p><img src="(.+?)"/>\s*</p>\s*<p>\s*<a href="(.+?)" target="_blank">\s*<img src=".+?"/></a>\s*<a href="(.+?)" target="_blank">\s*<img src=".+?"/></a>\s*<a href="(.+?)" target="_blank">\s*<img src=".+?"/></a>\s*<a href="(.+?)" target="_blank">\s*<img src=".+?"/></a>\s*',html)
			i = 1
			pos = 0
			for link in links:
				img = link[0]
				for i in range(4):
					url = link[i+1]
					title = 'Part %s'%(i+1)
					out.append((title,url,img))


		return out





	def resolve(self,url):
		html=client.request(url)
		soup=webutils.bs(html)
		try:
			link=soup.find('iframe',{'frameborder':'0'})['src']
		except:    
			sd = url=re.findall('<source src=["\']([^"\']+)["\'] type=["\']video/mp4["\'] data-res=["\']360p',html)[0]
			try:
				hd = url=re.findall('<source src=["\']([^"\']+)["\'] type=["\']video/mp4["\'] data-res=["\']720p',html)[0]
			except:
				hd = sd
			return hd

		if 'http' not in link:
			link = 'http://nbahd.com' + link
		try:
			html=client.request(link)
			sd = url=re.findall('<source src=["\']([^"\']+)["\'] type=["\']video/mp4["\'] data-res=["\']360p',html)[0]
			try:
				hd = url=re.findall('<source src=["\']([^"\']+)["\'] type=["\']video/mp4["\'] data-res=["\']720p',html)[0]
			except:
				hd = sd
			return hd
		except:
				try:
					import urlresolver
					resolved = urlresolver.resolve(link)
					return resolved
				except:
					return




	def next_page(self):

		html = client.request(self.url)
		try:
			next_page=re.findall('<a.+?rel="next".+?href="(.+?)"',html)[0]
			if 'nbahd.com' not in next_page:
				next_page = self.base + next_page
		except:
			next_page=None
		return next_page


