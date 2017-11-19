#Run_MAFFT.py

import subprocess
import glob
import os

#Change to point to unaligned fasta files
Main_Directory = '/media/rrodgers/Seagate_Expansion_Drive/Individual_Analysis/Matrix4/Raw_Sequences/'

#Create new directory to hold aligned files
AlignedSequenceDirectory = (Main_Directory + 'Aligned_Files/')
if not os.path.exists (AlignedSequenceDirectory):
	os.makedirs(AlignedSequenceDirectory)

Unaligned_SeqFiles = glob.glob(Main_Directory + '*.fasta')

for SeqFile in Unaligned_SeqFiles:
	#Get orthogroup name
	Orthogroup = os.path.basename(SeqFile).replace('.fasta','')
	#Build MAFFT command string
	mafft_command_string = 'mafft --auto ' + SeqFile + ' > ' + AlignedSequenceDirectory + Orthogroup + '_aligned.fasta'
	#Run MAFFT
	mafft_process = subprocess.Popen(mafft_command_string, shell=True)
	mafft_process.wait()
