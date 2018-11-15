from xml.dom import minidom
import subprocess
import os
from joblib import Parallel, delayed
import multiprocessing
from test_unitaire.tvd.rip import Ripper #modified version
from glob import glob
import yaml
import pandas as pd
import csv

xml_path = 'test_unitaire/xml/'
input_path = '/vol/work2/maurice/dvd'
output_rip = '/vol/work1/maurice/rip_temp/'

files = glob(xml_path+'*.xml')

texts = []
for f in files:
    #print('FILE', f)
    fi = open(f, 'r', encoding = 'utf-8', errors = 'ignore' )
    content = fi.read()
    content = content.replace('&', '')
    texts.append(content)

to_rip = []
for t in texts:
    current = minidom.parseString(t)
    ripper = Ripper()
    tracks = ripper.get_tracks(current)

    title = current.getElementsByTagName('device')[0].firstChild.data
    title = title.split('/')[-1]
    nsfl = title.split('.')
    name = nsfl[0]
    season = int(nsfl[1].strip('Season'))
    fl = nsfl[2].strip('Episodes').split('to')
    first = int(fl[0])
    last = int(fl[1])
    for track in tracks:
        to_rip.append((name, season, first, last, track.title))

    #audio = ripper.get_languages(current, ref_episodesef['from'], ref_episodes['to'])
            
with open('to_rip.txt', mode='w') as file:
    wr = csv.writer(file)#, delimiter='\n')
    for x in to_rip:
        wr.writerow(x)