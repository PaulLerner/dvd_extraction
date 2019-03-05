#!/bin/bash

containsElement () {
    local e match="$1"
    shift
    for e; do [[ "$e" == "$match" ]] && return 0; done
    return 1
}

export TESSDATA_PREFIX=/vol/work3/maurice/tessdata
#IFS='$'
source /people/maurice/anaconda3-4.3.1/bin/activate /people/maurice/anaconda3-4.3.1/envs/pyannote-video-dev-new
#cd dvd_extraction_git/dvd_extraction
#python launch_rip.py $1 &>output_rip_all/$1.txt & #& $2 $3 $4 $5 &
langs=("aar" "abk" "afr" "aka" "alb" "amh" "ara" "arg" "arm" "asm" "ava" "ave" "aym" "aze" "bak" "bam" "baq" "bel" "ben" "bih" "bis" "bos" "bre" "bul" "bur" "cat" "cha" "che" "chi" "chu" "chv" "cor" "cos" "cre" "cze" "dan" "div" "dut" "dzo" "eng" "epo" "est" "ewe" "fao" "fij" "fin" "fre" "fry" "ful" "geo" "ger" "gla" "gle" "glg" "glv" "gre" "grn" "guj" "hat" "hau" "heb" "her" "hin" "hmo" "hrv" "hun" "ibo" "ice" "ido" "iii" "iku" "ile" "ina" "ind" "ipk" "ita" "jav" "jpn" "kal" "kan" "kas" "kau" "kaz" "khm" "kik" "kin" "kir" "kom" "kon" "kor" "kua" "kur" "lao" "lat" "lav" "lim" "lin" "lit" "ltz" "lub" "lug" "mac" "mah" "mal" "mao" "mar" "may" "mlg" "mlt" "mon" "nau" "nav" "nbl" "nde" "ndo" "nep" "nno" "nob" "nor" "nya" "oci" "oji" "ori" "orm" "oss" "pan" "per" "pli" "pol" "por" "pus" "que" "roh" "rum" "run" "rus" "sag" "san" "sin" "slo" "slv" "sme" "smo" "sna" "snd" "som" "sot" "spa" "srd" "srp" "ssw" "sun" "swa" "swe" "tah" "tam" "tat" "tel" "tgk" "tgl" "tha" "tib" "tir" "ton" "tsn" "tso" "tuk" "tur" "twi" "uig" "ukr" "urd" "uzb" "ven" "vie" "vol" "wel" "wln" "wol" "xho" "yid" "yor" "zha" "zul")
while read p; do
  echo 'p' $p
  #name=$($p | cut -c2-)
  name=${p%?}
  echo 'name' $name
  IFS='.' read -ra names <<< "$name"
  read p
  episodes=$p
  echo 'episodes' $episodes
  e=$(echo $episodes | cut -d"[" -f2)
  IFS=', ' read -r -a epis <<< "${e%?}"
  i=0
  IFS='$'
  epi_start=$(echo $name | grep -o -P '(?<=Episodes).*(?=to)')
  echo 'epi_start' $epi_start
  epi_=$(echo "$i + $epi_start" | bc)
  echo 'epi_' $epi_
  epi_n=$(printf "%.2d" $epi_)
  echo 'epi_n' $epi_n
  #echo 'path' /vol/work1/maurice/dvd_extracted/${names[0]}/${names[0]}.${names[1]}.Episode$epi_n.mkv
  readarray -t res <<<"$(ffprobe /vol/work1/maurice/dvd_extracted/${names[0]}/${names[0]}.${names[1]}.Episode$epi_n.mkv 2>&1 | grep Subtitle)"
  for epi in "${epis[@]}"
  do
    #echo 'epi' $epi
    #echo 'res' ${res[@]}
    langs_visited=()
    for l in ${res[@]}
    do
        track=$(echo $l | cut -d"(" -f1 | grep -o -m 1 "#.*" | cut -c2-)
        lang=$(echo $l | cut -d")" -f1 | grep -o -m 1 "(.*" | cut -c2-)
        containsElement "$lang" "${langs_visited[@]}"
        cl=$?
        echo 'l' $l
        echo $track
        echo $lang
        echo $cl
        if [ $cl -eq 1 ]
        then
            #ffmpeg -i $1 -map $track -y -ar 16000 -ac 1 ${1%.*}-$lang.wav
            ii=$(printf "%.2d" $i)
            echo $ii
           # mencoder dvd://$epi -dvd-device /vol/work2/maurice/dvd/$name -o /dev/null -nosound -ovc copy -vobsubout /vol/work1/maurice/dvd_extracted/Subtitles/${names[0]}.${names[1]}.Episode$epi_n.$lang -slang $lang
            #/people/bredin/dev/VobSub2SRT/build/bin/vobsub2srt /vol/work1/maurice/dvd_extracted/Subtitles/${names[0]}.${names[1]}.Episode$epi_n.$lang
            #mv /vol/work1/maurice/dvd_extracted/Subtitles/${names[0]}.${names[1]}.Episode$epi_n.$lang.srt /vol/work1/maurice/dvd_extracted/Subtitles/${names[0]}.${names[1]}.Episode$epi_n.$lang.tesseractV3.srt
           # vobsub2srt /vol/work1/maurice/dvd_extracted/Subtitles/${names[0]}.${names[1]}.Episode$epi_n.$lang 2>&1
            #mv /vol/work1/maurice/dvd_extracted/Subtitles/${names[0]}.${names[1]}.Episode$epi_n.$lang.srt /vol/work1/maurice/dvd_extracted/Subtitles/${names[0]}.${names[1]}.Episode$epi_n.$lang.tesseractV4.srt
            langs_visited+=("$lang")
        fi
    done
    i=$((i+1))
  done
  read p
  audios=$p
done <$1
