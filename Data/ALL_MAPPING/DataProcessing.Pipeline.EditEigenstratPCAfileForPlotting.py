#!/usr/bin/python

import sys
import re
import gzip
from argparse import ArgumentParser

file1 = None
file2 = None
hash1 = {}

#File1 Ex: DataProcessing.Pipeline.CreateProperIndvPhenoLinkFile.vs1.20130930_POP_genomics_sample.status_list_9-16-13.output 
#File2 Ex: Pools/PostMerge/mapping_pool_merged/Samtools/AllPools.QCed.preGATK.QCed.samplesMerged.rmdup.BQSR.calmd.AllPoolsMerged.Samtools.ChrAll.C50.flt.250k.phenoColEdit.Results.pca

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

	hash1[line1[3]] = line1

file1.close()

if args.file2 == "-":
	file2 = sys.stdin
elif re.search('gz$', args.file2):
	file2 = gzip.open(args.file2, 'rb')	
else:
	file2 = open(args.file2, 'r')

for line2 in file2:
	line2 = line2.rstrip().split()	

	indvID = None 
	indvIDarrayPre = line2[0].split(":")
	indvIDarray = indvIDarrayPre[0].split("_")

#	if indvIDarray[1]:
	if len(indvIDarray) > 1:
		indvID = indvIDarray[0] + "-" + indvIDarray[1]
	else:
		indvID = indvIDarray[0] 

	if indvID in hash1:
#		hash1[indvID][len(hash1[indvID])-1] = line2[
		line2[len(line2)-1] = "_".join(hash1[indvID][4].split())
#		line2[len(line2)-1] = hash1[indvID][4]
		print "\t".join(line2)
	else:
		sys.stderr.write("Error 1a -- indvID not found in hash1 (indvID: " + str(indvID) + ")\n")


file2.close()


def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

