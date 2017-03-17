#!/usr/bin/env python

from history import History

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import datetime
import os
import time
import sys
import subprocess
import re
import urllib.parse
import urllib.request

debug = False

class AppURLopener(urllib.request.FancyURLopener):
	version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'   # Set this to a string you want for your user agent
  

class RottenTomatoesRating:
		
	def search_movie(self):
		print ("Hello, it\'s the movie search function.\n Here are the movie scoring sources: \n")

		scoring = {"rotten tomato" : "https://www.rottentomatoes.com/browse/dvd-top-rentals?minTomato=0&maxTomato=100&minPopcorn=60&maxPopcorn=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=release"}

		for k in scoring.items():
			print (k)  

		url = scoring["rotten tomato"]

		opener = AppURLopener()
		soup = BeautifulSoup(opener.open(url).read(), 'html5lib')

		if debug:
			f = open('workfile', 'w')
			f.write(str(soup))
			f.close() 

		contents = soup.find('title').contents
		titles = self.parseSoupMovieTitle(soup)

		if contents[0] == "Page Not Found":
			return 'Sorry, there is no movie found'
		else:
			return	titles
 
	def parseSoupMovieTitle(self, soup):
		text = str(soup)
		titles = re.findall(r"title\".*?,", text)
		result = []

		for st in titles:
			st = st[:-1]
			st = st.replace("title\":", "")
			st = st.replace("\"", "")
			result.append(st)
		return result
		
	def fetch_torrent(self, titles):

		history = History()
		downloaded_titles = history.init_downloaded_title()
		computed_titles = self.diff(titles, downloaded_titles)
		print ('computed titles: ', computed_titles);

		if not computed_titles:
			print ('nothing to download...exit now')
			return

		url_base = 'https://thepiratebay.org'
		for title in computed_titles:
			torrent_page_url = url_base + '/search/' + title +'%201080p/0/99/207'
			print (torrent_page_url)

			history = History()
			history.add_downloaded_title(title)
			time.sleep(1)

			self.invoke_transmission(title, torrent_page_url)
			time.sleep(5)
			
	def invoke_transmission(self, title, link):
		url = link
               
		opener = AppURLopener()
		soup = BeautifulSoup(opener.open(url).read(), 'html5lib')

		if debug:
			f = open('torrent_page_workfile', 'w')
			f.write(str(soup))
			f.close()

		magnet_link = self.parseSoupMagnetLink(soup)
		if magnet_link is None:
			print ('Unable to find torrent for it')
		
		else:
			now = str(datetime.datetime.now())
			with open('transmission.' + now + '.log', 'w') as output:
				cwd=(os.getcwd())
				p = subprocess.Popen([ cwd + "/" + "call_transmission.sh", magnet_link], stdout=output)
				p.communicate()

	def parseSoupMagnetLink(self, soup):
		text = str(soup)
		links = re.findall(r"magnet\:\?xt.*?\"", text)

		if not links:
			print("List is empty")
			return None
		
		else:
			result = []

			for st in links:
				st = st[:-1]
				st = st.replace("\"", "")
				result.append(st)
			return result[0]

	def diff(self, first, second):
		second = set(second)
		return [item for item in first if item not in second]


def main(argv):
	print ('Argument List:' + ' ' + str(len(argv)), '\n')
	if (len(argv) == 0):
		
		rt = RottenTomatoesRating()
		titles = rt.search_movie()
		print ('\n### Here are the results:\n')
		print (titles)

		rt.fetch_torrent(titles)

	elif (len(argv) == 1):
		print ('fetching: ' + argv[0], '\n')
		rt = RottenTomatoesRating()
		title = argv[0]

		titles = []
		titles.append(title)
		rt.fetch_torrent(titles)
		
	else:
		print ('incorrent input\n')
		print ('Usage: python3 movie_search.py [movie title]')


if __name__ == "__main__":
   main(sys.argv[1:])



