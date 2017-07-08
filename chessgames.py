import os
import sys
import urllib
import urlparse
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool 

def readGameLinks(url, cur=1):
    links = []
    page = html.fromstring(urllib.urlopen(url).read())
    hasNext = False    
    nextURL = None
    for link in page.xpath("//a"):
        if link.get("href") != None:
            if 'chessgame?gid' in link.get("href"):
                parsed = dict(urlparse.parse_qsl(urlparse.urlsplit(link.get("href")).query))
                links.append(parsed['gid'])
            elif 'page=' in link.get("href") and hasNext == False:
                page = int(link.get('href').split('page=')[1].split('&')[0])
                if page == cur + 1:
                    hasNext = True
                    nextURL = 'http://www.chessgames.com/' + link.get("href")
    if nextURL is not None:
        links = links + readGameLinks(nextURL, cur=cur+1)    
    return links

def readPGN(url):
    return urllib.urlopen(url).read()

def readGame(game):
    url = 'http://www.chessgames.com/perl/nph-chesspgn?gid={0}&text=1'.format(game)
    return readPGN(url) + '\n'

# http://www.chessgames.com/perl/chessplayer?pid=24694
url = sys.argv[1]

toks = url.split('?')

# http://www.chessgames.com/perl/chess.pl?page=1&pid=24694
url = 'http://www.chessgames.com/perl/chess.pl?page=1&' + toks[1]

# Parse all games for the player
games = list(reversed(readGameLinks(url)))

# Read the games
results = [readGame(i) for i in games]

print ''.join(results)