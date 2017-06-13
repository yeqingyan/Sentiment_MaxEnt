#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Input parameter is not correct. ./train_maxent.sh [train_data]"
    exit
fi

mallet_folder="./mallet/mallet-2.0.8RC3/bin"
input="$1"
output_folder=${input%%/*}

# Delete old train file
rm -f me.classifier

# Preprocessing
python preprocessing/pre_addname.py "$1" temp.input

#import train file
"$mallet_folder"/mallet import-file --input temp.input --output /tmp/mallet_train.mallet

# train classifier
"$mallet_folder"/mallet train-classifier --trainer MaxEnt --input /tmp/mallet_train.mallet --output-classifier me.classifier

rm /tmp/mallet_train.mallet

# back me.classifier
mv -v me.classifier "$output_folder"/me.classifier

rm -v temp.input
