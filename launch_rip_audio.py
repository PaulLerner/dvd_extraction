import os
import argparse
import subprocess

input_path = '/vol/work2/maurice/dvd'
output_rip = '/vol/work1/maurice/rip_temp/'

parser = argparse.ArgumentParser()
parser.add_argument("all", type=str, help="Serie's name, Season, First episode, Last episode, Ix of lsdvd xml file")
'''parser.add_argument("name", type=str, help="Serie's name")
parser.add_argument("season", type=int, help="Season")
parser.add_argument("first", type=int, help="First episode")
parser.add_argument("last", type=int, help="Last episode")
parser.add_argument("ix", type=int, help="Ix of lsdvd xml file")'''

args = parser.parse_args()
alls = args.all.split(',')
name = alls[0]
season = int(alls[1])
first = int(alls[2])
last = int(alls[3])
ix = int(alls[4])
with open(os.devnull, mode='w') as f:
    subprocess.call([
    'HandBrakeCLI', '-i', f'{input_path}/{name}.Season{season:02d}.Episodes{first:02d}to{last:02d}', '-t', str(ix), '-o',
    f'{output_rip}/{name}.Season{season:02d}.Episodes{first:02d}to{last:02d}.Track_ix{ix}.mkv',
    '--cfr', '--crop', '0:0:0:0', '-r', '25', '--all-audio', '--all-subtitles'
    ])
