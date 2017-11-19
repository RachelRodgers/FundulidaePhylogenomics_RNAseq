#Fetch_Outgroup_Sequences.py

import glob
import os
import subprocess

MainDirectory = '/home/papasammich/Desktop/Test/'

tags = ['LATIPES','VARIEGATUS','MACULATUS','RETICULATA']

Database_Dictionary = {
	'LATIPES' : r'/home/papasammich/Desktop/Test/outgroup_seq_files/Oryzias_latipes.MEDAKA1.cds.all.fa',
	'VARIEGATUS' : r'/home/papasammich/Desktop/Test/outgroup_seq_files/C_variegatus_rna.fa',
	'MACULATUS' : r'/home/papasammich/Desktop/Test/outgroup_seq_files/Xiphophorus_maculatus.Xipmac4.4.2.cds.all.fa',	
	'RETICULATA' : r'/home/papasammich/Desktop/Test/outgroup_seq_files/P_reticulata_rna.fa'
	}

nt_Sequence_Dictionary = {
	'LATIPES' : r'/home/papasammich/Desktop/Test/outgroup_seq_files/Oryzias_latipes.MEDAKA1.cds.all.fa',
	'VARIEGATUS' : r'/home/papasammich/Desktop/Test/outgroup_seq_files/C_variegatus_rna.fa',
	'MACULATUS' : r'/home/papasammich/Desktop/Test/outgroup_seq_files/Xiphophorus_maculatus.Xipmac4.4.2.cds.all.fa',	
	'RETICULATA' : r'/home/papasammich/Desktop/Test/outgroup_seq_files/P_reticulata_rna.fa'
	}

for tag in tags:
	if not os.path.exists(MainDirectory + tag):
		os.makedirs(MainDirectory + tag)


OriginalSequenceFiles = glob.glob(MainDirectory + '*.fasta')

#---------------------------------------------------------------------------------------------#
# Separate the outgroup sequences into their own directories and sequence files.
#---------------------------------------------------------------------------------------------#

for File in OriginalSequenceFiles:
	#Get OrthoGroup Name
	OrthoGroupName = os.path.basename(File).replace('.fasta','')
	
	#Open file and read line-by-line
	CurrentSequenceFile = open(File)

	copy_line = False

	for line in CurrentSequenceFile:

		for tag in tags:

			QueryFile = open(MainDirectory + tag + '/' + OrthoGroupName + '.fasta','a') 

			if line.find(tag) != -1:
				copy_line = True

			elif line.startswith('>') and copy_line == True:
				break
			
			if copy_line == True:

				QueryFile.write(line)
				QueryFile.close
	
			QueryFile.close()

	CurrentSequenceFile.close()

#---------------------------------------------------------------------------------------------#
# Loop through the outgroup species directories, opening each file and tBLASTn the sequence.
# Then, open the results for each blast, and get the sequence for the top hit in the results.
#---------------------------------------------------------------------------------------------#

for tag in tags:
	#Make directory to hold the blast output
	BLAST_OutDir = MainDirectory + tag + '/' + tag + '_BLAST_output/'
	if not os.path.exists(BLAST_OutDir):
		os.makedirs(BLAST_OutDir)

	#Make dictionary to hold final nucleotide sequences
	nt_Sequence_Dir = MainDirectory + tag + '/' + tag + '_nt_sequences/'
	if not os.path.exists(nt_Sequence_Dir):
		os.makedirs(nt_Sequence_Dir)

	#Get the database name for the species
	Database_Name = Database_Dictionary.get(tag)
	
	#For the current tag (species) put its sequence files into a list)
	OutgroupSpecies_SequenceFiles = glob.glob(MainDirectory + tag + '/*.fasta')
	#print OutgroupSpecies_SequenceFiles

	for File in OutgroupSpecies_SequenceFiles:
		#Get OrthoGroup Name
		OrthoGroupName = os.path.basename(File).replace('.fasta','')
		
		#Build BLAST command string
		BLAST_Command_String = 'tblastn -query ' + File + ' -task \'tblastn\' -db ' + Database_Name + ' -out ' + BLAST_OutDir + OrthoGroupName + '.txt' + ' -evalue 0.001 -outfmt 6 -num_threads 8'

		#print BLAST_Command_String
		BLAST_process = subprocess.Popen(BLAST_Command_String, shell = True)
		BLAST_process.wait()
	#End of BLAST

	#Retrieve dna sequences for the top hits
	BLAST_Results_Files = glob.glob(BLAST_OutDir + '*.txt')

	for Results_File in BLAST_Results_Files:
		OrthoGroupName = os.path.basename(Results_File).replace('.txt','')
		#Open the .txt results file.  The first line will be the top hit.
		Current_Results_File = open(Results_File)
		
		nt_Sequence_Identifier = None

		for line in Current_Results_File:
			columns = line.split('\t')
			#global nt_Sequence_Identifier
			nt_Sequence_Identifier = columns[1] #This is the string that will be used to get the correct sequence
			print "nt_SeqIdentifier: " + nt_Sequence_Identifier
			break #No need to read any further

		Current_Results_File.close()

		#Search the outgroup species' nucleotide file and retrieve the sequence for the identifier

		Original_Nucleotide_Sequence_File = open(nt_Sequence_Dictionary.get(tag))

		New_Nucleotide_Sequence_File = open(nt_Sequence_Dir + OrthoGroupName + '.fasta','a')

		copy_line = False

		for line in Original_Nucleotide_Sequence_File:
			if line.find(str(nt_Sequence_Identifier)) != -1:
				copy_line = True #Correct header found

			elif line.startswith('>') and copy_line == True:
				break #Next header found, don't copy

			if copy_line == True:
				New_Nucleotide_Sequence_File.write(line) #Sequence found

		New_Nucleotide_Sequence_File.close()
		Original_Nucleotide_Sequence_File.close()


		
		
