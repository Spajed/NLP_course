import os
import pandas as pd 
from sentiment_translator import SentimentTranslator

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(SCRIPT_PATH, '..', 'data', 'morphologicaltagging_v_2_12.csv')

# universal dependencies hebrew tagging dataset 
UD_POS_TAGGING = pd.read_csv(DATA_PATH)

# example of using the class SentimentTranslator: 
df = pd.DataFrame(columns=['word','translation','sentiment'])
sentiment_translator = SentimentTranslator()
iterations = 0 
for index, row in UD_POS_TAGGING.iterrows():
    word = row['LEMMA']
    upos = row['U-POS']
    feats =  row['FEATS']
    translation = sentiment_translator.pos_translator.translate(word, upos, feats)
    sentiment = sentiment_translator.translate(word, upos, feats)
    new_row = {'word': word, 'translation': translation ,'sentiment': sentiment}
    df.loc[len(df)] = new_row
    iterations += 1
    print(iterations)

print(df.head(50))
# df.to_csv('pos_translation_test2.csv', index = False, encoding = 'utf-8-sig')

