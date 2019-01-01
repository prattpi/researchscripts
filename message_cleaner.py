#!/usr/bin/env python3

import re
import os
import datetime

# regex for header keys e.g 'Date:  ' 'Reply-To:  ' etc.
HEADER_KEY_PATTERN = re.compile(r"^[A-Z].*:\s+")

# regex for delimiter '===== x30'
NEW_MESSAGE_PATTERN = re.compile(r"^={30,}")

# regex for date times, which change format
# this part is consistent however -> %a, %d %b %Y %H:%M:%S 
DATE_TIME_PATTERN = (r"^Date:\s+(\w{3},\s\d{1,2}\s\w{3}\s\d{4}\s\d{2}:\d{2}):")

# Globals for totals
total_messages = 0
jobs_messages = 0 
    
def read_input_dir():		
    input_dir = input("Enter the path to the input log files dir: ")
    if os.path.isdir(input_dir):
        file_list = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
        print(file_list)
        return file_list
    else:
        print("Input directory does not exist, exiting!")
        exit()
        
def set_output_dir():
    # prompt for and create output directory
    # all messages will be placed in this directory as an individual
    # file for text processing
    output_dir = input("Enter the path to desired output files dir: ")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    return output_dir
    
def parse_log_file(filepath,output_dir):
    with open(filepath, 'r') as file:
        print("Processing file "+filepath+"...")
        count = 0
        date = ""
        fromText = ""
        subjectLine = ""
        message = []
        is_job = False

        try:
            for line in file:
                # Check for delimiter '===== x30' and read as new comment if true
                if NEW_MESSAGE_PATTERN.match(line):
                    # Will be end of message if we've seen it before
                    if count and date:
                        filename = "{}.txt".format(date)
                        global total_messages
                        total_messages = total_messages + 1 
                        if is_job:
                            global jobs_messages
                            jobs_messages = jobs_messages + 1
                            filename = "Job_"+filename
                        else:
                            filename = "Message_"+filename
                        writeFile = open ("{}/{}".format(output_dir,filename),'w')
                        print("Creating file: {}".format(filename))
                        writeFile.write(fromText)
                        writeFile.write(subjectLine)
                        for m in message:
                            writeFile.write(m)
                        # Close the file and clean up for next message
                        writeFile.close()
                        date = ""
                        fromText = ""
                        subjectLine = ""
                        message = []                                       
                    count = count + 1
                # date format for the file name
                elif line.startswith("Date:"):
                    try:
                        date_str = re.findall(DATE_TIME_PATTERN, line)[0]
                        d = datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M")
                    except IndexError:
                        print("No date found for date line of "+line)
                        d = datetime.datetime.now()
                        pass
                    date = ("{}_{}_{}_{}-{}-{}").format(d.year,d.month,d.day,d.hour,d.minute,d.second)
                # identify the job listing messages
                elif line.startswith("Subject:"):
                    if "job" in line.lower():
                        is_job = True
                    else:
                        is_job = False
                    subjectLine = re.sub(HEADER_KEY_PATTERN,"",line)

                elif line.startswith("From:"):
                    fromText = re.sub(HEADER_KEY_PATTERN,"",line)

                # skipping the reply
                elif re.match(r"^>", line):
                    continue

                # skipping new line
                elif line[0] == '\n':
                    continue

                #skip writing these header keys
                elif line.lower().startswith("Reply-To:".lower()):
                    continue
                elif line.lower().startswith("Sender:".lower()):
                    continue
                elif line.lower().startswith("MIME-Version:".lower()):
                    continue
                elif line.lower().startswith("Content-Type:".lower()):
                    continue
                elif line.lower().startswith("Content-type".lower()):
                    continue
                elif line.lower().startswith("Content-Transfer-Encoding:".lower()):
                    continue
                elif line.lower().startswith("Message-ID:".lower()):
                    continue

                # stripping the text from the standard email
                else:
                    message.append(line)
        except (KeyboardInterrupt, SystemExit):
            raise
        except UnicodeDecodeError: 
            print("Decoding of file failed, skipping file...")
            pass

def main():
    # Get input file directory and list of files
    file_list = read_input_dir()
    output_dir = set_output_dir()
    for file in file_list:
        parse_log_file(file,output_dir)
    print("++++++++++++++++++++++++++++++++++++++")
    print("Total messages processed: "+str(total_messages))
    print("-- Jobs messages processed: "+str(jobs_messages))
    print("-- Non-jobs messages processed: "+str(total_messages-jobs_messages))   
    print("Files viewable in "+output_dir+" directory")
    print("++++++++++++++++++++++++++++++++++++++")
	
if __name__ == '__main__':
    main()