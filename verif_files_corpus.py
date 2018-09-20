#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pathlib, argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="path of the wav and mkv files")
parser.add_argument("seuil", help="threshold in percent to considere that a file as a bad size compare to the mean of all the season", type=float)
args = parser.parse_args()

current_directory = pathlib.Path(args.folder)

size_mkv = []
size_16kHz_wav = []
size_48kHz_wav = []
for current_file in current_directory.iterdir():
    current_file = str(current_file)
    current_file_split = current_file.split('/')[-1].split('.')
    print(current_file, current_file_split)
    name = current_file_split[0]
    season = current_file_split[1].split('Season')[1]
    episode = current_file_split[2].split('Episode')[1]
    print(name, season, episode)
    if '16kHz.wav' in current_file :
        size_16kHz_wav.append(os.path.getsize(current_file))
        #print('wav 16kHz', os.path.getsize(current_file))
    if '48kHz.wav' in current_file :
        size_48kHz_wav.append(os.path.getsize(current_file))
        #print('wav 48kHz', os.path.getsize(current_file))
    if 'mkv' in current_file :
        size_mkv.append(os.path.getsize(current_file))
        #print('mkv', os.path.getsize(current_file))

#Compute the average size per season ; assume that 1 folder correspond to 1 season
mean_mkv = np.average(np.asarray(size_mkv))
mean_16kHz_wav = np.average(np.asarray(size_16kHz_wav))
mean_48kHz_wav = np.average(np.asarray(size_48kHz_wav))

def error_seuil(size_file, size_mean, seuil):
    print(100 * abs(size_file - size_mean) / max(size_file, size_mean))
    if 100 * abs(size_file - size_mean) / max(size_file, size_mean) > seuil :
        return True
    else :
        return False

for current_file in current_directory.iterdir():
    current_file = str(current_file)
    if '16kHz.wav' in current_file and error_seuil(os.path.getsize(current_file), mean_16kHz_wav, args.seuil) :
        print(f'Size problem with the file {current_file}')
    if '48kHz.wav' in current_file and error_seuil(os.path.getsize(current_file), mean_48kHz_wav, args.seuil) :
        print(f'Size problem with the file {current_file}')
    if 'mkv' in current_file and error_seuil(os.path.getsize(current_file), mean_mkv, args.seuil) :
        print(f'Size problem with the file {current_file}')
