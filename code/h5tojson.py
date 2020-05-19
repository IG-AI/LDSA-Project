import json, sys, os
import hdf5_getters

dir = sys.argv[1]

for filename in os.listdir(dir):
	filename = dir+filename
	print(filename)
	h5 = hdf5_getters.open_h5_file_read(filename)
	titles = hdf5_getters.get_title(h5)
	print(titles)

	with open('data.json', 'a') as f_out:
		f_out.write(json.dumps(str(titles)))