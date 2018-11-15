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

while IFS=, read -r name season first last ix
do
  echo "I got:$name|$season|$first|$last|$ix"
  for m in m148 m149 m150 m173 m174 m175
  do
    echo $m
    load_cpu=$(ssh $m "cut -d ' ' -f2 /proc/loadavg")
    nb_cpu=$(ssh $m "grep -c ^processor /proc/cpuinfo")
    load_cpu_percent=$(echo $load_cpu / $nb_cpu | bc -l)
    echo $load_cpu_percent
    #ssh $m dvd_extraction_git/dvd_extraction/launch_rip.sh $name $season $first $last $ix &
    break
  done
done < $1

'''while IFS=, read -r name season first last ix
do
  echo "I got:$name|$season|$first|$last|$ix"
  for m in m148 m149 m150 m173 m174 m175 #m154 m155 m156 m157 m158 m159 m160 m161 m162 m163 m164 m165 m166 m168 m169
  do
    echo $m
    load_cpu=$(ssh $m "cut -d ' ' -f2 /proc/loadavg")
    nb_cpu=$(ssh $m "grep -c ^processor /proc/cpuinfo")
    #load_cpu_percent=$(echo $load_cpu / $nb_cpu | bc -l)
    #echo $load_cpu_percent
    #if [ $(echo $load_cpu_percent'<'$seuil_cpu | bc -l) -eq 1 ]
    #then
      echo 'ok' $m
      #ssh $m dvd_extraction_git/dvd_extraction/launch_rip.sh $name $season $first $last $ix &
      #break
    #fi
  done
done < $1'''

