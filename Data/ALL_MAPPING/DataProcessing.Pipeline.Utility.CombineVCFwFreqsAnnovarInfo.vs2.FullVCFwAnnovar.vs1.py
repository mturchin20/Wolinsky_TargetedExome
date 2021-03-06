#!/usr/bin/python

import sys
import re
import gzip
import itertools
import copy
import random
from argparse import ArgumentParser

file1 = None
file2 = None
hash1 = {}
FlipAlleles = 0 #Flag for if I need to flip the reference allele to be the derived allele down the road and whether I have to change any of the annotation information for this reason

#File1 Ex: /home/pg/michaelt/Data/ALL_MAPPING/Pools/PostMerge/mapping_pool_merged/GATK/AllPools.QCed.preGATK.QCed.samplesMerged.rmdup.BQSR.calmd.AllPoolsMerged.ChrAll.GATK.ReduceReads.UG.VQSR.SNP.PASS.vcf.AnnovarFormat.genome_summary.csv
#File2 Ex: /home/pg/michaelt/Data/ALL_MAPPING/Pools/PostMerge/mapping_pool_merged/GATK/AllPools.QCed.preGATK.QCed.samplesMerged.rmdup.BQSR.calmd.AllPoolsMerged.ChrAll.GATK.ReduceReads.UG.VQSR.SNP.PASS.wAA.DropOffTargetVariants.1kbWindow.95geno.recode.vcf.gz

#Argument handling and parsing
#Parsing arguments
parser = ArgumentParser(add_help=False)

#Required arguments
required = parser.add_argument_group('required arguments:')
required.add_argument("--file1", dest="file1", help="location of file1", required=True, metavar="FILE1")
required.add_argument("--file2", dest="file2", help="location of file2", required=True, metavar="FILE2")

#Optional arguments
optional = parser.add_argument_group('optional arguments:')
optional.add_argument("-h", "--help", help="show this help message and exit", action="help")

args = parser.parse_args()

#print(args.file1)

#Main script


if args.file1 == "-":
	file1 = sys.stdin
elif re.search('gz$', args.file1):
	file1 = gzip.open(args.file1, 'rb')	
else:
	file1 = open(args.file1, 'r')

for line1 in file1:
	line1 = line1.rstrip().split(",")
	multiTranscript=0
	multiTranscriptsArray=[]

	if line1[0] == "Func":
		continue

	ChrBP1 = str(line1[len(line1)-6]) + "_" + str(line1[len(line1)-5])

	if ChrBP1 not in hash1:
		
		SynnonSynLocation=2

		if not re.search('^$|stoploss SNV|stopgain SNV|unknown|synonymous SNV|nonsynonymous SNV', line1[2]):
#			sys.stderr.write("Happening!\n")
			foundEndofGeneAnnot=0
			multiTranscript=1			
			multiTranscriptsArray.extend([line1[1], line1[2]])
			i=3
			while foundEndofGeneAnnot != 1:
				if not re.search('^$|stoploss SNV|stopgain SNV|unknown|synonymous SNV|nonsynonymous SNV', line1[i]):
					sys.stderr.write("Happening2!\n")
					multiTranscriptsArray.extend([line1[i]])
					i += 1
				else:
#					sys.stderr.write("Happening3!\n")
					SynnonSynLocation = i
					if re.search('stoploss SNV|stopgain SNV|synonymous SNV|nonsynonymous SNV', line1[i]):
						line1[i] = "_".join(line1[i].split())
					foundEndofGeneAnnot = 1

		if multiTranscript == 0:
			line1[2] = "_".join(line1[2].split())
			hash1[ChrBP1] = [",".join(map(str, line1))]
		else:
			hash1[ChrBP1] = []
			for j in range(0,len(multiTranscriptsArray)):
				hash1[ChrBP1].append(",".join(map(str, list(itertools.chain.from_iterable([[line1[0], multiTranscriptsArray[j], line1[SynnonSynLocation]], line1[SynnonSynLocation+1:len(line1)+1]])))))
#			sys.stderr.write(hash1[ChrBP1][0] + "\n")
	else:
		sys.stderr.write("Error1a -- ChrBP1 found more than once in hash1 (" + ChrBP1 + ")\n")


file1.close()

if args.file2 == "-":
	file2 = sys.stdin
elif re.search('gz$', args.file2):
	file2 = gzip.open(args.file2, 'rb')	
else:
	file2 = open(args.file2, 'r')

for line2 in file2:
	line2 = line2.rstrip().split()	

	if not re.search('^#', line2[0]):
#		ChrBP2 = "_".join([str(line2[0]), str(line2[1]), "1"])
		ChrBP2 = "_".join([str(line2[0]), str(line2[1])])
		if ChrBP2 in hash1:
#				for k in range(0, len(hash1[ChrBP2])):
#					tempOrigLine2 = copy.copy(line2)
#					tempOrigLine2[8:8] = [hash1[ChrBP2][k]]
#					print "\t".join(tempOrigLine2)
				tempOrigLine2 = copy.copy(line2)
				tempOrigLine2[8:8] = [hash1[ChrBP2][random.randint(0,len(hash1[ChrBP2])-1)]]
				print "\t".join(tempOrigLine2)
				
		else:
			sys.stderr.write("Error2a -- ChrBP2 not found in hash1 (" + ChrBP2 + ")\n")
	else:
		print "\t".join(line2)

file2.close()

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

