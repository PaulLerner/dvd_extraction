from xml.dom import import minidom
from glob import import glob
import yaml
import numpy as np
import pandas as pd
import os
from shutil import import copyfile
import csv

list_to_rip = ['BuffyContreLesVampires', 'GameOfThrones', 'HarryPotter', 'Homeland', 'LeSeigneurDesAnneaux', 'SixFeetUnder', 'TheBigBangTheory', 'TheWalkingDead']
input_path = '/vol/work1/maurice/rip_temp/'
output_path = '/vol/work1/maurice/dvd_extracted/'

for folder in list_to_rip:
    if not os.path.exists(output_path+folder):
        os.makedirs(output_path+folder)

with open('data.yml', 'r', encoding = 'utf-8', errors = 'ignore') as file:
    data_str = file.read()
data = yaml.load(data_str)

def parse_title(title):
    all_ = title.split('.')
    serie = all_[0]
    season = all_[1]
    from_to = all_[2].split('Episodes')[1].split('to')
    return serie, season, from_to[0], from_to[1]

for title, datas in data.items():
    serie_, season_, from_, to_ = parse_title(title)
    if serie_ in list_to_rip:
        print(title, datas)
        for epi, ix in enumerate(datas['episodes']):
            try:
                #copyfile(input_path+title+'.Track_ix'+str(ix)+'.mkv', output_path+serie_+'.'+season_+'.Episode'+str(int(from_)+epi).zfill(2)+'.mkv')
                os.rename(input_path+serie_+'/'+title+'.Track_ix'+str(ix)+'.mkv', output_path+serie_+'/'+serie_+'.'+season_+'.Episode'+str(int(from_)+epi).zfill(2)+'.mkv')
                #print('move', input_path+serie_+'/'+title+'.Track_ix'+str(ix)+'.mkv', 'to', output_path+serie_+'/'+serie_+'.'+season_+'.Episode'+str(int(from_)+epi).zfill(2)+'.mkv')
            except FileNotFoundError:
                print('ERROR of move with file', title, ix)#pass'''
                #print('move', input_path+serie_+'/'+title+'.Track_ix'+str(ix)+'.mkv', 'to', output_path+serie_+'/'+serie_+'.'+season_+'.Episode'+str(int(from_)+epi).zfill(2)+'.mkv')
