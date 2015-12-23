import logging, traceback
from Preprosessing.Converters import *
from FirstPass.TextExtraction import *
from NamedEntityExtraction.Personal_Info_Extraction import *
from NamedEntityExtraction.OrganizationNameExtraction.OrganisationExtraction import *
from Utils import NER_name
from NamedEntityExtraction.AddressExtraction import *
from NamedEntityExtraction.Skills_Extraction import *
def main_parse(file=None):
    """
        Function executed upon a parsing request and returns a XML Tree of extracted Information.
    """
    if file:
       try:
            #Convert the file to pdf
            doc_converter_obj = DocumentConverter()
            pdf_file = doc_converter_obj.converttopdf(file)
            #Extract the json content
            json_content = doc_converter_obj.converttojson(pdf_file)
            #Extract the lines from the resumes.
            text_extracted = TextExtraction(json_content).getLines()
            #Extract the features from a line.
            feature_text_extracted = FeatureExtraction(text_extracted).get_feature_list()
            #Extract the Sections.
            sections_extracted = SectionExtractor(feature_text_extracted).getSections()
            #Reverse Map Sections.
            reverse_mapped_sections = ReverseMapper(sections_extracted).reverseMap()
            print reverse_mapped_sections.keys()
            #Extract personal_info
            		
            #if reverse_mapped_sections.has_key("PERSONAL_INFORMATION"):
             #   personal_section = reverse_mapped_sections["PERSONAL_INFORMATION"]
	#	personal_info_extracted_entities = Personal_Info_Sections(personal_section,file).extract_personal_info_entites()
         #       print personal_info_extracted_entities
          #      address_extraction = AddressExtraction(personal_section).get_address()
           #     print "ADDRESS", address_extraction
            #Extract Work Experience Info
            #Skills Extraction
            if reverse_mapped_sections.has_key("SKILL"):
                skill_list = reverse_mapped_sections["SKILL"]
		print "SKILLS:\n", '\n'.join(skill_list.split("#"))


       except Exception as e:
           print e
           logging.info("Error Discovered.")
           pass

    else:
       logging.info("Enter a Valid Message")


file = "/home/likewise-open/PUNESEZ/rohitangsu.das/CV/4himanshumishra@gmail.com.doc"
main_parse(file)
