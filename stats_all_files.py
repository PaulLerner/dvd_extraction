#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pathlib, argparse
import pandas as pd
import numpy as np
from pyannote.video import Video

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="path of the series")
args = parser.parse_args()

current_directory = pathlib.Path(args.folder)

def get_nb_all_files():
    nb = 0
    for folder_serie in current_directory.iterdir():
        for current_file in folder_serie.iterdir():
            nb += 1
    return nb

def get_nb_all_episodes():
    nb = 0
    for folder_serie in current_directory.iterdir():
        for current_file in folder_serie.iterdir():
            if '.mkv' in str(current_file):
                nb += 1
    return nb

def get_nb_episodes_per_serie():
    nb_all = {}
    for folder_serie in current_directory.iterdir():
        nb = 0
        for current_file in folder_serie.iterdir():
            current_file = str(current_file)
            if '.mkv' in current_file:
                nb += 1
                current_file_split = current_file.split('/')[-1].split('.')
                name = current_file_split[0]
        nb_all[name] = nb
    return nb_all

def get_stats_languages():
    langs = pd.DataFrame(columns=['name', 'season', 'episode', 'nb_languages', 'nb_subtitles', 'en_language', 'fr_language', 'en_subtitle', 'fr_subtitle', 'en_language_and_subtitle'])
    data = {}
    nb_total_serie = get_nb_series()
    for i_serie, folder_serie in enumerate(current_directory.iterdir()):
        print(str(i_serie)+'/'+str(nb_total_serie), str(folder_serie))
        for current_file in folder_serie.iterdir():
            current_file = str(current_file)
            current_file_split = current_file.split('/')[-1].split('.')
            name = current_file_split[0]
            season = current_file_split[1].split('Season')[1]
            episode = current_file_split[2].split('Episode')[1]
            if name+'.'+season+'.'+episode not in data:
                nb_language_per_episode = 0
                nb_subtitle_per_episode = 0
                presence_en_language_per_episode = False
                presence_fr_language_per_episode = False
                presence_en_subtitle_per_episode = False
                presence_fr_subtitle_per_episode = False
            else:
                data_epi = data[name+'.'+season+'.'+episode]
                nb_language_per_episode = data_epi[0]
                nb_subtitle_per_episode = data_epi[1]
                presence_en_language_per_episode = data_epi[2]
                presence_fr_language_per_episode = data_epi[3]
                presence_en_subtitle_per_episode = data_epi[4]
                presence_fr_subtitle_per_episode = data_epi[5]
            if '.srt' in current_file:
                nb_subtitle_per_episode += 1
            if '16kHz.wav' in current_file:
                nb_language_per_episode += 1
            if 'en.srt' in current_file:
                presence_en_subtitle_per_episode = True
            if 'fr.srt' in current_file:
                presence_fr_subtitle_per_episode = True
            if 'en16kHz.wav' in current_file:
                presence_en_language_per_episode = True
            if 'fr16kHz.wav' in current_file:
                presence_fr_language_per_episode = True
            data[name+'.'+season+'.'+episode] = [nb_language_per_episode, nb_subtitle_per_episode, presence_en_language_per_episode, presence_fr_language_per_episode, presence_en_subtitle_per_episode, presence_fr_subtitle_per_episode]
        for k,v in data.items():
            nse = k.split('.')
            name = nse[0]
            season = nse[1]
            episode = nse[2]
            nb_language_per_episode = v[0]
            nb_subtitle_per_episode = v[1]
            presence_en_language_per_episode = v[2]
            presence_fr_language_per_episode = v[3]
            presence_en_subtitle_per_episode = v[4]
            presence_fr_subtitle_per_episode = v[5]
            langs = pd.concat([langs,
                               pd.DataFrame([[name, season, episode, nb_language_per_episode,
                                             nb_subtitle_per_episode, presence_en_language_per_episode,
                                             presence_fr_language_per_episode,
                                             presence_en_subtitle_per_episode,
                                             presence_fr_subtitle_per_episode,
                                             presence_en_language_per_episode and presence_en_subtitle_per_episode]],
                               columns=['name', 'season', 'episode', 'nb_languages', 'nb_subtitles', 'en_language', 'fr_language', 'en_subtitle', 'fr_subtitle', 'en_language_and_subtitle'])])
    return langs

def get_movie_infos():
    videos = pd.DataFrame(columns=['name', 'season', 'episode', 'duration', 'frame_rate', 'width', 'height'])
    nb_total_serie = get_nb_series()
    for id_serie, folder_serie in enumerate(current_directory.iterdir()):
        print(str(id_serie)+'/'+str(nb_total_serie), str(folder_serie))
        for current_file in folder_serie.iterdir():
            current_file = str(current_file)
            if '.mkv' in current_file:
                if 'GameOfThrones.Season06.Episode09.mkv' in current_file or 'GameOfThrones.Season06.Episode10.mkv' in current_file:
                    continue
                print(current_file)
                vid = Video(current_file)
                current_file_split = current_file.split('/')[-1].split('.')
                name = current_file_split[0]
                season = current_file_split[1].split('Season')[1]
                episode = current_file_split[2].split('Episode')[1]
                #print(vid.duration, vid.frame_rate, vid.frame_size)
                videos = pd.concat([videos,
                                    pd.DataFrame([[name, season, episode, vid.duration,
                                                  vid.frame_rate, vid.frame_size[0], vid.frame_size[1]]],
                                   columns=['name', 'season', 'episode', 'duration', 'frame_rate', 'width', 'height'])])
    return videos

def get_nb_series():
    nb = 0
    for folder_serie in current_directory.iterdir():
        nb += 1
    return nb

print(get_nb_series())
print(get_nb_all_files())
print(get_nb_all_episodes())
print(get_nb_episodes_per_serie())
print(get_stats_languages())
print(get_movie_infos())
