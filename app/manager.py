from fetcher import Fetcher
from processor import Processor
import json

class Manager:

    def __init__(self):
        self.Fetcher = Fetcher()
        self.Processor = Processor()
        self.Cursor = None
        self.DataFrame = None

    def fetch(self):
        self.Fetcher.open_connection()
        self.Fetcher.identify_collection()
        self.Cursor = self.Fetcher.fetch_all()

    def process(self):
        self.Processor.load_to_dataframe(self.Cursor)
        self.Fetcher.close_connection()
        self.Processor.load_guns_black_list()
        self.Processor.col_uncommon_word()
        self.Processor.col_compound()
        self.Processor.col_gun()
        self.Processor.id_col()
        self.DataFrame = self.Processor.DataFrame

    def rename_cols(self):
        self.DataFrame.rename(columns={'Text': 'original_text'}, inplace=True)
        self.DataFrame.drop('TweetID', axis=1, inplace=True)
        self.DataFrame.drop('_id', axis=1, inplace=True)

    def reorder_cols(self):
        self.DataFrame = self.DataFrame[['id', 'original_text', 'rarest_word', 'sentiment', 'weapons_detected']]

    def convert_to_json(self):
        # self.DataFrame = self.DataFrame.to_dict(orient='records')
        lst = []
        for row in range(len(self.DataFrame)):
            lst.append(dict(self.DataFrame.loc[row]))
        return lst

    def get_data(self):
        # result = self.convert_to_json()
        # return json.dumps(result, indent=4)
        return self.convert_to_json()

    def run(self):
        self.fetch()
        self.process()
        self.rename_cols()
        self.reorder_cols()
        self.convert_to_json()