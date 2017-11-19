#ChangeGapCharacters.py

import glob
import os

WorkingDirectory = '/media/rrodgers/Seagate_Expansion_Drive/Individual_Analysis/Matrix3/genes/'

ModifiedFilesDirectory = (WorkingDirectory + 'ModifiedGenes/')

if not os.path.exists(ModifiedFilesDirectory):
	os.makedirs(ModifiedFilesDirectory)

OriginalSequenceFiles = glob.glob(WorkingDirectory + '*.fasta')

for SequenceFile in OriginalSequenceFiles:
	#Get the filename so we know what to call the output file
	FileName = os.path.basename(SequenceFile)
	
	#Open and name the output file
	OutFile = open(ModifiedFilesDirectory + FileName,'a')

	#Open the file and read in the contents, replaceing gaps with missing data characters
	Current_SequenceFile = open(SequenceFile)

	for line in Current_SequenceFile:
		modified_line = line.replace('-','?')
		OutFile.write(modified_line)

	OutFile.close()
	Current_SequenceFile.close()
