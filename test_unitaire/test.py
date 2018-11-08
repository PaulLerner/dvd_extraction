from xml.dom import minidom
from tvd.rip import Ripper #modified version
from glob import glob
import yaml

files = glob('*.xml')

data = open('data.yml', 'r', encoding = 'utf-8', errors = 'ignore')
data = data.read()
data = yaml.load(data)

texts = []

for f in files:
    print('FILE', f)
    fi = open(f, 'r', encoding = 'utf-8', errors = 'ignore' )
    content = fi.read()
    content = content.replace('&', '')
    texts.append(content)

verification = True
for t in texts:
    if verification:
        current = minidom.parseString(t)
        ripper = Ripper()
        ripper.print_contentTitle(current)
        tracks = ripper.sort_tracks(ripper.get_tracks(current))

        input = data.get(ripper.get_contentTitle(current))

        episodes = ripper.get_episodes(tracks, input.get('from'), input.get('to'))
        episodes = ripper.sort_episodes(episodes)

        print('sorted tracks lists')
        for t in tracks:
            print(t.title, t.duration)
        print('sorted episodes lists')
        for e in episodes:
            print(e.title, e.duration)

        audio = ripper.get_languages(current, input.get('from'), input.get('to'))

        test_episodes = input.get('episodes')
        test_audio = input.get('audio')

        i = 0
        print('video')
        while i < len(test_episodes) and verification:
            print(str(test_episodes[i]) + '    ' + str(episodes[i].title))
            if int(test_episodes[i]) != int(episodes[i].title):
                verification = False
            i += 1
        j = 0

        print('audio')
        while j<len(test_audio) and verification:
            print(str(test_audio[j]) + '    ' + str(audio[j].title))
            if int(test_audio[j]) != int(audio[j].title):
                verification = False
            j += 1
