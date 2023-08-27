import os 
import sys
import pandas as pd
import re

module_folder_path = os.path.abspath('src\dicta_for_morphological_analysis\src')
sys.path.append(module_folder_path)
import dicta_api_utils as dicta
from conllu_parser import ConlluParser

module_folder_path = os.path.abspath('src\hebrew_sentiment_based_on_pos\src')
sys.path.append(module_folder_path)
from sentiment_translator import SentimentTranslator
from sentiment_lexicon import Sentiment

# open sentiment files
script_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_path, 'data', 'train.csv')
with open(data_path, 'r', encoding="utf-8") as file:
    train_file = pd.read_csv(file)
data_path = os.path.join(script_path, 'data', 'test_gold.csv')
with open(data_path, 'r', encoding="utf-8") as file:
    test_file = pd.read_csv(file)
data_path = os.path.join(script_path, 'data', 'dev.csv')
with open(data_path, 'r', encoding="utf-8") as file:
    dev_file = pd.read_csv(file)

# open file to save sentiment sentences in UD format
current_file = (dev_file,"dev")
sentiment_ud_format_file = open(f"sentiment_in_UD_format_{current_file[1]}.txt", 'a', encoding="utf-8")

def remove_punctuation(sentence):
    """
    Remove all panctuation marks from the middle of a sentence 
    """
    sentence = re.sub(r'\!|\״|\#|\$|\%|\&|\'|\(|\)|\|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~|\'|\:|\'|\"', '',sentence)
    return sentence

def parse_feats(feats):
    """
    parse feats to match the formt needed for SentimentTranslator.

    Args:
        feats (Dictionary): a dictionary with UD features
    Returns:
        feats_string (String): A concatenates string of featurs, that is needed for the use of SentimentTranslator.  
    """
    feats_string = ''
    for key, value in feats.items():
        feats_string = feats_string + '|' + f"{key}={value}"
    
    feats_string = feats_string[1:]
    return feats_string

def get_sentence_sentiment_score(conllu_sentence, sentimet_translator):
    """
    Get sentiment score for sentence in conllu format

    Args:
    conllu_sentence (ConlluParser): Sentence in onllu format

    Returns: 
    A sentiment score for sentence
    """
    positive_count = 0
    negative_count = 0
    total_number_of_words = conllu_sentence.count_tokens
    # calculate sentiment score for each of the tokens in the dataset
    for i in range(conllu_sentence.count_tokens):
        print(f"sentiment score iteartion: {i}")
        word = conllu_sentence.get_token_value(i, 'lemma')
        upos = conllu_sentence.get_token_value(i, 'upos')
        feats = conllu_sentence.get_token_value(i, 'feats')
        if feats == -1: 
            feats = '_'
        else: 
            feats = parse_feats(feats)
        word_sentiment = sentimet_translator.translate(word, upos, feats)
        if word_sentiment == 0:
            positive_count += 1
        elif word_sentiment == 1:
            negative_count += 1
    
    sentiment_score = (positive_count - negative_count) / total_number_of_words
    if sentiment_score < 0:
        return Sentiment.NEGATIVE.value
    elif sentiment_score > 0:
        return Sentiment.POSITIVE.value
    else: 
        return Sentiment.NEUTRAL.value
    

# open new  data frame for results 
model_results = pd.DataFrame(columns=['sentence', 'sentiment', 'model_sentiment'])

# for each sentence in dataset
sentimet_translator = SentimentTranslator(False)
for index, row in current_file[0].iterrows():
    print(f"sentence number: {index}")
    sentence = current_file[0].loc[index, 'comment']
    sentiment = current_file[0].loc[index, 'label']
    # remove punctuation
    sentence= remove_punctuation(sentence)
    print(f"sentence : {sentence}")
    # open dicta request
    ud_sentence = dicta.dicta_request(sentence)
    # convert to conluu format
    conllu_sentence = ConlluParser(ud_sentence)
    # get sentiment score
    sentiment_score = get_sentence_sentiment_score(conllu_sentence, sentimet_translator)
    new_row = [sentence, current_file[0].loc[index, 'label'], sentiment_score]
    model_results.loc[len(model_results)] = new_row

    # export sentiment sentence in UD format
    conllu_sentence.insert_sentence_value('sentiment', str(sentiment))
    sentiment_ud_format_file.write(conllu_sentence.sentence.serialize())


# model_results.to_csv(f"model_results2.csv", index = False, encoding = 'utf-8-sig')

# sentence = train_file.loc[0, 'sentence']
# # remove punctuation
# sentence= remove_punctuation(sentence)
# # open dicta request
# ud_sentence = dicta.dicta_request(sentence)
# print(repr(ud_sentence))
# # convert to conluu format
# conllu_sentence = ConlluParser(ud_sentence)
# print(repr(conllu_sentence.sentence[1]))
# print(parse_feats(conllu_sentence.sentence[1]['feats']))

# print(conllu_sentence.sentence)
# for i in range(conllu_sentence.count_tokens):
#     print(i)
#     print(conllu_sentence.get_token_value(i, 'lemma'))
#     print(conllu_sentence.get_token_value(i, 'upos'))
#     feats = conllu_sentence.get_token_value(i, 'feats')
#     if feats == -1: 
#         print('_')
#     else: 
#         print(parse_feats(feats))














