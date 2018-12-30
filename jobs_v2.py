import re
import os

filepath = 'code4lib.log1810.txt'

file = open(filepath)
count = 0
date = ""
fromText = ""
subjectLine = ""
message = []

# regex for header keys e.g 'Date:  ' 'Reply-To:  ' etc.
HEADER_KEY_PATTERN = re.compile(r"^[A-Z].*:\s+")

# regex for delimiter '===== x30'
NEW_MESSAGE_PATTERN = re.compile(r"^={30,}")

# flag to determine whether to write the message to atext file or not
# if writeMessage is true this means the subject has job keyword and
# the message will be written to a text file
writeMessage = False

# Creating directory 'jobs' at the current path
# all comments will be placed in this directory as an individual file
if not os.path.isdir("jobs"):
    os.makedirs("jobs")

for line in file:
    # Check for delimiter '===== x30' and read as new comment if true
    if NEW_MESSAGE_PATTERN.match(line):
        if writeMessage:
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
        date = re.sub(HEADER_KEY_PATTERN,"",line)
        date = date.replace(",", "")
        date = date.replace(" ", "_")
        date = date.replace(":", "_")
    elif line.startswith("Subject:"):
        if "job" in line.lower():
            writeMessage = True
            subjectLine = re.sub(HEADER_KEY_PATTERN,"",line)
        else:
            writeMessage = False

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
        #newLine = re.sub(HEADER_KEY_PATTERN,"",line)
        message.append(line)
