from xml.dom import minidom
from ripper import Ripper
from glob import glob

files = glob('*.xml')
contents = []


for f in files:
    fic = open(f, 'r', encoding = 'utf-8', errors = 'ignore' )
    content = fic.read()
    content = content.replace('&', '')
    contents.append(content)
    fic.close()
    

for c in contents:
    print(c)
    current_content = minidom.parseString(c)
    


print(content.getElementsByTagName('title')[0].firstChild.data)
track = content.getElementsByTagName('track')

for t in track:
    ix = t.getElementsByTagName('ix')[0]
    length = t.getElementsByTagName('length')[0]
    print('Titre ' + ix.firstChild.data + ' : ' + length.firstChild.data)


