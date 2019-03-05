#!/bin/bash

containsElement () {
    local e match="$1"
    shift
    for e; do [[ "$e" == "$match" ]] && return 0; done
    return 1
}

IFS='$'
source /people/maurice/anaconda3-4.3.1/bin/activate /people/maurice/anaconda3-4.3.1/envs/pyannote-video-dev-new
#cd dvd_extraction_git/dvd_extraction
#python launch_rip.py $1 &>output_rip_all/$1.txt & #& $2 $3 $4 $5 &
readarray -t res <<<"$(ffprobe $1 2>&1 | grep Audio)"
langs=("aar" "abk" "afr" "aka" "alb" "amh" "ara" "arg" "arm" "asm" "ava" "ave" "aym" "aze" "bak" "bam" "baq" "bel" "ben" "bih" "bis" "bos" "bre" "bul" "bur" "cat" "cha" "che" "chi" "chu" "chv" "cor" "cos" "cre" "cze" "dan" "div" "dut" "dzo" "eng" "epo" "est" "ewe" "fao" "fij" "fin" "fre" "fry" "ful" "geo" "ger" "gla" "gle" "glg" "glv" "gre" "grn" "guj" "hat" "hau" "heb" "her" "hin" "hmo" "hrv" "hun" "ibo" "ice" "ido" "iii" "iku" "ile" "ina" "ind" "ipk" "ita" "jav" "jpn" "kal" "kan" "kas" "kau" "kaz" "khm" "kik" "kin" "kir" "kom" "kon" "kor" "kua" "kur" "lao" "lat" "lav" "lim" "lin" "lit" "ltz" "lub" "lug" "mac" "mah" "mal" "mao" "mar" "may" "mlg" "mlt" "mon" "nau" "nav" "nbl" "nde" "ndo" "nep" "nno" "nob" "nor" "nya" "oci" "oji" "ori" "orm" "oss" "pan" "per" "pli" "pol" "por" "pus" "que" "roh" "rum" "run" "rus" "sag" "san" "sin" "slo" "slv" "sme" "smo" "sna" "snd" "som" "sot" "spa" "srd" "srp" "ssw" "sun" "swa" "swe" "tah" "tam" "tat" "tel" "tgk" "tgl" "tha" "tib" "tir" "ton" "tsn" "tso" "tuk" "tur" "twi" "uig" "ukr" "urd" "uzb" "ven" "vie" "vol" "wel" "wln" "wol" "xho" "yid" "yor" "zha" "zul")
langs_visited=()
for l in ${res[@]}
do
    track=$(echo $l | cut -d"(" -f1 | grep -o -m 1 "#.*" | cut -c2-)
    lang=$(echo $l | cut -d")" -f1 | grep -o -m 1 "(.*" | cut -c2-)
    containsElement "$lang" "${langs_visited[@]}"
    cl=$?
    echo $l
    echo $track
    echo $lang
    echo $cl
    if [ $cl -eq 1 ]
    then
        ffmpeg -i $1 -map $track -y -ar 16000 -ac 1 ${1%.*}-$lang.wav
        langs_visited+=("$lang")
    fi
done
