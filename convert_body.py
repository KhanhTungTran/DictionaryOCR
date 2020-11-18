import pickle
import docx
import os
from docx.shared import RGBColor

entries = pickle.load(open('test_1611.pkl', 'rb'))
print(entries)

inputsDir = 'LMresults'
path = os.listdir(inputsDir)

for fileName in path:
    doc = docx.Document(inputsDir + '/' + fileName)
    entryNo = 0
    for para in doc.paragraphs:
        entryIdx = 0

        # Replacing
        for run in para.runs:
            # Nếu text nằm trong định nghĩa của mục từ và được tô đỏ (tức cần thay thế):
            if not run.bold and run.font.color.rgb == RGBColor(0xFF, 0x00, 0x00):
                # Phải check cái này vì trong file .pkl các index chỉ là các từ, không có khoảng trắng
                if run.text.endswith(' '):
                    run.text = entries[entryNo][entryIdx] + ' '
                else:
                    run.text = entries[entryNo][entryIdx]
                entryIdx += 1

        entryNo += 1
        if entryNo >= len(entries):
            break
        
        # Color me black
        for run in para.runs:
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            
doc.save('test.docx')