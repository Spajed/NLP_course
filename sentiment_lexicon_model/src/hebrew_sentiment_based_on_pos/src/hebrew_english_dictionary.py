import os
import json
import pandas as pd

# Get the path of the relevant data
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(SCRIPT_PATH, '..', 'data', 'dict-he-en.json')

# open data as a Json file
with open(DATA_PATH, 'r') as DICTIONARY_DATA:
    DICTIONARY_DATA =  json.load(DICTIONARY_DATA)

def parse_data():
    """
    parse the given dictionary data such that each hebrew word will hold all it's possible tanslations in the dictionary.
    
    Returns:
        hebrew_english_dictionary (Dictionary): dictionary with hebrew words as keys, and list of all possible translations as values
    """
    hebrew_english_dictionary = {}
    for translation in DICTIONARY_DATA:
        translated_word = translation['translated']
        if translated_word not in hebrew_english_dictionary:
            hebrew_english_dictionary[translated_word] = []
        hebrew_english_dictionary[translated_word].append(translation)

    return hebrew_english_dictionary

class HebrewEnglishDictionary:
    """
    A class for creating simple use of the hebrew-english dictionary data. 
    
    Attributes:
        dictionary (Dictionary): Dictionary with hebrew words as keys, and list of all translation records as values.
    """
    def __init__(self): 
        """
        initialaze dictionary
        """
        self.dictionary = parse_data()
    
    def get_translation_records(self, word):
        """
        Gets all translation records of an hebrew word. 

        Args:
            word (String): An hebrew word.
        Returns: 
            translation_records (List): A list of all translation records that correspond to the provided word.
            If a word is not found in the dictionary, return -1.  
        """
        if word not in self.dictionary:
            return -1
        
        return self.dictionary[word]

    
    def get_items(self, word, item_type):
         """
        Gets all items values of a specific item_type that match a Hebrew word.

        Args: 
        word (String): An hebrew word
        item_type (String): Type of dictionary record item.
        
        Returns: 
        items (Dictionary): Return a dictionary with record ids as keys and lists of possible item values as values. 
        If a word is not found in the dictionary, return -1.        
        """
         if word not in self.dictionary:
             return -1 
         items = {}
         for record in self.dictionary[word]:
             items[record["id"]] = record[item_type]
        
         return items
    
    def get_translations(self, word):
        """
        Gets all translations that match a Hebrew word.

        Args: 
        word (String): An hebrew word

        Returns: 
        items (Dictionary): Return a dictionary with record ids as keys and lists translations as values. 
        If a word is not found in the dictionary, return -1.       
        """
        return self.get_items(word, "translation")
    
    def get_poss(self, word):
        """
        Gets all POSs that match a hebrew word.

        Args: 
        word (String): An hebrew word

        Returns: 
        items (Dictionary): Return a dictionary with record ids as keys and lists of POSs as values. 
        If a word is not found in the dictionary, return -1.    
        """
        return self.get_items(word, "part_of_speech")

# dict = HebrewEnglishDictionary()
# get = dict.get_translation_records('בְּ')
# print(get)

