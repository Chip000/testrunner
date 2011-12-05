#!/usr/bin/python
# -*- coding:utf-8 -*-

import argparse
import os
import sys
sys.path.append("./class/")
# Class for input instance
import Inst
# Class for the timer
import Timer
from datetime import datetime
import time

RESULT_DIR = "./results/"
BIN_DIR = "./bin/"
TMP_DIR = "./tmp/"

MODEL = ['trans','rev','trans_rev']
BOUNDS = ['def', # default
	  'tra_br', 'tra_cg', # transposition
	  'rev_br', 'rev_cg', # reversal
	  't_r_br', 't_r_cb', 't_r_cc'] # rev+trans
THEORIES = ['csp','cop','ilp']

ECLIPSE = "eclipse"
ECLIPSE_FILE = "lib_proj.clp"
ECLIPSE_CMD = "eclipse -b " + BIN_DIR + ECLIPSE_FILE
ECLIPSE_MODEL_CSP = {'rev':"reversal_dist", 
		     'trans':"transposition_dist", 
		     'trans_rev':"trans_rev_dist"}
ECLIPSE_MODEL_COP = {'rev':"reversal_dist_cop", 
		     'trans':"transposition_dist_cop",
		     'trans_rev':"trans_rev_dist_cop"}
ECLIPSE_MODEL = {'csp': ECLIPSE_MODEL_CSP, 'cop': ECLIPSE_MODEL_COP}

GLPK = "glpsol"
GLPK_MODEL = {'rev':"rev.mod", 
	      'trans':"trans.mod", 
	      'trans_rev':"trans_rev.mod"}
GLPK_TMP_FILE = TMP_DIR + "tmp.data"
GLPK_OUTFILE = TMP_DIR + "out.data"
GLPK_CMD = "glpsol"


def my_parser(in_argv=sys.argv):
	'''Creates the parser for the options used in tests.'''
	# Getting the program name
	prog_name = os.path.basename(in_argv[0])

	# Creating the parser object
	parser = argparse.ArgumentParser(
		prog=prog_name, add_help=True,
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		description='Run tests for the given program.')

	# Common to all programs
	program_group = parser.add_argument_group('program', 
						  'Input program.')
 	program_group.add_argument(
		'prog', help='program that will run the tests. '+
		'"glpsol" for glpk implementation. '+ 
		'"eclipse" for eclise implementation')
	program_group.add_argument(
		'inst', help='set of instances to run.')
	program_group.add_argument(
		'--timeout', type=int, default=90000,
		help='time limit to run all the tests (in seconds).')

	# Specific options
	sort_group = parser.add_argument_group(
		'sorting', 'Sorting specific options.')
	sort_group.add_argument('--model', choices=MODEL, 
				help='model to run.',
				required=True)
	sort_group.add_argument(
		'--bound', default='def', choices=BOUNDS,
		help='bounds to use with the given model.')
	sort_group.add_argument(
		'--theory', default='ilp', choices=THEORIES,
		help='theory to use with the given model.')

	args = parser.parse_args()

	return dict(prog=args.prog, inst=args.inst, 
		    timeout=args.timeout, model=args.model, 
		    bound=args.bound, theory=args.theory)

def run(args=None):
	'''Run the tests for the given program.'''
	if args == None:
		return 0

	# Creating instance object
	inst = Inst.Inst(args['inst'])

	# Prints some info
	print ">>> prog: " + args['prog']
	print ">>> theory: " + args['theory']
	print ">>> model: " + args['model']
	print ">>> bound: " + args['bound']
	print ">>> timout: " + str(args['timeout'])
	print ">>> inst_file: " + args['inst']

	# Prints the start time
	print ">>> start: " + datetime.now().ctime()
	# Sets the timer
	total_time = 0.0
	proc = Timer.Timer(args['timeout'])
	
	# Creating the output file name
	prog_name = os.path.basename(args['prog'])
	filename = RESULT_DIR + prog_name + "-" 
	filename += args['model'] + "_"
	if (args['theory'] != 'ilp'):
		filename += args['theory'] + "-"
	filename += args['bound'] + "-"
	filename += inst.getInstanceFile()
	print ">>> output file: " + filename

	# Creating the header of output file
	out = open(filename, "w")
	out.write(prog_name+"\n")
	out.write("Model:    "+args['theory']+"\n")
	out.write("Bound:    "+args['bound']+"\n")
	out.write("Instance: "+inst.getInstanceFile())
	out.write("\n\n")

	# running all the instances in the instance input file
	retcode = 0
	L = inst.getContent()
	for item in L:
		print "Remaining Time: %d" % proc.getRemainingTime()
		print "Total Time: %f" % total_time

		if proc.getRemainingTime() <= 0:
			stri = item + " -> Timeout\n"
			out.write(stri)
			break

		# Creating the right command
		if args['prog'] == ECLIPSE:
			op = ECLIPSE_MODEL
			cmd = op[args['theory']][args['model']] 
			cmd += '([' + ','.join(item.split())
			cmd +='], RESULT, ' + args['bound'] + ').'
		elif args['prog'] == GLPK:
			# Create data.tmp file
			entry = item.split()
			lpi = []
			lsigma = []
			for i in range(len(entry)):
				lpi.append("[%d] %d" % 
					   (i+1, int(entry[i])))
				lsigma.append("[%d] %d" % (i+1, i+1))

			pi = ",".join(lpi)
			sigma = ",".join(lsigma)

			tmp_file = open(GLPK_TMP_FILE, "w")
			tmp_file.write("data;\n\n")
			tmp_file.write("param N:= %d;\n\n" % 
				       len(entry))
			tmp_file.write("param UB := %d;\n\n" % 
				       len(entry))
			tmp_file.write("param LB := 0;\n\n")
			tmp_file.write("param Pi := "+pi+";\n\n") 
			tmp_file.write("param Sigma := "+sigma+";\n\n")
			tmp_file.write("end;\n")
			tmp_file.close()

			op = BIN_DIR + GLPK_MODEL[args['model']]
			cmd = GLPK_CMD + ' -m ' + op
			cmd += ' -d ' + GLPK_TMP_FILE
			cmd += ' -o ' + GLPK_OUTFILE
		else: # ILOG
			cmd = args['prog'] + " "
			if args['theory'] != 'ilp': # CP have theory
				cmd += args['theory'] + " "
			cmd += args['model'] + " " + args['bound']
			cmd += ' "' + item + '"'
		print ">>> cmd: " + cmd

		try:
			# Run the correct program
			if args['prog'] == ECLIPSE:
				res = proc.run(ECLIPSE_CMD, cmd,
					       "RESULT = ([0-9]+)",
					       ".*.\(([0-9]+\.[0-9]+)s")
			elif args['prog'] == GLPK:
				res = proc.run(
					target=cmd, 
					result_str="Objective:.*([0-9]+)",
					time_str="Time used:.*([0-9]+\.[0-9]+).*",
					glpk=True, 
					glpk_outfile=GLPK_OUTFILE)

			else: # ILOG
				res = proc.run(cmd)
			
			# adjust the timer
			proc.adjustTimer(res['time'])

			stri = item + " -> R:" 
			stri += str(res['result'])
			stri += " T: %.5f" % res['time']
			out.write(stri+"\n")

			total_time += res['time']
		except UserWarning:
			stri = item + " -> Timeout\n"
			proc.adjustTimer(float(args['timeout']))
			out.write(stri)
			retcode = 1
			break
		except AttributeError as detail:
			print "<ERROR> Error in the following command:"
			print "<ERROR> cmd> " + cmd
			print "<ERROR> Run in a separated terminal"
			print "<ERROR> and try to find the mistake."
			print "<ERROR> Remove the output file."
			print "<ERROR> " + filename
			print "<ERROR> ", detail
			retcode = 1
			break
				
	avertime = total_time / inst.getInstanceQty()
	out.write("Average Time: %.5f\n" % avertime)
	out.write("Total Time: %.5f\n" % total_time)
	out.write("Remaining Time: %d\n" % proc.getRemainingTime())
	out.close()

	return retcode

# main
if __name__ == "__main__":
	# Someone is launching this directly
	# Creating the command line parser
	args = my_parser(sys.argv)

	if args == None:
		exit(1)

	exit(run(args))
#EOF
