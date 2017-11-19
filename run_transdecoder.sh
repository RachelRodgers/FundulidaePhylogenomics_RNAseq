#!/bin/bash

fasta_files=($(find . -name "*.fasta"))

for i in ${fasta_files[@]}
do
	TransDecoder.LongOrfs -m 500 -t $i
	TransDecoder.Predict -t $i --single_best_orf
done
