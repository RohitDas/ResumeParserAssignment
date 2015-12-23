__author__ = 'dhaval.makwana'

"""This file uses Snowball Stemmer and stems whole string than just single word stemming provided by Snowball"""
from nltk.stem.snowball import SnowballStemmer
import re

class TextStemmer(object):
    __instance = None
    __snowBallStemmer = None
    __regx = None

    def __new__(cls):
        if TextStemmer.__instance is None:
            TextStemmer.__instance = object.__new__(cls)
            TextStemmer.__snowBallStemmer = SnowballStemmer("english", ignore_stopwords=True)
            TextStemmer.__regx = re.compile('[^a-zA-Z0-9(\.\w)]') #split on all non alphanum except '.' followed by alphanum
                                                                  #this is to save important context like gmail.com, .Net etc
        #SingleTone.__instance.str = str
        return TextStemmer.__instance

    def stem(self,str):
        return ' '.join([self.__snowBallStemmer.stem(word) for word in self.__regx.split(str)])