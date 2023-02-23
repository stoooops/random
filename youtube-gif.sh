#!/bin/bash

set -e

VENV_NAME="venv"

# create virtualenv
python3 -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"

# install packages
type gifsicle || sudo apt-get install -y gifsicle
pip install yt-dlp
pip install imageio
pip install imageio_ffmpeg

# run the script
python youtube-gif/main.py "$@"
