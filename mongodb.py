from load_data import add_songs
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.client = self.create_client()
        self.db = self.client.music
        self.collection = self.db.songs

    @staticmethod
    def create_client():
        client = MongoClient(host='130.238.29.66', port=27018)
        return client

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