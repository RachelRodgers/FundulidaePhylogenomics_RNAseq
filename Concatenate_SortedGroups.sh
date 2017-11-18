#!/bin/bash

species_names=( A_xenica F_catanatus F_chrysotus F_diaphanus F_grandis F_heteroclitus F_notatus F_notti F_olivaceous F_parvapinis F_rathbuni F_sciadicus F_similis F_zebrinus L_goodei L_parva )

for Species in ${species_names[@]}
do
	cd /media/dduvern/Seagate\ Expansion\ Drive/Sorted_Groups/$Species
	echo "Concatenating $Species R1 files..."	
	cat *_R1_00*.OutputPaired.fastq.gz* > $Species.R1_Combined.fastq.gz
	echo "Concatenating $Species R2 files..."	
	cat *_R2_00*.OutputPaired.fastq.gz* > $Species.R2_Combined.fastq.gz
	echo "Moving to next set of files."
done

echo "Done!"
