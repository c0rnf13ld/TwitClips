# TwitClips
Simple Script written in python3 to download Twitch clips from the terminal.

## Requirements:

>python3 -m pip install colorama

## Usage:

> python3 TwitClips.py --file clips_file --resolution 1080 --path /home/c0rnf13ld/vds


## Parameters:
*   -h, --help            show help message and exit
*  -f **FILE**, --file **FILE**  File with clips to download
*  -c **CLIP**, --clip **CLIP**  Clip to download
*  -p **PATH**, --path **PATH**  Path where all downloaded clips will be stored
*  -r **{1080,720,480,360}**, --resolution **{1080,720,480,360}** Resolution that the downloaded clip will have, by default: 1080p
