from src.Preprosessing.Converters import DocumentConverter
from src.FirstPass.SectionExtraction import *
import logging
import nltk
import json
from src.Config.ConfigReader  import ConfigReader
#Function name: Append unseen Sections to Gazzetteer

def enhance_gazzetteer(file=None):
    """
       Extract All the sections from the resume.
       Run a Loop, and Append to the Gazzetter List.
    :return:
    """
    if file:
        #Code to Extract the sections from a resume.
        sections = extract_sections_from_resume(file)
        #Import the Gazzetter Hash DataStructure that is created once in the current execution environment.
        section_gazzet_list = SectionGazzatteer().hashGazzatter
        gazzet_file_instance = open(ConfigReader.Gazetter,"a")
        for section in sections:
            # If in GazzetList, then ignore.
            if not section_gazzet_list.has_key(section):
                gazzet_file_instance.write(section+"\t"+"UNKNOWN")
        return

def extract_sections_from_resume(file=None):
    """
        Helper Function to Extract all the sections from the resume.
    """
    #Convert to PDF
    file = DocumentConverter().converttopdf(file)
    #Convert to JSON
    file = DocumentConverter().return_json(file)
    #Run the model on the lines and separate the lines as sections.
    sections = SectionExtractor(file).getfeaturedtext(flag=True)
    #Iterate through the sections, keeping only the sections.
    sections = filter(lambda x: x[2] == 1, sections)
    logging.info(sections)
    return sections

def extract_sub_sections_from_resume(file=None):
    """
        Helper Function to Extract all the sub-sections from the resume
    """
    file = DocumentConverter().converttopdf(file)
    file = DocumentConverter().return_json(file)
    sub_sections = SectionExtractor(file).getfeaturedtext(flag=True)
    sub_sections = filter(lambda x: x[2] == 2, sub_sections)
    logging.info(sub_sections)
    return sub_sections

def creation_of_training_data(folderpath):
    """
        This function would ensure that after every new resume is passed, from every line of the resume
        and populate the training data file.
    """
    #Iterate over all the files in the folder path.
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(folderpath) if isfile(join(folderpath,f))]
    for file in onlyfiles:
        #Run the SectionExtraction  Code that will in turn populate the Standard Trainning Data file.
        file = DocumentConverter().converttopdf(file)
        file = DocumentConverter().return_json(file)
        line_label_feature = SectionExtractor(file).getfeaturedtext(flag=False)
        #Open the Training Data File for Append Information.
        training_file = open(ConfigReader.DecisionTreeTrainingFile,"a")
        for line in line_label_feature:
            training_file.write(line[0]+"\t"+str(line[1])+"\t"+line[2])
        training_file.close()




def model_training_decision_tree():
    """
        This function is used to further train the Decision Tree model.
    """
    file_pointer = open("/home/likewise-open/PUNESEZ/rohitangsu.das/Documents/training_set_8000.dat","r")
    training_list_of_tuples = []
    for line in file_pointer.read().split("\n"):
        if line:
            line = line.split('\t')
            print line
            training_list_of_tuples.append((json.loads(line[0]),line[1]))
    trainset = training_list_of_tuples[:int(0.8 * len(training_list_of_tuples))]
    testset = training_list_of_tuples[int(0.8 * len(training_list_of_tuples)):]
    print trainset
    classifier = nltk.DecisionTreeClassifier.train(trainset)
    accuracy = nltk.classify.accuracy(classifier, testset)
    print accuracy



def get_work_experience_section(file=None):
    if file:
         #Convert to PDF
        file = DocumentConverter().converttopdf(file)
        #Convert to JSON
        file = DocumentConverter().return_json(file)
        #Run the model on the lines and separate the lines as sections.
        sections = SectionExtractor(file).getSections()
        file_pointer = open("/home/likewise-open/PUNESEZ/rohitangsu.das/ResumeParser/Experiments/OrgNameExtractor/dataset2016.dat","a")
        file_pointer.write(sections["WORK_EXPERIENCE"])
        file_pointer.close()

