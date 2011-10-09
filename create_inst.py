#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import random

if (len(sys.argv) < 3):
	print "USAGE:"
	print "======"

	print sys.argv[0] + " <length> <times>\n\n"


	print "where:\n"

	print "  <length> = size of permutations"
	print "  <times> = number of permutations to be created\n"

	exit(-1)


length = int(sys.argv[1])
str_length = sys.argv[1]
times = int(sys.argv[2])
str_times = sys.argv[2]

inst_dir = "./inst/"

output = open(inst_dir+"inst-"+str_length+"-"+str_times+".txt", "w")

for j in range(times):
	seq = range(1,length+1)

	for i in range(length):
		x = random.choice(seq)
		
		output.write(str(x))
		if i < length - 1:
			 output.write(" ")
		seq.remove(x)

	output.write("\n")

output.close()
