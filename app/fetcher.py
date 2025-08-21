from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import os


class Fetcher:

    def __init__(self):
        load_dotenv(find_dotenv())
        self.User = os.getenv('PROJECT_MONGODB_USER')
        self.Password = os.getenv('PROJECT_MONGODB_PASSWORD')
        self.Database = os.getenv('PROJECT_MONGODB_DATABASE')
        self.Connection_String = os.getenv('PROJECT_MONGODB_CONNECTION_STRING')
        self.Collection = None
        self.connection = None

    def open_connection(self):
        if self.connection is None:
            self.connection = MongoClient(self.Connection_String)

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def identify_collection(self):
        self.Collection = self.connection[self.Database].list_collections().to_list()[0]['name']

    def fetch_all(self):
        return self.connection[self.Database][self.Collection].find()

    def convert_to_dataframe(self, documents):
        return pd.DataFrame(list(documents))