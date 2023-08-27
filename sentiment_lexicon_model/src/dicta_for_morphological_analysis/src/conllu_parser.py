import os
import conllu 
from io import open
import copy
import pandas as pd

# Get the path of the relevant data
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(SCRIPT_PATH, '..', 'data', 'trimmed.csv')

# open data
data = open(DATA_PATH, "r", encoding="utf-8")

class ConlluParser: 
    """
    A class for working with a sentence in conllu format

    Attributes: 
    sentence (conllu.models.TokenList): a conllu.models.TokenList sentence
    count_tokens (Int): number of tokens in a sentence
    current_token (Int) marks the currenct token index 
    """
    def __init__(self, sentence_string):
        """
        Initialize sentence, count_tokens and current_token
        """
        self.sentence = conllu.parse(sentence_string)[0]
        self.count_tokens = len(self.sentence)
        self.current_token = -1
    
    def __iter__(self):
        return self.sentence
    
    def __next__(self):
        self.current_token += 1
        if self.current_token < self.count_tokens:
            return self.current_token
        else: 
            raise StopIteration
        
    
    def to_sentence(self, token_list):
        """
        Converts conllu.models.TokenList to a string sentence

        Returns:
        sentence (String): the sentence composing the token list.
        if there is no metadata, return -1  

        """
        if len(token_list.metadata) == 0:
            return -1 
        sentence = copy.deepcopy(token_list.metadata['text'])
        return sentence

    def get_metadata(self):
        """
        Gets a sentence's metadata. 
        Side effect: returns pointer to data
        """
        return self.sentence.metadata

    def get_token_value(self, token_index, key):
        """
        Gets the value of a token in a specific index, that matches the key.
        If key not in dictionary, return -1 
        Side effect: returns actual pointer to data
        """
        if key not in self.sentence[token_index] or self.sentence[token_index][key] == None:
            return -1 
        return self.sentence[token_index][key]
    
    def insert_token_value(self, token_index, key, value):
        """
        Add a value to a given key of a token in a specific index
        """
        self.sentence[token_index][key] = value
    
    def insert_sentence_value(self, key, value):
        """
        Add a value to a given key, in the sentence metadata 
        """
        self.sentence.metadata[key] = value

    
    

    
# conllu_data = ConlluParser(DATA_PATH)
# cunllu_df = pd.DataFrame(conllu_data.to_sentences(), columns=['sentence'])
# cunllu_df.to_csv('hebrew_corpus_sentences_only.csv', index = False, encoding = 'utf-8-sig')
# file_path = os.path.join(SCRIPT_PATH, '..', 'data\dicta_hebrew_corpus_raw', 'morph_normal_name2.tsv')
# conllu_data_format = ConlluParser(file_path)