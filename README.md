# FundulidaePhylogenomics_RNAseq
Scripts and files associated with "Phylogenomic analysis of Fundulidae (Teleostei: Cyprinodontiformes) using RNA-sequencing Data"

The scripts and steps listed below correspond to the data analysis pipeline used for the phylogenomic analysis of 16 Fundulidae species as described in article listed above.  Please note that the scripts are not configured to run specific computers, as they contain many hard-coded paths and appear just as they were written for analysis.  These scripts are intended to provide information about how the analyses were performed but need further updating to be easily re-runnable on other computing systems.

## 1. Trimming and Filtering
**fundulus_trimmer.pl**

fundulus_trimmer.pl was run on raw sequence files within the RNAseq directory.  Data were quality trimmed and filtered with [Trimmomatic v0.33](http://www.usadellab.org/cms/?page=trimmomatic "Trimmomatic") to remove adaptor sequences, low-quality bases (Phred <5) and low-quality reads (Phred <5).  Reads were removed from the data set if fewer than 25 base pairs remained after all trimming steps were completed.  Output files were directed to rnaseqOutput directory.

## 2. Group and Concatenate Trimmed Read Files by Sample
**Group_Trimmed_Species.sh**

**Concatenate_Sorted_Groups.sh**

Trimmed read files from the rnaseqOutput directory were grouped by species using Group_Trimmed_Species.sh.  Individual sample files were then concatenated into single R1 and R2 fastq files using the script Concatenate_Sorted_Groups.sh.  Concatenated species were placed in the Concatenated_Individuals directory.  Every species contained more than one sample.

## 3. Select Individual Samples with Highest Number of Reads
**Names_and_Counts.sh**

The number of reads for each sample's R1 file was counted and output into a plain text file.  The one sample per species with the highest number of reads was selected for further analysis.

## 4. *de novo* Assembly of Transcripts using Trinity

*de novo* assembly of transcripts was performed on the individual samples selected in step 3. Each assembly job was submitted to the [SIUC BigDog Cluster](http://oit.siu.edu/rcc/bigdog/ "SIUC BigDog High Performance Computing Cluster) via command line with the following parameters:
```bash
Trinity.pl \
--seqType fq \
--left <path\to\leftReadFile.fq>\
--right <path\to\rightReadFile.fq>
--JM 60G \
--min_contig_length 20 \
--normalize_reads \
--full_cleanup\
```