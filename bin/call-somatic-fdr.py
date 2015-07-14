#!/usr/bin/env python
from __future__ import print_function, division
from optparse import OptionParser
import os
import sys
import vcf
from operator import itemgetter

__author__ = "Louis Dijkstra"

usage = """%prog [options] <calls-file> 

	<calls-file>	output file generated by sm_caller

Outputs the somatic variants while controlled for the Bayesian FDR. 
"""

def transformProbabilities(p_somatic, p_germline, p_not_present):
	p_not_somatic = (p_germline + p_not_present) * float(3.0) / float(2.0) 
	p_somatic *= float(3.0)
	normalization_factor = p_somatic + p_not_somatic
	return p_somatic / normalization_factor, p_not_somatic / normalization_factor 

def main():

	parser = OptionParser(usage=usage)
	parser.add_option("-q", action="store", dest="q_value", type=float, default=0.10,
                      		help="Q-value used for controlling Bayesian FDR.")
	parser.add_option("-v", action="store_true", dest="verbose", default=False,
                      		help="Verbose. Prints regularly how many variants have been processed.")
	(options, args) = parser.parse_args()
	
	if (len(args)!=1):
		parser.print_help()
		return 1
	
	calls_filename 		= os.path.abspath(args[0])
	calls_file		= open(calls_filename, 'r') ; 

	posterior_probabilities 	= []
	line_numbers			= []

	n = 0 
	for line in calls_file: 
		values 	= line.split('\t')
		
		if len(values) != 10: 
			break  

		if options.verbose and n % 10000 == 0: 
			print("Processed %d variants"%n)

		p_somatic, p_germline, p_not_present = 'NONE', 'NONE', 'NONE'
		if values[7].strip() != '.':	p_somatic 	= float(values[7])
		if values[8].strip() != '.':	p_germline 	= float(values[8])
		if values[9].strip() != '.':	p_not_present 	= float(values[9])
		
		if not (p_somatic is 'NONE' and p_germline is 'NONE' and p_not_present is 'NONE'):
			p_somatic, p_not_somatic = transformProbabilities(p_somatic, p_germline, p_not_present)
			if p_somatic > p_not_somatic: 
				posterior_probabilities.append(p_somatic)
			else:
				posterior_probabilities.append(p_not_somatic)
		else: 
			posterior_probabilities.append(float(1.0)/float(2.0)) # prior	
	
		line_numbers.append(n)
		n += 1 

	calls_file.close()

	# sort both lists simultaneously
	posterior_probabilities, line_numbers = [list(x) for x in zip(*sorted(zip(posterior_probabilities, line_numbers), key=itemgetter(0), reverse=True))]	

	k = 1
	prob_sum = posterior_probabilities[0]
	while (k - prob_sum <= k * options.q_value) and k <= len(posterior_probabilities):
		k += 1 
		prob_sum += posterior_probabilities[k - 1] 
		#print("%d:\t%lf\t<=\t%lf"%(k, (k - prob_sum)/float(k), options.q_value))

	significant_line_numbers = line_numbers[:k-1] # list of line numbers with calls considered 'significant'
	significant_line_numbers.sort()

	# walk again through the file with the calls and output the significant ones
	calls_file = open(calls_filename, 'r') ; 
	n_read = 0
	line = calls_file.readline()
	n_som = 0 
	for line_number in significant_line_numbers:
		while n_read != line_number:
			n_read += 1
			if options.verbose and n_read % 10000 == 0: 
				print("Processed %d variants"%n_read)
			line = calls_file.readline()

		values 	= line.split('\t')
		p_somatic, p_germline, p_not_present = 'NONE', 'NONE', 'NONE'
		if values[7].strip() != '.':	p_somatic 	= float(values[7])
		if values[8].strip() != '.':	p_germline 	= float(values[8])
		if values[9].strip() != '.':	p_not_present 	= float(values[9])
		if not (p_somatic is 'NONE' and p_germline is 'NONE' and p_not_present is 'NONE'):
			p_somatic, p_not_somatic = transformProbabilities(p_somatic, p_germline, p_not_present)
			if p_somatic > p_not_somatic: 
				n_som += 1 
	
	calls_file.close()

	print("\nTotal # of calls: %d\tConsidered to be significant: %d\tSomatic calls: %d\n"%(len(posterior_probabilities), k-1, n_som))

			 

if __name__ == '__main__':
	sys.exit(main())
