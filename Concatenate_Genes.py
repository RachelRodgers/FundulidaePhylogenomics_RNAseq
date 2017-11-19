#Concatenate_Genes.py

import glob
import os

#Designate output directory and open the log file
out_dir = "/media/rrodgers/Seagate_Expansion_Drive/Individual_Analysis/Matrix4/Concatenation/"

if not os.path.exists(out_dir):
	os.makedirs(out_dir)

output_file = open (out_dir + "GeneIndexFile.txt", "a")
chunk_outfile = open (out_dir + "chunk.txt",'a')
concatenated_alignment_file = open (out_dir + "Concatenated_Alignment.txt", "a")

#Initialize empty dictionary and tag variable
species_dictionary={}
current_tag = None

#Find original alignment files
filenames = (glob.glob('/media/rrodgers/Seagate_Expansion_Drive/Individual_Analysis/Matrix4/Raw_Sequences/Aligned_Files/RenamedFiles/TrimmedGenes/*.fas'))

chunk = 0

extra_count = 0

#Begin looping through files
for file in filenames:

	basename = os.path.basename(file).replace('.fas','')
	#output_file.write("\n" + "File: " + basename + "\n")
		
	#Open the original alignment file
	current_file = open(file)

	geneIndexFound = False

	for line in current_file:

		if ">" in line:
			columns = line.split()
			current_tag = columns[0]
			#output_file.write("Tag: " + current_tag + "\n")

		else:
			
			if current_tag not in species_dictionary.keys(): #Occurs in first file only

				species_dictionary[current_tag] = line.rstrip('\n')
				
				if geneIndexFound == False:
					chunk += 1
					extra_count += 1
					output_file.write('charset ' + basename + ' = 1 - ' + str(len(species_dictionary[current_tag]) - extra_count) + ';\n')
					chunk_outfile.write('chunk' + str(chunk) + ':' + basename + ', ')
					#chunk_outfile.write(basename + ', ')
					geneIndexFound = True
										

			else: 
			
				nextStartingIndex = len(species_dictionary[current_tag]) - extra_count + 1

				species_dictionary[current_tag]+= line.rstrip('\n')
	
				if geneIndexFound == False:
					chunk += 1
					extra_count += 1
					output_file.write('charset ' + basename + ' = ' + str(nextStartingIndex) + ' - ' + str(len(species_dictionary[current_tag]) - extra_count) + ';\n')
					chunk_outfile.write('chunk' + str(chunk) + ':' + basename + ', ') 
					#chunk_outfile.write(basename + ', ')
					geneIndexFound = True		
	
	current_file.close()


output_file.close()
chunk_outfile.close()

nameList = species_dictionary.keys()
for name in nameList:
	concatenated_alignment_file.write(name +"\n" + species_dictionary[name] + "\n")
	
concatenated_alignment_file.close()

