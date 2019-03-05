#!/bin/bash

#IFS='$'
while read p; do
  name=$p
  echo $name
  read p
  episodes=$p
  echo $episodes
  e=$(echo $episodes | cut -d"[" -f2)
  IFS=', ' read -r -a epis <<< "${e%?}"
  for epi in "${epis[@]}"
  do
    echo $epi
  done
  read p
  audios=$p
done <$1
