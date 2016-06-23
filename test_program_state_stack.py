#!/usr/bin/env python

import os

def GetHashofDirs(directory, verbose=0):
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

	file_list.sort(key=lambda x:x[5:])
	
	# print file_list
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
	# parser.add_option("--ir",		type= "int",   default= 1,                  help="inner radius for rotational correlation > 0 (set to 1)")
	(options, args) = parser.parse_args(sys.argv[1:])
	
	
	myhashes = []
	for counter in xrange(2,84):
	# for counter in [5]:
	# for counter in [82]:
		os.system("rm -rf a")
		os.system("mkdir -p a/a1")
		os.system("mkdir -p a/a2")
		os.system("rm my_state.json ; mpirun -np 2 python long_computation_test.py %d a/a1/"%counter)
		os.system("mpirun -np 2 python long_computation_test.py 100000 a/a2/")
		myhashes.append(GetHashofDirs("a"))
		
		sys.stdout.write("%d "%counter + str(len(set(myhashes)) == 1) + " ")
		sys.stdout.flush()
		
	print 
	print 
	print 
	print len(set(myhashes)) == 1
	print myhashes

main()
