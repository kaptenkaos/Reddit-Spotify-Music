#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spotipy
import praw
import HTMLParser
import re
import sys
import spotipy.util as util
from urlparse import urlparse

		
class Reddit(): # Class for Reddit

	def Get_comments(self, subreddit, c_limit):
		'''
		Stream comments from Reddit.
		'''
		Bot_name = ""
		r = praw.Reddit(user_agent=Bot_name)
		m_com = praw.helpers.comment_stream(r, subreddit, limit=c_limit)
		while True:
			try:
				for comments in m_com:
					h = HTMLParser.HTMLParser()
					Comment_body = h.unescape(comments.body)
					Reddit().Search_links(Comment_body)
			except KeyboardInterrupt:
				print('Keyboard Exit')
				sys.exit()
			except:
				continue

	def Search_links(self, Comment):
		'''
		Filter out all links from reddit_search and filter out the links you are after
		'''
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', Comment)
		for i in urls:
			url_parse = urlparse(i)
			if "spotify.com" in url_parse.netloc:
				print(urls)
				if '/track/' in url_parse.path:
					ex_track = url_parse.path.rsplit('/',1)
					Clean_track = ex_track[1].replace(')', '')
					Spotify().Spotify_Track(Clean_track)
					
				elif '/album/' in url_parse.path:
					Ex_album = url_parse.path.rsplit('/',1)
					Clean_album = Ex_album[1].replace(')', '')
					Spotify().Spotify_Album(Clean_album)
					
				elif '/playlist/' in url_parse.path:
					Ex_playlist = url_parse.path.rsplit('/',1)
					Clean_playlist = Ex_playlist[1].replace(')', '')
					Spotify().Spotify_Playlist(Clean_playlist)
					
				elif '/artist/' in url_parse.path:
					# Adds artist top-tracks, first 3 only
					Ex_artist = url_parse.path.rsplit('/',1)
					Clean_artist = Ex_artist[1].replace(')', '')
					Spotify().Spotify_Artist(Clean_artist)
				else:
					pass
			else:
				pass


class Spotify(): # Spotify Class
		def __init__(self):
		
			'''
			Spotify Client id, get it when you create a app at spotify
			'''
			self.client = ''
			'''
			Spotify Client secret, get it when you create a app at spotify
			'''
			self.clientsecret = ''
			'''
			Url to direct the first valid request to spotify, does not need to be a address that works.
			Intended to be the webpage of your application
			'''
			self.redirecturi = ''
			'''
			Spotify username
			'''
			self.username = ''
			'''
			Spotify playlist to add tracks to
			'''
			self.playlist_id = ''
			
		def Spotify_Track(self, track_id):
			try:
				track_id = [track_id]
				print track_id
				scope = 'playlist-modify-public'
				token = util.prompt_for_user_token(self.username, scope, client_id=self.client, client_secret=self.clientsecret, redirect_uri=self.redirecturi)
				if token:
					sp = spotipy.Spotify(auth=token)
					sp.trace = False
					results = sp.user_playlist_add_tracks(self.username, self.playlist_id, track_id)
					print results
				else:
					print "Can't get token for", username
			except:
				print('Something went wrong... :(')
			pass
			
		def Spotify_Playlist(self, playlist_id):
			# Will be coming.
			print(playlist_id)
			print('Function is not yet ready')
		
		def Spotify_Album(self, album_id):
			# Will be coming
			print(album_id)
			print('Function is not yet ready')
			
		def Spotify_Artist(self, artist_id):
			# Adds artist top-tracks, top 3 only
			sp = spotipy.Spotify()
			response = sp.artist_top_tracks(artist_id)
			for track in response['tracks'][:3]:
				Spotify().Spotify_Track(track['id'])
				print(track['id'], '-', track['name'])

if __name__ == '__main__':
	# Choose Subreddit and numbers of post
	Reddit().Get_comments('all', 150)
