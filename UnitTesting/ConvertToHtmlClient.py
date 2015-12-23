__author__ = 'rohitangsu.das'
__author__ = 'sameer.pidadi'


from pysimplesoap.client import SoapClient, SoapFault
import os


#create a simple consumer
client = SoapClient(
    location = "http://104.155.235.252:9001/",
    action = 'http://104.155.235.252:9001/', #SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    #trace = True,
    ns = False,

)
#
# client = SoapClient(
#     location = "http://localhost:9001/",
#     action = 'http://localhost:9001/', #SOAPAction
#     namespace = "http://example.com/sample.wsdl",
#     soap_ns='soap',
#     #trace = True,
#     ns = False,
#
# )
#call the remote method

file_dir = '/home/likewise-open/PUNESEZ/rohitangsu.das/datastore/'
for file in os.listdir(file_dir):
    print file
    #path = "/tmp/resume.pdf"
    path =file_dir+file
    f = open(path,'rb')
    data = f.read().encode("base64")
    name = path.split('/')[-1]
    print name
    #credentials = {'username': 'Searce', 'userkey': 'Aasdf01'}
    response_1 = client.ConverttoHtml(uploaded_file_name=name, uploaded_file_value=data)
    # extract and convert the returned value
    result = response_1.path
    print "RESPONE 4: ", str(result).decode("base64")


    #print result



