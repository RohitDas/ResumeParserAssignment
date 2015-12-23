__author__ = 'rohitangsu.das'

""" This file contains the class definition that creates a dictionary instance of country names in the memory only once."""
import re
from Config.ConfigReader import *

class CountryNamesGazzetter(object):
    __instance = None
    countryGazzatter = None
    capitalGazzatter = None


    def __new__(cls):
        if CountryNamesGazzetter.__instance is None:
            CountryNamesGazzetter.__instance = object.__new__(cls)
            CountryNamesGazzetter.countryGazzatter, CountryNamesGazzetter.capitalGazzatter = CountryNamesGazzetter.HashGazzetLoader(CountryNamesGazzetter.__instance)
            CountryNamesGazzetter.subsectionhashGazzatter = CountryNamesGazzetter.SubHashGazzetLoader(CountryNamesGazzetter.__instance)

        #SingleTone.__instance.str = str
        return CountryNamesGazzetter.__instance

    @property
    def HashGazzetLoader(self):
        """
            The Dictionary would be stored in the form State -> Capital
        """
        country_name_gazetter_path = ConfigReader.CountryGazetter
        gazetter=open(country_name_gazetter_path,"r")
        country_hash_gazet = {}
        capital_hash_gazet = {}
        for line in gazetter:
            lines = line.split("\t")
            country_hash_gazet[lines[0].encode("utf8","replace").strip().upper()] = "LOCATION"
            capital_hash_gazet[lines[1].encode("utf8","replace").strip().upper()] = "LOCATION"
        return country_hash_gazet, capital_hash_gazet
