#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Input parameter is not correct. ./test_maxent.sh [test_data]"
    exit
fi

mallet_folder="./mallet/mallet-2.0.8RC3/bin"
input_file="$1"
input_basename=$(basename $input_file)
output_file=${input_basename%.*}"_me.output"
output_folder=${input_file%%/*}

# Check classifier exists
if [ ! -f  "$output_folder"/me.classifier ]; then
    echo "Classifier $output_folder/me.classifier not found! Please trian first"
    exit
fi

# Run on test file
"$mallet_folder"/mallet classify-file --input "$input_file" --output me_test.tmp --classifier "$output_folder"/me.classifier
python preprocessing/extract_mallet_result.py me_test.tmp "$output_folder"/"$output_file"
echo "Output write to ""$output_folder"/"$output_file"
echo "Remove temporary files"
rm -v me_test.tmp
