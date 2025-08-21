from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

class Processor:

    def __init__(self):
        self.DataFrame = None

    def load_to_dataframe(self, tweets):
        self.DataFrame = pd.DataFrame(list(tweets))

    def col_uncommon_word(self):
        self.DataFrame['uncommon_word'] = self.DataFrame['Text'].apply(lambda text: self.count_words(text))

    def col_compound(self):
        self.DataFrame['compound'] = self.DataFrame['Text'].apply(lambda text: self.detect_the_compound(text))

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

