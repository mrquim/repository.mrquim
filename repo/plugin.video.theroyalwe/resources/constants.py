from dudehere.routines import *
WATCHLIST_COLOR = 'yellow'
HAS_TRANMOGRIFIED = 'orange'
WATCH_PERCENT = 94
RESULT_LIMIT = 500

if ADDON.get_setting('enable_default_views') == 'true':
	VIEWS = enum(DEFAULT=ADDON.get_setting('default_folder_view'), LIST=50, BIGLIST=51, THUMBNAIL=500, SMALLTHUMBNAIL=522, FANART=508, POSTERWRAP=501, MEDIAINFO=504, MEDIAINFO2=503, MEDIAINFO3=515, WIDE=505, LIST_DEFAULT=ADDON.get_setting('default_list_view'), TV_DEFAULT=ADDON.get_setting('default_tvshow_view'), MOVIE_DEFAULT=ADDON.get_setting('default_movie_view'), SEASON_DEFAULT=ADDON.get_setting('default_season_view'), EPISODE_DEFAULT=ADDON.get_setting('default_episode_view'))
else:
	from dudehere.routines.plugin import VIEWS