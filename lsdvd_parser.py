from xml.dom import minidom
import subprocess
import os 

class Track:
    def __init__(self, ix, length):
        self.title = str(ix)
        self.duration = float(length)

with open(os.devnull, mode='w') as f:
    doc = subprocess.check_output(
    ['lsdvd', '-x', '-Ox', '/dev/dvd'] , stderr = f)

doc = doc.decode('utf-8', 'ignore').replace('&', '')
doc = doc.encode('utf-8')

content = minidom.parseString(doc)


print(content.getElementsByTagName('title')[0].firstChild.data)
track = content.getElementsByTagName('track')

longest = content.getElementsByTagName('longest_track')[0]
print('The longest title : ' + longest.firstChild.data) 

tracks = []
i = 0

for t in track:
    ix = t.getElementsByTagName('ix')[0]
    length = t.getElementsByTagName('length')[0]
    
    t = Track(ix.firstChild.data, length.firstChild.data)
    tracks.append(t)
    print('Title ' + tracks[i].title + ' : ' + str(tracks[i].duration))
    
    i = i+1

print('')

'''
def get_duree(Piste):
    return Piste.duree
    
sorted(pistes, key=pistes.get_duree, reverse=True)
'''

swap = True
i = 0
while swap == True:
    swap = False
    i = i + 1
    for j in range(0, len(tracks)-i):
        if tracks[j].duration < tracks[j+1].duration:
            swap = True
            tracks[j],tracks[j+1] = tracks[j+1],tracks[j]          

print('')

for t in tracks:
    print('Title ' + t.title + ' : ' + str(t.duration))
    

episodes = []
nbEpisodes = int(input('How many episodes ?'))

if nbEpisodes > 1 and tracks[0].duration > tracks[1].duration*1.5 :
    firstTitleContainsAll = True
else:
    firstTitleContainsAll = False

if firstTitleContainsAll:
    for i in range(1,nbEpisodes+1):
        episodes.append(tracks[i])
else:
    for i in range(0,nbEpisodes+0):
        episodes.append(tracks[i])
        
i = 1
for e in episodes:
    print('Episode ' + str(i) + ' : title -> ' + e.title + ' | duration -> ' + str(e.duration))
    i = i + 1 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
