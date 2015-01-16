#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spotipy
import praw
import HTMLParser
import re
import spotipy.util as util
from urlparse import urlparse
'''
Spotify Client id, get it when you create a app at spotify
'''
client = 'Client-ID'
'''
Spotify Client secret, get it when you create a app at spotify
'''
clientsecret = 'Client-Secret'
'''
Url to direct the first valid request to spotify, does not need to be a address that works.
Intended to be the webpage of your application
'''
redirecturi='redirect-URL'
'''
Spotify username
'''
username = 'Spotify Username'
'''
Spotify playlist to add tracks to
'''
playlist_id = 'Playlist ID'

def reddit_search():
	r = praw.Reddit(user_agent='Reddit-Spoitfy-Music')
	m_com = praw.helpers.comment_stream(r, 'all', limit=150)
	while True:
		try:
			for comments in m_com:
				h = HTMLParser.HTMLParser()
				comment_body = h.unescape(comments.body)
				search(comment_body)
				
				
		except KeyboardInterrupt:
			print('Keyboard Exit')
			pass
		except:
			continue

def search(body_comment):
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body_comment)
	for i in urls:
		search_spotify(i)
		
def search_spotify(i):
	url_parse = urlparse(i)
	if url_parse.netloc == 'open.spotify.com':
		if '/track/' in url_parse.path:
			ex_track = url_parse.path.rsplit('/',1)
			clean_track = ex_track[1].replace(')', '')
			print(clean_track)
			spotify_track(clean_track)
		else:
			pass
	else:
		pass

def spotify_artist(artist):
	sp = spotipy.Spotify()
	track = sp.artist(artist)
	print(track.get('name'))

def spotify_track(track_id):
	try:
		track_id = [track_id]
		print track_id
		scope = 'playlist-modify-public'
		token = util.prompt_for_user_token(username, scope, client_id=client, client_secret=clientsecret, redirect_uri=redirecturi)
		if token:
			sp = spotipy.Spotify(auth=token)
			sp.trace = False
			results = sp.user_playlist_add_tracks(username, playlist_id, track_id)
			print results
		else:
			print "Can't get token for", username
	except:
		print('Something went wrong... :(')
		pass


if __name__ == '__main__':
	reddit_search()
