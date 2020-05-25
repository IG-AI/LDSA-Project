import sys, io, os
from pymongo import MongoClient
from gridfs import GridFS


dir = sys.argv[1]

client = MongoClient(host='130.238.29.66', port=27018)
db = client.test_database
fs = GridFS(db)

for filename in os.listdir(dir):
    filename = dir + filename
    f = io.FileIO(filename, 'r')
    fid = fs.put(f)
    f.close()

print("Folowing files has been loaded in to the server: {}".format(fs.list()))
