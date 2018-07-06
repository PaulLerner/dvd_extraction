""" 
Usage: 
    rip.py --series=<name> --season=<season> --from=<first> --to=<last>
    rip.py -h | --help
    
Options:
    --series <name>    name of the serie
    --season <season>  number of the season
    --from <first>     number of the first episode
    --to <last>        number of the last episode
    
"""

from xml.dom import minidom
from docopt import docopt
from tvd.rip import Ripper
import subprocess 
import os 

arguments = docopt(__doc__)

class Track:
    def __init__(self, ix, length):
        self.title = str(ix)
        self.duration = float(length)  
        
name   = arguments.get('--series')
season = arguments.get('--season')
first  = int(arguments.get('--from'))
last   = int(arguments.get('--to'))

ripper = Ripper()

doc = ripper.lsdvd()
doc = ripper.recode(doc)

content = minidom.parseString(doc)
ripper.print_contentTitle(content)

tracks = ripper.get_tracks(content)
tracks = ripper.sort_tracks(tracks)

episodes = ripper.get_episodes(tracks, first, last)
episodes = ripper.sort_episodes(episodes)
        
ripper.print_episodes(episodes)
audios = ripper.get_languages(content)
for a in audios:
    print(a.language + '   ' + str(a.channels))


ripper.rip(episodes, name, season, first)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
