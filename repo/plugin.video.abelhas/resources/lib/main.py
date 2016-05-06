# -*- coding: utf-8 -*-

""" 2016 fightnight"""

import cache,requester
from functions import *
from variables import *

def first_menu():
        if setting('warning') == "true":
                warning_dialog(title="CopiaPop.com",text="Os sites abelhas.pt, toutbox e lolabits vão encerrar dia 31 de Março.\n\nO addon foi migrado para o novo site do grupo Abelhas, o CopiaPop.com. O site é espanhol e é bastante semelhante ao abelhas.\n\nCom a alteração do site, o addon foi re-escrito e as restantes funcionalidades vão sendo adicionadas nos próximos dias.\n\nFaçam upload dos vossos conteúdos para este novo site (CopiaPop.com) para aceder via este addon.")
                setSetting('warning',value="false")
        
        myuser=setting('copiapop-username')
        addDirectoryItem("[COLOR red][B]Addon em actualização[/B][/COLOR]", 'user', 'movies.png', 'DefaultMovies.png')
        addDirectoryItem("Colecções mais recentes", 'recents', 'movies.png', 'DefaultMovies.png')
        addDirectoryItem("Ir para um utilizador", 'user', 'movies.png', 'DefaultMovies.png')
        if myuser != "": addDirectoryItem("Ir para o meu utilizador (%s)" % myuser, 'user&query=%s' % myuser, 'movies.png', 'DefaultMovies.png')
        addDirectoryItem("Pesquisar", 'search', 'movies.png', 'DefaultMovies.png')
        endDirectory()

def open_folder(url,page="1"):
        formating=''
        headers={'Accept':'*/*','Accept-Encoding':'gzip,deflate','Connection':'keep-alive','X-Requested-With':'XMLHttpRequest'}
        if len(url.split('/')) > 4:
                final_url = url + '/list,1,%s?ref=pager' % page
        else: final_url = url
        result = requester.request(final_url,headers=urllib.urlencode(headers))
        
        if checkvalid(result):
                list=list_folders(final_url,result=result)
                list.extend(list_items(final_url,result=result))
                show_items(list)
                page_check(result=result, baseurl=url)
                endDirectory()

def page_check(result,baseurl):
        if 'data-nextpage-number=' in result:
                page=re.compile('data-nextpage-number="(.+?)"').findall(result)[0]
                addDirectoryItem('Página %s >>' % (page), 'folder&url=%s&page=%s' % (urllib.quote_plus(baseurl),page), '', '')
                #endDirectory()

def go_to_user(query=None):
        if query == None:
                #t = lang(30201).encode('utf-8')
                t='Ir para utilizador'
                k = keyboard('', t) ; k.doModal()
                query = k.getText() if k.isConfirmed() else None
        if (query == None or query == ''): return
        url='%s/%s' % (CopiaPopURL,query)
        open_folder(url)    

def search(query=None):
        types=['Todos os ficheiros','Video','Imagens','Musica','Documentos','Arquivos','Programas']
        params=['','Video','Image','Music','Document','Archive','Application']
        index=dialog.select('CopiaPop', types)
        if index > -1:
                if not infoLabel('ListItem.Title') == '':
                        query = window.getProperty('%s.search' % addonInfo('id'))
                elif query == None:
                        #t = lang(30201).encode('utf-8')
                        t='Procurar Ficheiros'
                        k = keyboard('', t) ; k.doModal()
                        query = k.getText() if k.isConfirmed() else None
                        #cache.get('last_search',5,query)
                if (query == None or query == ''): return

                window.setProperty('%s.search' % addonInfo('id'), query)
                show_items(list_items('%s%s' % (CopiaPopURL, SearchParam),query=query,content_type=params[index]))
                endDirectory()

def list_folders(url,query=None,result=None):
        try:
                list=[]
                items=[]
                headers={'Accept':'*/*','Accept-Encoding':'gzip,deflate','Connection':'keep-alive','X-Requested-With':'XMLHttpRequest'}
                if result==None: result = requester.request(url,headers=urllib.urlencode(headers))
                result = result.decode('iso-8859-1').encode('utf-8')
                result = requester.parseDOM(result, 'div', attrs = {'class': 'collections_list responsive_width'})[0]
                items=requester.parseDOM(result, 'li')
                for indiv in items:
                        name = requester.replaceHTMLCodes(requester.parseDOM(indiv, 'a', attrs = {'class': 'name'})[0].encode('utf-8'))
                        length = re.compile('(\d+)').findall(requester.parseDOM(indiv, 'p', attrs = {'class': 'info'})[0].encode('utf-8'))[0]
                        pageurl = CopiaPopURL + requester.parseDOM(indiv, 'a', attrs = {'class': 'name'}, ret = 'href')[0]
                        thumb = requester.parseDOM(indiv, 'img', ret='src')[0].replace('/thumbnail','')
                        list.append({'type':'folder','name': name, 'length': length, 'thumb':thumb, 'pageurl':pageurl})
                list = sorted(list, key=lambda k: re.sub('(^the |^a )', '', k['name'].lower()))
                return list
        except: return []
                
                
def list_items(url,query=None,result=None,content_type=None):
        list=[]
        try:
                if result==None:
                        headers={'Accept':'*/*','Accept-Encoding':'gzip,deflate','Connection':'keep-alive','X-Requested-With':'XMLHttpRequest'}
                        if query:
                                post={'Mode':'List','Type':content_type,'Phrase':query,'SizeFrom':'0','SizeTo':'0','Extension':'','ref':'pager','pageNumber':'1'}
                                result = requester.request(url,post=urllib.urlencode(post),headers=urllib.urlencode(headers))
                        else: result = requester.request(url,headers=urllib.urlencode(headers))
        except:
                pass

        result = result.decode('iso-8859-1').encode('utf-8')
        items = requester.parseDOM(result, 'div', attrs = {'class': 'list_row'})
        try:thumb = requester.parseDOM(result, 'meta', ret='content', attrs = {'property': 'og:image'})[0]
        except:thumb = None

        for indiv in items:
                name = requester.replaceHTMLCodes(requester.parseDOM(requester.parseDOM(indiv, 'div', attrs = {'class': 'name'}), 'a')[0].encode('utf-8'))
                size = requester.parseDOM(requester.parseDOM(indiv, 'div', attrs = {'class': 'size'}), 'p')[0].encode('utf-8')
                pageurl = CopiaPopURL + requester.parseDOM(requester.parseDOM(indiv, 'div', attrs = {'class': 'name'}), 'a', ret = 'href')[0]
                temp = requester.parseDOM(requester.parseDOM(indiv, 'div', attrs = {'class': 'date'})[0], 'div')[0]
                fileid = requester.parseDOM(temp, 'input', ret='value', attrs = {'name': 'fileId'})[0]
                list.append({'type':'content','name': name, 'size': size, 'fileid':fileid, 'thumb':thumb, 'pageurl':pageurl})
        return list

def show_items(list):
        for items in list:
                if items['type']=='content':
                        url = '%s?action=play&url=%s' % (sysaddon, urllib.quote_plus(items['pageurl']))
                        cm = []
                        cm.append(('Info'.encode('utf-8'), 'Action(Info)'))
                        item_ind = item(label='[B]%s[/B] (%s)' % (items['name'],items['size']), iconImage=items['thumb'], thumbnailImage=items['thumb'])

                        try: item_ind.setArt({'poster': items['thumb'], 'banner': items['thumb']})
                        except: pass

                        item_ind.setProperty('Fanart_Image', items['thumb'])
                        item_ind.setProperty('Video', 'true')
                        item_ind.setProperty('IsPlayable', 'true')
                        item_ind.addContextMenuItems(cm, replaceItems=True)
                        addItem(handle=int(sys.argv[1]), url=url, listitem=item_ind, isFolder=False)
                elif items['type']=='folder':
                        url = 'folder&url=%s' % (urllib.quote_plus(items['pageurl']))
                        addDirectoryItem('[B]%s[/B] (%s ficheiros)' % (items['name'],items['length']), url, items['thumb'], items['thumb'])
        #endDirectory()

def checkvalid(content):
        try:
                if 'id="error404"' in content: return False
                else: return True
        except: return False

def resolve_url(url,play=False):
        headers={'Accept':'*/*','Accept-Encoding':'gzip,deflate','Connection':'keep-alive','X-Requested-With':'XMLHttpRequest'}
        result = requester.request(url,headers=urllib.urlencode(headers))
        result = result.decode('iso-8859-1').encode('utf-8')
        name = requester.parseDOM(result, 'meta', ret='content', attrs = {'property': 'og:title'})[0]
        fileid = requester.parseDOM(result, 'input', ret='value', attrs = {'name': 'fileId'})[0]
        token = requester.parseDOM(result, 'input', ret='value', attrs = {'name': '__RequestVerificationToken'})[0]
        formurl = CopiaPopURL + requester.parseDOM(result, 'form', ret='action', attrs = {'class': 'download_form'})[0]
        headers={'Accept':'*/*','Accept-Encoding':'gzip,deflate','Connection':'keep-alive','X-Requested-With':'XMLHttpRequest'}
        post={'fileId':fileid,'__RequestVerificationToken':token}
        result = json.loads(requester.request(formurl,post=urllib.urlencode(post),headers=urllib.urlencode(headers)))
        if result['DownloadUrl'].startswith('http'):
                if play==True: play_url(result['DownloadUrl'],name,original_url=url,original_filename=name)
                else: return result['DownloadUrl']

def check_subtitle(original_url,original_name):
        subtitle_url=None
        try:
                base_url = '/'.join(original_url.split('/')[:-1])
                page=original_url.split('/')[-1].split(',')[4].split('.')[0]
                for content in list_items(base_url + '/list,1,%s?ref=pager' % page):
                        if content['name'].encode('utf-8') == '%s.srt' % (original_name):
                                subtitle_url=resolve_url(content['pageurl'])
                                break
                if subtitle_url == None:
                        for content in list_items(base_url + '/list,1,%s?ref=pager' % str(int(page+1))):
                                if content['name'].encode('utf-8') == '%s.srt' % (original_name):
                                        subtitle_url=resolve_url(content['pageurl'])
                                        break
        except Exception:
                (etype, value, traceback) = sys.exc_info()
                Debug("%s\n%s\n%s" % (etype,value,traceback))
        return subtitle_url
                        
def play_url(url,name='CopiaPop File',thumb=None,original_url='http://www.example.com/foobar.mp4',original_filename='foobar.mp4'):
        if not addonInfo('id').lower() == infoLabel('Container.PluginName').lower():
                progress = True if setting('progress.dialog') == '1' else False
        else:
                resolve(int(sys.argv[1]), True, item(path=''))
                execute('Dialog.Close(okdialog)')
                progress = True
        
        item_ind = item(label=name,path=url, iconImage='DefaultVideo.png', thumbnailImage=thumb)
        item_ind.setInfo(type='Video', infoLabels = {})
        item_ind.setProperty('Video', 'true')
        item_ind.setProperty('IsPlayable', 'true')
                        
        player.play(url, item_ind)
        resolve(int(sys.argv[1]), True, item_ind)

        if setting('file-subtitles') == 'true':
                result=check_subtitle(original_url,original_filename)
                if result!=None:
                        player.setSubtitles(result)
