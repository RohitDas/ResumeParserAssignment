import os
import logging
import timeit
from  Preprosessing.Converters import *



class ToolAnalysis:
    """
     Main Class for analyzing the speed of several tools used in the project.
    """
    def __init__(self,command_line_tool):
        self.command_line_tool = command_line_tool
        self.average_time_taken = 0

    def calculate(self, folder_path=None):
        """
            This function takes the resume folder and excutes the command_line tool on the pdf's of the folder
            and returns the average time taken for the command line tool to do the specific job.
        """
        if folder_path:
            #List the files in the folder.
            only_files = [f for f in os.listdir(folder_path) if os.isfile(os.join(folder_path, f))]
            file_count  = len(only_files)
            original_count = 0
            time_taken_total = 0
            #Run the command on the file and then calculate the average.
            for file in only_files:
                try:
                    #Add code to perform the conversion.
                    if self.command_line_tool == "ABIWORD":
                        logging.info("Running the command on: " + file)
                        start_time = timeit.timeit()
                        returned_path = DocumentConverter.converttopdf(file)
                        end_time = timeit.timeit()
                        logging.info("It took" + str(end_time-start_time) + "to convert the file using Abiword")
                        time_taken_total += (end_time - start_time)
                        original_count += 1
                    elif self.command_line_tool == "PDF2JSON":
                        logging.info("Running the command on: " + file)
                        start_time = timeit.timeit()
                        returned_path = DocumentConverter.convert(file)
                        end_time = timeit.timeit()
                        logging.info("It took" + str(end_time-start_time) + "to convert the file using Abiword")
                        time_taken_total += (end_time - start_time)
                        original_count += 1
                    else:
                        logging.info("Invalid Tool Name, enter either ABIWORD or PDF2JSON")
                except Exception as e:
                    logging.info("Error in performing the required command on the file" + file)

            #Calculate the average
            self.average_time_taken = time_taken_total/original_count
            return self.average_time_taken


        else:
            logging.error("Please Add a valid Folder Path")



if __name__ == "__name__":
    analysis = ToolAnalysis()
    print analysis.calculate("ABIWORD")
