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

filename = "%sinst-%02d-%d.txt" % (inst_dir, length, times)
output = open(filename, "w")

identity = range(1,length+1)
j = 0
while j < times:
	seq = range(1,length+1)
	line = []

	for i in range(length):
		x = random.choice(seq)
		
		line.append(x)
		seq.remove(x)
	if line != identity:
		for i in range(length):
			output.write(str(line[i]))
			if i < length - 1:
				output.write(" ")
		j += 1
		output.write("\n")

output.close()
