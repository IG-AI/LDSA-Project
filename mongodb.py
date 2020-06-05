from load_data import add_songs, parse_songs
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.client = self.create_client()
        self.db = self.client.music
        self.collection1 = self.db.songs
        self.collection2 = self.db.songs2
        self.collection3 = self.db.songs3

    @staticmethod
    def create_client():
        client = MongoClient(host='130.238.29.66', port=27018)
        return client

    def access_text_data(self, amount):
        text = self.collection1.find().limit(amount)
        return text

    def delete_collection(self):
        self.db.drop_collection("songs")
        self.db.drop_collection("songs2")
        self.db.drop_collection("songs3")

    def add_collection(self, directory):
        add_songs(self.collection1, self.collection2, self.collection3, directory)

    def parse_data(self, directory):
        parse_songs(directory)

    def print_collection(self, amount):
        text = self.access_text_data(amount)
        for doc in text:
            print(doc)

    def __del__(self):
        self.client.close()