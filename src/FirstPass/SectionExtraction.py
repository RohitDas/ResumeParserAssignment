from Exceptions import ParserExceptions
from Config.ConfigReader import *
import pickle,re
from FeatureExtraction import *
from NamedEntityExtraction.Skills_Extraction import *

class SectionExtractor:
    """This class reads json element by element and considers any two lines
    having vertical distance more than 1.5 times of line height as paragraph break"""
    regx = re.compile('"top":(.*?),.*?"height":(.*?),.*?"data":"(.*?)"}')

    def __init__(self, resume_lines):
        self.resume_lines = resume_lines
        self.classifier = pickle.load(open(ConfigReader.ModelFilePath))
        self.storeLabelledInfo = None

    def getSections(self):
        """
        :return: Returns a List of Extracted Sections.
        Note: It returns all the broader sections however it still needs to be reversed mapped.
        The method extracts paragraphs from jsontext variable as per the logic described earlier
           Function which does line by line feature Extraction of a PDF Text.
            Feature1 : Camel Casing
            Feature2 : Less Than Six Words
            Feature3 : Empty Previous Line
            Feature4 : Line Idented from the rest.
            Feature5 : Font Feature
            Feature6 : Big Gazzaetter
            Feature7 : Small Gazzaatteer
            Feature8 : Right Text Present
            Feature9 : End MArkers
        """
        predicted_list = []
        for line,feature in self.resume_lines:
            predicted_label = self.label_feature(feature)
            predicted_list.append((line, predicted_label))

        return self.grouptextIntoSections(predicted_list)

    def label_feature(self,feature_dict):
        """
        :param feature_dict: Takes a Dictionary of features
        :return: This function labels the list as either a Section,Sub-Section or otherwise
        """
        return self.classifier.classify(feature_dict)

    def isSkillSection(self,line):
        """
        :param line: Line in a paragraph
        :return: Boolean , whether it is a skill section or not.
        """

        if "SKILL" in line or "PROFICIENCY" in line or "EXPERTISE" in line:
            return True
        else:
            return False

    def grouptextIntoSections(self,linelist):
        """
            This function groups the text into sections.
            It takes the label of the line and checks whether it is a section or a sub-section.
        """
        current_section_head = "PERSONAL_INFORMATION"
        sectionlist = []
        sectionblock = []
        skill_subsection_detected = False
        skill_subsection = []
        for (line,label) in linelist:
            if line.strip():
                if int(label) == 1:
                    if skill_subsection_detected: skill_subsection_detected = False
                    if current_section_head == "SKILL_SECTION":
                        skills_list = SkillsExtraction(sectionblock).get_Skills()
                        sectionlist.append((current_section_head,'#'.join(skills_list)))
                    else:
                        #End the previous section.
                        sectionlist.append((current_section_head,'\n'.join(sectionblock)))
                    #Set new section head
                    current_section_head = re.sub('\s+','_',re.sub(':|\-',"",line.strip().upper()))
                    #Check for the skill section
                    if self.isSkillSection(current_section_head):
                        current_section_head = "SKILL_SECTION"
                    sectionblock = []
                elif int(label) == 2:
                    if possible_skill_sub_section.match(line):
                        #Skill subsection detected
                        if not skill_subsection_detected:
                            skill_subsection_detected = True
                        skill_subsection.append(line.strip())
                    else:
                        if skill_subsection_detected:
                            skill_subsection_detected = False
                    sectionblock.append(line.strip())
                else:
                    if skill_subsection_detected :
                        if line.count(":") == 0:
                            skill_subsection.append(line.strip())
                        else:
                            skill_subsection_detected = False
                    sectionblock.append(line.strip())
        sectionlist.append((current_section_head.replace(" ","_"),'\n'.join(sectionblock)))
        if skill_subsection:
            skills_list = SkillsExtraction(sectionblock).get_Skills()
            sectionlist.append(("SKILL_SECTION",'#'.join(skills_list)))

        return sectionlist






