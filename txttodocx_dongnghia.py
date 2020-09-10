from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import os
from docx.shared import RGBColor
import json

def searchForUnderline(para, text, start, end, indexes, bold, italic):
    cuts = []
    for index in indexes:
        if start <= index and index < end:
            cuts.append(index - start)
        else:   break
    
    low = 0
    for index in cuts:
        high = index
        # if high > 0:
        run = para.add_run(text[low:high])
        run.bold = bold
        run.italic = italic

        run = para.add_run(text[index])
        run.bold = bold
        run.italic = italic
        run.underline = True

        low = high + 1

    run = para.add_run(text[low:end-start])
    run.bold = bold
    run.italic = italic



inputsDir = 'results'
path = os.listdir(inputsDir)
# Đi từng dòng, dòng nào là '' thì bỏ qua
# Tìm những cụm như ' ph.', ' vch.', ... => quay ngược lại tìm dấu chấm trước đó, in đậm từ dấu chấm đến trước cụm,
# và thêm '\n' trước dấu chấm vừa tìm được
doc = Document()
para = ''

docPara = doc.add_paragraph('')
docPara.add_run('KÍ HIỆU:').bold = True

docPara = doc.add_paragraph('', style = 'ListBullet')
docPara.add_run('*').font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
docPara.add_run(': các kí tự lạ nằm ngoài bảng chữ cái Tiếng Việt')

docPara = doc.add_paragraph('', style = 'ListBullet')
docPara.add_run('_').bold = True
docPara.add_run(': các chữ cái có xác suất dự đoán sai cao')


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

        indexes = []
        # print(line[line.rfind('['):line.rfind(']') + 1])
        if line[line.rfind('['):line.rfind(']') + 1] != '':
            indexes = json.loads(line[line.rfind('['):line.rfind(']') + 1]) # string to list
        
        line = line[:line.rfind('[')]

        if line.find(' - ') != -1:
            cumTu = False
            vidu = False
            docPara = doc.add_paragraph('')
            if line.lower().find('ví dụ') != -1:
            # print("something")
                searchForUnderline(docPara, line[:line.find(' - ')], 0, line.find(' - '), indexes, True, False)
                searchForUnderline(docPara, line[line.find(' - '):line.lower().find('ví dụ')], line.find(' - '), line.lower().find('ví dụ'), indexes, False, False)
                while line.lower().find('ví dụ') != -1 and line.lower().find(':') != -1:
                    searchForUnderline(docPara, line[line.lower().find('ví dụ'):line.find(':') + 1], line.lower().find('ví dụ'), line.find(':') + 1, indexes, False, True)
                    line = line[line.find(':') + 1:]
                    # print(line)
                    if line.lower().find('ví dụ') != -1 and line.lower().find(':') != -1:
                        searchForUnderline(docPara, line[0:line.lower().find('ví dụ')], 0, line.lower().find('ví dụ'), indexes, False, False)
                    else:
                        searchForUnderline(docPara, line, 0, len(line), indexes, False, False)
            else:
                searchForUnderline(docPara, line[:line.find(' - ')], 0, line.find(' - '), indexes, True, False)
                searchForUnderline(docPara, line[line.find(' - '):], line.find(' - '), len(line), indexes, False, False)
            # docPara.add_run(line[:line.find(' - ')]).bold = True
            # docPara.add_run(line[line.find(' - '):])

        elif line.lower().find('ví dụ') != -1:
            # print("something")
            searchForUnderline(docPara, line[:line.find(':')], 0, line.find(':'), indexes, False, True)
            searchForUnderline(docPara, line[line.find(':'):], line.find(':'), len(line), indexes, False, False)
            # docPara.add_run(' ' + line[:line.find(':')]).italic = True
            # docPara.add_run(line[line.find(':'):])

        elif cumTu == True and not line.isupper():
            if not first:
                docPara.add_run(' ').bold = True
                searchForUnderline(docPara, line, 0, len(line), indexes, True, False)
                # docPara.add_run(' ' + line).bold = True
            else:
                docPara = doc.add_paragraph('')
                # docPara.add_run(line).bold = True
                searchForUnderline(docPara, line, 0, len(line), indexes, True, False)
                docParaFormat = docPara.paragraph_format
                docParaFormat.alignment = WD_ALIGN_PARAGRAPH.CENTER
                first = False
                

        elif line.isupper():
            if cumTu == True:
                docPara.add_run(' ').bold = True
                searchForUnderline(docPara, line, 0, len(line), indexes, True, False)
                # docPara.add_run(' ' + line).bold = True
            else:
                docPara = doc.add_paragraph('')
                searchForUnderline(docPara, line, 0, len(line), indexes, True, False)
                # docPara.add_run(line).bold = True
                docParaFormat = docPara.paragraph_format
                docParaFormat.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cumTu = True
            first = True
        
        else:
            docPara.add_run(' ')
            searchForUnderline(docPara, line, 0, len(line), indexes, False, False)
            # docPara.add_run(' ' + line)
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