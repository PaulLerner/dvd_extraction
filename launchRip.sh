#!/bin/bash

for file in $1; do #../dvd/TheWalkingDead*; do
    echo $1
    echo $file
    IFS='/'
    read -ra arrPath <<< "$file"
    IFS='.'
    file=${arrPath[-1]}
    read -ra arrFile <<< "$file"    # str is read into an array as tokens separated by IFS
    serie=${arrFile[0]}
    season=${arrFile[1]#"Season"}
    IFS='t'
    read -ra fromTo <<< "${arrFile[2]}"
    from=${fromTo[0]#"Episodes"}
    to=${fromTo[1]#"o"}
    IFS='§'
    echo $serie
    echo $season
    echo $from
    echo $to
    python dvd_extraction/dvd_extraction.py --series=$serie --season=$season --from=$from --to=$to
    echo '-------'
done
