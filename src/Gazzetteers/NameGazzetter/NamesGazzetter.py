__author__ = 'rohitangsu.das'
__author__ = 'dhaval.makwana'

"""This FIle contains the Name Gazzetter Loader."""

import re
from Config.ConfigReader import *


class NamesGazzatteer(object):
    __instance = None
    namesGazzatter = None

    def __new__(cls):
        if NamesGazzatteer.__instance is None:
            NamesGazzatteer.__instance = object.__new__(cls)
            NamesGazzatteer.namesGazzatter = NamesGazzatteer.NameGazzetLoader(NamesGazzatteer.__instance)
        return NamesGazzatteer.__instance


    def NameGazzetLoader(self):
        gazetter_path = ConfigReader.NamesGazzetter
        gazetter=open(gazetter_path,"r")
        hash_gazet = {}
        for line in gazetter:
            lines = line.split("\t")
            hash_gazet[lines[0].encode("utf8","replace").strip().lower()]= "Name"
        return hash_gazet

