#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Tobias Marschall
# 
# This file is part of CLEVER.
# 
# CLEVER is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CLEVER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CLEVER.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, division
from optparse import OptionParser
import sys
import os
import math
import subprocess
import datetime

__author__ = "Tobias Marschall"

usage = """%prog [options] <predictions(.gz)> <insert-size-mean>
"""

log_factorial_table = [0,0]

def locate_executeable(exe_dict, name):
	def isexecutable(f):
		return os.path.isfile(f) and os.access(f, os.X_OK)
	for path in os.environ["PATH"].split(os.pathsep):
		f = os.path.join(path, name)
		if isexecutable(f):
			exe_dict[name] = f
			print('Found executable', f, file=sys.stderr)
			return True
	scriptpath = os.path.dirname(os.path.abspath(__file__))
	f = os.path.join(scriptpath, name)
	if isexecutable(f):
		exe_dict[name] = f
		print('Found executable', f, file=sys.stderr)
		return True
	f = os.path.abspath(os.path.join(scriptpath, '..', 'src', name))
	if isexecutable(f):
		exe_dict[name] = f
		print('Found executable', f, file=sys.stderr)
		return True
	print('Could not locate executable \"%s\". It\'s not in your PATH.'%name, file=sys.stderr)
	return False

def log_factorial(n):
	"""Factorial"""
	while n >= len(log_factorial_table):
		log_factorial_table.append(log_factorial_table[-1] + math.log(len(log_factorial_table)))
	return log_factorial_table[n]

def log_binomial(n, k):
	assert 0 <= k <= n
	return log_factorial(n) - log_factorial(k) - log_factorial(n-k)

def log_binomial_dist(n, p):
	assert 0.0 <= p <= 1.0
	if p == 0.0:
		return [0.0] + n*[float('-inf')]
	if p == 1.0:
		return n*[float('-inf')] + [0.0]
	d = []
	log_p = math.log(p)
	log_1p = math.log1p(-p)
	for k in range(n+1):
		d.append(log_binomial(n, k) + k*log_p + (n-k)*log_1p)
	return d

def binomial_dist(n, p):
	return [math.exp(x) for x in log_binomial_dist(n, p)]

class ScoreComputer:
	def __init__(self, stddev):
		self.norm = scipy.stats.norm(0, stddev)
		# maps (deviation, coverage) --> CCDF
		self.binomial_deviation = {}
		# maps coverage --> CDF
		self.binomial_zygosity = {}
	def get_random_prob(self, deviation, support, coverage):
		"""Compute probability that at least "support" many out of "coverage" many
		reads will randomly deviate from mean insert size at least as much as the given deviation."""
		deviation_int = int(round(abs(deviation)))
		if self.binomial_deviation.has_key((deviation_int,coverage)):
			return self.binomial_deviation[(deviation_int,coverage)][support]
		else:
			p = self.norm.sf(deviation_int)
			binom = binomial_dist(coverage,p)
			dist = coverage*[0.0] + [binom[-1]]
			for i in xrange(len(binom)-2,-1,-1):
				dist[i] = dist[i+1] + binom[i]
			if (deviation_int < 1000) and (coverage < 100):
				self.binomial_deviation[(deviation_int,coverage)] = dist 
				#print('binomial_deviation[(%d,%d)]:'%(deviation_int,coverage), dist, file=sys.stderr)
			return dist[support]
	def get_p_too_little_support(self, support, coverage):
		"""Compute probability that the the seen number or fewer read stem from the variant allele
		assuming it to be a heterozyguos indel in a dizygotic individual."""
		if self.binomial_zygosity.has_key(coverage):
			return self.binomial_zygosity[coverage][support]
		else:
			binom = binomial_dist(coverage,0.5)
			dist = [binom[0]]
			for i in xrange(1,len(binom)):
				dist.append(dist[i-1] + binom[i])
			self.binomial_zygosity[coverage] = dist
			#print('binomial_zygosity.has_key[%d]'%coverage, dist, file=sys.stderr)
			return dist[support]
		

def parse_readgroupstats(s):
	results = []
	for fields in (x.split(',') for x in s.split(';')):
		assert len(fields) == 3
		support = int(fields[0])
		exp_support = float(fields[1])
		coverage = int(fields[2])
		results.append((support,exp_support,coverage))
	return results

def parse_readgroupsetstats(s):
	results = []
	for fields in (x.split(',') for x in s.split(';')):
		assert len(fields) == 2
		pvalue = float(fields[0])
		probability = float(fields[1])
		results.append((pvalue,probability))
	return results

class Variation:
	def __init__(self, line, linenr):
		self.linenr = linenr
		fields = line.split()
		assert len(fields) >= 14
		self.chromosome = fields[0]
		self.coord1 = int(fields[1]) - 1
		self.coord2 = int(fields[2])
		self.var_type = fields[3]
		self.expected_support = float(fields[4])
		self.support = int(fields[5])
		self.coverage = int(fields[6])
		self.intersection_start = int(fields[7]) - 1
		self.intersection_end = int(fields[8])
		self.intersection_length = int(fields[9])
		self.variation_length = float(fields[10])
		self.raw_pvalue = float(fields[11])
		self.pvalue = float(fields[12])
		self.qvalue = float(fields[13])
		self.readgroups = fields[14] if len(fields) >= 15 else None
		self.readgroupstats = parse_readgroupstats(fields[15]) if len(fields) >= 16 else None
		self.readgroupsetstats = parse_readgroupsetstats(fields[16]) if len(fields) >= 17 else None
		if self.readgroupsetstats != None:
			assert len(self.readgroupsetstats) == 2**len(self.readgroupstats) - 1
		#if not self.chromosome.startswith('chr'):
			#self.chromosome = 'chr' + self.chromosome
	def __str__(self):
		if self.readgroups == None:
			return '%s %d %d %s %d %e'%(self.chromosome,self.coord1,self.coord2,self.var_type,self.support,self.pvalue)
		else:
			return '%s %d %d %s %d %e %s'%(self.chromosome,self.coord1,self.coord2,self.var_type,self.support,self.pvalue,self.readgroups)
	def to_vcf_line(self, insert_size_stddev):
		lendiff = int(math.ceil(insert_size_stddev / math.sqrt(self.support)))
		if self.var_type == 'INS':
			length = self.coord2
			info = 'IMPRECISE;SVTYPE=INS;SVLEN=%d;BPWINDOW=%d,%d;CILEN=%d,%d'%(length, self.intersection_start+1, self.intersection_end, length-lendiff, length+lendiff)
		elif self.var_type == 'DEL':
			length = self.coord2 - self.coord1
			info = 'IMPRECISE;SVTYPE=DEL;SVLEN=%d;BPWINDOW=%d,%d;CILEN=%d,%d'%(-length, self.intersection_start+1, self.intersection_end, length-lendiff, length+lendiff)
		else:
			assert False, 'Invalid variation type'
		return '%s\t%d\tL%d\t.\t<%s>\t.\tPASS\t%s\tGT:DP\t1/.:%d'%(self.chromosome, self.coord1, self.linenr, self.var_type, info, self.support)
		#CHROM  POS ID REF ALT           QUAL  FILTER  INFO                                                                                          FORMAT        NA00001

	def pack(self):
		readgroups_exp_support = None
		if self.readgroupstats != None:
			readgroups_exp_support = [exp_support for (support,exp_support,coverage) in self.readgroupstats]
		return PackedVariation(self.chromosome, self.coord1, self.coord2, self.var_type, self.expected_support, self.readgroups, self.linenr, readgroups_exp_support)
	def distance(self, var):
		assert self.var_type == var.var_type
		if self.var_type == "DEL":
			d = max(self.coord1,var.coord1) - min(self.coord2,var.coord2)
			if d < 0: d = 0
			return d
		elif self.var_type == "INS":
			return abs(self.coord1 - var.coord1)
		else:
			assert False
	def fix_read_groups(self, score_computer, samplenames):
		assert self.readgroupstats != None
		# probability that a random insert size will deviate from the mean
		# at least as much as the size of the putative indel
		new_readgroup_set = []
		# sum up total of individual that (possibly) have the indel
		total_support = 0
		total_exp_support = 0.0
		total_coverage = 0
		for i, (support,exp_support,coverage) in enumerate(self.readgroupstats):
			#print('Individual', i, ':', file=sys.stderr)
			prob_random = score_computer.get_random_prob(self.variation_length, support, coverage)
			p_too_little_support = score_computer.get_p_too_little_support(support,coverage)
			#print('  prob_random:', prob_random, file=sys.stderr)
			#print('  p_too_little_support:', p_too_little_support, file=sys.stderr)
			possible_hit = True
			if (prob_random < 0.05) and (p_too_little_support >= 0.05):
				# case: we are sure this individual has the indel
				if samplenames == None:
					new_readgroup_set.append(str(i))
				else:
					new_readgroup_set.append(samplenames[i])
			elif prob_random >= 0.5:
				# case: we are fairly sure this individual does not have the indel
				possible_hit = False
			else:
				# case: we don't really know
				if samplenames == None:
					new_readgroup_set.append(str(i)+'?')
				else:
					new_readgroup_set.append(samplenames[i]+'?')
			if possible_hit:
				total_support += support
				total_exp_support += exp_support
				total_coverage += coverage
		self.expected_support = total_exp_support
		self.support = total_support
		self.coverage = total_coverage
		self.readgroups = ','.join(new_readgroup_set) if len(new_readgroup_set) > 0 else 'None'

class PackedVariation:
	"""Only the most essential information on a variation to save space."""
	def __init__(self, chromosome, coord1, coord2, var_type, expected_support, readgroups, linenr, readgroups_exp_support):
		self.chromosome = chromosome
		self.coord1 = coord1
		self.coord2 = coord2
		self.var_type = var_type
		self.expected_support = expected_support
		self.readgroups = readgroups
		self.linenr = linenr
		self.readgroups_exp_support = readgroups_exp_support
	def center(self):
		if self.var_type == "DEL":
			return (self.coord1 + self.coord2) // 2
		elif self.var_type == "INS":
			return self.coord1
		else:
			assert False
	def distance(self, var):
		assert self.var_type == var.var_type
		return abs(self.center() - var.center())
		#if self.var_type == "DEL":
			#d = max(self.coord1,var.coord1) - min(self.coord2,var.coord2)
			#if d < 0: d = 0
			#return d
		#elif self.var_type == "INS":
			#return abs(self.coord1 - var.coord1)
		#else:
			#assert False
	def __str__(self):
		return '%s %d %d %s %.2f %s %d'%(self.chromosome,self.coord1+1,self.coord2,self.var_type,self.expected_support,self.readgroups,self.linenr)
	def to_str_readgroupwise(self, readgroup_index):
		assert self.readgroups_exp_support != None
		return '%s %d %d %s %.2f'%(self.chromosome,self.coord1+1,self.coord2,self.var_type,self.readgroups_exp_support[readgroup_index])

class SamplewiseFiles:
	def __init__(self, prefix, samplenames):
		self.prefix = prefix
		self.samplenames = samplenames
		self.files = {}
	def get_file(self, sample_index):
		if self.files.has_key(sample_index):
			return self.files[sample_index]
		else:
			if self.samplenames != None:
				if sample_index >= len(self.samplenames):
					print("Error: Name unknown for sample with index", sample_index, file=sys.stderr)
					sys.exit(1)
				f = open('%s.%s.predictions.txt'%(self.prefix,self.samplenames[sample_index]), 'w')
			else:
				f = open('%s.%d.predictions.txt'%(self.prefix,sample_index), 'w')
			self.files[sample_index] = f
			return f

def variation_cmp(var1, var2):
	if var1.chromosome != var2.chromosome: return cmp(var1.chromosome,var2.chromosome)
	if var1.var_type != var2.var_type: return cmp(var1.var_type,var2.var_type)
	return cmp(var1.coord1,var2.coord1)

def variation_support_cmp(var1,var2):
	return cmp(var1.expected_support, var2.expected_support)

def select_best(l):
	if len(l) == 0: return
	l.sort(cmp=variation_support_cmp, reverse=True)
	return l[0].linenr

def print_best(l, samplewise_output_files, vcf_output, insert_size_stddev, covbal_cutoff):
	if len(l) == 0: return
	l.sort(cmp=variation_support_cmp, reverse=True)
	if covbal_cutoff != None:
		covbal =  l[0].support / l[0].coverage
		if covbal < covbal_cutoff: return
	if vcf_output:
		print(l[0].to_vcf_line(insert_size_stddev))
	else:
		print(l[0])
		if samplewise_output_files != None:
			assert l[0].readgroups_exp_support != None
			for i, exp_support in enumerate(l[0].readgroups_exp_support):
				if exp_support == 0: continue
				print(l[0].to_str_readgroupwise(i), file=samplewise_output_files.get_file(i))

def main():
	parser = OptionParser(usage=usage)
	parser.add_option("-d", action="store", dest="min_del_support", type=float, default=2,
			  help="Minimum expected support for deletion cliques (cliques with lower support are discarded).")
	parser.add_option("-i", action="store", dest="min_ins_support", type=float, default=2,
			  help="Minimum expected support for insertion cliques (cliques with lower support are discarded).")
	parser.add_option("--covbal", action="store", dest="coverage_balance", type=float, default=None,
			  help="Minimum coverage balance (=support/coverage). Filter is applied after merging (default: disabled).")
	parser.add_option("-c", action="store", dest="min_coverage", type=int, default=2,
			  help="Minimum coverage at clique center.")
	parser.add_option("-C", action="store", dest="min_ind_coverage", type=int, default=None,
			  help="Minimum individual coverage at clique center, that is, only cliques are retains for which ALL individuals have at least the given coverage.")
	parser.add_option("-R", action="store_true", dest="fix_read_groups", default=False,
			  help="Re-evaluate which cliques lead to which sets of individuals (requires standard deviation to be given).")
	parser.add_option("--stddev", action="store", dest="insert_size_stddev", default=None, type=float,
			  help="Standard deviation of insert size (necessary for some options).")
	parser.add_option("-S", action="store", dest="samplewise_output_prefix", default=None,
			  help="Also store output in separate files for each sample. Parameter: prefix of filenames for samplewise output.")
	parser.add_option("-N", action="store", dest="samplename_file", default=None,
			  help="Filename to read samplenames from.")
	parser.add_option("--only-del", action="store_true", dest="only_deletions", default=False,
			  help="Only process deletions.")
	parser.add_option("--only-ins", action="store_true", dest="only_insertions", default=False,
			  help="Only process insertions.")
	parser.add_option("--vcf", action="store_true", dest="vcf_output", default=False,
			  help="Output VCF format.")
	(options, args) = parser.parse_args()
	if (len(args)!=2):
		parser.print_help()
		sys.exit(1)
	predictions_file = args[0]
	insert_size_mean = int(round(float(args[1])))
	exe_dict = dict()
	#if not locate_executeable(exe_dict, 'ctk-version'): return 1
	#ctk_version = subprocess.Popen([exe_dict['ctk-version']], stdout=subprocess.PIPE).stdout.readline().strip()
	#print('CTK version: ', ctk_version, file=sys.stderr)
	if options.only_deletions and options.only_insertions:
		print("Error: Options --only-del and --only-ins are mutually exclusive.", file=sys.stderr)
		sys.exit(1)
	if (options.coverage_balance != None) and not options.vcf_output:
		print("Error: Option --covbal can only be used in connection with --vcf.", file=sys.stderr)
		sys.exit(1)
	if options.fix_read_groups:
		import scipy.stats
		if options.insert_size_stddev == None:
			print('Error: When using option -R, parameter --stddev is mandatory', file=sys.stderr)
			return 1
		score_computer = ScoreComputer(options.insert_size_stddev)
	if options.vcf_output and (options.insert_size_stddev == None):
		print('Error: When using option --vcf, parameter --stddev is mandatory', file=sys.stderr)
		return 1
	samplenames = None
	if options.samplename_file != None:
		samplenames = [s.strip() for s in open(options.samplename_file)]
	samplewise_output_files = None
	if options.samplewise_output_prefix != None:
		if options.vcf_output:
			print('Error: Options --vcf and -S cannot be combined.', file=sys.stderr)
			return 1
		samplewise_output_files = SamplewiseFiles(options.samplewise_output_prefix, samplenames)
	if predictions_file.endswith('.gz'):
		input = subprocess.Popen('gunzip', stdin=open(predictions_file), stdout=subprocess.PIPE).stdout
	else:
		input = open(predictions_file)
	l = []
	linenr = 0
	for line in input:
		linenr += 1
		v = Variation(line, linenr)
		if options.fix_read_groups:
			v.fix_read_groups(score_computer, samplenames)
		if linenr % 50000 == 0:
			print("Having read %d lines"%linenr, file=sys.stderr)
		if (v.var_type != 'INS') and options.only_insertions: continue
		if (v.var_type != 'DEL') and options.only_deletions: continue
		if (v.var_type == 'INS') and (v.expected_support < options.min_ins_support): continue
		if (v.var_type == 'DEL') and (v.expected_support < options.min_del_support): continue
		if v.coverage < options.min_coverage: continue
		if options.min_ind_coverage != None:
			if v.readgroupstats == None:
				print("Error: Option -C can only be used when read-group-wise statistics are available (offending line: %d)"%linenr, file=sys.stderr)
				return 1
			test_passed = True
			for support, exp_support, coverage in v.readgroupstats:
				if coverage < options.min_ind_coverage:
					test_passed = False
					break
			if not test_passed:
				continue
		if options.vcf_output:
			l.append(v)
		else:
			l.append(v.pack())
	l.sort(cmp=variation_cmp)
	cluster = []
	previous = None
	lines_numbers = set()
	if options.vcf_output:
		print('##fileformat=VCFv4.1')
		print('##fileDate=%s'%datetime.datetime.now().strftime('%Y%m%d'))
		print('##source=clever-postprocessing-%s cmdline: %s'%(ctk_version, ' '.join(sys.argv)))
		print('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tdefault')
	for v in l:
		if previous != None:
			if (previous.chromosome == v.chromosome) and (previous.var_type == v.var_type) and (previous.distance(v) <= insert_size_mean):
				cluster.append(v)
			else:
				#lines_numbers.add(select_best(cluster))
				print_best(cluster, samplewise_output_files, options.vcf_output, options.insert_size_stddev, options.coverage_balance)
				cluster = [v]
		else:
			cluster.append(v)
		previous = v
	if len(cluster) > 0:
		print_best(cluster, samplewise_output_files, options.vcf_output, options.insert_size_stddev, options.coverage_balance)
		#lines_numbers.add(select_best(cluster))
	#linenr = 0
	#for line in file(predictions_file):
		#linenr += 1
		#if not linenr in lines_numbers: continue
		#print(line.strip())

if __name__ == '__main__':
	sys.exit(main())
