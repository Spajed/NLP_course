import hebrew_english_dictionary
import re
import copy

DATA = {
        "כינוי נפרד": {"U-POS": "PRON", "FEATS": "PronType=Prs"},
        "כינוי סתמי": {"U-POS": "DET", "FEATS": ''},
        "כינוי רומז לקרוב": {"U-POS": "PRON", "FEATS": "PronType=Dem"},
        "כינוי רומז לרחוק": {"U-POS": "PRON", "FEATS": ''},
        "כינוי שאלה": {"U-POS": "DET", "FEATS": "PronType=Int"},
        "מילת הסבר": {"U-POS": "", "FEATS": ''},
        "מילת יחס": {"U-POS": "ADP", "FEATS": ''},
        "מילת קישור": {"U-POS": "CCONJ", "FEATS": ''},
        "מילת קריאה": {"U-POS": "", "FEATS": ''},
        "מילת שאלה": {"U-POS": "DET", "FEATS": "PronType=Int"},
        "מספר מונה": {"U-POS": "NUM", "FEATS": ''},
        "מספר מחלק": {"U-POS": "NUM", "FEATS": ''},
        "מספר סודר": {"U-POS": "ADJ", "FEATS": ''},
        "סופית": {"U-POS": "", "FEATS": ''},
        "פ' הופעל": {"U-POS": "VERB", "FEATS": "HebBinyan=HUFAL"}, 
        "פ' הפעיל": {"U-POS": "VERB", "FEATS": "HebBinyan=HIFIL"},
        "פ' התפעל": {"U-POS": "VERB", "FEATS": "HebBinyan=HITPAEL"},
        "פ' התפעל (השתפעל)": {"U-POS": "VERB", "FEATS": "HebBinyan=HITPAEL"},
        "פ' התפעל (התפעלל)": {"U-POS": "VERB", "FEATS": "HebBinyan=HITPAEL"},
        "פ' נפעל": {"U-POS": "VERB", "FEATS": "HebBinyan=NIFAL"},
        "פ' פועל": {"U-POS": "VERB", "FEATS": "HebBinyan=PUAL"},
        "פ' פועל (פועלל)": {"U-POS": "VERB", "FEATS": "HebBinyan=PUAL"},
        "פ' פועל (שופעל)": {"U-POS": "VERB", "FEATS": "HebBinyan=PUAL"},
        "פ' פיעל": {"U-POS": "VERB", "FEATS": "HebBinyan=PIEL"},
        "פ' פיעל (פעלל)": {"U-POS": "VERB", "FEATS": "HebBinyan=PIEL"},
        "פ' פיעל (שפעל)": {"U-POS": "VERB", "FEATS": "HebBinyan=PIEL"},
        "פ' קל": {"U-POS": "VERB", "FEATS": "HebBinyan=PAAL"},
        "שֵם": {"U-POS": "NOUN", "FEATS": ''},
        "שֵם ז'": {"U-POS": "NOUN", "FEATS": "Gender=Masc"},
        'שֵם ז"ר': {"U-POS": "NOUN", "FEATS": "Gender=Masc"},
        'שֵם ז"ר (בצורת זוגי)': {"U-POS": "NOUN", "FEATS": "Gender=Masc"},
        'שֵם זו"נ': {"U-POS": "NOUN", "FEATS": "Gender=Fem,Masc"},
        'שֵם זנ"ר': {"U-POS": "NOUN", "FEATS": "Gender=Fem,Masc"},
        'שֵם זנ"ר (בצורת זוגי)': {"U-POS": "NOUN", "FEATS": "Gender=Fem,Masc"},
        "שֵם כמות": {"U-POS": "NOUN", "FEATS": ''},
        "שֵם נ'": {"U-POS": "NOUN", "FEATS": "Gender=Fem"},
        'שֵם נ"ר': {"U-POS": "NOUN", "FEATS": "Gender=Fem"},
        'שֵם נ"ר (בצורת זוגי)': {"U-POS": "NOUN", "FEATS": "Gender=Fem"},
        "תואר": {"U-POS": "ADJ", "FEATS": ''},
        "תואר הפועל": {"U-POS": "ADV", "FEATS": ''},
        "תחילית": {"U-POS": "", "FEATS": ''},
        "": {"U-POS": "", "FEATS": ''}
    }

class POSTranslator:
    """
    A class for translating a single hebrew word to a single english word using a mapping between the given dictionary POS to Universal Dependencies POS in hebrew: https://universaldependencies.org/he/index.html.

    Attributes:
     mapper (Dictionary): A dictionary with the given dictionary POSs as keys and the corresponding Universal Dependencies tags and features as values
     dictionary (HebrewEnglishDictionary): an HebrewEnglishDictionary instance. 
    """ 
    def __init__(self):
        """
        initialize mapper and dictionary
        """
        self.mapper = DATA
        self.dictionary = hebrew_english_dictionary.HebrewEnglishDictionary()
    
    def calculate_score(self, translation_record, upos, feats):
        """
        Calculates the score of a translation record. higher score means more accuarte translaion of a word.

        Args:
            translation_record (Dictionary): All attributes of a single potential translation of a word.
            upos (String): Universal Dependencies tag of a given word.
            feats (String): Universal Dependencies features of a given word.

        Returns: 
            score (int): the score of a translation record
            Possible scores for translation records are:
            0: it dose not match. 
            1: it has the same feats but not the same upos
            2: it has the same upos but not the same feats 
            3: it has the same upos and feats.
        """    
        score = 0
        pos = translation_record["part_of_speech"]
        if self.mapper[pos]['U-POS'] != '' and self.mapper[pos]['U-POS'] == upos: 
            if self.mapper[pos]['FEATS'] != '' and self.mapper[pos]['FEATS'] in feats.split("|"):
                score = 3
            else: 
                score = 2
        elif self.mapper[pos]['FEATS'] != '' and self.mapper[pos]['FEATS'] in feats.split("|"):
            score = 1
        else:
            score = 0
        
        return score

    def find_best_translation_record(self, word, upos, feats):
        """
        finds the most accurate translation record of the given word, based on the score calculted using calculate_score()

        Arg:
            word (String): An hebrew word.
            translation_record (Dictionary): All attributes of a single potential translation of a word.
            upos (String): Universal Dependencies tag of a given word.
            feats (String): Universal Dependencies features of a given word.
        
        Returns:
            best_translation_record[0] (Dictionary): the most accurate translation record the corresponds to the given word. 
            If the word is not in the dictionary, return -1
        """
        translation_records = self.dictionary.get_translation_records(word)
        if translation_records == -1:
            return -1 
        # initialize best_translation_record to the first translation_record, with score 0
        best_translation_record = (translation_records[0],0)
        # iterate over all translation recoreds to find the one with the best score 
        for translation_record in translation_records:
            if best_translation_record[1] == 3:
                break
            score = self.calculate_score(translation_record, upos, feats) 
            if score > best_translation_record[1]:
                best_translation_record = (translation_record, score)
        
        return best_translation_record[0]
    
    def parse_translation_record(self, translation_record):
        """
        parse a single translation record into a list of list of single english words.

        Args:
            translation_record (Dictionary): All attributes of a single potential translation of a word.
        
        Returns:
            translations (List): A list of lists, where each list is a parsed translation phrase, splitted into single words. 
        """
        translations = translation_record['translation']
        for index, translation in enumerate(translations):
            # remove all brasket in phrase 
            translation = re.sub(r'\([^)]*\)', '', translation).strip()
            # if its a verb, check if it starts with "to" or "to be" and parse it accordingly
            if "פ'" in translation_record['part_of_speech']:
                if 'to be' in translation:
                    translation = re.sub('to be', '', translation).strip()
                elif 'to ' in translation:
                    translation = re.sub('to ', '', translation).strip()
            # split translation into single words
            translation = translation.split(' ')
            translations[index] = translation
        
        return translations

    def find_best_translation_word(self, translation_record):
        """
        finds an english word that best describes the given hebrew word

        Args:
            translation_record (Dictionary): All attributes of a single potential translation of a word.
        
        Returns:
            best_translation_word (String): a single english word that best describes the given hebrew word.
            Side effect: it changes the translation_record, and this is way a deep copy is made.
        """
        # copy translation_record so it wont change in dictionary
        translation_record = copy.deepcopy(translation_record)
        translations = self.parse_translation_record(translation_record)
        best_translation_word = ''
        for index, translations_words in enumerate(translations):
            # If it is the first iteration, assign a value to best_translation_word.
            # If a translation is composed of only one word, we will choose this word to be the translation word. 
            # if there is not translation that is composed of only one word , the first word of the first translation is chosen.    
            if index == 0:
                best_translation_word =  translations_words[0]
            if len(translations_words) == 1:
                best_translation_word = translations_words[0]
                break
        
        return best_translation_word
    
    def translate(self, word, upos, feats):
        """
        Translate a single hebrew word to a single english word based on it's Universal Dependencies POS tags, and features

        Args: 
            word (String): An hebrew word.
            translation_record (Dictionary): All attributes of a single potential translation of a word.
            upos (String): Universal Dependencies tag of a given word.
            feats (String): Universal Dependencies features of a given word.
         
        Returns:
            translation_word (String): A single english word
            If hebrew word is not found in dictionary, return -1.
        """
        translation_record = self.find_best_translation_record(word, upos, feats)
        # if word is not in the dictionary, return -1
        if translation_record == -1:
            return -1
        translation_word = self.find_best_translation_word(translation_record)
        return translation_word
        
         
# translator = POSTranslator()
# translation_record = translator.dictionary.get_translation_records('טִפֵּשׁ')
# print(translation_record)

    

                

            

