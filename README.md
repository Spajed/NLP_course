# NLP_course
This project consists of sevral parts including a jupyter notebook containing our code model and expermintal results, dicta preprocessing code and sentiment lexicon code.

## Notebook
The notebook was written using huggingface's package "transformers" and our model was written using pytorch. 
At first, we test Alephbert on the sentiment database to see that we can get the same results as the article. After that, we examine the results using SHAP to see where Alephbert made mistakes.

The second task was creating a POS tagger using Alephbert on the Hebrew UD treebank and comparing the model to dicta using a new database unrelated to the treebank.

Finally, seen as dicta got better results, we used dicta to get a new morphlogy disambugation and POS tags on the sentiment 

## sentiment_lexicon_model
1. __main__py: parses a the sentiment corpus and using dicta creates a UD format of the corpus. furthermore, it calculates a sentiment score using the sentiment lexicon.
2. src/dicta_for_morphological_analysis: uses the dicta api to get a morphological analysis of sentences.
3. src/hebrew_sentiment_based_on_pos: library to calculate a sentiment score based on PoS and a lexicon.