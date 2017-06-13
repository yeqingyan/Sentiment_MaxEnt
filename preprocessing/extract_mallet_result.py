import argparse
import sys
import csv

# Input arguments
PROGRAM_DESCRIPTION = "Extract form Mallet result"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('input_file', type=file, help='Input files')
parser.add_argument('output_file', type=argparse.FileType('w'), help='Output files')
args = vars(parser.parse_args())

label_dict = {}
for line in args['input_file'].readlines():
    tags = line.split('\t')[1:]
    labels = tags[::2]
    polarity = map(float, tags[1::2])
    win_label = labels[polarity.index(max(polarity))]
    args['output_file'].write(win_label+"\n")
