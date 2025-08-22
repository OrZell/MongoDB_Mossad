import pymongo.synchronous.cursor
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import nltk

class Processor:

    def __init__(self):
        self.DataFrame = None
        self.Guns = None

    def load_guns_black_list(self):
        with open('weapon_list.txt', 'r') as file:
            all_lines = file.readlines()
        weapons = []
        for line in all_lines:
            weapons.append(line.replace('\n', ''))
        self.Guns = weapons

    def load_to_dataframe(self, tweets:pymongo.synchronous.cursor.Cursor):
        self.DataFrame = pd.DataFrame(list(tweets))

    def col_uncommon_word(self):
        self.DataFrame['rarest_word'] = self.DataFrame['Text'].apply(lambda text: self.count_words(text))

    def col_compound(self):
        self.DataFrame['sentiment'] = self.DataFrame['Text'].apply(lambda text: self.detect_the_compound(text))

    def col_gun(self):
        self.DataFrame['weapons_detected'] = self.DataFrame['Text'].apply(lambda text: self.search_weapon(text))

    def id_col(self):
        self.DataFrame['id'] = self.DataFrame['_id'].apply(lambda id: str(id))

    @staticmethod
    def count_words(words):
        words = words.split()
        words_and_counters = {}

        for word in words:
            if word not in words_and_counters:
                words_and_counters[word] = 0
            words_and_counters[word] += 1

        words_and_counters = sorted(words_and_counters.items(), key= lambda x: x[1])
        return words_and_counters[0][0]

    def detect_the_compound(self, text):
        nltk.download('vader_lexicon')
        compound = SentimentIntensityAnalyzer().polarity_scores(text)['compound']
        str_compound = self.stringing_the_score(compound)
        return str_compound

    @staticmethod
    def stringing_the_score(num:int):
        if 1 >= num >= 0.5:
            return 'positive'
        elif 0.49 >= num >= -0.49:
            return 'neutral'
        else:
            return 'negative'

    def search_weapon(self, text):
        sign = True
        i = 0
        weapon = ''
        while sign and i < len(self.Guns):
            if self.Guns[i] in text:
                weapon = self.Guns[i]
                sign = False
            i += 1
        return weapon

