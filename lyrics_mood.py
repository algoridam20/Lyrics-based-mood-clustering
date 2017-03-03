import urllib
import urllib2
import pickle
import csv
from bs4 import BeautifulSoup
from google import search

class song:
	name = ''
	artist = ''
	lyrics = ''
	mood = ''
	cluster = ''

def read_lyrics( str ):

	handle = urllib.urlopen(str).read()
	soup = BeautifulSoup(handle,'lxml')
	l_data = soup.find_all("div", {"id":"lyrics-body-text"})
	for item in l_data:
		try:
			return item.text.encode('utf8')     ;
		except:
			pass
	return;

def fold(string):
	string = string.lower().replace(" ","-")
	ans = ''
	for c in string:
		if(c == '[' or c == '('):
			break
		elif(c.isalpha() or c.isdigit()	 or c == '-' ):
			ans = ans + c
	return ans[:-1]

def allmusic(root_url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	f = opener.open(root_url)
	soup = BeautifulSoup(f,'lxml')

	div_data = soup.find_all("div",{"class":"mood-container"})
	for div in div_data:
		links = div.findAll('a')
		for a in links:
			read_mood_songs(a['href'],a.text)
	return;

def read_mood_songs(mood_url,song_mood):
	#print ("**********" + song_mood + "**********\n\n")
	mood_url = mood_url + "/songs"
	
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	f = opener.open(mood_url)
	soup = BeautifulSoup(f,'lxml')
	songs_data = soup.find_all("tr")
	i = 0
	no = 0
	l = 0
	for item in songs_data:
	    i = i + 1
	    if(i>1):
	    	try:
	    		song_name = fold(item.contents[1].text)
	    		song_artist = fold(item.contents[3].text)
	    		
	    		
	    		lyric_url = "https://www.metrolyrics.com/" + song_name + "-lyrics-" + song_artist + ".html"
	    		song_lyrics = (read_lyrics(lyric_url))
	    		
	    		if(not song_lyrics):
	    			query = song_name + " " + song_artist + " metrolyrics"
		    		for url in search(query, stop=1):
		    			sub_lyric_url = url
		    			break
		    		song_lyrics = (read_lyrics(sub_lyric_url))
		    	
		    	no = no + 1
		    	
		    	s = song()
		    	s.name = song_name
		    	s.artist = song_artist
		    	s.lyrics = song_lyrics.replace('\n','\t')
		    	s.mood = song_mood
		    	s.cluster = '0'
		    	data.append(s)
		    	
		    	col = ";"
		    	inv = ""
		    	string = s.name+col+s.artist+col+s.mood+col+s.cluster+col+inv+s.lyrics+inv+col
		    	
		    	print(string)
	    	except:    		
	    		pass


	return;


data = list()
print("Name;Artist;Mood;cluster;lyrics")
allmusic("https://www.allmusic.com/moods")
with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)

