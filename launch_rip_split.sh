#!/bin/bash

source /people/maurice/anaconda3-4.3.1/bin/activate /people/maurice/anaconda3-4.3.1/envs/pyannote-video-dev-new
cd dvd_extraction_git/dvd_extraction
while IFS=, read -r name season first last ix
do
  echo "I got:$name|$season|$first|$last|$ix"
  echo "" | python launch_rip.py $name $season $first $last $ix
done < $1