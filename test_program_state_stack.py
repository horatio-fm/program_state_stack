#!/usr/bin/env python

import os

def GetHashofDirs(directory):
	import hashlib, os
	SHAhash = hashlib.md5()
	if not os.path.exists (directory):
		return -1

	file_set = set()
	file_list = []

	for root, dirs, files in os.walk(directory):
		for names in files:
			# print names
			if names in file_set:
				# print names
				continue
			else:
				file_set.add(names)
			file_list.append(os.path.join(root,names)) 

	## 5 comes from the length of "a/a1/" or "a/a2/" 
	## that precedes the name of the files
	file_list.sort(key=lambda x:x[5:])

	# calculate hash for all files using the 
	# first 4k info from each file
	for filepath in file_list:
		f1 = open(filepath, 'rb')
		while 1:
			buf = f1.read(4096)
			if len(buf) == 0:
				break
			SHAhash.update(hashlib.md5(buf).hexdigest())
		f1.close()
	return SHAhash.hexdigest()


def main():
	import sys
	from optparse import OptionParser

	progname = os.path.basename(sys.argv[0])
	usage = progname + " dir"
	parser = OptionParser(usage,version="v1")
	(options, args) = parser.parse_args(sys.argv[1:])

	myhashes = []

	## there are 84 places were the "long_computation_test.py" program 
	## saves its state; we simulate a program failure in all of them.
	## the program "long_computation_test.py" will "abnormally" exit 
	## when the "program_state_stack" function has been called "counter" times.
	for counter in xrange(2,84):
		os.system("rm -rf a")
		os.system("mkdir -p a/a1")
		os.system("mkdir -p a/a2")
		os.system("rm -f my_state.json ; mpirun --tag-output -np 2 python long_computation_test.py %d a/a1/"%counter)
		os.system("mpirun --tag-output -np 2 python long_computation_test.py 100000 a/a2/")
		myhashes.append(GetHashofDirs("a"))

		sys.stdout.write("%d "%counter + str(len(set(myhashes)) == 1) + " \n")
		sys.stdout.flush()

	print 
	print 
	print len(set(myhashes)) == 1
	print myhashes

main()
