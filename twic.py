#
# Script for loading and merging TWIC chess games. This is a free and efficient way to build a megadatabase for chess.
#

from urllib import urlopen
from zipfile import ZipFile
from StringIO import StringIO

def downloadPGN(issue):
    issue = 'http://www.theweekinchess.com/zips/twic' + str(issue) + 'g.zip'
    
    try:
        zipFile = ZipFile(StringIO(urlopen(issue).read()))

        # Eg: twic1147.pgn
        files = [x for x in zipFile.namelist() if x.endswith('.pgn')] 
        
        return ''.join(zipFile.open(files[0]).readlines())
    except Exception:
        print ('Failed to download: ' + str(issue))
        return ''

def downloadPGNs(start, end):
    games = ''    
    for i in range(start, end):
        games = games + downloadPGN(i)
    return games
        
print (downloadPGNs(1000, 1147))