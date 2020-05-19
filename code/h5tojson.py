import json, h5py, sys, os
import hdf5_getters

dir = sys.argv[1]

def dump_file(f):
	f.write(json.dumps(f[x].visit))

for filename in os.listdir(dir):
	filename = dir+filename
	# check all keys
	with h5py.File(filename, "r") as f:
		my_keys_list=list(f.keys())
		for x in my_keys_list:
			print(x)

	# check each keys' values2
	with h5py.File(filename, "r") as f:
		my_keys_list=list(f.keys())
		for x in my_keys_list:
			f.visit(dump_file)
			print(list(f[x]))
			print(type(f[x]))



	# # dump the data into json
	# with open('data.json','a') as f_out:
	# 	 with h5py.File(filename, "r") as f:
	# 			 my_keys_list=list(f.keys())
	# 			 for x in my_keys_list:
	# 					f_out.write(json.dumps(f[x].visit))