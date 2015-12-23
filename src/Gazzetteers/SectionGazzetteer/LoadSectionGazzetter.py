__author__ = 'dhaval.makwana'

"""This file contains the SectionGazzatteer class that reads the gazzatteer file and loads it to memory."""

import re
from Config.ConfigReader import *

class SectionGazzatteer(object):
    __instance = None
    hashGazzatter = None
    subsectionhashGazzatter = None


    def __new__(cls):
        if SectionGazzatteer.__instance is None:
            SectionGazzatteer.__instance = object.__new__(cls)
            SectionGazzatteer.hashGazzatter = SectionGazzatteer.HashGazzetLoader(SectionGazzatteer.__instance)
            SectionGazzatteer.subsectionhashGazzatter = SectionGazzatteer.SubHashGazzetLoader(SectionGazzatteer.__instance)

        #SingleTone.__instance.str = str
        return SectionGazzatteer.__instance

    def SubHashGazzetLoader(self):
        subgazatpath = ConfigReader.SubGazetter
        subgazzat = open(subgazatpath,"r")
        subhasgazet = {}
        for line in subhasgazet:
            subhasgazet[line.encode("utf8","replace").strip().upper()] = ""
        return subhasgazet

    def HashGazzetLoader(self):
        gazetter_path = ConfigReader.Gazetter
        gazetter=open(gazetter_path,"r")
        hash_gazet = {}
        for line in gazetter:
            lines = line.split("\t")
            hash_gazet[lines[0].encode("utf8","replace").strip().upper()]=lines[1].encode("utf8","replace").strip().upper()
        return hash_gazet

