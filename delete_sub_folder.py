#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pathlib, argparse, subprocess
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="path of the wav and mkv files")
args = parser.parse_args()

current_directory = pathlib.Path(args.folder)

for folder_serie in current_directory.iterdir():
    folder_serie_str = str(folder_serie)
    for sub_folder in folder_serie.iterdir():
        sub_folder_str = str(sub_folder)
        if os.path.isdir(sub_folder_str):
            for current_file in sub_folder.iterdir():
                current_file = str(current_file)
                #print('mv '+current_file+' '+folder_serie_str)
                subprocess.call(['mv', current_file, folder_serie_str])
            subprocess.call(['rm', '-rf', sub_folder_str])
