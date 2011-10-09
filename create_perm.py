#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

def all_perms(l):
	if len(l) <= 1:
		yield l
	else:
		for perm in all_perms(l[1:]):
			for i in range(len(perm)+1):
				yield perm[:i] + l[0:1] + perm[i:]


length = int(sys.argv[1])
str_length = sys.argv[1]

inst_dir = "./inst/"

output = open(inst_dir+"perm-"+str_length+".txt", "w")

for l in all_perms(range(1, length+1)):
	print l
	a = [str(i) for i in l]
	output.write(" ".join(a))
	output.write("\n")

output.close()
