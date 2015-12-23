#!/bin/bash
sudo apt-get install python-dev libxml2-dev libxslt1-dev antiword poppler-utils pstotext tesseract-ocr flac lame libmad0 libsox-fmt-mp3 sox
sudo apt-get install python-pip
sudo pip install textract
sudo pip install -U numpy
sudo pip install -U nltk
sudo pip install pysimplesoap
sudo apt-get install abiword
python -c "import nltk;nltk.download('maxent_treebank_pos_tagger')"
