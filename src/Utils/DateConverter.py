__author__ = 'rohitangsu.das'

from Utils.CommonRegx import  *
import re



""" This file converts a DOB date or any Date to the Standard Format ."""

class DateConverter():

    def __init__(self,date):
        self.date= re.sub('(\-|/|\.|,)' ," ",date).split()
        map((lambda x: x.strip()),self.date)

    def getDateList(self):
        return self.date

    def getDate(self):

        if len(self.date) == 3:
               return self.dateConvert()

        return '/'.join(self.date)

    #Get the modified Day
    def getDay(self,day):

        if re.search(r'\D+',day):
            day = re.sub(r'\D+','',day.strip())
        if len(day) < 2:
            day = "0" + day

        return day

    #Get the modified month.
    def getMnth(self,mnth):

        if mnth.isdigit():
            if len(mnth) < 2:
                mnth = "0" + mnth
            return mnth
        else:
            if mnthHashModified.has_key(mnth.upper()):
                return mnthHashModified[mnth.upper()]


    #Get the modified year.
    def getYrs(self,year):
        if len(year) ==  2:
            if int(year) < 20:
                year = "20" + year
            else:
                year = "19" + year
        return year

    def dateConvert(self):
        """
            Function to return the standardised date format
        """
        day_index, mnth_index, year_index = None, None, None
        #Mark the following list elements as AlphaNumeric, Numeric, Alpha
        date_list = self.date
        set_of_indices = set([0,1,2])

        #Keep a list of tags.
        tag_list = self.get_tag_list(date_list)
        print tag_list

        if "A" in tag_list:
            mnth_index = tag_list.index("A")
            if "AN" in tag_list:
                day_index = tag_list.index("AN")
                year_index = list(set_of_indices - set([mnth_index,day_index]))[0]
            else:
                #The remaining numbers are N, N.
                other_indices = list(set_of_indices - set([mnth_index]))
                number_greater_than_thirtyone_list = filter(lambda x: int(date_list[x]) > 31, other_indices)
                if len(number_greater_than_thirtyone_list) == 1:
                    year_index = number_greater_than_thirtyone_list[0]
                    day_index = list(set_of_indices - set([mnth_index,year_index]))[0]
                else:
                    remaining_indices = list(set_of_indices - set([mnth_index]))
                    year_index = remaining_indices[0]
                    day_index = remaining_indices[1]
        elif "AN" in tag_list:
            day_index = tag_list.index("AN")
            remaining_indices = list(set_of_indices - set([day_index]))
            #Rest of them are N, N
            number_greater_than_twelve_list = filter(lambda x: int(date_list[x]) > 12, remaining_indices)
            if len(number_greater_than_twelve_list) == 1:
                year_index = number_greater_than_twelve_list[0]
                mnth_index = list(set_of_indices - set([day_index,year_index]))[0]
            else:
                remaining_indices = list(set_of_indices - set([day_index]))
                year_index = remaining_indices[0]
                mnth_index = remaining_indices[1]
        else:
            #Case of All N.
            number_greater_than_thirtyone_list = filter(lambda x: int(date_list[x]) > 31, set_of_indices)
            number_greater_than_twelve_list = filter(lambda x: int(date_list[x]) > 12, set_of_indices)
            print number_greater_than_twelve_list
            if number_greater_than_thirtyone_list:
                year_index = number_greater_than_thirtyone_list[0]
                number_greater_than_twelve_but_not_greater_thirtyone = list(set(number_greater_than_twelve_list) - set(number_greater_than_thirtyone_list))
                if number_greater_than_twelve_but_not_greater_thirtyone:
                    day_index = number_greater_than_twelve_but_not_greater_thirtyone[0]
                    mnth_index = list(set_of_indices - set([day_index,year_index]))[0]
                else:
                    if year_index == 0:
                        mnth_index = 1
                        day_index = 2
                    else:
                        remaining_indices = list(set_of_indices - set([year_index]))
                        day_index =  remaining_indices[0]
                        mnth_index = remaining_indices[1]
            elif number_greater_than_twelve_list:
                #List can be of length 2 or 1 or 0
                if len(number_greater_than_twelve_list) == 2:
                    mnth_index = list(set_of_indices - set(number_greater_than_twelve_list))[0]
                    year_index = number_greater_than_twelve_list[0]
                    day_index = number_greater_than_twelve_list[1]
                else:
                    day_index = 0
                    mnth_index = 1
                    year_index = 2

            else:
                #Every N is less than 12.
                day_index = 0
                mnth_index = 1
                year_index = 2

        print "Day Index: ", day_index
        print "Mnth Index: ", mnth_index
        print "Year Index: ", year_index

        return "/".join([self.getDay(date_list[day_index]),self.getMnth(date_list[mnth_index]),self.getYrs(date_list[year_index])])



    def get_tag_list(self,date_list):
        tag_list = []
        print date_list
        for item in date_list:
            if item.isalpha():
                tag_list.append("A")
            elif item.isdigit():
                tag_list.append("N")
            else:
                tag_list.append("AN")
        return tag_list



if __name__ == "__main__":
    print DateConverter("04  Apr 1987").dateConvert()