import os
import argparse
import subprocess
    
input_path = '/vol/work2/maurice/dvd'
output_rip = '/vol/work1/maurice/rip_temp/'

parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, help="Serie's name")
parser.add_argument("season", type=int, help="Season")
parser.add_argument("first", type=int, help="First episode")
parser.add_argument("last", type=int, help="Last episode")
parser.add_argument("ix", type=int, help="Ix of lsdvd xml file")

args = parser.parse_args()
with open(os.devnull, mode='w') as f:
    subprocess.call([
    'HandBrakeCLI', '-i', f'{input_path}/{args.name}.Season{int(args.season):02d}.Episodes{args.first:02d}to{args.last:02d}', '-t', str(args.ix), '-o',
    f'{output_rip}/{args.name}.Season{int(args.season):02d}.Episodes{args.first:02d}to{args.last:02d}.Track_ix{args.ix}.mkv',
    '--cfr', '--crop', '0:0:0:0', '-r', '25', '--all-audio', '--all-subtitles'
    ])