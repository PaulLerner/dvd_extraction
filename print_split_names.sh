#!/bin/bash

#IFS='/'        # space is set as delimiter
for file in ../dvd/*; do
    #arrFile=(${file//./});
    IFS='/'
    #echo 'newwwwwww'
    #echo $file ;
    #echo ${arrFile[0]};
    read -ra arrPath <<< "$file"
    #echo ${arrPath[-1]};
    IFS='.'
    file=${arrPath[-1]}
    #echo $file
    read -ra arrFile <<< "$file"    # str is read into an array as tokens separated by IFS
    serie=${arrFile[0]}
    season=${arrFile[1]#"Season"}
    IFS='t'
    #echo ${arrFile[2]}
    read -ra fromTo <<< "${arrFile[2]}"
    from=${fromTo[0]#"Episodes"}
    to=${fromTo[1]#"o"}
    echo '----'
    echo $serie
    echo $season
    echo $from
    echo $to
    echo '----'
    #for i in "${arrFile[@]}"; do    # access each element of array
    #    echo "$i"
    #done
done
