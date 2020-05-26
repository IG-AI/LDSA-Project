import json, sys, os
import hdf5_getters
from pymongo import MongoClient


client = MongoClient(host='130.238.29.66', port=27018)
db = client.music
collection = db.songs
print('mongo client: ', client)
print('mongo db: ', db)
print('mongo collection: ', collection)




dir = sys.argv[1]
print('loading data from directory: ' + dir)

MAX_SONGS = 1000
count = 0
def add_songs(directory):
  global count
  global MAX_SONGS
  for filename in os.listdir(directory):
    if count >= MAX_SONGS: return
    file_path = os.path.join(directory, filename)
    if os.path.isdir(file_path):
        add_songs(file_path)
    else:
      count += 1
      if count % 100 == 0: print('loaded ' + str(count) + ' songs')

      with hdf5_getters.open_h5_file_read(file_path) as h5:
        for i in range(hdf5_getters.get_num_songs(h5)):
          title = hdf5_getters.get_title(h5, i)
          year = hdf5_getters.get_year(h5, i)
          danceability = hdf5_getters.get_danceability(h5, i)
          song = {
            'title': str(title),
            'year': int(year),
            'danceability': float(danceability)
          }
          collection.insert_one(song)

add_songs(dir)
