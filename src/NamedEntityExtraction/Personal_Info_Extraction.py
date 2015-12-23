from Utils.DateConverter import *
import logging
import nltk
from Gazzetteers.NameGazzetter.NamesGazzetter import *


class Personal_Info_Sections:
    """
        This function extracts the named entities from the Personal Information section
    """
    def __init__(self,personal_info=None, file_name = None):
        self.personal_info = personal_info
        self.fileName = file_name
        self.name = None
        self.email = None
        self.phone = None
        self.dob = None
        self.others = []

    def extract_personal_info_entites(self):
        """
            This extracts the Name, DOB etc form the Personal Information Section
        """


        #Extract only the Personal Information Portion.
        personal_info_sections = ["FIRST_SECTION_OF_RESUME", "PERSONAL INFORMATION", "PERSONAL DETAIL", "PERSONAL DETAILS",
                                  "PERSONAL PROFILES", "PERSONAL DOSSIER", "PERSONAL PROFILE","PERSONAL VITAE","PERSONAL DATA", "PERSONAL SNIPPETS","CONTACT DETAILS","PERSONAL PARTICULAR","PERSONAL PARTICULARS","PERSONAL INFORMAIION","PERSONAL MEMORANDA"
                                  ,"OTHER DETAIL","OTHER DETAILS"]

        phoneNumberExtracted = False
        emailAddressExtracted = False
        nameExtracted = False
        dobExtracted = False
        allExtracted = False
        locationExtracted = False
        genderExtracted = False
        fatherNameExtracted = False
        motherNameExtracted = False
        maritalNameExtracted = False
        nationalityExtracted = False
        languagesExtracted = False
        passportExtracted = False
        licenseExtracted = False
        panExtracted = False
        addressExtracted = False
        probableNameFromFileName = None
        probableNameFromSection = None
        probableNameFromEmail = None
        probable_mobiles = []
        probable_emails = []
        probableName = ""
        possibleLocation = ""
        gender = ""
        fathername = ""
        mothername = ""
        maritalstate =""
        nationality = ""
        languages = ""
        passportno = ""
        licenseno = ""
        panno = ""
        tmeinextrname = 0

        splitPath = self.fileName.split("/")
        if len(splitPath):
            fileName = splitPath[len(splitPath)-1]
        probableNameFromFileName = self.getNameFromFileName(fileName)

        #Years of Experience Extraction.
        possibleYrsOfExp = self.getYrsFromFileName(self.fileName)


        #Location from File_name.
        possibleLocation = self.getLocation(fileName,self.personal_info)

        if possibleYrsOfExp:
            logging.info("YRS OF EXP :" + str(possibleYrsOfExp))

        #Second Pass
        personal_info = junkCharactersRemoveRegx.sub("", self.personal_info)

        #Remove common words not appearing in name, email, ph
        personal_info = extraHeadersRemoveRegx.sub("", personal_info)

        #Replace tabs and 4 white spaces with a new Line.
        personal_info = replaceTabsRegx.sub(" * ", personal_info)

        #Iterate over each line of section and find name, email and ph
        for line in personal_info.split("\n"):
            line = line.strip()
            if not line:
                continue
            if not emailAddressExtracted:
                    email = ""
                    lineparts = notemailRegx.split(line)
                    for linepart in lineparts:
                        emailRes = emailRegx.search(linepart)
                        if emailRes:
                                email = emailRes.group().strip()
                                if email:
                                    logging.info("Email : " + email)

                                    probable_emails.append(email)
                                    emailAddressExtracted = True



            if not phoneNumberExtracted:
                    contact_number = ""
                    lineparts =  notphonenoRegx.split(line)

                    for linepart in lineparts:
                        noRes = phonenoRegx.search(linepart)
                        if noRes:
                            contact_number = noRes.group().strip()
                            contact_number = removebrackethypenRegex.sub("",contact_number).strip()
                            #Find whether there is a balanced parenthesis
                            if len(re.findall(r'\([^\)]*\)',contact_number)) == 0:
                                #Replace all the parenthesis from the ends.
                                contact_number = contact_number.replace("(","").replace(")","")

                            if len(re.findall(r'\d', contact_number)) >= 10:
                                logging.info("NUMBER :" + contact_number)
                                probable_mobiles.append(contact_number)
                                phoneNumberExtracted = True

            if not dobExtracted:
                    probable_dob = ""
                    if "birth" in line.lower() and re.search(r'birth\W', line, re.IGNORECASE):
                        probable_dob = dateOfBirthRearCleaningRegex.sub("", dateOfBirthFrontCleaningRegex.sub("",line))
                        print probable_dob
                        probable_dob = DateConverter(probable_dob).getDate()
                        logging.info("STANDARD DOB :" + probable_dob)
                        dobExtracted = True

                    if "DOB" in line or "Dob" in line or "d.o.b" in line.lower() or "d-o-b" in line.lower():
                        probable_dob = dateOfBirthRearCleaningRegex.sub("", dobFrontCleaningRegex.sub("",line))
                        print probable_dob
                        probable_dob = DateConverter(probable_dob).getDate()
                        logging.info("STANDARD DOB :" + probable_dob)
                        dobExtracted = True


            #Name Extraction.
            # The general assumption is that the Name of the applicant occurs in First Few Lines of a Resume.
            # We consider lines less than 6 words , As name cannot be more than six.
            # We POS Tag it and we select the first 3 consective NN* words .
            if not nameExtracted :
                    probableNameFromSection = ""
                    junkStrippedline = removeJunktillAphaRegx.sub("",line)
                    words = junkStrippedline.split()
                    if len(words) < 7:

                        #tag words
                        taggedWords = nltk.pos_tag(words)

                        if len(taggedWords) > 1 and taggedWords[1][1].startswith("N") :
                            if len(taggedWords) > 2 and  taggedWords[2][1].startswith("N"):
                                    probableNameFromSection = taggedWords[0][0] + " " + taggedWords[1][0] + " " + taggedWords[2][0]
                            else:
                                    probableNameFromSection = taggedWords[0][0] + " " + taggedWords[1][0]
                        else:

                            if  len(taggedWords) > 0 and taggedWords[0][1].startswith("N"):
                                probableNameFromSection = taggedWords[0][0]

                        probableNameFromSection = probableNameFromSection.strip()
                        if probableNameFromSection:
                            probableNameFromSection = re.sub(r'\W'," ",probableNameFromSection).replace("  "," ")
                            nameExtracted = True

            if not genderExtracted:

                    gendermatchobject = GenderRegx.match(line)
                    if gendermatchobject:
                            gender = gendermatchobject.group(3).strip()
                            genderExtracted = True

            if not fatherNameExtracted:
                    fathernamematchobject = FatherNameRegx.match(line)
                    if fathernamematchobject:
                        fathername = fathernamematchobject.group(2).strip()
                        fatherNameExtracted = True

            if not motherNameExtracted:

                    mothernamematchobject = MotherNameRegx.match(line)
                    if mothernamematchobject:
                        mothername = mothernamematchobject.group(2).strip()
                        motherNameExtracted = True

            if not maritalNameExtracted:
                    maritalstatusobject = MaritalNameRegx.match(line)
                    if maritalstatusobject:
                        maritalstate = maritalstatusobject.group(2).strip()
                        maritalNameExtracted = True

            if not nationalityExtracted:
                    nationalityobject = NationalityNameRegx.match(line)
                    if nationalityobject:
                        nationality = nationalityobject.group(2).strip()
                        nationalityExtracted = True

            if not languagesExtracted:
                    languagesobject =LanguagesRegx.match(line)
                    if languagesobject:
                        languages = languagesobject.group(2).strip()
                        languagesExtracted = True

            if not passportExtracted:
                    passportobject =PassportRegx.match(line)
                    if passportobject:
                        passportno = passportobject.group(2).strip()
                        passportExtracted = True

            if not licenseExtracted:
                    licenseobject =LicenceRegx.match(line)
                    if licenseobject:
                        licenseno = licenseobject.group(2).strip()
                        licenseExtracted = True

            if not panExtracted:
                    panobject = PanNumberRegx.match(line)
                    if panobject:
                        panno = panobject.group(2).strip()
                        panExtracted = True

            if phoneNumberExtracted and emailAddressExtracted and nameExtracted and dobExtracted and genderExtracted and fatherNameExtracted and mothernamematchobject and maritalNameExtracted and nationalityExtracted and languagesExtracted and passportExtracted and licenseExtracted and panExtracted:
                    allExtracted = True
                    break
        #Create List.

        listHR = []

        if emailAddressExtracted and probable_emails:

            try:
                probableNameFromEmail = re.match(r'(.*)@.*',probable_emails[0]).group(1)
            except Exception as e:
                probableNameFromEmail = probable_emails[0]
            probableNameFromEmail = re.sub(r'\s+', " ", re.sub(r'\W', " ",probableNameFromEmail))
        nameExtracted = True

        if nameExtracted:
           list = self.decideName(probableNameFromFileName,probableNameFromSection,probableNameFromEmail)
           print list
           print "TIME TO EXTRACT NAME(sec):\t" , tmeinextrname
           FirstName =  list[0]
           LastName = ""
           if len(list) > 1:
               LastName = " ".join(list[1:])

           listHR.append(("GivenName", FirstName))
           if LastName:
                listHR.append(("FamilyName", LastName))


        if emailAddressExtracted:
            if probable_emails:
               listHR.append(("Email",','.join(probable_emails)))

        if phoneNumberExtracted:
            if probable_mobiles:
                listHR.append(("Mobile",','.join(probable_mobiles)))

        if dobExtracted:
            listHR.append(("DateOfBirth",probable_dob))

        if possibleYrsOfExp:
            listHR.append(("YrsOfExp",str(possibleYrsOfExp)))

        if possibleLocation:
           listHR.append(("Location", possibleLocation))

        if gender:
            listHR.append(("gender",str(gender)))

        if fathername:
            listHR.append(("FatherName",str(fathername)))

        if mothername:
            listHR.append(("MotherName",str(mothername)))

        if maritalstate:
            listHR.append(("MaritalState",str(maritalstate)))

        if nationality:
            listHR.append(("Nationality",str(nationality)))

        if languages:
            listHR.append(("Languages",str(languages)))

        if passportno:
            listHR.append(("PassportNo",str(passportno)))

        if licenseno:
            listHR.append(("LicenseNo",str(licenseno)))

        if panno:
            listHR.append(("PanNo",str(panno)))



        return listHR

    def decideName(self,name1,name2,name3):
        # print name1
        # print name2
        # print name3

        #Preprocess the names to remove non-Alphanumeric and numbers from the names.
        if name1: name1 = re.sub(r'\W|[0-9]'," ",name1.lower())
        if name2: name2 = re.sub(r'\W|[0-9]'," ",name2.lower())
        if name3: name3 = re.sub(r'\W|[0-9]'," ",name3.lower())
        #Split by Words and create a set.
        name1_word_list = []
        name2_word_list = []
        name3_word_list = []
        if name1:
            name1_word_list = filter(lambda x: x.strip() != "",name1.split(" "))
        if name2:
            name2_word_list = filter(lambda x: x.strip() != "",name2.split(" "))
        if name3:
            name3_word_list = filter(lambda x: x.strip() != "",name3.split(" "))

        #Aggregated the word list
        aggregrated_word_list = list(set(name2_word_list + name1_word_list + name3_word_list))
        for word in remove_unwanted_words:
            if word in aggregrated_word_list:
                index = aggregrated_word_list.index(word)
                del aggregrated_word_list[index]
        #Create counts list
        count_list = [0] * len(aggregrated_word_list)

        for word in name1_word_list:
            if word in aggregrated_word_list:
                index = aggregrated_word_list.index(word)
                count_list[index] += 1

        for word in name2_word_list:
            if word in aggregrated_word_list:
                index = aggregrated_word_list.index(word)
                count_list[index] += 1

        for word in name3_word_list:
            if word in aggregrated_word_list:
                index = aggregrated_word_list.index(word)
                count_list[index] += 1


        #Extra Step Added to increase Accuracy.
        for word in list(set(name1_word_list+name2_word_list)):
            joined_email = ' '.join(name3_word_list)
            if word in joined_email:
                index = aggregrated_word_list.index(word)
                count_list[index] += 1

        for word in list(set(name1_word_list+name2_word_list)):
            joined_email = ' '.join(name3_word_list)
            if word in joined_email:
                index = aggregrated_word_list.index(word)
                count_list[index] += 1
        #Name Gazzetter check , weight to be assigned is 2.
        for word in aggregrated_word_list:
            if word in NamesGazzatteer().namesGazzatter.keys():
                index = aggregrated_word_list.index(word)
                count_list[index] += 2

        # for word in aggregrated_word_list:
        #     print "WORD: ", word, " COUNT: ", count_list[aggregrated_word_list.index(word)]
        #Take the 2 Max Counts .
        max_word_1 = None
        max_word_2 = None
        name_list = []
        print count_list
        max_count_1 = count_list.index(max(count_list))
        del count_list[max_count_1]
        name_list.append(aggregrated_word_list[max_count_1])
        del aggregrated_word_list[max_count_1]
        if count_list:
            max_count_2 = count_list.index(max(count_list))
            name_list.append(aggregrated_word_list[max_count_2])
        return name_list


    """ Function that takes a filename and extracts the name of the applicant from the filename"""

    def getNameFromFileName(self,file_name):
        #Remove all characters after @
        try:
            file_name = re.match(r'(.*)@.*',file_name).group(1)
        except Exception as e:
            pass
        # Split the name based on the delimeters.
        splittedWords  = re.sub(r'\s+', " ", re.sub(r'(\||\-|_|\.|\[|\]|@|[0-9])', " ", file_name)).split()
        # Remove junk words from the splitted words.
        current_index =  0
        while current_index < len(splittedWords):
            if splittedWords[current_index].upper() in removeJunkWordsInFileName.keys():
                del splittedWords[current_index]
            else:
                current_index =  current_index + 1

        #Print the first 2 elements of the array.
        if len(splittedWords) > 1 and (not splittedWords[0].isdigit()) and (not splittedWords[1].isdigit()):
            return splittedWords[0] + " " + splittedWords[1]
        else:
            return ""



    """ Helper Function to check whether a string actually represents a Float Value or Not. """
    def isfloat(self,value):
      try:
        float(value)
        return True
      except ValueError:
        return False


    """ Function that takes a filename and extracts the number of years of experience from the filename  """

    def getYrsFromFileName(self,file_name):
        #remove filename extensions
        file_name = re.sub('\.(docx|doc|pdf)', "", file_name)

        # Split the name based on the delimeters.
        splittedWords  = re.sub(r'\s+', " ", re.sub(r'(\||\-|_|\[|\])', " ", file_name)).split()
        for curIndex in range(len(splittedWords)):
            word = splittedWords[curIndex].upper()

            #if a field before/after 'yrs', 'exp' etc word is float, convert to month.
            if possibleYRSOfExpInFileName.has_key(word):
               yrs_field = ""
               if curIndex and self.isfloat(splittedWords[curIndex-1]) and float(splittedWords[curIndex-1]) < 50:
                    yrs_field = splittedWords[curIndex-1]
               elif curIndex+1 < len(splittedWords) and self.isfloat(splittedWords[curIndex+1]) and float(splittedWords[curIndex+1]) < 50:
                    yrs_field = splittedWords[curIndex+1]
               if yrs_field:
                    yr_parts = yrs_field.split(".")
                    logging.info(yr_parts)
                    total_exp = int(yr_parts[0])*12
                    if len(yr_parts) > 1:
                        total_exp += int(yr_parts[1])
                    return total_exp
               else:
                    return ""


    def getLocationfromFileName(self,file_name):
        splittedWords  = re.sub(r'\s+', " ", re.sub(r'(\||\-|_|\[|\])', " ", file_name)).split()
        for words in splittedWords:
            listoflocations = CityRegx.findall(words)
            if listoflocations:
                return listoflocations[0][1]
        return ""

    '''Extract location from Personal Info or work experience'''
    def extractLocationFromString(self,workexpsection):
         for line in workexpsection.split('\n'):
            listoflocations = CityRegx.findall(line)
            if listoflocations:
               return listoflocations[0][1]

         return None

    def getLocation(self,filename,section):
        # Check from File Name
        possiblelocation = self.getLocationfromFileName(filename)

        if not possiblelocation:
        #Check for Personal Info
           possiblelocation = self.extractLocationFromString(self.personal_info)

        # #Check from Work Exp
        # if not possiblelocation:
        #     if section.has_key("WORK EXPERIENCE"):
        #         possiblelocation = self.extractLocationFromString(section["WORK EXPERIENCE"])

        return possiblelocation


    def get_name(self):
        """
            Get the name.
        """
        return self.name

    def get_email(self):
        """
            Get the Email List.
        """
        return self.email

    def get_number(self):
        """
            Get the Phone numbers
        """
        return self.phone

    def get_dob(self):
        """
            Get the Date of Births.
        """
        return self.dob

    def other_info(self):
        """
            Returns secondary information like Mother's name, Father's name, ,PAN CARDs etc
        """
        return self.others