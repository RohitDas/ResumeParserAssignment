
from Gazzetteers.SectionGazzetteer.LoadSectionGazzetter import *
from SecondPass.ReverseMap import *

class FeatureExtraction:
    """
        This class contains functionalities to extract the 9 named features from a line and would be
        predictors while training and predicting the label of a new line.
        3 Classes are considered: A Section Header, A Normal Line and a subsection.

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
            Feature10: Section Gazzetter
            Feature11: Subsection Gazzetteer

    """


    def __init__(self,list_of_lines):
        self.list_of_lines = list_of_lines
        self.gazatInstance = SectionGazzatteer()


    def get_feature_list(self):
        """
        :return: A list of features
        """
        try:
            line_label_dict = []
            ispreviouslineempty = False
            previous_pad = 10000
            indent_level = 0
            line_label_dict = []
            #List of probable section fonts.
            fontlist = self.getFontList(self.list_of_lines)
            #Iterate through the lines.
            for (line,font,pad) in self.list_of_lines:
                # Clean Line used for some feature extraction like main and secondary gazat
                cleaned_line = self.pre_process_string(line)
                if cleaned_line:
                    # Set the whether the line contains Camel Case Feature.
                    contain_camel_case_feature = self.is_line_camel_case(line)
                    # Set the Length Feature
                    less_than_six_word_feature = self.check_less_than_six_words(cleaned_line)
                    #Empty Previous Line Feature.
                    empty_previous_line_feature = "False"
                    if ispreviouslineempty:
                        empty_previous_line_feature = "True"

                    #Padding Feature.
                    #Set the identation level of the current line and calculate the level of the new line
                    indent_level_feature = str(indent_level)
                    #Set the new indentation level
                    indent_level = self.set_current_indent_level(pad,previous_pad,indent_level)
                    previous_pad = pad

                    #Font Feature.
                    if fontlist and (font in fontlist): font_feature = "True"
                    else: font_feature = "False"

                    # Set the Gazat Features
                    main_gazat_feature,small_gazat_feature = self.get_gazat_features(cleaned_line)

                    #SUb-section feature
                    mainsubsectionfeature,loosesubsectionfeature = self.get_sub_sec_gazt_feature(cleaned_line)

                    # Check for a possible section by looking for a colon | semi-colon
                    right_text,left_text,right_text_feature_present,end_marker_feature = self.check_left_right_case(line)

                    dict = {}

                    #make the dictionary
                    dict["a"] = contain_camel_case_feature
                    dict["b"] = less_than_six_word_feature
                    dict["c"] = empty_previous_line_feature
                    dict["d"] = indent_level_feature
                    dict["e"] = font_feature
                    dict["f"] = main_gazat_feature
                    dict["g"] = small_gazat_feature
                    dict["h"] = right_text_feature_present
                    dict["i"] = end_marker_feature
                    dict["j"] = mainsubsectionfeature
                    dict["k"] = loosesubsectionfeature
                    line_label_dict.append((line,dict))
                    # print line, "\t" ,dict,"\t", int(self.label_feature(dict))
                else:
                    ispreviouslineempty = "True"
            return line_label_dict
        except Exception as e:
            pass


    def getFontList(self,lines):
        """
        :return: A list of poosible section header fonts.
        """
        try:
        #Iterate over the list
            fontlist =[]
            for (line,font,leftpad) in lines:
                processedline = self.pre_process_string(line)
                main,small = self.get_gazat_features(processedline)
                if processedline:
                    if main == "True"  and (font not in fontlist):
                        fontlist.append(font)
                    elif self.subsection_loose_gazatfeature(processedline) == "True" and (font not in fontlist):
                        fontlist.append(font)
                    else:
                        continue

            return fontlist
        except Exception as e:
            print e.message


    def is_line_camel_case(self,line):
        """ Utilty Function to check whether a line contains camel-casing words. """
        splitWords = cleanLine(line).split()
        if len(splitWords):
            for word in splitWords:
                if not word.strip()[0].isupper():
                    return "False"
            return "True"
        else:
            return "False"

    def get_sec_gazt_feature(self,line):
        """ Utlility Function to check whether a line contains a catch words from Gazzaatteer. """
        for sectionHead in commonSectionNamesToCompare.keys():
            if sectionHead in line:
               return "True"

        return "False"



    def check_left_right_case(self,line):
        """  Takes a line as an input and checks for a :,:- and returns the left and right text respectively
             Return Value : (RightText,RightTextPresentFeature,EndMarkerFeaturePresent)
        """
        right_left_text = None
        if line.count(":") >= 1:
            regex=re.search('(.*?)(:\-|:|\t|    )+?(.*)',line)
            right_left_text = (regex.group(1),regex.group(3))

            if right_left_text[1].strip() != "":
                return (right_left_text[0],right_left_text[1],"True","True")
            else:
                return (right_left_text[0],"","True","False")
        else:
            return (line,"","False","False")

    def get_main_gazat_feature(self,line):
        """
        :param line: Line in a paragraph
        :return: Return True if it contains Main Gazat Feature , else False
        """
        # print "LINEEEE: ", line
        regx_search = re.search("^(.*)(:|-)$",line.strip())
        if regx_search:
            line = regx_search.group(1).strip()
            # print "MODIFY: ", line
        if self.gazatInstance.hashGazzatter.has_key(line): return "True"
        else: return "False"

    def subsection_loose_gazatfeature(self,line):
        """
        :param line: Line in a Paragraph
        :return: Return True if it contains sub section feature.
        """
        for i in commonSubSectionNamesToCompare:
            if i in line:
                return "True"
        return "False"


    def subsection_main_gazatfeature(self,line):
        """
        :param line: Preprocessed line from a paragraph
        :return: Boolean if feature is found.
        """
        if self.gazatInstance.subsectionhashGazzatter.has_key(line): return "True"
        else: return "False"


    def get_sub_sec_gazt_feature(self,line):
        """
        :param line:
        :return:
        """
        return (self.subsection_main_gazatfeature(line),self.subsection_loose_gazatfeature(line))


    def get_gazat_features(self,line):
        """
        :param line:
        :return: Returns a tuple of boolean values , respectively informing whether the line contains gazat Feature or not.
        """
        return (self.get_main_gazat_feature(line),self.get_sec_gazt_feature(line))

    def check_less_than_six_words(self,line):
        """
        :param line:
        :return:
        """
        if  len(line.split()) < int(ConfigReader.WordLengthThetha): return "True"
        else: return "False"


    def set_current_indent_level(self,current_left,previous_left,current_indent_level):
        """
        :param previous_left:
        :param current_left:
        :return:
        """
        padding_diff = int(current_left) - int(previous_left)
        if padding_diff != 0:
            if padding_diff > int(ConfigReader.PaddingThetha):
                current_indent_level += 1
            elif padding_diff < -int(ConfigReader.PaddingThetha):
                current_indent_level -= 1
            if current_indent_level < 0:
                current_indent_level = 0
        else:
            return current_indent_level

        return current_indent_level
        """ Utilty Function to check whether a line contains camel-casing words. """
        splitWords = cleanLine(line).split()
        if len(splitWords):
            for word in splitWords:
                if not word.strip()[0].isupper():
                    return "False"
            return "True"
        else:
            return "False"

    def get_sec_gazt_feature(self,line):
        """ Utlility Function to check whether a line contains a catch words from Gazzaatteer. """
        for sectionHead in commonSectionNamesToCompare.keys():
            if sectionHead in line:
               return "True"

        return "False"



    def check_left_right_case(self,line):
        """  Takes a line as an input and checks for a :,:- and returns the left and right text respectively
             Return Value : (RightText,RightTextPresentFeature,EndMarkerFeaturePresent)
        """
        right_left_text = None
        if line.count(":") >= 1:
            regex=re.search('(.*?)(:\-|:|\t|    )+?(.*)',line)
            right_left_text = (regex.group(1),regex.group(3))

            if right_left_text[1].strip() != "":
                return (right_left_text[0],right_left_text[1],"True","True")
            else:
                return (right_left_text[0],"","True","False")
        else:
            return (line,"","False","False")

    def get_main_gazat_feature(self,line):
        """
        :param line: Line in a paragraph
        :return: Return True if it contains Main Gazat Feature , else False
        """
        # print "LINEEEE: ", line
        regx_search = re.search("^(.*)(:|-)$",line.strip())
        if regx_search:
            line = regx_search.group(1).strip()
            # print "MODIFY: ", line
        if self.gazatInstance.hashGazzatter.has_key(line): return "True"
        else: return "False"

    def subsection_loose_gazatfeature(self,line):
        """
        :param line: Line in a Paragraph
        :return: Return True if it contains sub section feature.
        """
        for i in commonSubSectionNamesToCompare:
            if i in line:
                return "True"
        return "False"


    def subsection_main_gazatfeature(self,line):
        """
        :param line: Preprocessed line from a paragraph
        :return: Boolean if feature is found.
        """
        if self.gazatInstance.subsectionhashGazzatter.has_key(line): return "True"
        else: return "False"


    def get_sub_sec_gazt_feature(self,line):
        """
        :param line:
        :return:
        """
        return (self.subsection_main_gazatfeature(line),self.subsection_loose_gazatfeature(line))


    def get_gazat_features(self,line):
        """
        :param line:
        :return: Returns a tuple of boolean values , respectively informing whether the line contains gazat Feature or not.
        """
        return (self.get_main_gazat_feature(line),self.get_sec_gazt_feature(line))

    def check_less_than_six_words(self,line):
        """
        :param line:
        :return:
        """
        if  len(line.split()) < int(ConfigReader.WordLengthThetha): return "True"
        else: return "False"


    def pre_process_string(self,sentence):
        """ Function takes a String and cleans the Line """
        sentence = re.sub(r'(\[pic\])',"",sentence.encode("utf8","replace").replace("|","").strip())
        sentence = sentence.strip().strip("-").strip(":").strip(":-").strip().upper()
        sentence = re.sub(r'[^A-Za-z0-9:\-\+,]'," ",sentence)
        sentence = re.sub(r'(\s){2,}'," ",re.sub("\b(AND|FOR|AT)\b","",sentence.strip()))
        return sentence
