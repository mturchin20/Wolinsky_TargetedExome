#!/usr/bin/python

import sys
import re
import gzip
from argparse import ArgumentParser

file1 = None
file2 = None
hash1 = {}

#File1 Ex: /data/userdata/pg/michaelt/Data/ALL_MAPPING/Pools/MM5/PostMerge/mapping_pool_merged/GATK/AllPools.Vs2.QCed.preGATK.QCed.samplesMerged.rmdup.BQSR.calmd.AllPoolsMerged.ChrAll.GATK.ReduceReads.UG.VQSR.SNP.PASSts99_9.wAA.Bi.DropOffTarg_1kb.geno95.hwe1e4.FreqInfo.AnnovarAnnotation.vs5.txt.gz 
#File2 Ex: /data/userdata/pg/michaelt/Data/ALL_MAPPING/Pools/MM5/PostMerge/mapping_pool_merged/GATK/DataAnalysis.GATK.CorrelatePCsWithIndvSumAC.vs1.output

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

	ChrBP1 = str(line1[0]) + "_" + str(line1[1].split("_")[0])

	if ChrBP1 in hash1:
		hash1[ChrBP1].extend([line1[26]])
	else:
		hash1[ChrBP1] = [line1[26]]

file1.close()

if args.file2 == "-":
	file2 = sys.stdin
elif re.search('gz$', args.file2):
	file2 = gzip.open(args.file2, 'rb')	
else:
	file2 = open(args.file2, 'r')

for line2 in file2:
	line2 = line2.rstrip().split()	

	ChrBP2 = str(line2[0]) + "_" + str(line2[1])

	if ChrBP2 in hash1:
		print "\t".join(line2) + "\t" + ",".join(map(str, hash1[ChrBP2]))
	else:
		sys.stderr.write("Error1a -- SNP " + ChrBP2 + " has no entry in the AnnovarAnnotation file. Skipping...\n")


file2.close()

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

