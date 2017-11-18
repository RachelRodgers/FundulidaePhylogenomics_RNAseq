#!/usr/bin/env perl
# fundulus_trimmer.pl 
# This script performs Trimmomatic on every file within the rnaseq directory.
use strict; use warnings;

#include some file modules needed to find and manipulate file paths
use File::Find;
use File::Path;
use File::Basename;

#Paths to trimmomatic, IlluminaClip, and the top level directory for input files
#The top level directory for input files must be named "rnaseq" --- CASE SENSITIVE!!

my $trimmoPath = "/home/dduvern/RNAseq_Analysis/Trimmomatic-0.33/trimmomatic-0.33.jar";
my $IlluminaClipPath = "/home/dduvern/Desktop/NEBnextAdapt.fa";
my $dir = "/home/dduvern/Desktop/rnaseq/";

my @R1Array;
my @R2Array;

#The find function will recursively search through all folders starting from the top level directory.
#For every file that it finds, it will call the "Add_File_To_Arrays" function.
find(\&Add_File_To_Arrays, $dir);

#Now that both arrays are filled, lets loop through the R1 array.
for(my $i=0; $i < scalar @R1Array; $i++)
{

   #Lets get the directory of the current R1 file and replace "rnaseq" with "rnaseqOutput. This will give us our current output directory.  
   my $R1Dir = dirname($R1Array[$i]);
   $R1Dir =~ s/rnaseq/rnaseqOutput/;

   #if the output directory does not exist, then create it.
   if(! -d $R1Dir)
   {
      mkpath($R1Dir);
   }


   #Now lets get the paths for all output and input files for trimmomatic.
   my $R1 = $R1Array[$i];
   my $R1OutPaired = $R1Array[$i];
   my $R1OutUnPaired = $R1Array[$i];

   my $R2 = $R2Array[$i];
   my $R2OutPaired = $R2Array[$i];
   my $R2OutUnPaired = $R2Array[$i];

   #The Output files need to have their paths changed so that they are named correctly and go to the rnaseqOutput directory.

   $R1OutPaired =~ s/fastq/OutputPaired\.fastq/;
   $R1OutPaired =~ s/rnaseq/rnaseqOutput/;
   $R1OutUnPaired =~ s/fastq/OutputUnPaired\.fastq/;
   $R1OutUnPaired =~ s/rnaseq/rnaseqOutput/;

   $R2OutPaired =~ s/fastq/OutputPaired\.fastq/;
   $R2OutPaired =~ s/rnaseq/rnaseqOutput/;
   $R2OutUnPaired =~ s/fastq/OutputUnPaired\.fastq/;
   $R2OutUnPaired =~ s/rnaseq/rnaseqOutput/;

   #Now we call trimmomatic and pass in all the appropriate command line parameters
   system("java\ -jar\ $trimmoPath PE -phred33 $R1 $R2 $R1OutPaired $R1OutUnPaired $R2OutPaired $R2OutUnPaired ILLUMINACLIP:$IlluminaClipPath:2:30:10 SLIDINGWINDOW:4:5 LEADING:5 TRAILING:5 MINLEN:25");	
	
}


#---------This function will add an R1 file and an R2 file to the appropriate arrays.------------
sub Add_File_To_Arrays
{
   #"$File::Find::name" will always equal the path of the file that the "find" function is currently looking at.

   #Lets check to make sure the current file is an R1.gz file.
    if($File::Find::name =~ /.*_R1_.*\.gz/)
    {
 
       #Get the path of the R1 and R2 files and push them into their arrays
       my $R1File = $File::Find::name;

       my $R2File = $File::Find::name;
       $R2File =~ s/_R1_/_R2_/;

       push @R1Array, $R1File;
       push @R2Array, $R2File;
    }
}

