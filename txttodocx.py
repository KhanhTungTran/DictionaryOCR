from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import os
from docx.shared import Inches

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
    capTu = False
    for line in contents:
        if line == '':
            continue
        
        # print(line, ' ', capTu)

        if line.startswith('Ví dụ'):
            docPara = doc.add_paragraph('')
            paraFormat = docPara.paragraph_format
            paraFormat.left_indent = Inches(0.5)
            docPara.add_run(line)
            capTu = False

        elif line.find(' - ') != -1:
            if line.isupper():
                docPara = doc.add_paragraph('')
                docPara.add_run(line).bold = True
                docPara.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                capTu = False
            elif line[:line.find(' - ')].isupper():
                docPara = doc.add_paragraph('')
                docPara.add_run(line[:line.find(' - ')]).bold = True
                docPara.add_run(line[line.find(' - '):])
                capTu = False
            elif capTu == True:
                docPara = doc.add_paragraph('')
                run = docPara.add_run(line)
                run.font.bold = True
                run.font.italic = True
                docPara.paragraph_format.left_indent = Inches(0.5)      

        elif line == 'Gặp từ trái nghĩa:' or line == 'Cặp từ trái nghĩa:':
            docPara = doc.add_paragraph('')
            paraFormat = docPara.paragraph_format
            paraFormat.left_indent = Inches(0.5)
            run = docPara.add_run('Cặp từ trái nghĩa:')
            run.font.bold = True
            run.font.underline = True
            capTu = True

        elif capTu == True:
            docPara = doc.add_paragraph('')
            run = docPara.add_run(line)
            docPara.paragraph_format.left_indent = Inches(0.5)  

        else:
            docPara.add_run(line)
        # if line.find(' - ') != -1:
        #     cumTu = False
        #     vidu = False
        #     docPara = doc.add_paragraph('')
        #     docPara.add_run(line[:line.find(' - ')]).bold = True
        #     docPara.add_run(line[line.find(' - '):])

        # elif line.lower().find('ví dụ') != -1:
        #     docPara.add_run(' ' + line[:line.find(':')]).italic = True
        #     docPara.add_run(line[line.find(':'):])
        #     pass

        # elif cumTu == True and not line.isupper():
        #     if not first:
        #         docPara.add_run(' ' + line).bold = True
        #     else:
        #         docPara = doc.add_paragraph('')
        #         docPara.add_run(line).bold = True
        #         docParaFormat = docPara.paragraph_format
        #         docParaFormat.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #         first = False
                

        # elif line.isupper():
        #     if cumTu == True:
        #         docPara.add_run(' ' + line).bold = True
        #     else:
        #         docPara = doc.add_paragraph('')
        #         docPara.add_run(line).bold = True
        #         docParaFormat = docPara.paragraph_format
        #         docParaFormat.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #         cumTu = True
        #     first = True
        
        # else:
        #     docPara.add_run(' ' + line)
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