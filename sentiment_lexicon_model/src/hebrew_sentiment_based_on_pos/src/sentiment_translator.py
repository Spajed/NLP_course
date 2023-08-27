import pos_translator
import sentiment_lexicon
import os
import pandas as pd

class SentimentTranslator:
    """
    A class for assigning sentiment value to a single hebrew word based on the sentiment assigned to it's most accurate translation in english. the most accurate translation of an hebrew word is calculated with the class POSTranslator using a dictionary and Universal Dependencies POS tags and features.

    Attributes:
        sentiment_lexicon (SentimentLexicon): sentiment lexicon from hebrew to english and from english to hebrew.
        pos_translator (POSTranslator): Translator from hebrew to english using Universal Dependencies tags and features. 

    """
    def __init__(self, naive=True):
        """
        Initialize sentiment_lexicon and pos_translator
        """
        self.sentiment_lexicon = sentiment_lexicon.SentimentLexicon(naive)
        self.pos_translator = pos_translator.POSTranslator()
    
    def translate(self, word, upos, feats):
        """
        Assign sentiment value to a single hebrew word. 
        
        Args: 
            word (String): An hebrew word.
            translation_record (Dictionary): All attributes of a single potential translation of a word.
            upos (String): Universal Dependencies tag of a given word.
            feats (String): Universal Dependencies features of a given word.
        
        Returns: 
            sentiment (Int): sentiment value for the word.
            If word could to be translated, a neutral sentiment value is assigned. 
        """
        # translate hebrew word to english word
        translation_word = self.pos_translator.translate(word, upos, feats)
        sentiment = sentiment_lexicon.Sentiment.NEUTRAL.value
        # If word is not in dictionary, check if it's in sentiment lexicon
        if translation_word == -1: 
            # If word is not in sentiment lexicon, assign neutral sentiment
            if word in self.sentiment_lexicon.hebrew_english:
                sentiment =  self.sentiment_lexicon.hebrew_english[word]['sentiment']
            else:
                sentiment = sentiment_lexicon.Sentiment.NEUTRAL.value
        else: 
            # If translation_word is not in sentiment lexicon, check in hebrew word in sentiment lexicon
            if translation_word in self.sentiment_lexicon.english_hebrew:
                sentiment = self.sentiment_lexicon.english_hebrew[translation_word]['sentiment']
            else: 
                # If word is not in sentiment lexicon, assign neutral sentiment
                if word in self.sentiment_lexicon.hebrew_english:
                    sentiment =  self.sentiment_lexicon.hebrew_english[word]['sentiment']
                else:
                    sentiment = sentiment_lexicon.Sentiment.NEUTRAL.value
        
        return sentiment






