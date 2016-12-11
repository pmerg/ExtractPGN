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
    for link in page.xpath("//a"):
        if link.get("href") != None:
            if 'chessgame?gid' in link.get("href"):
                parsed = dict(urlparse.parse_qsl(urlparse.urlsplit(link.get("href")).query))
                links.append(parsed['gid'])
            elif ('perl/chess.pl?page=' + str(cur+1)) in link.get("href") and hasNext == False:
                hasNext = True
                links = links + readGameLinks('http://www.chessgames.com/' + link.get("href"), cur=cur+1)
    return links

def readPGN(url):
    return urllib.urlopen(url).read()

def readGame(game):
    url = 'http://www.chessgames.com/perl/nph-chesspgn?gid={0}&text=1'.format(game)
    return readPGN(url) + '\n\n'

# Parse all games for the player
games = readGameLinks(sys.argv[1])

pool = ThreadPool(10)
results = pool.map(readGame, games)

print results
print ''.join(results)
