__author__ = 'rohitangsu.das'


import re
from Config.ConfigReader import *

class DesignationGazzetter(object):
    """
        Singleton class that creates a single distance of the Designation Data Structure.
    """
    __instance = None
    dict_level_1 = {}
    dict_level_2 = {}
    dict_level_3 = {}

    def __new__(cls):
        if DesignationGazzetter.__instance is None:
            DesignationGazzetter.__instance = object.__new__(cls)
            DesignationGazzetter.HashGazzetLoader(DesignationGazzetter.__instance)

        #SingleTone.__instance.str = str
        return DesignationGazzetter.__instance

    @property
    def initialize_dict_level_1(self):
        self.dict_level_1["JUNIOR"] = None
        self.dict_level_1

    @property
    def HashGazzetLoader(self):
        """
            The Dictionary would have 3 levels.

            Level 1                       level 2                            level 3
            -------                       -------                            -------

            Junior     ----------->       Software    -------------------->  Engineer
            Senior
            Head
            Blank
        """
        #The file path
        country_name_gazetter_path = ConfigReader.CountryGazetter
        #Open the file path for reading.
        gazetter=open(country_name_gazetter_path,"r")
        designation_hash_level_1 = {}
        designation_hash_level_2 = {}
        designation_hash_level_3 = {}

        #The first dictionary represent the common prefixes that are not that relevant.
        for i in ["JUNIOR", "SENIOR", "HEAD",""]:
            self.dict_level_1[i] = ""

        #The third dictionary stores the different final designations.


        for line in gazetter:
            lines = line.split("\t")
            self.dict_level_3[lines[-1]] = ""
            for word in lines:
                if not self.dict_level_2.has_key(word.upper()):
                    self.dict_level_2[word.upper()] = ""
        return
