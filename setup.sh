#!/bin/bash
mkdir -p ~/.nltk_data
python3 -m nltk.downloader -d ~/.nltk_data stopwords averaged_perceptron_tagger
