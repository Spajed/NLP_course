import os 
import sys
import pandas as pd
import re

module_folder_path = os.path.abspath('src\hebrew_sentiment_based_on_pos\src')
sys.path.append(module_folder_path)
from sentiment_translator import SentimentTranslator
from sentiment_lexicon import Sentiment

# open sentiment dataset in UD format
with open("lexicon.csv", 'r', encoding="utf-8") as file:
    sentiment_lexicon = pd.read_csv(file)
sentiment_lexicon['sentiment'] = None

# create new sentiment translator
sentiment_translator = SentimentTranslator(naive=False)
for index, row in sentiment_lexicon.iterrows():
    # print(f"Word number {index}")
    word = sentiment_lexicon.loc[index, 'word']
    upos = sentiment_lexicon.loc[index, 'upos']
    feats = sentiment_lexicon.loc[index, 'feats']
    # get the word sentiment score
    word_sentiment = sentiment_translator.translate(word, upos, feats)
    sentiment_lexicon.loc[index, 'sentiment'] = word_sentiment
    # print(f"Result: {word} {word_sentiment}")

# export results to csv
sentiment_lexicon.to_csv(f"sentiment_lexicon.csv", index = False, encoding = 'utf-8-sig')

