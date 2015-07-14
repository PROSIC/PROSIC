#!/usr/bin/env python
from __future__ import print_function, division
from optparse import OptionParser
import os
import sys
import vcf

__author__ = "Louis Dijkstra"

usage = """%prog [options] <vcf-file> <calls-file> <new-vcf-file> 

	<vcf-file> 	tabix-indexed VCF file 
	<calls-file>	output file generated by sm_call 
	<new-vcf-file> 	annoted VCF file

Annotates the given VCF file with the results generated by the sm_call 
application. 
"""

def makeCall (p_somatic, p_germline, p_not_present):
	"""Makes the call on the basis of the posterior probabilities."""
	if p_somatic > p_germline and p_somatic > p_not_present:
		return 'SOMATIC', p_somatic
	if p_germline > p_somatic and p_germline > p_not_present:
		return 'GERMLINE', p_germline
	return 'ABSENT', p_not_present	

def main():

	parser = OptionParser(usage=usage)
	parser.add_option("-v", action="store_true", dest="verbose", default=False,
                      		help="Verbose. Prints regularly how many variants have been processed.")
	(options, args) = parser.parse_args()
	
	if (len(args)!=3):
		parser.print_help()
		return 1
	
	vcf_filename 		= os.path.abspath(args[0])
	calls_filename 		= os.path.abspath(args[1])
	new_vcf_filename 	= os.path.abspath(args[2])

	vcf_reader 		= vcf.Reader(open(vcf_filename))
	vcf_writer 		= vcf.Writer(open(new_vcf_filename, 'w'), vcf_reader)
	calls_file		= open(calls_filename, 'r') ; 

	line_number = 0 
	for line in calls_file: 
		line_number += 1 
		values 	= line.split('\t')
		
		if len(values) == 1: # end of file is reached
			break 
		if len(values) != 10: 
			print("ERROR: line number %d in file %s does not contain 10 values as required. The line in question is:\n\t%s\n"%(line_number, calls_filename, line))
			return 1 

		if options.verbose and line_number % 1000 == 0: 
			print("Processed %d variants"%line_number)

		position 	= int(values[2])

		call = 'UNKNOWN'
		post_prob_call = 'NONE'
		h_vaf, c_vaf, max_logl = 'NONE', 'NONE', 'NONE' 
		p_somatic, p_germline, p_not_present = 'NONE', 'NONE', 'NONE'
	
		if values[4].strip() != '.':	h_vaf 		= float(values[4])
		if values[5].strip() != '.': 	c_vaf 		= float(values[5])
		if values[6].strip() != '.':	max_logl	= float(values[6])
		if values[7].strip() != '.':	p_somatic 	= float(values[7])
		if values[8].strip() != '.':	p_germline 	= float(values[8])
		if values[9].strip() != '.':	p_not_present 	= float(values[9])
		
		if not (p_somatic is 'NONE' and p_germline is 'NONE' and p_not_present is 'NONE'):
			# make call
			call, post_prob_call = makeCall(p_somatic, p_germline, p_not_present)

		vcf_record = vcf_reader.next() 
		while (vcf_record.POS != position):
			vcf_writer.write_record(vcf_record)
			vcf_record = vcf_reader.next()

		vcf_record.INFO['CALL'] 		= call 
		vcf_record.INFO['POSTERIOR_PROB'] 	= post_prob_call
		vcf_record.INFO['MAP_HEALTHY_VAF'] 	= h_vaf
		vcf_record.INFO['MAP_CANCER_VAF'] 	= c_vaf
		vcf_writer.write_record(vcf_record)

	for vcf_record in vcf_reader:
		vcf_writer.write_record(vcf_record)
			
			 

if __name__ == '__main__':
	sys.exit(main())
