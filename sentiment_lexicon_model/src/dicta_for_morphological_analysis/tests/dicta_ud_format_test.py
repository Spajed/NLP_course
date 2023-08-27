import os 
import sys
import pandas as pd
import re
import conllu

module_folder_path = os.path.abspath('src\dicta_for_morphological_analysis\src')
sys.path.append(module_folder_path)
import dicta_api_utils as dicta
from conllu_parser import ConlluParser

# open a file in ud-conllu format for comparison
data_path = os.path.abspath(os.path.join('src\dicta_for_morphological_analysis\data', 'trimmed.csv'))
hebrew_corpus =  open(data_path, 'r', encoding="utf-8")
hebrew_corpus = conllu.parse_incr(hebrew_corpus)

def print_token_list_morph_analysis(token_list, source_name):
    print(f"{source_name} morphological analysis")
    for i in range(len(token_list)):
        if type(token_list[i]['id']) == tuple:
            continue
        print(f"{token_list[i]['id']} {token_list[i]} {token_list[i]['upos']}")

def combine_token_lists(token_lists):
    """
    correct indexes for sentence with multiple token lists 
    """
    # find the last id in the first token list, and add 1 to it 
    current_index = len(token_lists[0]) + 1
    # change index to all tokens in the next token lists, and add this token to the first token list
    for i in range(1,len(token_lists)):
        for token in range(len(token_lists[i])):
            token_lists[i][token]['id'] = current_index
            current_index += 1
    
def remove_composed_tokens(token_list):
    """
    remove all "continues" tokens from token list (with id type: int-int)
    """
    current_length = len(token_list)
    i = 0 
    while i < current_length:
        if type(token_list[i]['id']) == tuple:
            del token_list[i]
            current_length -= 1
        else:
            i += 1

def remove_punctuation_tags(token_list):
    """
    remove all tokens that has a PUNCT tag
    """
    current_length = len(token_list)
    i = 0 
    while i < current_length:
        if token_list[i]['upos'] == 'PUNCT':
            del token_list[i]
            current_length -= 1
        else:
            i += 1
    # correct indexes
    for j in range(len(token_list)):
        token_list[j]['id'] = j+1
    
def remove_undefined_tags(token_list):
    current_length = len(token_list)
    i = 0 
    while i < current_length:
        if token_list[i]['upos'] == 'X' or token_list[i]['upos'] == '_':
            del token_list[i]
            current_length -= 1
        else:
            i += 1
    # correct indexes
    for j in range(len(token_list)):
        token_list[j]['id'] = j+1

def remove_exstra_infinitive_the1(token_list):
    """
    Remove redundent "the" when deconstracting Possesives. for example: באפשרותו -> ב ה אפשרות שלו <- ב אפשרות שלו
    """
    current_length = len(token_list)
    i = 0 
    while i < current_length:
        # remove "ה" before "של". need to remove in all cases 
        if token_list[i]['form'] == '_ה_' and  i+2 < len(token_list) and token_list[i+2]['form'] == '_של_':
            del token_list[i]
            current_length -= 1   
        else:
            i += 1
    # correct indexes
    for j in range(len(token_list)):
        token_list[j]['id'] = j+1

def remove_exstra_infinitive_the2(token_list):
    current_length = len(token_list)
    i = 0 
    while i < current_length:
        # remove "ה" after "ל" or "ב".
        if (token_list[i]['form'] == '_ה_' or token_list[i]['form'] == '_ה' or token_list[i]['form'] == 'ה_') and i-1 >= 0 and (token_list[i-1]['form'] == 'ב' or token_list[i-1]['form'] == 'ל' or token_list[i-1]['form'] == 'לְ' or token_list[i-1]['form'] == 'בְּ' or token_list[i-1]['form'] == 'לַ' or token_list[i-1]['form'] == 'בַּ' or token_list[i-1]['form'] == 'בָּ'):
            del token_list[i]
            current_length -= 1
        else:
            i += 1
    # correct indexes
    for j in range(len(token_list)):
        token_list[j]['id'] = j+1

# open files for saving both dicta and copuse parsed and comperable sentences
# corpus_ud_format = open('src\dicta_for_morphological_analysis\\tests\corpus_UD_format.txt', 'a', encoding="utf-8")
# dicta_ud_format = open('src\dicta_for_morphological_analysis\\tests\dicta_UD_format.txt', 'a', encoding="utf-8")

# open file to save the results of the comparison
prediction_value_file =  open('src\dicta_for_morphological_analysis\\tests\\prediction_matrixs.txt', 'a', encoding="utf-8")
true_value_file =  open('src\dicta_for_morphological_analysis\\tests\\true_matrixs.txt', 'a', encoding="utf-8")

# define variables for results
tags = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']

prediction_value_metrix = []
true_value_metrix = []
true_positives = {}
true_negatives = {}
false_positives = {}
false_negatives = {}
success_tokens = 0
total_tokens = 0 
# compare each file in 
index = 0
errors_count = 0
for corpus_token_list in hebrew_corpus:
    print(f"SENTENCE NO. {index}")
    index += 1
    # extract original sentence
    if 'text' not in corpus_token_list.metadata:
        continue
    original_sentence = corpus_token_list.metadata['text']
    dicta_token_lists = dicta.dicta_request(original_sentence)
    dicta_token_lists = conllu.parse(dicta_token_lists)
    # parse dicta sentence
    dicta_sentence_length = 0
    for token_list in dicta_token_lists:
        # remove all "continues" tokens from tokenlist (with id type: int-int)
        remove_composed_tokens(token_list)
        # remove all tokens with PUNC upos
        remove_punctuation_tags(token_list)
        # remove all undefined upos tags
        remove_undefined_tags(token_list)
        # remove redundent "ה", need to parse dicta_token_lists to use it.
        remove_exstra_infinitive_the2(token_list)
        # add token list length
        dicta_sentence_length += len(token_list)
    # fix indexes in all token lists
    combine_token_lists(dicta_token_lists)

    # parse corpus sentence 
    # remove all "continues" tokens from tokenlist (with id type: int-int)
    remove_composed_tokens(corpus_token_list)
    # remove all tokens with PUNC upos
    remove_punctuation_tags(corpus_token_list)
    # remove all undefined upos tags
    remove_undefined_tags(corpus_token_list)
    # remove redundent "ה", need to parse dicta_token_lists to use it. 1 is not needed in dicta format 
    remove_exstra_infinitive_the1(corpus_token_list)
    remove_exstra_infinitive_the2(corpus_token_list)
    # corpus sentence length
    curpos_sentence_length = len(corpus_token_list)

    if curpos_sentence_length != dicta_sentence_length:
        continue
    
    # calculate results
    i = 0 
    prediction_values = []
    true_values = []
    for token_list in dicta_token_lists: 
        for token in token_list:
            # add true value and prediction value
            prediction_values.append(token['upos'])
            true_values.append(corpus_token_list[i]['upos'])
            if token['upos'] == corpus_token_list[i]['upos']:
                success_tokens +=1
            # calculate confution metrix for each tag
            for tag in tags:
                if corpus_token_list[i]['upos'] == tag: 
                    # TP
                    if token['upos'] == tag:
                        if tag not in true_positives:
                            true_positives[tag] = 1
                        else:
                            true_positives[tag] +=1
                    # FN
                    else:
                        if tag not in false_negatives:
                            false_negatives[tag] = 1
                        else:
                            false_negatives[tag] +=1
                else:
                    # FP
                    if token['upos'] == tag:
                        if tag not in false_positives:
                            false_positives[tag] = 1
                        else:
                            false_positives[tag] +=1
                    # TN
                    else:
                        if tag not in true_negatives:
                            true_negatives[tag] = 1
                        else:
                            true_negatives[tag] +=1
            total_tokens += 1
            i += 1
    # append predictions and true values to metrix
    prediction_value_metrix.append(prediction_values)
    true_value_metrix.append(true_values)
    
print(f"errors: {errors_count}")
print(f"test results:\n{success_tokens / total_tokens}\n{true_positives}\n{false_negatives}\n{false_positives}\n{true_negatives}")
# test_results.write(f"Accuracy: {str(success_tokens / total_tokens)}\n")
# test_results.write(f"TP: {str(true_positives)}\n")
# test_results.write(f"FN: {str(false_negatives)}\n")
# test_results.write(f"FP: {str(false_positives)}\n")
# test_results.write(f"TN: {str(true_negatives)}\n")

prediction_value_file.write(str(prediction_value_metrix))
true_value_file.write(str(true_value_metrix))


      
# parse resultes


# sentence = 'במידה והלקוח שכח את הסיסמה, יש ללחוץ "שכחתי סיסמה". להסבר על תהליך איפוס הסיסמה, לחץ כאן . '
# dicta_tokens_list = dicta.dicta_request(sentence)
# dicta_tokens_list = conllu.parse(dicta_tokens_list)
 
# for token_list in dicta_tokens_list:
#     # remove all "continues" tokens from tokenlist (with id type: int-int)
#     remove_composed_tokens(token_list)
#     # remove all tokens with PUNC upos
#     remove_punctuation_tags(token_list)
#     # remove all undefined upos tags
#     remove_undefined_tags(token_list)

# # combine all token lists into one token list
# combine_token_lists(dicta_tokens_list)

# # print_token_list_morph_analysis(dicta_tokens_list[0], "dicta")
# # print_token_list_morph_analysis(dicta_tokens_list[1], "dicta")

# corpus_token_list = list(hebrew_corpus)[5]
# # remove all "continues" tokens from tokenlist (with id type: int-int)
# remove_composed_tokens(corpus_token_list)
# # remove all tokens with PUNC upos
# remove_punctuation_tags(corpus_token_list)
# # remove all undefined upos tags
# remove_undefined_tags(corpus_token_list)
# # print_token_list_morph_analysis(corpus_token_list, "corpus")






