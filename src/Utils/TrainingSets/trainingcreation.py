__author__ = 'rohitangsu.das'

from src.Preprosessing.Converters import *
from src.FirstPass.SectionExtraction import *

class CreateTrainingSet():

    def __init__(self,list_of_files):
        self.list_of_files = list_of_files

    def createTrainingData(self):
        """
            This function takes a series of lines and runs the previously created model on the list of resumes.
        """

        feature_label_list = []

        for every_file in self.list_of_files:

            try:
                #convert to pdf.
                every_file_to_pdf = DocumentConverter().converttopdf(every_file)

                #Get the Json for the pdf.
                every_file_to_json = DocumentConverter().return_json(every_file_to_pdf)

                #Get the extracted Features and the label as well.
                get_feature_label_of_every_file = SectionExtractor(every_file_to_json).getfeaturedtext()

                feature_label_list.append(get_feature_label_of_every_file)

            except Exception as e:
                print "Error with file: ", str(every_file)
                pass
        return feature_label_list


