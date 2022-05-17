import re
import sys
import os

argv = sys.argv

if len(argv) < 2:
    print("No filename given")
    exit()

fileOSPath = os.getcwd() + '/' + argv[1]

if not os.path.exists(fileOSPath):
    print("File does not exist")
    exit()

with open(fileOSPath, "r") as file:
    text = file.read()

print("Fixing chars and removing unwanted Apple Books stuff")
text = re.sub("( \\n)", "\n", text)
text = re.sub("(_\\d{1,2} \\w+ \\d{4})", '', text)
text = re.sub("^Excerpt from:\\n[\\S\\s]*\\n[\\S\\s]*\\nThis material may be protected by copyright.*$", '', text)
text = re.sub("\\[â€¦]", '', text)
text = re.sub("â€™", '\'', text)
text = re.sub("â€œ", '"', text)
text = re.sub("â€”", ', ', text)
text = re.sub("â€", '"', text)
text = re.sub("Ã¨", 'è', text)
text = re.sub("Ã©", 'é', text)

with open(fileOSPath, "w") as file:
    file.write(text)

with open(fileOSPath, "r") as file:
    text = file.readlines()

i = 0
section = None
currentTitle = ""

print("Removing double new lines and grouping notes to section titles")
while i < len(text):
    if text[i] == "\n":
        if text[i + 1] == "\n":
            text.pop(i)
            continue

    section = re.match("^\\d{1,3}: [\\w -':.?!]*_ *\n", text[i])
    if section:
        if currentTitle == section.string:
            text.pop(i)
        else:
            text[i] = "#### " + text[i]
            currentTitle = section.string
        section = None
    i += 1

with open(fileOSPath, "w") as file:
    file.writelines(text)

print("Finish")
