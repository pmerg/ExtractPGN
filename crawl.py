import os
import urllib
from lxml import html

def searchURLForLE(year):
    url = 'http://www.chessgames.com/perl/chess.pl?yearcomp=le&year={0}&playercomp=either&pid=&player=&pid2=&player2=&movescomp=exactly&moves=&opening=&eco=&result='
    return url.format(year)

def readGameLinks(year):
    page = html.fromstring(urllib.urlopen(searchURLForLE(year)).read())    
    for link in page.xpath("//a"):
        if 'chessgame?gid' in link.get("href") :
            yield link.get("href")

a = readGameLinks(1500)
for x in a:
    print x
        
#print (downloadPGNs(1000, 1147))
