import json, sys, os
import hdf5_getters



dir = sys.argv[1]

songs = []
def add_songs(directory):
  for filename in os.listdir(directory):
    file_path = os.path.join(dir, filename)
    if os.path.isdir(file_path): add_songs(file_path)
    else:
      print(file_path)
      h5 = hdf5_getters.open_h5_file_read(file_path)
      titles_list = []
      for i in range(hdf5_getters.get_num_songs(h5)):
        title = hdf5_getters.get_title(h5, i)
        year = hdf5_getters.get_year(h5, i)
        danceability = hdf5_getters.get_danceability(h5, i)
        songs.append({
          'title': str(title),
          'year': int(year),
          'danceability': float(danceability)
        })
add_songs(dir)
print(songs)

"""
for filename in os.listdir(dir):
  filename = os.path.join(dir, filename)
  if os.is_dir(filename):

  h5 = hdf5_getters.open_h5_file_read(filename)
  titles_list = []
  for i in range(hdf5_getters.get_num_songs(h5)):
    title = hdf5_getters.get_title(h5, i)
    titles_list.append(str(title))
  print(titles_list)

  filename_json = filename.split('.')
  print(filename_json)
  with open(filename_json[0]+".json", 'a') as f_out:
      f_out.write(json.dumps(titles_list))
      """
