from Utils.CommonRegx import  *
from Gazzetteers.CityNameGazzetter.readcitynames import *


class AddressExtraction:
    def __init__(self,personalInfo):
        self.personalInfo = personalInfo

    def get_address(self):

        namelineignored = False
        addressextracted = False
        #for section_head in self.sectiondict.keys():
        address = None
        header = self.personalInfo[0]
        section = self.personalInfo[1]
       # print "HEADER" , header , "SECTION" , section
        if header == "FIRST_SECTION_OF_RESUME":
            # Ignore the firstline of any resume because we assume that it has to be a name
            section = extraHeadersRemoveRegx.sub("", section)
            lines = section.split("\n")
            lines = [i for i in lines if i.strip()]
            if lines:
                del lines[0]
            namelineignored = True
            section = '\n'.join(lines)

        list =  ColonRegx.findall(section)
        if header != "FIRST_SECTION_OF_RESUME":
        #print list
            for (a,b,c,d) in list:
                if not addressRegx.findall(b) and not ("," in b)  and (not CityGazzatteer().CityNameGazzatter.has_key(b.strip().upper())):
                   section  = section.replace(a," ")



        #print section
        #Remove all the : stuff from the personal section.


        #Separate the ones with a mobile header.
        section = emailregx.sub(" ",section)

       # print "*******************", section
        #Do not delete the pincode.
        section= mobileregx.sub(" ",section)
       # print "SECTION",header , section
      #  print "___________________________" ,section

        #Separate without the headers.
        section = emailRegx.sub(" ",section)
       # print section

        mobilegroup = phonenoRegx.match(section)
        if mobilegroup:
            if len(re.findall(r'\d', mobilegroup.group().strip())) > 6:
                 section = section.replace(mobilegroup.group().strip()," ")

        #Possible Catch Words Check.
        #print "CATCH WORDS", AddressCatchWordRegx.findall(section)

        #Read the line one by one , ending with a number of about 6 which is the pin code.
        address = []

        #Search for a Address subsection now.
        addresssectionmatch = re.findall('(.*)(Address|Contact|Location)\s*(:\s*-|:)(.*)',section)
        if addresssectionmatch:
            #Remove the previous portions
            section = section.replace(addresssectionmatch[-1][0],"")
            #section = addresssectionmatch[-1][3]

        #print section
        addresssectiondetected = False
        for line in section.split('\n'):
            if line.strip() == "" and addresssectiondetected:
                break



            addresssectionmatchobject = re.match('(.*)(Address|Contact|Location)\s*(:\s*-|:|\-)(.*)',line,re.IGNORECASE)
            if addresssectionmatchobject:
                addresssectiondetected = True
                line = addresssectionmatchobject.group(4)

            #Look for a City Pincode pair in the line.
            citypinlist = cityPinRegx.findall(line)
           # print line , citypinlist
            if citypinlist:
                probablecityname = citypinlist[-1][1].strip().upper()
               # print probablecityname
                if CityGazzatteer().CityNameGazzatter.has_key(probablecityname):
                    address.append(line.strip())
                    break


            #End if u get a six digit pincode.
            if len(re.findall(r'\d{6}',line.strip())) > 0:
                address.append(line.strip())
                break
            address.append(line)


        #Separate the ones without the headers.
        address = "\n".join(address).strip()
        # print "ADDRESS:" , address
        if len(re.findall(r'\d',address)) <  2:
            address = None

        #print "ADDRESS =", "\n".join(address).strip()
        return address


if __name__ == "__main__":
    text = open("text","r").read()
    print AddressExtraction(text).get_address()




