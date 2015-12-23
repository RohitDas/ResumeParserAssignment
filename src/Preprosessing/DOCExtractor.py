__author__ = 'sameer.pidadi'

import textract
from Exceptions.ParserExceptions import *

class DOCExtractor:

    def __init__(self):
        pass

    def getText(self, path):
        text = ""
        try:
            text = textract.process(path)
        except Exception:
            pass
            #raise TextractError(path)
            #print text
        return text

