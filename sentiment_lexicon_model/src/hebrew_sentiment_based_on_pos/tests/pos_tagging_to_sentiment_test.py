import os
import pandas as pd
import sys
# to import module from another folder:
# Get the absolute path to the parent directory (project directory)
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the 'src' directory to the Python path
sys.path.append(os.path.join(project_dir, "src"))
import sentiment_translator


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(SCRIPT_PATH, '..', 'data', 'morphologicaltagging_v_2_12.csv')

POS_TAGGINGS = pd.read_csv(DATA_PATH)

df = pd.DataFrame(columns=['word','translation','sentiment'])
sentiment_translator = sentiment_translator.SentimentTranslator()
iterations = 0 
for index, row in POS_TAGGINGS.iterrows():
    word = row['LEMMA']
    translation = sentiment_translator.pos_translator.translate(row['LEMMA'],row['U-POS'], row['FEATS'])
    sentiment = sentiment_translator.translate(row['LEMMA'],row['U-POS'], row['FEATS'])
    new_row = {'word': word, 'translation': translation ,'sentiment': sentiment}
    df = df.append(new_row, ignore_index=True)
    iterations += 1
    print(iterations)

df.to_csv('pos_translation_test3.csv', index = False, encoding = 'utf-8-sig')