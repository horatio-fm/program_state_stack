#!/usr/bin/env python

import os
from mpi import mpi_init, mpi_finalize, MPI_COMM_WORLD, mpi_comm_rank
from inspect import currentframe, getframeinfo
from program_state_stack import program_state_stack

global mydir

def f1():

	myid = mpi_comm_rank(MPI_COMM_WORLD)
	program_state_stack(locals(), getframeinfo(currentframe()), "my_state.json")

	for local_var_i in range(2):
		for local_var_j in range(2):
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f1_%d_%d_%03d_%03d.txt"%(mydir, local_var_i, local_var_j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f1_%d_%d_%03d_%03d.txt"%(mydir, local_var_i, local_var_j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f1_%d_%d_%03d_%03d.txt"%(mydir, local_var_i, local_var_j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
				a(local_var_i,local_var_j)
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f1_%d_%d_%03d_%03d.txt"%(mydir, local_var_i, local_var_j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()

	program_state_stack(locals(), getframeinfo(currentframe()), last_call="LastCall")

	mpi_finalize()

def b(x,y):
	f2(x,y)

def a(x,y):
	b(x,y)

def f2(x,y):

	myid = mpi_comm_rank(MPI_COMM_WORLD)

	for local_var_h in range(2):
		for local_var_g in range(2):
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f2_%d_%d_%d_%d_%03d_%03d.txt"%(mydir, x, y, local_var_h, local_var_g, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f2_%d_%d_%d_%d_%03d_%03d.txt"%(mydir, x, y, local_var_h, local_var_g, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f2_%d_%d_%d_%d_%03d_%03d.txt"%(mydir, x, y, local_var_h, local_var_g, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f2_%d_%d_%d_%d_%03d_%03d.txt"%(mydir, x, y, local_var_h, local_var_g, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()

def main():
	import sys
	from optparse import OptionParser
	global mydir

	progname = os.path.basename(sys.argv[0])
	usage = progname + " dir"
	parser = OptionParser(usage,version="v1")
	(options, args) = parser.parse_args(sys.argv[1:])

	program_state_stack.PROGRAM_STATE_VARIABLES = \
		{"local_var_i", "local_var_j", "local_var_h", "local_var_g"}

	program_state_stack.CCC = int(args[0])

	mydir = args[1]

	mpi_init(0, [])

	f1()


if __name__ == '__main__':
	main()