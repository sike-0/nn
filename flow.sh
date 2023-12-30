#!/bin/bash

mkdir faces imgs

source .env/bin/activate

python clean.py
python faces.py
python embed.py
