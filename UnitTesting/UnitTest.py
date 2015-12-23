__author__ = 'sameer.pidadi'

from src.main_parse import main_parse
import os
import time

#Get curr time in milliseconds
mT = lambda: int(round(time.time()*1000))


def test_folder(file_dir):
    start_time = mT()
    for file in os.listdir(file_dir):
        print "Parsing file:", file
        file_start_time = mT()
        parsed_resume = main_parse(file_dir+file)
        file_end_time = mT()
        print "RESUME PARSED IN :", file_end_time-file_start_time, "ms"
        print parsed_resume
        print "---------------------------------------------------------"
    end_time =mT()
    file_count = len(os.listdir(file_dir))
    print "##############################################"
    print "Avg time taken for ", file_count, "files :", str((end_time-start_time)/file_count), "ms"
    print "##############################################"


def test_file(path):
    file_start_time = mT()
    parsed_resume = main_parse(path)
    file_end_time = mT()
    print "RESUME PARSED IN :", file_end_time-file_start_time, "ms"
    print parsed_resume
    print "---------------------------------------------------------"


if __name__ == '__main__':

       # path = "/home/likewise-open/PUNESEZ/sameer.pidadi/self_projects/test_profiles/Profiles_16-Dec-2014/docx/"
       # test_folder(path)

      test_folder("/home/likewise-open/PUNESEZ/rohitangsu.das/CV/")

