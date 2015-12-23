from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from Config.ConfigReader import ConfigReader
import xml.etree.cElementTree as ET
import parse
import datetime
import logging
from  Preprosessing.PDFExtractor import *
from Preprosessing.Converters import *

logging.basicConfig(filename=ConfigReader.LOG,
                    level=logging.INFO, format='%(asctime)s %(message)s',
                    )



def filehandler (filedata, filename):
    time_stamp = datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
    filename_arr = filename.split('.')
    if(len(filename_arr) < 2):
        return -1

    filename_arr[-2] = filename_arr[-2] + "_" + str(time_stamp)
    filename_unique = '.'.join(filename_arr)
    logging.info("FILENAME :" + filename_unique)

    path = ConfigReader.ResumeDir
    fh = open(path+'/'+filename_unique, "wb")
    fh.write(filedata.decode('base64'))
    fh.close()
    filepath = path + "/" + filename_unique
    print "PATHS",filepath
    print "File saved at ", path,"\t", filename_unique
    if filename_unique.endswith("docx") or filename_unique.endswith("doc"):
        logging.info("Converting "+filename_unique+" to Pdf ..........")
        print "Converting ",filename_unique," to Pdf .........."
        filepath = DOCtoPDFConverter().convert(path+'/'+filename_unique)
        logging.info("Converted")
        print "Converted"

    xml_str = parse.getHRXML(filepath)
    print xml_str
    logging.info("Parsed tree..." + xml_str)


    print "Parsed tree...", xml_str
    return xml_str

dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:8088/",
    action = 'http://localhost:8088/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    # trace = True,
    ns = True)


dispatcher.register_function('Filehandler',filehandler,
                             returns= {'parsedData': str},
                             args = {'filedata':str,'filename':str})


print "Starting server..."
httpd = HTTPServer(("", 8088), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()