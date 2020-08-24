from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import os

inputsDir = 'results'
path = os.listdir(inputsDir)
# Đi từng dòng, dòng nào là '' thì bỏ qua
# Tìm những cụm như ' ph.', ' vch.', ... => quay ngược lại tìm dấu chấm trước đó, in đậm từ dấu chấm đến trước cụm,
# và thêm '\n' trước dấu chấm vừa tìm được
doc = Document()
para = ''
wordTypes = { 'bt.': 'biến từ', 'chđt.': 'chỉ định từ', 'dt.': 'danh từ', 'đdt.': 'đại danh từ', 'đt.': 'động từ', 'gt.': 'giới từ', 'lt.': 'liên từ', 'pht.': 'phó từ', 'st.': 'số từ', 'tt.': 'tĩnh từ', 'trt.': 'trạng từ', 'tht.': 'thán từ', 'vt.': 'vấn từ'}
docPara = doc.add_paragraph('')
for txt in path:
    print(txt)
    txtFile = open(inputsDir + '/' + txt, encoding='utf-8', errors='ignore').read()
    txtFile = re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+','', txtFile) # remove all non-XML-compatible characters
    # par = doc.add_paragraph(txtFile)
    contents = txtFile.split('\n')
    cumTu = False
    vidu = False
    first = False
    for line in contents:
        if line == '':
            continue
        
        if line.find(' - ') != -1:
            cumTu = False
            vidu = False
            docPara = doc.add_paragraph('')
            docPara.add_run(line[:line.find(' - ')]).bold = True
            docPara.add_run(line[line.find(' - '):])

        elif line.lower().find('ví dụ') != -1:
            docPara.add_run(' ' + line[:line.find(':')]).italic = True
            docPara.add_run(line[line.find(':'):])
            pass

        elif cumTu == True and not line.isupper():
            if not first:
                docPara.add_run(' ' + line).bold = True
            else:
                docPara = doc.add_paragraph('')
                docPara.add_run(line).bold = True
                docParaFormat = docPara.paragraph_format
                docParaFormat.alignment = WD_ALIGN_PARAGRAPH.CENTER
                first = False
                

        elif line.isupper():
            if cumTu == True:
                docPara.add_run(' ' + line).bold = True
            else:
                docPara = doc.add_paragraph('')
                docPara.add_run(line).bold = True
                docParaFormat = docPara.paragraph_format
                docParaFormat.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cumTu = True
            first = True
        
        else:
            docPara.add_run(' ' + line)
        # for wordType in wordTypes.keys():
        #     if wordType in line:
        #         if line.find(wordType) + len(wordType) < len(line) and line[line.find(wordType) + len(wordType)] == ')':
        #             continue
        #         newPara = para[para.rfind('.') + 1:] + line[:line.find(wordType)]
        #         line = line[line.find(wordType) + len(wordType):]
        #         para = para[:para.rfind('.') + 1]
        #         # break
        #         docPara.add_run(para)
        #         docPara = doc.add_paragraph('')
        #         docPara.add_run(newPara).bold = True
        #         # docPara.add_run(' ')
        #         docPara.add_run(wordTypes[wordType]).italic = True
        #         para = ''
        #         break
        
        # para += (line + ' ')

doc.save('result.docx')