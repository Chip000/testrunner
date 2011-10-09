# -*- coding:utf-8 -*-

import time
import signal
import subprocess
import os
import re

class Timer(object):
	"Class representing a Timer"

	_runTime = 0
	_delta = float(0)
	_curr_proc = None

	def __init__(self, seconds):
		# Setting the timer
		self._runTime = seconds
		self._delta = float(0)
		self._curr_proc = None
		return

	def handler(self, signum, frame):
		"Handler for SIGALRM"
		if (self._curr_proc != None):
			if (self._curr_proc.pid != 0):
				os.kill(self._curr_proc.pid, 9)
				os.wait()
			raise UserWarning("Time Out")
		return

	def run(self, target=None, cmd=None, 
		result_str="Optimal value: ([0-9]+)",
		time_str="Total Time: ([0-9]+\.[0-9]+)",
		glpk=False, glpk_outfile=""):
		"Run the target. Returns the result and time"
		# creating process
		fd = subprocess.Popen(target, shell=True,
				      stdin=subprocess.PIPE, 
				      stdout=subprocess.PIPE, 
				      stderr=subprocess.PIPE)

		# setting the process id
		self._curr_proc = fd

		# setting the handler and the time
		signal.signal(signal.SIGALRM, self.handler)
		signal.alarm(self._runTime)

		# running the target
		(fd_stdout, fd_stderr) = fd.communicate(cmd)

		# the process ended successfully
		signal.alarm(0)
		self._curr_proc = None

		# extracting the result
		if glpk == False:
			res = re.search(result_str,	
					fd_stdout).group(1)
		else:
			glpkfile = open(glpk_outfile, "r")
			for line in glpkfile:
				find = re.search(result_str,	
						 line)
				if find != None:
					res = find.group(1)
					break
			glpkfile.close()

		time_str = re.search(time_str,
				     fd_stdout).group(1)
		
		return dict(result=res, time=float(time_str))


	def adjustTimer(self, elapsed=0.0):
		"adjust the timer with elapsed time"
		if elapsed.is_integer():
			self._runTime -= int(elapsed)
		else:
			i_part = int(elapsed)
			self._runTime -= i_part
			self._delta += elapsed - i_part
		if self._delta >= 1:
			if self._delta.is_integer():
				self._runTime -= int(self._delta)
				self._delta = float(0)
			else:
				i_part = int(self._delta)
				self._runTime -= i_part
				self._delta -=  i_part
		return

	def getRemainingTime(self):
		return self._runTime

	def getDelta(self):
		return self._delta

	def getCurrPid(self):
		return self._curr_proc.pid
