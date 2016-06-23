# This software is issued under a joint BSD/GNU license. You may use the
# source code in this file under either license. However, note that the
# complete EMAN2 and SPARX software packages have some GPL dependencies,
# so you are responsible for compliance with the licenses of these packages
# if you opt to use BSD licensing. The warranty disclaimer below holds
# in either instance.
#
# This complete copyright notice must be included in any revised version of the
# source code. Additional authorship citations may be added, but existing
# author citations must be preserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA



def if_error_then_all_processes_exit_program(error_status):
	import sys, os
	from utilities import print_msg

	if "OMPI_COMM_WORLD_SIZE" not in os.environ:
		def mpi_comm_rank(n): return 0
		def mpi_bcast(*largs):
			return [largs[0]]
		def mpi_finalize():
			return None
		MPI_INT, MPI_COMM_WORLD = 0, 0
	else:
		from mpi import mpi_comm_rank, mpi_bcast, mpi_finalize, MPI_INT, MPI_COMM_WORLD

	myid = mpi_comm_rank(MPI_COMM_WORLD)
	if error_status != None and error_status != 0:
		error_status_info = error_status
		error_status = 1
	else:
		error_status = 0

	error_status = mpi_bcast(error_status, 1, MPI_INT, 0, MPI_COMM_WORLD)
	error_status = int(error_status[0])

	if error_status > 0:
		if myid == 0:
			if type(error_status_info) == type((1,1)):
				if len(error_status_info) == 2:
					frameinfo = error_status_info[1]
					print_msg("***********************************\n")
					print_msg("** Error: %s\n"%error_status_info[0])
					print_msg("***********************************\n")
					print_msg("** Location: %s\n"%(frameinfo.filename + ":" + str(frameinfo.lineno)))
					print_msg("***********************************\n")
		sys.stdout.flush()
		mpi_finalize()
		sys.exit(1)


def store_program_state(filename, state, stack):
	import json
	with open(filename, "w") as fp:
		json.dump(zip(stack, state), fp, indent = 2)
	fp.close()

def restore_program_stack_and_state(file_name_of_saved_state):
	import json; f = open(file_name_of_saved_state, 'r')
	saved_state_and_stack = json.load(f); f.close()
	return list(zip(*saved_state_and_stack)[0]), list(zip(*saved_state_and_stack)[1])


def program_state_stack(full_current_state, frameinfo, file_name_of_saved_state=None, last_call="", force_starting_execution = False):

	"""

	When used it needs: from inspect import currentframe, getframeinfo
	Also: from utilities import program_state_stack

	This function is used for restarting time consuming data processing programs/steps from the last saved point. 

	This static variable must be defined before the first call:
	program_state_stack.PROGRAM_STATE_VARIABLES = {"isac_generation", "i", "j"}
	It contains local variables at any level of the stack that define uniquely the state(flow/logic) of the program.
	
	It is assumed that the processed data is saved at each step and it is independent from the variables that uniquely define 
	the state(flow/logic) of the program. All the variables that are used in more than one step must be calculated before
	the "if program_state_stack(locals(), getframeinfo(currentframe())):" call. It is assumed that they are not time consuming.
	Passing processed data from one step to the next is done only through files. 
	
	First call needs to contain "file_name_of_saved_state".
	Then, the next calls are "if program_state_stack(locals(), getframeinfo(currentframe())):" to demarcate the blocks of 
	processing steps that take a long time (hours/days).
	
	Example of initialization:
	program_state_stack.PROGRAM_STATE_VARIABLES = {"isac_generation", "i", "j"}
	program_state_stack(locals(), getframeinfo(currentframe()), "my_state.json")
	
	Then regular usage in the program:
	
	if program_state_stack(locals(), getframeinfo(currentframe())):
	# if 1:
		pass
	
	"""

	from traceback import extract_stack
	from mpi import mpi_comm_rank, mpi_bcast, MPI_COMM_WORLD, MPI_INT
	
	import os

	def get_current_stack_info():
		return [[x[0], x[2]] for x in extract_stack()[:-2]]

	START_EXECUTING_FALSE = 0
	START_EXECUTING_TRUE = 1
	START_EXECUTING_ONLY_ONE_TIME_THEN_REVERT = 2
	
	# error_status = 1
	# if_error_then_all_processes_exit_program(error_status)
	
	current_state = dict()
	for var in program_state_stack.PROGRAM_STATE_VARIABLES & set(full_current_state) :
		current_state[var] =  full_current_state[var]

	if "restart_location_title" in program_state_stack.__dict__:
		# location_in_program = frameinfo.filename + "___" + program_state_stack.restart_location_title + "___" + last_call
		location_in_program = frameinfo.filename + "___" + program_state_stack.restart_location_title
		del program_state_stack.restart_location_title
	else:
		location_in_program = frameinfo.filename + "___" + str(frameinfo.lineno) + "_" + last_call
		# location_in_program = frameinfo.filename + "___" + last_call
		
	current_state["location_in_program"] = location_in_program
	
	current_stack = get_current_stack_info()

	error_status = 0

	# not a real while, an if with the possibility of jumping with break
	while mpi_comm_rank(MPI_COMM_WORLD) == 0:
		if "file_name_of_saved_state" not in program_state_stack.__dict__:
			if type(file_name_of_saved_state) != type(""):
				print "Must provide the file name of saved state as a string in the first call of the function!"
				error_status = 1
				break

			program_state_stack.file_name_of_saved_state = os.getcwd() + os.sep + file_name_of_saved_state
			program_state_stack.counter = 0
			program_state_stack.track_stack = get_current_stack_info()
			program_state_stack.track_state = [dict() for i in xrange(len(program_state_stack.track_stack))]
			program_state_stack.track_state[-1] = current_state

			if (os.path.exists(file_name_of_saved_state)):
				program_state_stack.saved_stack, \
				program_state_stack.saved_state = restore_program_stack_and_state(file_name_of_saved_state)
				program_state_stack.start_executing = START_EXECUTING_FALSE
			else:
				# check to see if file can be created
				f = open(file_name_of_saved_state, "w"); f.close()
				program_state_stack.start_executing = START_EXECUTING_TRUE
		else:
			program_state_stack.counter += 1
			# print "counter: ", program_state_stack.counter
			# if program_state_stack.counter == program_state_stack.CCC:
			# 	error_status = 1
			# 	break

			if program_state_stack.start_executing == START_EXECUTING_ONLY_ONE_TIME_THEN_REVERT:
				program_state_stack.start_executing = START_EXECUTING_FALSE
			
			# correct track_state to reflect track_stack 
			for i in xrange(len(current_stack)):
				if i < len(program_state_stack.track_state):
					if program_state_stack.track_stack[i] != current_stack[i]:
						program_state_stack.track_state[i] = dict()
				else:
					# print "i:", i, len(program_state_stack.track_state), len(current_stack), current_stack
					program_state_stack.track_state.append(dict())
			program_state_stack.track_state[i] = current_state
			
			# correct track_stack to reflect current_stack
			program_state_stack.track_stack = current_stack
			
			# if program_state_stack.counter == 68:
			# 	print range(len(current_stack), len(program_state_stack.track_state))
				
			# delete additional elements in track_state so that size of track_state is the same as current_stack  				
			program_state_stack.track_state[len(current_stack):len(program_state_stack.track_state)] = []
			
			if program_state_stack.start_executing == START_EXECUTING_TRUE or last_call != "" or force_starting_execution:
				store_program_state(program_state_stack.file_name_of_saved_state, program_state_stack.track_state, current_stack)
				program_state_stack.start_executing = START_EXECUTING_TRUE
			else:
				if len(program_state_stack.saved_state) >= len(current_stack):
					for i in range(len(program_state_stack.saved_state)):
						if i < len(current_stack):
							if program_state_stack.track_stack[i] == current_stack[i]:
								if program_state_stack.track_state[i] == program_state_stack.saved_state[i]:
									continue
							break
						else:
							program_state_stack.start_executing = START_EXECUTING_ONLY_ONE_TIME_THEN_REVERT
							# print "////////////////////////////" 
							# print "Entering function: ", location_in_program
							# print "////////////////////////////"
							break
					else:
						program_state_stack.start_executing = START_EXECUTING_TRUE
						# print "////////////////////////////" 
						# print "Start executing: ", location_in_program
						# print "////////////////////////////"
		break
	else:
		program_state_stack.start_executing = START_EXECUTING_FALSE
		
	if_error_then_all_processes_exit_program(error_status)
		
	program_state_stack.start_executing = mpi_bcast(program_state_stack.start_executing, 1, MPI_INT, 0, MPI_COMM_WORLD)
	program_state_stack.start_executing = int(program_state_stack.start_executing[0])

	# print "program_state_stack.start_executing ", program_state_stack.start_executing

	return program_state_stack.start_executing

def qw(s):
	s = s.replace("\n"," ")
	s = s.replace("\t"," ")
	return tuple(s.split())

