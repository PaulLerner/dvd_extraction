#!/bin/bash
source /people/maurice/anaconda3-4.3.1/bin/activate /people/maurice/anaconda3-4.3.1/envs/pyannote-video-dev-new
cd dvd_extraction_git/dvd_extraction
python launch_rip.py $1 &>output_rip_all/$1.txt & #& $2 $3 $4 $5 &
