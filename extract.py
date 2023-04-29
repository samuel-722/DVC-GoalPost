import re
from pdfminer.high_level import extract_text
from collections import deque


#data
Dict = {}                                                                                   #key is uni, value is college
q = deque()                                                                                 #initialize queue
text = extract_text("Assist_SFState.pdf")                                                   #text from the pdf
# text = extract_text("Assist_Simple.pdf")
university_pattern = re.compile("[A-Z]{2,5}\s\d{1,5}[A-Z]?\s-\s(.*){5,80}\(.{4}\)")         #from class code to units
college_pattern = re.compile("←\s[A-Z]{2,5}\s\d{1,5}[A-Z]?\s-\s(.*){5,80}\(.{4}\)")         #from arrow to units

#prepare text for processing
unicode_removedText = text.replace('\u200b', '')                                            #remove invisible unicode chars
text_to_erase = re.split(university_pattern, unicode_removedText, maxsplit = 1)[0]          #split the code at the first instance of the pattern, and only save everything before it
essential_text = unicode_removedText.partition(text_to_erase)[2]                            #remove text_to_erase from the text
newline_removedText = essential_text.replace('\n','')                                       #remove \n everywhere
additional_newLine_Text = re.sub(r"(\(\d\.\d0\))", r"\1\n", newline_removedText)            #add a \n after units
ready_text = re.sub(r"(\.*)([←\s]*[A-Z]{2,5}\s\d{1,5}[A-Z]?\s-\s(.*){5,80}\(.{4}\))", r"\1\n\2", additional_newLine_Text) #add \n before the class code
ready_text = ready_text.replace("\n\n", "\n").strip()

merged_text = ""
previous_line = ""
line_before_previous = ""
ready_text = ready_text.replace("\n\n", "\n").strip()
for line in ready_text.split("\n"):
    if "--- And ---" in line:
        merged_line = line_before_previous.strip() + " AND " + previous_line.strip() + "\n" #+ line.replace(line, "").strip()
        merged_text += merged_line + "\n"
        previous_line = ""
        line_before_previous = ""    
    elif "--- Or ---" in line:
        merged_line = line_before_previous.strip() + " Or " + previous_line.strip() + "\n" #+ line.replace(line, "").strip()
        merged_text += merged_line + "\n"
        previous_line = ""
        line_before_previous = ""
    elif line == ready_text.split("\n")[-1]:
        merged_text += line_before_previous + "\n" + previous_line + "\n" + line + "\n"
    else:
        merged_text += line_before_previous + "\n"
        line_before_previous = previous_line
        previous_line = line
ready_text = merged_text.strip()
        
#process into a dictionary
for line in ready_text.split('\n'):
    print(line)
    if college_pattern.search(line):
        Dict[q.popleft()] = line[2:]      
    elif university_pattern.search(line):
        q.append(line)
    elif "No Course Articulated" in line:
        Dict[q.popleft()] = line[2:]  

#output
print(Dict)
print("----------------------------------------------------------------")
print(q)