import sys, os
import hdf5_getters
from pymongo import MongoClient

count = 0
MAX_SONGS = 1000

def add_songs(collection, directory):
    global count
    global MAX_SONGS
    for filename in os.listdir(directory):
        if count >= MAX_SONGS: return
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            add_songs(collection, file_path)
        else:
            count += 1
            if count % 100 == 0: print('Loaded ' + str(count) + ' songs')

            with hdf5_getters.open_h5_file_read(file_path) as h5:
                for i in range(hdf5_getters.get_num_songs(h5)):
                    title = hdf5_getters.get_title(h5, i).decode('UTF-8')
                    year = hdf5_getters.get_year(h5, i).item()
                    danceability = hdf5_getters.get_danceability(h5, i).item()
                    song = {
                        'title': title,
                        'year': year,
                        'danceability': danceability
                    }
                    collection.insert_one(song)


if __name__ == '__main__':
    dir = sys.argv[1]

    client = MongoClient(host='130.238.29.66', port=27018)
    db = client.music
    collection = db.songs
    print('Mongo client: ', client)
    print('Mongo db: ', db)
    print('Mongo collection: ', collection)

    print('Loading data from directory: ' + dir)
    add_songs(collection, dir)
