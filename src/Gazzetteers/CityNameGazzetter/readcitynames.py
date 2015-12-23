__author__ = 'regge'


""" This File contains the code to read the city name gazzetter only once ans save it into a dict object and expose the dict for external use. """
from Config.ConfigReader import *

class CityGazzatteer(object):
    __instance = None
    CityNameGazzatter = None
    

    def __new__(cls):
        if CityGazzatteer.__instance is None:
            CityGazzatteer.__instance = object.__new__(cls)
            CityGazzatteer.CityNameGazzatter = CityGazzatteer.CityGazzetLoader(CityGazzatteer.__instance)


        #SingleTone.__instance.str = str
        return CityGazzatteer.__instance

    def CityGazzetLoader(self):
        citygazzat = open(ConfigReader.CityNameGazzetter,"r")
        cityhasgazet = {}
        for line in citygazzat:
            cityhasgazet[line.encode("utf8","replace").strip().upper()] = ""
        return cityhasgazet