from __future__ import division
import numpy as np
import nltk
from nltk.metrics import *
from nltk.util import ngrams
import enchant
from enchant.checker import SpellChecker
from nltk.stem import PorterStemmer
from nltk.corpus import words

spell_dictionary = enchant.Dict('en')
class LanguageModel:
    def __init__(self,dictionary):
        self.dictionary = dictionary
        self.check = SpellChecker("en_US")
        self.stemmer = PorterStemmer()

    def levenshtein_distance(self,s1,s2):
        distance_btw_strings = edit_distance(s1,s2)
        return distance_btw_strings

    def ngram(self,word,n):
        grams = list(ngrams(word,n))
        return grams
    
    def check_mistakes_in_sentence(self,sentence):
        misspelled_words = []
        self.check.set_text(sentence)
        for err in self.check:
            misspelled_words.append(err.word)
            
        if len(misspelled_words) == 0:
            print " No mistakes found"
        return misspelled_words
    
    def jaccard(self,a,b):
        union = list(set(a+b))
        intersection = list(set(a) - (set(a)-set(b)))
        jaccard_coeff = float(len(intersection))/len(union)
        return jaccard_coeff

    def minimumEditDistance_spell_corrector(self,word):
        max_distance = 2
        if (self.dictionary.check(word)):
            return word
        suggested_words = self.suggest_words(word)
        num_modified_characters = []
        if suggested_words != 0:
            for sug_words in suggested_words:
                num_modified_characters.append(self.levenshtein_distance(word,sug_words))
            minimum_edit_distance = min(num_modified_characters)
            best_arg = num_modified_characters.index(minimum_edit_distance)
            if max_distance > minimum_edit_distance:
                best_suggestion = suggested_words[best_arg]
                return best_suggestion
            else:
                return word
        else:
            return word
        

    def ngram_spell_corrector(self,word):
        max_distance = 2
        if (self.dictionary.check(word)):
            return word
        suggested_words = self.suggest_words(word)
        num_modified_characters = []
        max_jaccard = []
        list_of_sug_words = []
        if suggested_words != 0:
            word_ngrams = self.ngram(word,2)
            for sug_words in suggested_words:
                if (self.levenshtein_distance(word,sug_words)) < 3 :  
                    sug_ngrams = self.ngram(sug_words,2)
                    jac = self.jaccard(word_ngrams,sug_ngrams)
                    max_jaccard.append(jac)
                    list_of_sug_words.append(sug_words)
            highest_jaccard = max(max_jaccard)
            best_arg = max_jaccard.index(highest_jaccard)
            word = list_of_sug_words[best_arg]
            return word
        else:
            return word
