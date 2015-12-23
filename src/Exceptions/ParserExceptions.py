__author__ = 'dhaval.makwana'

"""Define all exceptions here so that you can raise appropriate one and take actions later"""

class PDF2JSONError(Exception):
    """The expection is raised when pdf2json command fails"""

    def __init__(self, path):
        self.msg = "Could not convert pdf file" + path + "to json!!"

class DOC2PDFError(Exception):
    """The expection is raised when abiword command fails"""

    def __init__(self, path):
        self.msg = "Could not convert to pdf " + path + "to json!!"

class PDF2HTMLError(Exception):
    """The exception is raised when PDF2HTMLEx fails"""

    def __init__(self,path):
        self.msg = "Could not convert" + path + "to html "

class ParaExtractionError(Exception):
    """The expection is raised when paragraph extraction crashes.
    This could be due to encoding issues, illegal text processing etc"""

    def __init__(self, msg):
        self.msg = "Error while extracting paragraphs!!" \
                   "\nOriginal message = " + msg

class DOCtoPDFError(Exception):
    def __init__(self,path):
        self.msg = "Could not Convert doc file"+path+" to pdf!!"

class TextractError(Exception):
    def __init__(self,path):
        self.msg = "Could not extract text from " + path + "file!!"

class SectionExtractionError(Exception):
    """The exception is raised when we are extracting the sections and the
       program crashes"""
    def __init__(self,path):
        self.msg = "Could not extract section from the filename"

class NoFileException(Exception):
	""" The exception is raised when we are calling the parser function and it first a None filed in the file.
	"""
	def __init__(Exception):
		self.msg = "Invalid File, please enter a Valid File."
