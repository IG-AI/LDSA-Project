import os, json
import hdf5_getters

count = 0
MAX_SONGS = 1000000
def parse_songs(directory):
    global count
    global MAX_SONGS
    for filename in os.listdir(directory):
        if count >= MAX_SONGS: return
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            parse_songs(file_path)
        else:
            count += 1
            if count % 100 == 0: print('Parsed ' + str(count) + ' songs')

            with hdf5_getters.open_h5_file_read(file_path) as h5:
                for i in range(hdf5_getters.get_num_songs(h5)):
                    title = hdf5_getters.get_title(h5, i).decode('UTF-8')
                    year = hdf5_getters.get_year(h5, i).item()
                    danceability = hdf5_getters.get_danceability(h5, i).item()
                    tags = hdf5_getters.get_artist_mbtags(h5, i).tolist()
                    genres = [tag.decode('UTF-8') for tag in tags]
                    tempo = hdf5_getters.get_tempo(h5, i).item()
                    
                    song = {
                        'title': title,
                        'year': year,
                        'danceability': danceability,
                        'genres': genres,
                        'tempo': tempo
                    }
                    song = os.path.splitext(filename)
                    with open("/home/ubuntu/million_songs/parsed_data/" + song[0] + '.json', 'w') as fp:
                        json.dump(song, fp)

def add_songs(collection1, collection2, collection3, directory):
    i = 0
    for filename in os.listdir(directory):
        i += 1
        if i % 100 == 0: print('Loaded ' + str(i) + ' songs')
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as f:
            collection1.insert_one(f)

            for i in range(2):
                collection2.insert_one(f)

            for i in range(3):
                collection3.insert_one(f)
