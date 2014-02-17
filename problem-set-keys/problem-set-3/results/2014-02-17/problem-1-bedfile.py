#! /usr/bin/env python

'''
Problem 1.1. What is the region with the largest start position (2nd column) for
each chromosome in lamina.bed?

Problem 1.2 What is the region with the largest end position on chrY in
lamina.bed?
'''

import sys
from collections import defaultdict

if len(sys.argv) != 2:
    print >>sys.stderr, "error: specify bed file"
    sys.exit(1)

bedfilename = sys.argv[1]

regions_1_1 = defaultdict(list)
regions_1_2 = defaultdict(list)

for line in open(bedfilename):

    if line.startswith('#'): continue

    # get fields and coerce
    fields = line.strip().split('\t')
    chrom = fields[0]
    start = int(fields[1])
    end = int(fields[2])
    score = float(fields[3])

    # problem 1.1: add tuples of (start, end) to the list 
    regions_1_1[chrom].append((start,end))

    # problem 1.2: similar to problem 1.1, except put end in the first
    # position for max() to look at it. also want to keep the score for
    # reporting later
    regions_1_2[chrom].append((end, start, score))

print "problem 1.1: largest start positions for each chrom:"

for chrom in sorted(regions_1_1):

    max_start, max_end = max(regions_1_1[chrom]) 

    print '\t'.join([chrom, str(max_start)])

print
print "problem 1.2: region with largest end position on chrY, region " \
      "size in 5th col:"

for chrom in sorted(regions_1_2):

    if chrom != 'chrY': continue

    max_end, start, value = max(regions_1_2[chrom]) 
    region_size = max_end - start

    print '\t'.join([chrom, str(start), str(max_end),
                     str(value), str(region_size)])
