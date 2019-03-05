#!/bin/bash
# GPU
# Odessa      : m148 m149 m150
# ANR METADATV: m173
# ANR PLUMCOT : m174 m175
pas=1
seuil_cpu=0.9
seuil_gpu=0.5
seuil_mem=0.5
#for f in {0..9..$pas} # ATTENTION la fin est incluse !!! 

name=( {a..z} )
i=0
for m in m148 m149 m150 m173 m174 m175 #m153 m154 m155 m156 m157 m158 m159 m160 m161 m162 m163 m164 m165 m166 m168 m169
do
  echo $m
  echo $1a${name[i]}
  ssh $m dvd_extraction_git/dvd_extraction/launch_rip_split.sh $1a${name[i]} &
  ((i++))
done