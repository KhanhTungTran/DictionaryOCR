import pickle
import docx
import os
from docx.shared import RGBColor

entries = pickle.load(open('correct_entry.pkl', 'rb'))

inputsDir = 'LMresults'
path = os.listdir(inputsDir)

for fileName in path:
    doc = docx.Document(inputsDir + '/' + fileName)
    count = 0
    for para in doc.paragraphs:
        replace = True
        
        # Replacing
        for run in para.runs:
            if run.bold == True and replace:
                if entries[count] != '':
                    run.text = entries[count]
                    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
                else:
                    break
                replace = False
            elif run.bold == True:
                run.text = ''
            else:
                break
        count += 1
        if count >= len(entries):
            break
        
        # Color me black
        for run in para.runs:
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            
doc.save('test.docx')

