import re
import os

filepath = 'code4lib.log0405.txt'

file = open (filepath)
count = 0

if not os.path.isdir("extract"):
    os.makedirs("extract")
writeFile = open ("extract/test.txt",'w')
for line in file:
    # delimiter ======= create new file
    if re.match (r"^={30,}",line):
        writeFile.close()
    # date format for the file name
    elif line.startswith("Date:"):
        count = count + 1
        date = re.sub(r"^[A-Z].*:\s+","",line)
        date = date.replace(",", "")
        date = date.replace(" ", "_")
        date = date.replace(":", "_")

        filename = "{}_{}.txt".format(date,count)
        writeFile = open ("extract/{}".format(filename),'w')
        print "Creating file: {}".format(filename)
    # skipping the reply
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
        writeFile.write(newLine)
writeFile.close()
