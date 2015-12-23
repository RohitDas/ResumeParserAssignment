

__author__ = 'dhaval.makwana'


import subprocess
from subprocess import *
from Preprosessing.PDFExtractor import PDFExtractors
from Config.ConfigReader import ConfigReader
from Exceptions.ParserExceptions import *
import datetime,os
import random,tempfile



class DocumentConverter:
    """The class is abstract which defines common methods for all converters
        Possible classes inheriting this class are PDFtoJSONConverter, DOCtoJSONConverter, DOCXtoJSONConverter"""

    def __init__(self):
        pass

    def converttopdf(self,path):
        if path.endswith('.pdf'):
            return path
        elif path.endswith('.docx') or path.endswith('.doc'):
            return DOCtoPDFConverter().convert(path)
        else:
            return path

    def converttojson(self,path):
        if path.endswith('.pdf'):
            converter = PDFtoJSONConverter()
            jsoncontent = converter.convert(path)
            return jsoncontent

        elif path.endswith('.docx') or path.endswith('.doc'):
            pdfpath = DOCtoPDFConverter().convert(path)
            converter = PDFtoJSONConverter()
            jsoncontent = converter.convert(pdfpath)
            return jsoncontent

        else:
            print "WRONG FILE TYPE"

    def return_json(self,path):
        if path.endswith('.pdf'):
            converter = PDFtoJSONConverter()
            jsoncontent = converter.convert(path)
            return jsoncontent



class DOCtoPDFConverter(DocumentConverter):
     """ This class converts DOC to PDF using command line utility abiword.
        This utility has to be installed at the time of deployment"""

     def __init__(self):
        pass

     def convert(self,path):
         "Converts a doc or docx file to pdf and returns the file."

         #Create a new pdf file to store the output.
         pdfpath = path+".pdf"
         #Create the pdf file.
         try:
             subprocess.check_call(["touch",pdfpath])
         except CalledProcessError as e:
             print e.message

         #Run the Abiword shell command
         try:
             subprocess.check_call(["abiword","--to=PDF","-o",pdfpath,path])
         except CalledProcessError as e:
             raise DOC2PDFError(path)

         return pdfpath


class PDFtoJSONConverter(DocumentConverter):
    """This class converts PDF to JSON using command line utility pdftojson.
    The utility is checked into git and built at the time of deployment."""

    def __init__(self):
        pass

    def convert(self, path):
        """This method calls shell command pdf2json and returns json string"""
        resume_json_file_descriptor = tempfile.NamedTemporaryFile(delete=False)
        resume_json_file = resume_json_file_descriptor.name
        resume_json_file_descriptor.close()
        #Remove tmp file first
        try:
            subprocess.check_call(["rm", resume_json_file])
        except CalledProcessError:
            pass

        #Convert pdf file to JSON
        try:
            subprocess.check_output(["pdf2json", path, resume_json_file])
        except CalledProcessError:
            raise PDF2JSONError(path)

        #Read output tmp file and return the string
        f = open(resume_json_file, 'r')
        try:
            subprocess.check_output(["rm",resume_json_file])
        except Exception:
            print "Error Removing File"
        jsonStr = f.read()
        f.close()

        return jsonStr

class DOCtoJSONConverter(DocumentConverter):
    """This class converts MS .doc file to JSON."""

    def __init__(self):
        pass

    def convert(self, path):
        """Sameer is supposed to code this"""
        #subprocess.check_call(["rm", "/tmp/tmppycharm"])

        try:
            subprocess.check_call(["rm", "/tmp/resume.pdf"])
        except CalledProcessError:
            pass

        try:
            process = Popen(['java', '-jar', 'lib/doc(x)toPdf.jar', path, '/tmp/resume.pdf' ], stdout=PIPE, stderr=PIPE)
            response = []
            while process.poll() is None:
                line = process.stdout.readline()
                if line != '' and line.endswith('\n'):
                    response.append(line[:-1])
            stdout, stderr = process.communicate()
            response += stdout.split('\n')
            if stderr != '':
                response += stderr.split('\n')
            response.remove('')
            print response
            print "Successfully Converted!"
        except CalledProcessError:
            raise PDF2JSONError(path)

        try:
            converter = PDFtoJSONConverter()
            jsonstr = converter.convert("/tmp/resume.pdf")
        except CalledProcessError:
            raise PDF2JSONError(path)

        return jsonstr
        pass


class DOCXtoJSONConverter(DocumentConverter):
    """This class converts MS .docx file to JSON."""

    def __init__(self):
        pass

    def convert(self, path):
        """Sameer is supposed to code this"""

        try:
            subprocess.check_call(["rm", "/tmp/resume.pdf"])
        except CalledProcessError:
            pass

        try:
            process = Popen(['java', '-jar', 'lib/doc(x)toPdf.jar', path, '/tmp/resume.pdf' ], stdout=PIPE, stderr=PIPE)
            response = []
            while process.poll() is None:
                line = process.stdout.readline()
                if line != '' and line.endswith('\n'):
                    response.append(line[:-1])
            stdout, stderr = process.communicate()
            response += stdout.split('\n')
            if stderr != '':
                response += stderr.split('\n')
            response.remove('')
            print response
            print "Successfully Converted!"
        except CalledProcessError:
            raise PDF2JSONError(path)

        try:
            converter = PDFtoJSONConverter()
            jsonstr = converter.convert("/tmp/resume.pdf")
        except CalledProcessError:
            raise PDF2JSONError(path)

        return jsonstr

        pass


class PDFtoHTMLConverter(DocumentConverter):
    def __init__(self):
        pass

    def convert(self,path):
        try:
            filename = path.replace(".pdf",".html")
            subprocess.check_call(["pdf2htmlEX", path, "--dest-dir", ConfigReader.TemporaryFileLoad])
        except CalledProcessError:
            raise PDF2HTMLError(filename)
        return filename

if __name__ == "__main__":
    print PDFtoJSONConverter().convert("/home/likewise-open/PUNESEZ/sameer.pidadi/self_projects/test_profiles/upload/Abhishek_Singh_11.05_yrs.pdf")
