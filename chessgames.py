import os
import urllib
import urlparse
from lxml import html

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

readPGN('http://www.chessgames.com/perl/nph-chesspgn?gid=1652621&text=1')

games = readGameLinks('http://www.chessgames.com/perl/chessplayer?pid=128162')
pgn = ''

for game in games:
    url = 'http://www.chessgames.com/perl/nph-chesspgn?gid={0}&text=1'.format(game)
    pgn = pgn + readPGN(url) + '\n\n'