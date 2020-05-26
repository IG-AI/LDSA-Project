import sys
from bson import Code
from pymongo import MongoClient
from load_data import add_songs


class MongoDataBase:
    def __init__(self):
        self.client = self.create_client()
        self.db = self.client.music
        self.collection = self.db.songs

    @staticmethod
    def create_client():
        client = MongoClient(host='130.238.29.66', port=27018)
        return client

    def analysis_title(self):
        mapper = Code(
            """
            function () {
                var text = this.title
                if (text) {
                    words = text.toLowerCase().split(/[^A-Za-z]/)
                    for(var i = words.length - 1; i >= 0; i--) { 
                            emit(words[i], 1);
                        }
                    }
                }
            };
            """)

        reducer = Code(
            """
            function (key, values) {
                var result = 0;
                for (var i = 0; i < values.length; i++) {
                    result += values[i];
                }
                return result;
            }
            """)

        return self.db.map_reduce(mapper, reducer, "pronouns")

    def delete_collection(self, collection_name="songs"):
        self.collection.drop_collection(collection_name)

    def add_collection(self, dir, max_songs=1000):
        add_songs(self.collection, dir, max_songs)

    def __del__(self):
        self.client.close()


if __name__ == '__main__':
    dir = sys.argv[1]

    MongoDB = MongoDataBase()
    result = MongoDB.analysis_title()
    for doc in result.find():
        print(doc)
