"""
This file contains resume services that can be called to do
the desired tasks. These services have a web interface as well
"""

import requests
from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
import logging
from Preprosessing.Converters import *
import os
import Exceptions
logging.basicConfig(filename=ConfigReader.HTML_LOG,
                    level=logging.INFO, format='%(asctime)s %(message)s',
                    )



def ResumeToHtml(uploaded_file_name,uploaded_file_value):

    #Store on the server.
    logging.info("Storing on server ...........")
    path = store_resume_on_server(uploaded_file_name,uploaded_file_value)
    logging.info("Succesfully stored file on server ...........")
    print "stored temp file path", path

    #Convert to pdf
    logging.info("Converting to PDF ........... : "+ path)
    path_of_converted_pdf = DocumentConverter().converttopdf(path)
    logging.info("Succesfully converted to PDF ........... :" + path_of_converted_pdf )
    print "Converted pdf path", path_of_converted_pdf

    #Convert to html.
    logging.info("Converting to html ...........")
    html_path = PDFtoHTMLConverter().convert(path_of_converted_pdf)
    logging.info("Converted to html  ...........")
    print "Converted html path", html_path

    #Build encoded string of html content
    fp = open(html_path, "r")
    # print fp.read()
    data = fp.read().encode("base64")

    #Clean up temporary files
    try:
         subprocess.check_call(["rm",path_of_converted_pdf])
         subprocess.check_call(["rm",html_path])
    except Exception as e:
         logging.info("Cannot remove file............")
    print data
    return data

def store_resume_on_server(uploaded_file_name=None,uploaded_file_value=None):

    tmp_folder_path = ConfigReader.TemporaryFileLoad
    path = os.path.join(tmp_folder_path,(uploaded_file_name).replace(" ", "").replace("(","").replace(")",""))
    fp = open(path,'wb')
    data = uploaded_file_value
    fp.write(data.decode("base64"))
    fp.close()
    return path

dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:9001/",
    action = 'http://localhost:9001/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    # trace = True,
    ns = True)




dispatcher.register_function('ConverttoHtml',ResumeToHtml,
                             returns= {'path': str},
                             args = {'uploaded_file_name':str,'uploaded_file_value':str})




print "Starting server..."
httpd = HTTPServer(("", 9001), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()


