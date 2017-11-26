# -*- coding: utf-8 -*-

import simple_requests as requests
from common import *

class Client:

    def __init__(self):
    
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36 OPR/41.0.2353.69"
        }
   
    def matches(self):
        return requests.get(base_hltv+'/matches', headers=self.headers).text
    
    def archive(self):
        return requests.get(base_hltv+'/results', headers=self.headers).text
    
    def request(self, url):
        return requests.get(url, headers=self.headers).text