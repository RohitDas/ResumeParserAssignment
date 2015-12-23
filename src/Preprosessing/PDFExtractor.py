from Exceptions import ParserExceptions
from difflib import SequenceMatcher
__author__ = 'dhaval.makwana'


import re
from Exceptions import *
from Utils.CommonRegx import  *
from Config.ConfigReader import *
import pickle


class PDFExtractors:
    """This class reads json element by element and considers any two lines
    having vertical distance more than 1.5 times of line height as paragraph break"""
    regx = re.compile('"top":(.*?),.*?"height":(.*?),.*?"data":"(.*?)"}')

    def __init__(self, jsoncontent):
        self.jsontext = jsoncontent[jsoncontent.index("text")+7:]
        self.jsontext = self.jsontext.replace("\u0026lt;", "<")
        self.jsontext = self.jsontext.replace("\u0026gt;", ">")
        self.jsontext = self.jsontext.replace("\u0027", "'")
        self.jsontext = self.jsontext.replace("\u0026quot", "")
        self.jsontext = self.jsontext.replace("\u0026amp;", "")
        self.gazatInstance = SectionGazzatteer()
        self.classifier = pickle.load(open(ConfigReader.ModelFilePath))

    def extractParagraphs(self):
        """The method extracts paragraphs from jsontext variable as per the logic described earlier"""

        try:
            if(len(self.jsontext)):
                itr = self.regx.finditer(self.jsontext)
                lastTop = 0
                lastHeight = 0
                paraText = ""
                output = []
                superscript_detected = False

                #Loop for each line and find paragraphs
                for i in itr:
                    currentTop = int(i.group(1))
                    currentHeight = int(i.group(2))
                    currentText = i.group(3)

                    if(currentText.strip() == "" ):continue

                    #Set current top and height for the first line
                    if(lastTop == 0):
                        lastTop = currentTop
                        lastHeight = currentHeight

                    #Calculate line spacing
                    lineSpace = currentTop - lastTop
                    if(abs(lineSpace) > (lastHeight*2.0)) :
                        output.append(paraText)
                        paraText = currentText + " "
                    elif(lineSpace != 0):

                        if re.search("(st|ST|nd|ND|rd|RD|th|TH)",currentText.strip()) and currentHeight != lastHeight:
                            paraText = paraText.strip() + currentText + " "
                            superscript_detected = True
                        elif superscript_detected and currentHeight != lastHeight:
                            paraText = paraText + currentText + " "
                            superscript_detected = False
                        else:
                            paraText = paraText + "\n" + currentText + " "
                    else:
                       paraText = paraText + currentText + " "

                    lastHeight = currentHeight
                    lastTop = currentTop

                output.append(paraText)
        except Exception as e:
            raise ParserExceptions.ParaExtractionError(e.message)

        return output

    def getText(self):

        text = "\n\n".join(self.extractParagraphs())
        return text
