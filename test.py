from xml.dom import minidom
from tvd.rip import Ripper
from glob import glob
import yaml

files = glob('*.xml')

data = open('data.yml', 'r', encoding = 'utf-8', errors = 'ignore')
data = data.read()
data = yaml.load(data)
input = data.get('name')
print(input)


texts = []

print(files)

for f in files:
    fi = open(f, 'r', encoding = 'utf-8', errors = 'ignore' )
    content = fi.read()
    content = content.replace('&', '')
    texts.append(content)

for t in texts:
    current = minidom.parseString(t)
    ripper = Ripper()
    tracks = ripper.get_tracks(current)
    ripper.print_contentTitle(current)
    tracks = ripper.sort_tracks(tracks)
    ripper.print_tracks(tracks)
    print ('')
        



