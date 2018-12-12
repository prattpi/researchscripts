import re
import os

filepath = 'code4lib.log1810.txt'

file = open(filepath)
count = 0
date = ""
fromText = ""
subjectLine = ""
message = []
writeMessage = False

# Creating directory
if not os.path.isdir("jobs"):
    os.makedirs("jobs")

for line in file:
    # delimiter ======= create new file
    if re.match (r"^={30,}",line):
        if writeMessage == True:
            count = count + 1
            filename = "Job_{}_{}.txt".format(date,count)
            writeFile = open ("jobs/{}".format(filename),'w')
            print "Creating file: {}".format(filename)
            writeFile.write(fromText)
            writeFile.write(subjectLine)
            for m in message:
                writeFile.write(m)
            writeFile.close()
        date = ""
        fromText = ""
        subjectLine = ""
        message = []
    # date format for the file name
    elif line.startswith("Date:"):
        date = re.sub(r"^[A-Z].*:\s+","",line)
        date = date.replace(",", "")
        date = date.replace(" ", "_")
        date = date.replace(":", "_")
    elif line.startswith("Subject:"):
        subjectLine = re.sub(r"\bSubject:\b\s+","",line)
        print (subjectLine)
        if "job" in subjectLine.lower():
            writeMessage = True
        else:
            writeMessage = False
    # skipping the reply
    elif line.startswith("From:"):
        fromText = re.sub(r"^[A-Z].*:\s+","",line)
    elif re.match(r"^>", line):
        continue
    elif line[0] == '\n': # new line
        continue
    #skip writing this line from the header
    elif line.startswith("Reply-To:"):
        continue
    elif line.startswith("Sender:"):
        continue
    elif line.startswith("MIME-Version:"):
        continue
    elif line.startswith("Content-Type:"):
        continue
    elif line.startswith("Content-type"):
        continue
    elif line.startswith("Content-Transfer-Encoding:"):
        continue
    # stripping the text from the standard email
    else:
        newLine = re.sub(r"^[A-Z].*:\s+","",line)
        message.append(newLine)
