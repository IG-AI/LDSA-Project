import sys
from bson import Code
from pymongo import MongoClient
from load_data import add_songs
from numpy import sort


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
                    words = text.toLowerCase().split(" ")
                    for(var i = words.length - 1; i >= 0; i--) {
                        emit(words[i].replace(/[&\/\\#,+()$~%.'":*?<>{}]/g, ''), 1);
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

        return self.collection.map_reduce(mapper, reducer, "title_result")

    def access_text_data(self, amount):
        tweets_text = self.collection.find().limit(amount)
        return tweets_text

    def delete_collection(self, collection_name="songs"):
        self.db.drop_collection(collection_name)

    def add_collection(self, directory):
        add_songs(self.collection, directory)

    def print_collection(self, amount):
        text = self.access_text_data(amount)
        for doc in text:
            print(doc)

    def __del__(self):
        self.client.close()


def print_map_reduce(collection, key, amount):
    for doc in collection.find().sort(key, -1).limit(amount):
        print(doc)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        
    MongoDB = MongoDataBase()

    # MongoDB.delete_collection()
    # MongoDB.add_collection(directory)

    # MongoDB.print_collection(1000)

    result = MongoDB.analysis_title()
    print_map_reduce(result, "value", 10)
