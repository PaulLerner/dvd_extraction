#!/bin/bash
# GPU
# Odessa      : m148 m149 m150
# ANR METADATV: m173
# ANR PLUMCOT : m174 m175

###
# SEUILS A MODIFIER
# Temps entre 2 vérifications
sleep_time=5m
# Temps entre 2 soumission à une machine
sleep_time_computer=10s
# Taux d'occupation à ne pas dépassser
seuil_cpu=50 #0.7
seuil_gpu=0.5
seuil_mem=0.5
###

pas=1
#for f in {0..9..$pas} # ATTENTION la fin est incluse !!! 

IFS_old=$IFS
IFS=$(echo -en "\n\b")
computers=("m153" "m154" "m155" "m156" "m157" "m158" "m159" "m160" "m161" "m164" "m165" "m166" "m168" "m169")
id=0
for row in $(cat $1);
do
    echo "I got:$row"
    assign=0
    while [ $assign -eq 0 ]
    do
        #echo $assign
        #echo $id
        val=${computers[$id]}
        #echo $val
        id_prev=`echo "$id - 1" | bc`
        #echo $id
        #echo $id_next
        if [ $id -eq 0 ]
        then
            #unset computers_new
            computers_new=("${computers[@]}")
        else
        #echo unset
        #echo "${computers_new[@]}"
            computers_new=("${computers_new[@]:1}")
        fi
        #echo $computers_new
        #echo "${computers_new[@]}"
        for m in "${computers_new[@]}" #m153 m154 m155 m156 m157 m158 m159 m160 m161 m164 m165 m166 m168 m169 #m148 m149 m150 m173 m174 m175 m162 m163 m164 m165 m166 m168 m169
        do
            #echo $m
            #load_cpu=$(ssh $m "cut -d ' ' -f2 /proc/loadavg")
            #nb_cpu=$(ssh $m "grep -c ^processor /proc/cpuinfo")
            load_cpu_percent=$(ssh $m "./get_load_cpu.sh") #$(ssh $m "echo $[100-$(vmstat 1 2|tail -1|awk '{print $15}')]") #$(echo $load_cpu / $nb_cpu | bc -l)
            echo $m $load_cpu_percent
            if [ $(echo $load_cpu_percent'<'$seuil_cpu | bc -l) -eq 1 ]
            then
                #ssh $m dvd_extraction_git/dvd_extraction/launch_rip.sh $row &
                ssh $m dvd_extraction_git/dvd_extraction/launch_rip_subtitle.sh $row dvd_extraction_git/dvd_extraction/test_unitaire/data.yml &>output_rip_all/$1-subtitle.txt &
                echo "Tâche assignée à" $m
                sleep $sleep_time_computer
                assign=1
                computers_new+=($val)
                #echo "${computers_new[@]}"
                id=`echo "$id + 1" | bc`
                id=$(($id % ${#computers[@]}))
                continue 2
            fi
        done
        sleep $sleep_time
    done
done
IFS=IFS_old
