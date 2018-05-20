#!/bin/bash
python3 ECGCompression.py && echo "SIGNAL COMPRESSION COMPLETED AND ATTRIBUTES ARE GENERATED AT output.txt!" && python fcbf.py -inpath='output.txt' -delim=',' -header=false -thresh=0.001 -classAt=0 && echo "FEATURE SELECTION COMPLETED!" &&  python3 EMClustering.py
#rm features_output.txt
#rm output.txt
#rm output_class.txt
#rm output_class_compare.txt
#rm output_class_testing.txt
#rm output_testing.txt

