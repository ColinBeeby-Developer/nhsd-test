#!/bin/bash
nohup python3 datacleanerapi.py &>/dev/null &
sleep 1
python3 -m unittest discover  
