#Fetch_Ingroup_Sequences.py
#Retrieve the sequences for the genes identified in each OrthoGroup

#Create a list to hold species tags to check for the number of genes coming from each species in each orthogroup
tags = ['HETEROCLITUS', 'ZEBRINUS', 'NOTTI', 'XENICA', 'CATENATUS', 'CHRYSOTUS', 'DIAPHANUS', 'GRANDIS', 'NOTATUS', 'OLIVACEOUS', 'PARVAPINIS', 'RATHBUNI', 'SCIADICUS', 'SIMILIS', 'GOODEI', 'PARVA']

#Create dictionary to hold species tag and corresponding sequence file
species = {
	'HETEROCLITUS' : r'F_heteroclitus.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'ZEBRINUS' : r'F_zebrinus.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'NOTTI' : r'F_notti.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'XENICA' : r'A_xenica.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'CATANATUS' : r'F_catenatus.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'CHRYSOTUS' : r'F_chrysotus.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'DIAPHANUS' : r'F_diaphanus.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'GRANDIS' : r'F_grandis.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'NOTATUS' : r'F_notatus.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'OLIVACEOUS' : r'F_olivaceous.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'PARVAPINIS' : r'F_parvapinis.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'RATHBUNI' : r'F_rathbuni.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'SCIADICUS' : r'F_sciadicus.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'SIMILIS' : r'F_similis.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'GOODEI' : r'L_goodei.Trinity_Output.Trinity.fasta.transdecoder.cds',
	'PARVA' : r'L_parva.Trinity_Output.Trinity.fasta.transdecoder.cds'
	}

#Set path to dir containing .pep500.fasta files and Results dir
dir = '/media/rrodgers/Seagate Expansion Drive/'

#Create new dir to hold extracted sequence files
import os
if not os.path.exists(dir + 'OrthoFinderResults_9.7.16_pep500/Sequences/'):
	os.makedirs(dir + 'OrthoFinderResults_9.7.16_pep500/Sequences/')

#Open OrthoFinder results file (.txt)
OrthoGroupFile = open(dir + 'OrthoFinderResults_9.7.16_pep500/OrthologousGroups.txt')

for line in OrthoGroupFile:
	genes = line.split() #Divide line by spaces
	if len(genes) > 0: #Make sure the line isn't empty before performing any actions	
		OrthoGroupName = genes[0].replace(':','') #Edit OrthoGroupName and keep for naming the output file
		genes.pop(0) #Remove OrthoGroupName from list

	#Check that each species is represented exactly once in the OrthoGroup
	tag_count = 0 
	counts = []
	is_data_valid = True
	for tag in tags:
		for gene in genes:
			if tag in gene:
				tag_count = tag_count + 1
		counts.append(tag_count)
		tag_count = 0
	#print counts
	for item in counts:
		if item != 1: #Changed != 0
			is_data_valid = False
		else:
			is_data_valid = True
	if is_data_valid == False:		
		continue
	
	
	#Check if output file already exists
	import os.path
	if os.path.exists(dir + 'OrthoFinderResults_9.7.16_pep500/Sequences/' + OrthoGroupName + '.fasta') == True:
		continue
	else:
		#Create and open file to hold retrieved sequences
		OutputSequenceFile = open(dir + 'OrthoFinderResults_9.7.16_pep500/Sequences/' + OrthoGroupName + '.fasta', 'a') 
		
		#Loop through each gene name in the genes list and retrieve the corresponding sequence
		for gene in genes:
			for key in species.keys(): #Start iterating over items in species dictionary
				if key in gene: #Look for the key in the gene name
					FastaFileName = species.get(key) #Determine which fasta file to use
					FastaFile = open(dir + 'TransDecoder500/nucleotideFiles/' + FastaFileName)
					copy_line = False
					for line in FastaFile:
						if (line.find(gene) != -1):
							copy_line = True
						elif line.startswith ('>') and copy_line == True:
							break
						if copy_line == True:	
							OutputSequenceFile.write(line)
					FastaFile.close()						
		OutputSequenceFile.close()
OrthoGroupFile.close()
				
