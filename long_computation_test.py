#!/usr/bin/env python

from mpi import MPI_SUM, mpi_reduce, mpi_init, mpi_finalize, MPI_COMM_WORLD, mpi_comm_rank, mpi_comm_size, mpi_barrier, \
	mpi_comm_split, mpi_bcast, MPI_INT, MPI_CHAR, MPI_FLOAT

import os

global mydir

from inspect import currentframe, getframeinfo
import time

from program_state_stack import program_state_stack

def f1():

	mpi_init(0, [])
	
	myid = mpi_comm_rank(MPI_COMM_WORLD)
	program_state_stack(locals(), getframeinfo(currentframe()), "my_state.json")
	
	for i in range(2):
		for j in range(2):
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f1_%d_%d_%03d_%03d.txt"%(mydir, i, j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f1_%d_%d_%03d_%03d.txt"%(mydir, i, j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f1_%d_%d_%03d_%03d.txt"%(mydir, i, j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
				a(i,j)
				
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f1_%d_%d_%03d_%03d.txt"%(mydir, i, j, myid, getframeinfo(currentframe()).lineno)
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

	for i in range(2):
		for j in range(2):
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f2_%d_%d_%d_%d_%03d_%03d.txt"%(mydir, x, y, i, j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f2_%d_%d_%d_%d_%03d_%03d.txt"%(mydir, x, y, i, j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f2_%d_%d_%d_%d_%03d_%03d.txt"%(mydir, x, y, i, j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()
			if program_state_stack(locals(), getframeinfo(currentframe())):
				my_s = "%s_f2_%d_%d_%d_%d_%03d_%03d.txt"%(mydir, x, y, i, j, myid, getframeinfo(currentframe()).lineno)
				f = open(my_s, "w")
				f.write(my_s[5:])
				f.flush()
				f.close()


# f1()


def main():
	import sys
	from optparse import OptionParser
	global mydir
	
	progname = os.path.basename(sys.argv[0])
	usage = progname + " dir"
	parser = OptionParser(usage,version="v1")
	# parser.add_option("--ir",		type= "int",   default= 1,                  help="inner radius for rotational correlation > 0 (set to 1)")
	(options, args) = parser.parse_args(sys.argv[1:])
	
	program_state_stack.CCC = int(args[0])
	mydir = args[1]
	
	f1()
	

if __name__ == '__main__':
	main()