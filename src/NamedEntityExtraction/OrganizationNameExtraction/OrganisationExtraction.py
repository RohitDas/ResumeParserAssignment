""" THis File contains the class and methods for Feature Extraction  and for predicting   Organization Names from sentences"""


from NamedEntityExtraction.OrganizationNameExtraction.stringcrf2 import *
from arsenal.nlp.annotation import fromSGML, extract_contiguous
from arsenal.iterextras import partition, iterview
from Gazzetteers.CityNameGazzetter.readcitynames import *
from FirstPass.SectionExtraction import *
from Preprosessing.Converters import *
from NamedEntityExtraction.OrganizationNameExtraction.country_name import CountryNamesGazzetter

class OrgNameExtraction:
    """
        Class contains all the functionalities to extract except Organization names and also Location of Comapany , Duration in the company
        and also the Designation in the comapany.
    """
    class Token(object):
        """
            The Token Class.
        """
        def __init__(self, form, position):
            self.form = form
            self.attributes = []
            self.position = position
        def add(self, features):
            """ Add features to this Token. """
            self.attributes.extend(features)


    def __init__(self,workexpsection):
        # Load the CRF Model
        self.model = StringCRF.load(ConfigReader.CRFModelFilePath)
        self.workexpsection = workexpsection
        self.companynames = []
        self.duration = []
        self.location = []
        self.designation = []
        self.other =[]
        self.groupinfo = []


    def predictparagraph(self):
        """
              Step1: Split the WorkExpSection .
              Step2: Token each line and partition the data in proportion 1:0
              Step3: Predict each line by applying the CRF Model on the list of tokens .
              Step4: Get the different information from the predicted result.
        """

        sentences = self.workexpsection.split("\n")
        sentences = filter(lambda x: x.strip() != '', sentences)
        print "********************************"
        print sentences
        #Get the list of instances.
        [instances,nothing] = partition(map(self.tokenize,sentences),[1.0,0.0])
        predictedresult = map(self.predict,instances)
        self.getInfo(instances,predictedresult)
        #self.relate(instances,predictedresult)


    def tokenize(self,line):
        """ This function takes a sentence and tokenizes it. """
        #Break the line into tokens.
        WhitespaceLexer = re.compile('[\w\(\)\.\-]+')
        tokenlist = self.getTokenList(WhitespaceLexer.findall(line))
        if tokenlist:
            x, y = zip(*tokenlist)
            self.preprocessing(x)
            return Instance(x,truth=y)
        else:
            pass

    def preprocessing(self,s):

        """ Run instance through feature extraction. """
        s[0].add(['first-token'])
        s[-1].add(['last-token'])

        for tk in s:
            tk.add(self.featureExtraction(tk))
        if 1:
            # previous token features
            for t in xrange(1, len(s)):
                s[t].add(f + '@-1' for f in self.featureExtraction(s[t-1]))
            # next token features
            for t in xrange(len(s) - 1):
                s[t].add(f + '@+1' for f in self.featureExtraction(s[t+1]))
        return s


    def featureExtraction(self,token):
        """
            Feature Extractor that takes as an input a token and returns a list of extracted features.
            Features Extracted:
                               1. Word
                               2. Simpilified Word
                               3. Position of the word in the sentence
                               4. Company Suffix Feature
                               5. Preposition
                               6. Punctuation
                               7. Camel Case Feature
                               8. SingleQuote Feature
                               9. Month
                               10. City
                               11. Any Non-ALpha Numeric Characters.

        """
        word = token.form
        position = token.position

        yield 'word=' + word
        yield 'simplified=' + re.sub('[0-9]', '0', re.sub('[^a-zA-Z0-9()\.\,]', '', word.lower()))
        #Position Feature.
        yield 'position=' + str(position)
        #Designation Feature
        yield 'designation=' + str(self.get_desig_feature(word))
        #Company Suffix Feature
        yield 'company_suffix_present=' + str(self.get_company_prefix_features(word))
        #Preposition Feature
        yield 'preposition_feature=' + str(self.get_prepositon_feature(word))
        #punctuation(specially used for end marker),
        yield 'punctuation=' + str(self.get_punctuation_feature(word))
        #camel case
        yield 'camel_case_feature=' + str(self.get_camel_case_feature(word))
        #Single Quote Feature.
        yield 'singlequote_feature=' + str(self.get_single_quote_feature(word))
        #Mnth Feature
        yield 'mnth_feaure=' + str(self.get_mnth_feature(word))
        #City Feature
        yield 'city_feature=' + str(self.get_city_feature(word))
        #Digit Feature
       # yield 'digit_feature=' + get_digit_feature(word)
        for c in re.findall('[^a-zA-Z0-9]', word):  # non-alpha-numeric
            yield 'contains(%r)' % c


    def getInfo(self,x,y):
       """ It populates the respective instance variables from the predicted result."""


       for i in range(0,len(x)):
           sequence = x[i].sequence if x[i] else None
           if sequence:
               print sequence
               line = ""
               fp =open('/home/likewise-open/PUNESEZ/rohitangsu.das/ResumeParser/src/Utils/OrganizationNameExtraction/CRFdataset.dat','a')
               for span in y[i]:
                   # print span.label,'\t', ' '.join([z.form for z in sequence[span.begins:span.ends]])
                   if span.label == "COMPANY_NAME":
                       line += "<COMPANY_NAME>" + (' '.join([z.form for z in sequence[span.begins:span.ends]])).strip() + "</COMPANY_NAME>"
                       self.companynames.append(' '.join([z.form for z in sequence[span.begins:span.ends]]))
                   if span.label == "DURATION":
                       line += "<DURATION>" + (' '.join([z.form for z in sequence[span.begins:span.ends]])).strip() + "</DURATION>"
                       self.duration.append(' '.join([z.form for z in sequence[span.begins:span.ends]]))
                   if span.label == "DESIG":
                       line += "<DESIG>" + (' '.join([z.form for z in sequence[span.begins:span.ends]])).strip() + "</DESIG>"
                       self.designation.append(' '.join([z.form for z in sequence[span.begins:span.ends]]))
                   if span.label == "LOCATION":
                       line += "<LOCATION>" + (' '.join([z.form for z in sequence[span.begins:span.ends]])).strip() + "</LOCATION>"
                       self.location.append(' '.join([z.form for z in sequence[span.begins:span.ends]]))
                   if span.label == "O":
                       line += "<O>" + (' '.join([z.form for z in sequence[span.begins:span.ends]])).strip() + "</O>"
                       self.other.append(' '.join([z.form for z in sequence[span.begins:span.ends]]))

               fp.write(line)
               fp.write("\n<NEWREFERENCE>\n")
               fp.close()
               print line


    def relate(self,sequence,label):
        """ This Function relates the different extracted Info.  """
        map(self.relateAux,sequence,label)



    def relateAux(self,x,y):
        """ Auxillary Function for the relate function.  """
        pass



    def predict(self,tokenlist):
        """ Takes a list of Tokens and returns the prediction on the data. """

        for i, x in enumerate(iterview([tokenlist])):
            if x:
                predict = extract_contiguous(self.model(x))
            else:
                return None
        return predict


    def getTokenList(self,tokenlist):
        """             Auxillary Function.         """
        iterator = 0
        Tokenlist = []
        for x in tokenlist:
            Tokenlist.append((self.Token(x,iterator),"O"))

        return Tokenlist


    def get_company_prefix_features(self,word):
        """  THis checks for common ending prefixes   """
        search = companynameRegxOrg.search(word)
        if search:
            return  True
        return  False


    def get_prepositon_feature(self,word):
        """ Checks whether the word contains the Preposition Feature. """
        match = PrepRegxOrg.match(word)
        if match and match.group().strip():
           return  True
        return  False

    def get_camel_case_feature(self,word):
        """ Checks whether the word contains the Camel Case Feature. """
        if word[0].isupper():
            return True
        return  False

    def get_desig_feature(self,word):
        """ Checks whether the word contains the Designation Feature. """
        match = DesigRegxOrg.match(word)
        if match:
            return True
        return False

    def get_punctuation_feature(self,word):
        """ Checks whether the word contains the Punctuation Feature. """
        match = EndMarkerRegxOrg.match(word[-1])
        if match:
            return True
        return False

    def get_single_quote_feature(self,word):
        """ Checks whether the word contains the Single Quote Feature Feature. """
        if "'" in word:
            return True
        else:
            return False

    # Newly Added Feature.
    def get_year_feature(self, word):
        """
            More of a Duration Feature, year should be in the interval 1950 and less than the current year.
        """
        #Year Feature
        year_regx = re.compile('\d+', re.IGNORECASE)
        match = year_regx.match(word)
        if match:
            probable_year = int(match.group(0))
            print match.group(0)
            if probable_year >= 1900 and probable_year <= 2016:
                return True
            else:
                return False

    # Newly Added Feature.
    def get_location_feature(self, word):
        """
            A Location can be a city or a state.
        """
        if CountryNamesGazzetter().countryGazzatter.has_key(word.upper()):
            return True
        if CountryNamesGazzetter().capitalGazzatter.has_key(word.upper()):
            return True
        return False

    def get_mnth_feature(self,word):
        """ Checks whether the word contains the Month Feature. """
        match = mnthRegexOrg.match(word)
        if match:
            return True
        return False

    def get_digit_feature(self,word):
        """ Checks whether the word contains the Digit Feature. """
        digit_list = re.findall('([0-9])',word)
        if digit_list:
           return True
        return False




    def get_city_feature(self,word):
        """ Checks whether the word contains the City Feature Feature. """
        word = word.strip().upper()
        return CityGazzatteer().CityNameGazzatter.has_key(word)

    def getCompanyName(self):
        """Get function that returns the list of extracted company names."""
        return self.companynames

    def getLocation(self):
        """Get function that returns the list of extracted location names."""
        return self.location

    def getDuration(self):
        """Get function that returns the list of extracted duration names."""
        return self.duration

    def getDesignation(self):
        """Get function that returns the list of extracted designation names."""
        return self.designation

    def getOther(self):
        """Get function that returns the list of extracted other names."""
        return self.other

    def getinfo(self):
        """Get function that returns the list of extracted related  groups among the comapany,duration,desig,location."""
        return self.groupinfo





class WorkExpFilter:
    """             This class contains the heuristics that limits the lines for the OrgNameExtractor to run on.    """
    def __init__(self,workexpsection):
        self.workexpsection = workexpsection.split("\n")

    def getFilteredSection(self):
        """  Filter Function that runs a validation check on the lines ,If the validation check on the lines."""
        return '\n'.join([x for x in map(self.validate, self.workexpsection) if x])

    def validate(self,line):
        """
            Validation Check
        """
        if len(line.split()) > 12 : return None
        else: return line


def getOrgName(file=None):
   """ Function to fetch the organization names. """
   if file:
       file = DocumentConverter().converttopdf(file)
       list2 = SectionExtractor(DocumentConverter().return_json(file)).getfeaturedtext()
   # print [x for (x,y) in list2]
       reversedMapdict = list2
       workexp = ""
       if reversedMapdict.has_key("WORK_EXPERIENCE") :
            workexp = reversedMapdict["WORK_EXPERIENCE"]
            print workexp
       if reversedMapdict.has_key("PROJECTS"):
           projects = reversedMapdict["PROJECTS"]
       if reversedMapdict.has_key("EDUCATION"):
           others = reversedMapdict["EDUCATION"]
           print others
   else:
       #Read the input file.
       workexp = open("input","r").read()


   # Refine the WorkExp Section.
   # filteredworkexpsection = WorkExpFilter(workexp).getFilteredSection()

   #Load the CRF Module
   if workexp:
       print workexp
       object =  OrgNameExtraction(workexp)
       object.predictparagraph()
       print "Group:", object.getinfo()
       print "Company:\n", object.getCompanyName()
       print "Desig:\n", object.getDesignation()
       print "Location:\n", object.getLocation()
       print "Duration:\n",object.getDuration()
       return
   else:
        print "Work Experience Section not extracted"


if __name__ ==  "__main__":


   # workexp = open("input","r").read()
   # print workexp
   # # filteredworkexpsection = WorkExpFilter(workexp).getFilteredSection()
   # #Load the CRF Module
   # # print "FIltered Section: ", filteredworkexpsection
   object =  OrgNameExtraction("sdvfsgwbgqffq")
   object.predictparagraph()
   # lsCommand=subprocess.Popen("ls /home/likewise-open/PUNESEZ/rohitangsu.das/CV/*.pdf",stdout=subprocess.PIPE,shell=True)
   # outString=lsCommand.communicate()[0]
   # for file in outString.split("\n"):
   #     try:
   #       print file
   #       getOrgName(file)
   #       print "\n\n"
   #     except Exception as e:
   #         pass