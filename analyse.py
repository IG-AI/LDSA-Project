from bson import Code
from pymongo import MongoClient


class MongoDataBase:
    def __init__(self):
        self.client = self.create_client()
        self.twitter_db = self.client["music"]
        self.twitter_collection = self.twitter_db["songs"]

    @staticmethod
    def create_client():
        client = MongoClient("mongodb://130.239.29.66:27018/")
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

        return self.twitter_collection.map_reduce(mapper, reducer, "pronouns")

    def delete_collection(self, collection_name="twitter_collection"):
        self.twitter_db.drop_collection(collection_name)

    def delete_database(self, db_name="twitter_db"):
        self.client.drop_database(db_name)

    def __del__(self):
        self.client.close()


if __name__ == '__main__':
    MongoDB = MongoDataBase()
    result = MongoDB.analysis_title()
    for doc in result.find():
        print(doc)
