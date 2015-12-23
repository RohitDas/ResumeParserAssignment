import re

junkCharactersRemoveRegx = re.compile(r'[^\w\.\s,\-\@\(\)/\+:;]')

extraHeadersRemoveRegx = re.compile(r'RESUME|(Mr|Ms|Mrs)(\.|\t|\s)*|CV|^\s*Name(.*)(:|:\-)|(CURRICULUM[\s\t\-]*VITAE)|pic|actionURI\(.*?\):|reject|Email(\t\s)*(:|:\-)|Date(\s\t)*(:\:\-)|BIODATA|on hold',
                                      re.IGNORECASE)
#extraHeadersRemoveRegx = re.compile(r'RESUME|(Mr|Ms|Mrs)(\.|\t|\s)*|CV|Name(.*)(:|:\-)|(CURRICULUM[\s\t\-]*VITAE)|pic|NAME|actionURI\(.*?\):|reject|Email(\t\s)*(:|:\-)|Date(\s\t)*(:\:\-)|BIODATA',
  #                                    re.IGNORECASE)
replaceTabsRegx = re.compile(r'(\t)+|( ){4,}')

emailRegx = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b')

phonenoRegx = re.compile(r'[\s\d\+\-\(\)]{10,20}')

notphonenoRegx = re.compile(r'[^\s\d\+\-\(\)]')

notemailRegx = re.compile(r'[^\w._%\+\-@]')

removebrackethypenRegex = re.compile(r'(^[\)\s\-]*)|[\(\s\-]*$')

removeUnbalancedParenRegex = re.compile(r'(.*[^\(].*(?<![\)]))')
#                                        |\([^\)]*|[^\(]\)')

removeJunktillAphaRegx = regx = re.compile(r'^[^a-zA-Z]*')

#Date of birth extractions
#Lines having Birth words
#dateOfBirthFrontCleaningRegex = re.compile(r'^.*?birth(\W)*',re.IGNORECASE)
dateOfBirthFrontCleaningRegex = re.compile('(^.*birth.*?)(?=January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d)',re.IGNORECASE)
dateOfBirthRearCleaningRegex = re.compile(r'[^\d]*?$',re.IGNORECASE)
#Lines having DOB strings
dobFrontCleaningRegex = re.compile(r'^.*?dob(\W)*',re.IGNORECASE)

#Words present in filename.

removeJunkWordsInFileName = {'RESUME':'','OF':'','CV':'','PROFILE':'','CANDIDATE':'','CANDIDATURE':'','BIODATA':'','IT':'','BDM' : ''}


#Years of Experience.
possibleYRSOfExpInFileName = {'YRS':'','YEARS':'','YEAR':'','EXP':'','MONTHS':''}

mnthHash ={"1":'JANUARY',"2":"FEBRUARY","3":"MARCH","4":"APRIL","5":"MAY","6":"JUNE","7":"JULY","8":"AUGUST","9":"SEPTEMBER","10":"OCTOBER","11":"NOVEMBER","12":"DECEMBER"}
mnthHashModified = {"JAN":"01","JANUARY":"01","FEB":"02","FEBRUARY":"02","MAR":"03","MARCH":"03","APR":"04","APRIL":"04","MAY":"05","JUN":"06","JUNE":"06","JUL":"07","JULY":"07","AUG":"08","AUGUST":"08","SEP":"09","SEPT":"09","SEPTEMBER":"09","OCT":"10","OCTOBER":"10","NOV":"11","NOVEMBER":"11","DEC":"12","DECEMBER":"12"}

dayHash = {"1":"st","2":"nd","3":"rd"}

generalBlockHeaders = ["PERSONAL INFORMATION","OBJECTIVE","EDUCATION","WORK EXPERIENCE","PROJECTS","SKILL","QUALIFICATION","OTHERS"]

#Regex To remove Preposition form FileName
removePrepFromLineRegex = re.compile('( and )|( or )|( of )|( as )',re.IGNORECASE)

commonSectionNamesToCompare = {"PERSONAL":"PERSONAL INFORMATION", "SKILL":"SKILL", "EXPERTISE":"SKILL", "PROFICIENCY":"SKILL", "WORK":"WORK EXPERIENCE", "EXPERIENCE":"WORK EXPERIENCE", "JOB":"WORK EXPERIENCE", "EMPLOY":"WORK EXPERIENCE", "EDUCATION":"EDUCATION", "ACADEMIC":"EDUCATION", "QUALIFICATION":"EDUCATION", "KNOWLEDGE":"SKILL", "HOBBIES":"HOBBIES", "INTEREST":"INTERESTS",
                               "ACTIVITIES":"OTHERS", "ACHIEVEMENT":"OTHERS", "CERTIFICATE":"CERTIFICATE",
                               "REFERENCE":"REFERENCE", "FORTE":"SKILL", "RESPONSIBIL":"WORK EXPERIENCE", "PROJECT":"PROJECTS"}


commonSubSectionNamesToCompare = ["PHONE","MAIL","LANGUAGES","DATE","BIRTH","DOB","FATHER'S NAME","SEX","LANGUAGES","ADDRESS","E-MAIL","CONTACT","PROJECT","COMPANY","DESIGNATION","DURATION","JOB PROFILE","TEAM SIZE"
"ROLE","PROJECT DESCRIPTION","HOBBIES","LOCATION","CLIENT","MOBILE","SYNOPSIS"]


organizationNameRegx =  re.compile(r'(((VP|or|er|nt|st|ed)(\s+)(at|for|with|in|,|\-|\t|\s+3)|^)(\s*)(([A-Z]\w+\s)+)(Pvt\.*\s*Ltd\.*|Services|SERVICES|Networks|NETWORKS|Ltd|LTD|ltd|Limited|LIMITED|Solution|Solutions))')


#Designation Suffix Regular Expression
DesignationSuffixRegx = '(\w*)(VP|or|er|nt|st|ive|ions|ed)'

#Preposition Regular Expression.
PrepRegx = '(at|for|with|in|,|\-|\t|\s+3)|^)'



#CamelCase Regx
CamelCaseRegx = '(([A-Z]\w*\s*)+)'


#Company Name Marker Regx
ComapnayNameRegx = '(Pvt\.*\s*Ltd\.*|Services|SERVICES|Systems|SYSTEMS|Networks|Software|NETWORKS|Ltd|LTD|ltd|Limited|LIMITED|Solution|Solutions|Inc)'

#Messrs Regular Expression.
MessrsRegx = '(\s|M/S|M/s|MS)*'

#End Marker Regx.
EndMarkerRegx = '([^\w\d])'

#Frequent City Name
CityRegx = re.compile('(^|\W)(?P<city>Bangalore|Hyderabad|Pune|Gudgaon|Noida|Mumbai|Delhi|Chennai|Ahmedabad|Surat|Kolkata|Jaipur|Lucknow|Kanpur|Nagpur|Indore|Thane|Bhopal|Visakhapatnam|Pimpri-Chinchwad|Patna|Vadodara|Ghaziabad|Ludhiana|Agra|Nashik|Faridabad|Meerut|Rajkot|Kalyan-Dombivali|Vasai-Virar|Varanasi|Srinagar|Aurangabad|Dhanbad|Amritsar|Navi Mumbai|Allahabad|Ranchi|Howrah|Coimbatore|Jabalpur|Gwalior|Vijayawada|Jodhpur|Madurai|Raipur|Kota|Guwahati|Chandigarh|Solapur|Hubballi|Hubli|Dharwad)($|\W)')

#Gender Regular Expression.
GenderRegx = re.compile('(Sex|Gender)(\s*:\s*-|\s*:)(.*)',re.IGNORECASE)

#Father Name Regular Expression.
FatherNameRegx = re.compile('.*Father.*(:\s*-|:|\-)(.*)',re.IGNORECASE)

#Father Name Regular Expression.
MotherNameRegx = re.compile('.*Mother.*(:\s*-|:|\-)(.*)',re.IGNORECASE)

#Marital Status Regx
MaritalNameRegx = re.compile('Marital\s*Status\s*(:\s*-|:|\-)(.*)',re.IGNORECASE)

#Nationality Regx
NationalityNameRegx =  re.compile('Nationality\s*(:\s*-|:|\-)(.*)',re.IGNORECASE)

#Languages Regx
LanguagesRegx = re.compile(".*Languages.*(:\s*-|:|\-)\s*(.*)",re.IGNORECASE)

#Passport Number Regx
PassportRegx = re.compile('.*Passport.*(:\s*-|:|\-\s+)\s*(.*)',re.IGNORECASE)

#Liscencse Number Extracted.
LicenceRegx = re.compile('.*License.*(:\s*-|:)\s*(.*)',re.IGNORECASE)

#PAN Number Extracted Regx.
PanNumberRegx = re.compile('^\s*Pan.*(:|\s*-|:|\-)\s*(\w{5}\d{4}\w{1})',re.IGNORECASE)


#Regular Expressions for Address Extraction
mobileregx  = re.compile('(Mobile|Tel|Phone|Contact|Cell|Ph)(.*)(:\s*-|:|-|#|)(.*)',re.IGNORECASE)
emailregx =  re.compile('(Email|E-mail)(.*)(:\s*-|:|-|)(.*)',re.IGNORECASE)
AddressCatchWordRegx = re.compile('Society|Road|Flat|Mall|Hall|Tower|Building|Colony',re.IGNORECASE)
ColonRegx = re.compile('((.*)(:\s*-|:|\t)(.*))')
addressRegx = re.compile("Address|Location|Contact",re.IGNORECASE)
possiblesubsectioninpersonalinfo = ['Languages','Email','Mobile','Birth','Marital','Hobbies','Name','Nationality','Abilities','no','number','phone','Interests','References']
cityPinRegx = re.compile('((\w*)\s*(-|:)\s*(\d*))\s*$')



companynameRegxOrg = re.compile('(Pvt\.*\s*Ltd\.*|Services|SERVICES|Systems|SYSTEMS|Networks|Software|NETWORKS|Ltd|LTD|ltd|Limited|LIMITED|Solution|Solutions|Inc|INC)')
PrepRegxOrg = re.compile('(at|for|with|in)')
DesigRegxOrg = re.compile('(\w*)(ee|nt|ll|or|VP|GM|er|ve|an|st)')
EndMarkerRegxOrg = re.compile('(.|,|)')
mnthRegexOrg = re.compile('^(Jan[^a-zA-Z]|January|Feb[^a-zA-Z]|February|Mar[^a-zA-Z]|March|Apr[^a-zA-Z]|April|May|Jun[^a-zA-Z]|June|Jul[^a-zA-Z]|July|Aug[^a-zA-Z]|August|Sep[^a-zA-Z]|September|Oct[^a-zA-Z]|October|Nov[^a-zA-Z]|November|Dec[^a-zA-Z]|December)',re.IGNORECASE)

remove_unwanted_words = ['mobile','email','doc','docx','pdf','phone','resum','contact','address','date','com','gmail','male']

possible_skill_sub_section = re.compile('skill|expertise|databases|language|tool|technology',re.IGNORECASE)

# Utility function to clean a sentence.
def cleanLine(line):

  line = line.encode("utf8","replace").replace("|","").strip()
  line = line.strip().strip("-").strip(":").strip(":-").strip()
  line = removePrepFromLineRegex.sub(" ",line)
  line = re.sub(r'[^A-Za-z0-9:\-\+]'," ",line)
  line = re.sub(r'(\s){2,}'," ",line).strip()

  return line

