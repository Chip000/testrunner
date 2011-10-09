# -*- coding:utf-8 -*-
import os

class Inst(object):
	"Class representing the instance problem"

	# instance file
	_inst = ""

	def __init__(self, file_instance=""):
		self._inst = file_instance
		return

	def setInstanceFile(self, file_instance=""):
		"Set the instance file name"
		self._inst = file_instance
		return

	def getInstanceFile(self):
		"Return the instance file name"
		return os.path.basename(self._inst)

	def getContent(self):
		"Return a list with the content of instance file"
		file_instance = open(self._inst, "r")

		_L = []
		for item in file_instance:
			_L.append(item[0:-1])

		file_instance.close()

		return _L

	def getInstanceQty(self):
		"Return the number of instances"
		file_instance = open(self._inst, "r")

		_count = 0
		for item in file_instance:
			_count += 1

		file_instance.close()

		return _count
