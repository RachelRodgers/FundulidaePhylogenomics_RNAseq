#!/bin/bash

# names_and_counts.sh
# This script reports out the name of every .gz file and the number of reads in that file.
 
files=($(find /media/rrodgers/Seagate_Backup_Plus_Drive/Concatenated_Individuals/ -name "*R1.fastq.gz"))

# Count reads in each file by counting # lines and dividing by 4.

for i in ${files[@]}
do	
	#echo $i	
	filename=$(basename "$i")
	#echo $filename
	line_count=$(zcat $i | wc -l)
	#echo $line_count
	n=4	
	read_count=$(($line_count/$n))
	#echo $read_count
	printf "$filename %s\t $read_count %s\n" >> /home/rrodgers/Desktop/All_Files_and_ReadCounts.txt
done



