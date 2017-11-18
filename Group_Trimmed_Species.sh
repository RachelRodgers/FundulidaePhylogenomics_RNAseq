#!/bin/bash
# Group_Trimmed_Species.sh
# Copy all trimmed, paired read files from the rnaseqOutput directory (created by Trimmo sript) to external harddrive and group according to species.

species_names=( A_xenica F_catanatus F_chrysotus F_diaphanus F_grandis F_heteroclitus F_notatus F_notti F_olivaceous F_parvapinis F_rathbuni F_sciadicus F_similis F_zebrinus L_goodei L_parva )

# For each species name in the array, make a new folder using that name located under /media/dduvern/Seagate Expansion Drive

for Species in ${species_names[@]}
do
	mkdir -p /media/dduvern/Seagate\ Expansion\ Drive/Sorted_Groups/$Species
done

# Find all files (OutputPaired only) belonging to each species and move to their respective folders
# cp --backupwill allow files with identical names (but residing in different directories) to be copied w/o overwriting each other

for i in ${species_names[@]}
do
	find /home/dduvern/Desktop/rnaseqOutput -name "*$i*.OutputPaired.fastq.gz*" -exec cp --backup {} /media/dduvern/Seagate\ Expansion\ Drive/Sorted_Groups/$i \;
done

