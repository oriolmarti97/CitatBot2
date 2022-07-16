#!/bin/bash

wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
tar xzvf geckodriver\*
sudo mv geckodriver /usr/bin

python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
