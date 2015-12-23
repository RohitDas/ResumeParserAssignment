__author__ = 'rohitangsu.das'


""" Auxillary Function to reverseMap the sectionames to its general Headers and return the modified the list """


from Gazzetteers.SectionGazzetteer.LoadSectionGazzetter import *
from Utils.CommonRegx import  *


class ReverseMapper:
    """
        This class defines functions to do the reverse map of the  e
    """
    def __init__(self,sectionblocklist):
        self.sectionblocklist = sectionblocklist

    def reverseMap(self):
        """
        :param sectionblocklist: List of tuple (SectionHeader and Sectiontext)
        :return: return a list of reversemapped SectionHeadrrfs alongwith the text
        """
        #Use map functionality and apply the getheader function to each element of the list.
        sectionblocklist = map(self.getheader,self.sectionblocklist)
        # Return the grouped sections dictionary
        return self.groupSections(sectionblocklist)




    def getheader(self,headernameblocktuple):
        """
        :param headernameblocktuple: Takes a tuple (SectionHeader,Sectiontext)
        :return: it returns the reversed Map sectionheader by doing a lookup in the Big and Small Gazzeetteer respectively.
        """
        sectionheader, sectionblock = headernameblocktuple[0].upper().replace("_"," ").strip(), headernameblocktuple[1]
        #Look up in the main gazzeetter
        mappedheader = self.BigGazzetterLookup(sectionheader)
        #Look up in the small gazzetter
        if not mappedheader:
            mappedheader = self.SmallGazzetterLookup(sectionheader)

        value = (mappedheader.replace(" ","_"),sectionblock)
        return value



    def BigGazzetterLookup(self,sectionheader):
        """
        :param sectionheader: Takes the name of a sectionheader .
        :return: It returns the reverse mapped section header by looking up the Big Gazzeetteer.
        """

        if SectionGazzatteer().hashGazzatter.has_key(sectionheader):
            return SectionGazzatteer().hashGazzatter[sectionheader]
        return None

    def SmallGazzetterLookup(self,sectionheader):
        """
        :param sectionheader: Takes the name of a sectionheader .
        :return: It returns the reverse mapped section header by looking up the Big Gazzeetteer.
        """
        for key in commonSectionNamesToCompare.keys():
            if key in sectionheader:
                return commonSectionNamesToCompare[key]
        return sectionheader


    def groupSections(self,sectionblocklist):
        """
        :param sectionblocklist:  It takes a list of (reverse Mapped sectionheader,text) and groups it by header name.


                      list[i] = ("Work Experience",text1)
                      list[j] = ("Work Experience",text2)
                      result -> list[i] = ("Work Experience",text1.append(text2))

        :return: Reversed Mapped Dictionary.
        """
        resumeblocklist = {}
        for key,section in sectionblocklist:
            if resumeblocklist.has_key(key) : resumeblocklist[key] += section + "\n"
            else: resumeblocklist[key] = section + "\n"

        return resumeblocklist
















