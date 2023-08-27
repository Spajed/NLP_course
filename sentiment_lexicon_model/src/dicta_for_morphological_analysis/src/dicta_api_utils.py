import os
import pandas as pd
import requests
import json
import conllu
import re

# Get file path
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(SCRIPT_PATH, '..', 'data', 'hebrew_corpus_sentences_only.csv')

# open data
data = pd.read_csv(DATA_PATH, encoding="utf-8")
# print(data.loc[0, 'sentence'])

# calling Dicta API
def dicta_request(sentence, ud_format=True):
    """
    Sends a request for morphological analysis of a sentence

    Arg: 
    sentence (String): A sentence to preform morphological analysis on. 
    ud_format (Bool): If to return a UD format 

    Returns: 
    A list of jsons with all the data returend from the request. 
    if ud_format=True, then return a parsed string in UD format, sutable for conllu. 
    """
    headers = {'Content-Type': 'text/plain;charset=utf-8'}
    params = {
    "task" : "nakdan",
    "genre" :"modern",
    "apiKey" : "xxxx",
    "data" : sentence,
    "addmorph" : True,
    "matchpartial" : True,  
    "keepmetagim" : True ,
    "keepqq" :True,
    "freturnfullmorphstr": True,
    "newjson": True, 
    "keepnikud": True
    }
    r = requests.post("https://nakdan-5-3.loadbalancer.dicta.org.il/addnikud",headers=headers,json=params)
    r.encoding= "UTF-8"
    request_data = r.json()
    if ud_format == True:
        request_data = request_data[0]['UD']
        request_data = parse_ud_format(request_data)
    return request_data

def parse_ud_format(ud_format_sentence):
    """
    Parse data into defult Conllu formatting

    Args: 
    ud_format (String): A sentence string in UD format

    Rrturns:
    ud_format (String): A sentence string in Conllu format
    """
    # replace all X's with _ as thay are parsing errors
    conllu_format = re.sub(r'\tX', r'\t_', ud_format_sentence)
    # switch between lemma and lemmaVoc, and remove lemma without nikud.  
    conllu_format = re.sub(r'(.*\t.*\t)(.*)(\t.*\t.*\t.*\t)(.*)(\t.*)', r'\1\4\3', conllu_format)
    # remove tag "DictaNote"
    conllu_format = re.sub(r'\t(DictaNote=.*)\t', r'\t_\t', conllu_format)
    return conllu_format

# sentence = data.loc[0, 'sentence']
# sentence = 'شكراً سيدي الرئيس على هذا الموقف الجريء תודה אדוני הנשיא על הגיבוי הנועז שמחת הרבה לבבות שבורים'
# sentence = dicta_request(sentence, ud_format=False)[0]['UD']
# sentence = parse_ud_format(sentence)
# print(repr(sentence))
# print("")
# sentence = re.sub(r'\t(DictaNote=.*)\t', r'\t_\t', sentence)
# print(sentence)







