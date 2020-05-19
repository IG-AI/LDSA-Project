import json, sys, os
import hdf5_getters

dir = sys.argv[1]

for filename in os.listdir(dir):
	filename = dir+filename
	h5 = hdf5_getters.open_h5_file_read(filename)
	titles_list = []
	for i in range(hdf5_getters.get_num_songs(h5)):
		title = hdf5_getters.get_title(h5, i)
		titles_list.append(str(title))

	filename_json = filename.split('.')
	with open(filename_json[0]+".json", 'a') as f_out:
			f_out.write(json.dumps(titles_list))