import argparse
import sys
import os

# Input arguments
PROGRAM_DESCRIPTION = "Add name labe before each instance for mallet train data"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('input_file', type=file, help='Input file')
parser.add_argument('output_file', type=argparse.FileType('w'), help='output file name')
args = vars(parser.parse_args())

lines = args['input_file'].readlines()

print "Process {0} lines".format(len(lines))

count = 0
for line in lines:        
    args['output_file'].write("{0}\t{1}".format(count, line))
    count += 1