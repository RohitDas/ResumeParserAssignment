
"""This file contains classes for extracting personal info like First and Last Name, email id, phone no"""

import nltk

class NameExtractor:
    __instance = None

    def __new__(cls):
        if NameExtractor.__instance is None:
            NameExtractor.__instance = object.__new__(cls)

        return NameExtractor.__instance

    def extract(self, metaPara):
        words = nltk.word_tokenize(metaPara)
        taggedWords = nltk.pos_tag(words)
        neChunks = nltk.ne_chunk(taggedWords, binary=True)

        #Extract NEs from chunked info
        for i in range(len(neChunks)):
            if "NE" in str(neChunks[i]):
                print ' '.join(j[0] for j in neChunks[i].leaves())