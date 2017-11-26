# -*- coding: utf-8 -*-

from resources.lib.client import Client
from resources.lib import hltv
from resources.lib.common import *

client = Client()

args   = urlparse.parse_qs(sys.argv[2][1:])
mode   = args.get('mode', ['home'])[0]
title  = args.get('title', [''])[0]
_id     = args.get('id', [''])[0]
params = args.get('params', [''])[0]
if not args:
    args = version
log('[%s] arguments: %s' % (addon_id, str(args)))

if mode == 'home':
    hltv.home_items(client.matches())
elif mode == 'archive':
    hltv.archive_items(client.archive())
elif mode == 'details':
    hltv.details_items(client.request(base_hltv+_id))
elif mode == 'play':
    hltv.play(_id)