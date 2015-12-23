__author__ = 'sameer.pidadi'


from pysimplesoap.client import SoapClient, SoapFault
import os


#create a simple consumer
client = SoapClient(
    location = "http://104.155.235.252:8088/",
    action = 'http://104.155.235.252:8088/', #SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    #trace = True,
    ns = False,

)

# client = SoapClient(
#     location = "http://localhost:8088/",
#     action = 'http://localhost:8088/', #SOAPAction
#     namespace = "http://example.com/sample.wsdl",
#     soap_ns='soap',
#     #trace = True,
#     ns = False,
#
# )
# call the remote method


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
    response = client.Filehandler(filedata=data, filename=name)

    # extract and convert the returned value
    result = response.parsedData

    print result



