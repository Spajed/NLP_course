import os
import pandas as pd
from enum import Enum
import copy

# Get the path of the relevant data
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(SCRIPT_PATH, '..', 'data', 'Hebrew-NRC-EmoLex.txt')

# open data as a DataFrame
LEXICON_DATA = pd.read_csv(DATA_PATH, delimiter = '\t')

class Sentiment(Enum):
    """
    Sets all possible sentiment values
    """
    POSITIVE = 0
    NEGATIVE = 1
    NEUTRAL = 2

def naive_parse(lexicon_data):
    """
    parse the given lexicon data such will contain only the necessary columns: english_word, hebrew_word, sentiment
    naive parse the data means that only if one of the columns; "positive" , "negative" is on, then the word will non-neutral sentiment.
    Returns:
        lexicon_data (pd.DataFrame): parsed data of english to hebrew sentiment lexicon
    """
    for index, _ in lexicon_data.iterrows():
        if lexicon_data.loc[index, 'positive'] == 1:
            lexicon_data.loc[index, 'sentiment'] = Sentiment.POSITIVE.value
        elif lexicon_data.loc[index,'negative'] == 1:
            lexicon_data.loc[index, 'sentiment'] = Sentiment.NEGATIVE.value
        else:
            lexicon_data.loc[index, 'sentiment'] = Sentiment.NEUTRAL.value
    
    return lexicon_data

def rule_basted_parse(lexicon_data):
    """
    Parse the given lexicon data such will contain only the necessary columns: english_word, hebrew_word, sentiment
    Parse the data based on rules means that eche word will get a score based on the emotions and sentiment columns that are on.
    The score goes as follow: 
    1 positive point for all the emotions: 'anticipation', 'joy', 'surprise', 'trust'.
    5 positive points for the emotion 'positive'
    1 negative point for all the emotions: 'anger', 'disgust', 'fear', 'sadness'
    5 negative points for the emotion 'negative'
    Returns:
        lexicon_data (pd.DataFrame): parsed data of english to hebrew sentiment lexicon
    """
    # positive_points = 0
    # negative_points = 0 
    for index, _ in lexicon_data.iterrows():
        positive_points = lexicon_data.loc[index,'anticipation'] + lexicon_data.loc[index,'joy'] + lexicon_data.loc[index,'surprise'] + lexicon_data.loc[index,'trust'] + (5 * lexicon_data.loc[index,'positive'])
        negative_points = lexicon_data.loc[index,'sadness'] + lexicon_data.loc[index,'fear'] + lexicon_data.loc[index,'disgust'] + lexicon_data.loc[index,'anger'] + (5 * lexicon_data.loc[index,'negative'])
        if positive_points > negative_points:
         lexicon_data.loc[index,'sentiment'] = Sentiment.POSITIVE.value
        elif negative_points > positive_points:
         lexicon_data.loc[index,'sentiment'] = Sentiment.NEGATIVE.value
        else:
         lexicon_data.loc[index,'sentiment'] = Sentiment.NEUTRAL.value
    
    return lexicon_data
    
def parse_data(naive):
    """
    parse the given lexicon data such will contain only the necessary columns: english_word, hebrew_word, sentiment
    Returns:
        lexicon_data (pd.DataFrame): parsed data of english to hebrew sentiment lexicon
    """
    # add a sentiment column based on if the word was tagged "positive" or "negative"
    lexicon_data = LEXICON_DATA
    lexicon_data['sentiment'] = None
    # for index, _ in lexicon_data.iterrows():
    #     if lexicon_data.loc[index, 'positive'] == 1:
    #         lexicon_data.loc[index, 'sentiment'] = Sentiment.POSITIVE.value
    #     elif lexicon_data.loc[index,'negative'] == 1:
    #         lexicon_data.loc[index, 'sentiment'] = Sentiment.NEGATIVE.value
    #     else:
    #         lexicon_data.loc[index, 'sentiment'] = Sentiment.NEUTRAL.value
    if naive:
        lexicon_data = naive_parse(lexicon_data)
    else:
        lexicon_data = rule_basted_parse(lexicon_data)
    # Drop unrelevant columns 
    lexicon_data.drop(columns=['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust'], axis=1, inplace=True)
    # rename all columns with lower case letters
    lexicon_data = lexicon_data.rename(columns={"English Word": "english_word", "Hebrew Word": "hebrew_word"})
    
    return lexicon_data

class SentimentLexicon:
    """
    A class for creating simple use of the sentiment lexicon data.
    Attributes:
        en_he_sentiment_lexicon (Dictionary): sentiment lexicon from english to hebrew
        he_en_sentiment_lexicon (Dictionary): sentiment lexicon from hebrew to english
    """
    def __init__(self, naive=True): 
        """
        initialaze en_he_sentiment_lexicon and he_en_sentiment_lexicon. 

        Args: 
            naive (Bool) if true, parse the data in the naive way, otherwise, use rule based parsing. 
        """
        # Parse data 
        lexicon_data = parse_data(naive)
        # Create dictionary structure from an hebrew to it's translation and sentiment, and the same form an english word.
        self.english_hebrew = {}
        self.hebrew_english = {}
        # keep track of current sentiment and translation of an hebrew word
        hebrew_word_sentiment_count = {Sentiment.POSITIVE: 0, Sentiment.NEGATIVE: 0, Sentiment.NEUTRAL: 0}
        hebrew_word_translation = {Sentiment.POSITIVE: '', Sentiment.NEGATIVE: '', Sentiment.NEUTRAL: ''}
        for index , _ in lexicon_data.iterrows():
            hebrew_word = lexicon_data.loc[index,'hebrew_word']
            english_word = lexicon_data.loc[index,'english_word']
            sentiment = lexicon_data.loc[index,'sentiment']
            # Update he-en lexicon.
            # If a Hebrew word has multiple translations in the lexicon along with conflicting sentiments, then set the sentiment to the one with the greater count in the dictionary for that specific Hebrew word. Additionally, set the translation of the word to be the first English word that matches the Hebrew word, that has the chosen sentiment value.
            # Otherwise, set the hebrew word's translation as the first english word that matches this word in the lexicon. 
            if sentiment == Sentiment.POSITIVE.value:
                    if hebrew_word_translation[Sentiment.POSITIVE] == '':
                        hebrew_word_translation[Sentiment.POSITIVE] = english_word
                    hebrew_word_sentiment_count[Sentiment.POSITIVE] += 1
            elif sentiment == Sentiment.NEGATIVE.value:
                    if hebrew_word_translation[Sentiment.NEGATIVE] == '':
                        hebrew_word_translation[Sentiment.NEGATIVE] = english_word
                    hebrew_word_sentiment_count[Sentiment.NEGATIVE] += 1
            else:
                    if hebrew_word_translation[Sentiment.NEUTRAL] == '':
                        hebrew_word_translation[Sentiment.NEUTRAL] = english_word
                    hebrew_word_sentiment_count[Sentiment.NEUTRAL] += 1
            # If hebrew word is not in the lexicon yet, add new values
            if hebrew_word not in self.hebrew_english:
                 self.hebrew_english[hebrew_word] = {'translation': english_word,  'sentiment': sentiment}
            else:
                 # Find the sentiment with max value
                 # If positive == negative sentiment, assign hebrew word with neutral value
                 max_count_sentiment = ''
                 if hebrew_word_sentiment_count[Sentiment.POSITIVE] == hebrew_word_sentiment_count[Sentiment.NEGATIVE]:
                    max_count_sentiment = Sentiment.NEUTRAL
                 else:
                    max_count_sentiment =  max(hebrew_word_sentiment_count, key=lambda k: hebrew_word_sentiment_count[k])
                # set hebrew word lexicon record with max sentiment value, and the first english translation with the same sentiment value
                 self.hebrew_english[hebrew_word] = {'translation': hebrew_word_translation[max_count_sentiment],  'sentiment': max_count_sentiment.value}
                     
            # # If hebrew word is not in the dictionay, add new values 
            # if hebrew_word not in self.hebrew_english:
            #     self.hebrew_english[hebrew_word] = {'translation': english_word,  'sentiment': sentiment}
            # # Otherwise, set the hebrew word's translation as the first english word that matches this word in the lexicon. 
            # # If the hebrew word has multiple translations in the lexicon, with conflicting sentiments, set sentiment as neutral.
            # else:
            #     if self.hebrew_english[hebrew_word]['sentiment'] != sentiment:
            #         self.hebrew_english[hebrew_word]['sentiment'] = Sentiment.NEUTRAL.value
            
            # Update en-he lexicon.
            # There is an onto function between all english words to hebrew words, so each english word appears once in the lexicon data  
            self.english_hebrew[english_word] = {'translation': hebrew_word,  'sentiment': sentiment}
    
    def hebrew_to_sentiment(self, hebrew_word):
        """
        Converts hebrew word to it's sentiment value. 
        Args: 
            hebrew_word (String): an hebrew word
        Rturnes: 
            sentiment (int): the matching sentiment of the given word. if the word is not found in lexicon, return -1.  
        """
        if hebrew_word not in self.hebrew_english:
            return -1
        return self.hebrew_english[hebrew_word]['sentiment']

    def english_to_sentiment(self, english_word):
        """
        Converts english word to it's sentiment value. 
        Args: 
            english_word (String): an english word
        Rturnes: 
            sentiment (int): the matching sentiment of the given word. if the word is not found in lexicon, return -1.  
        """
        if english_word not in self.english_hebrew:
            return -1
        return self.english_hebrew[english_word]['sentiment']      







