
from pymongo import MongoClient
from gridfs import GridFS
import io

client = MongoClient(host='130.238.29.66',port=27018)
db = client.test_database
fs = GridFS(db)

f = io.FileIO('data/TRAAABD128F429CF47.h5', 'r')
fid = fs.put(f)
print(fs.get(fid).read())
f.close()
