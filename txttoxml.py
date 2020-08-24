# from docx import Document
import re
import os

inputsDir = 'results'
path = os.listdir(inputsDir)
# Đi từng dòng, dòng nào là '' thì bỏ qua
# Tìm những cụm như ' ph.', ' vch.', ... => quay ngược lại tìm dấu chấm trước đó, in đậm từ dấu chấm đến trước cụm,
# và thêm '\n' trước dấu chấm vừa tìm được
# doc = Document()
para = ''
wordTypes = { 'bt.': 'biến từ', 'chđt.': 'chỉ định từ', 'dt.': 'danh từ', 'đdt.': 'đại danh từ', 'đt.': 'động từ', 'gt.': 'giới từ', 'lt.': 'liên từ', 'pht.': 'phó từ', 'st.': 'số từ', 'tt.': 'tĩnh từ', 'trt.': 'trạng từ', 'tht.': 'thán từ', 'vt.': 'vấn từ'}
# docPara = doc.add_paragraph('')
words = []
types = []
contents = []
exs = []
i = 0
for txt in path:
    print(txt)
    txtFile = open(inputsDir + '/' + txt, encoding='utf-8', errors='ignore').read()
    txtFile = re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+','', txtFile) # remove all non-XML-compatible characters
    # par = doc.add_paragraph(txtFile)
    content = txtFile.split('\n')
    cumTu = False
    viDu = False
    first = False
    firsVD = False
    for line in content:
        if line == '':
            continue
        
        if line.find(' - ') != -1:
            cumTu = False
            viDu = False
            firsVD = True
            words.append(line[:line.find(' - ')])
            contents.append(line[line.find(' - ') + 3:])
            if len(exs) != len(words):
                exs.append('')
            if len(types) != len(words):
                types.append(types[len(types) - 1])
            # docPara = doc.add_paragraph('')
            # docPara.add_run(line[:line.find(' - ')]).bold = True
            # docPara.add_run(line[line.find(' - '):])

        elif line.lower().find('ví dụ') != -1:
            viDu = True
            if firsVD:
                exs.append(line[line.find(':') + 2:])
                firsVD = False
            else:
                exs[len(exs) - 1] += line[line.find(':') + 1:]
            # docPara.add_run(' ' + line[:line.find(':')]).italic = True
            # docPara.add_run(line[line.find(':'):])
            pass

        elif cumTu == True and not line.isupper():
            if not first:
                pass
                # docPara.add_run(' ' + line).bold = True
            else:
                # docPara = doc.add_paragraph('')
                # docPara.add_run(line).bold = True
                # docParaFormat = docPara.paragraph_format
                # docParaFormat.alignment = WD_ALIGN_PARAGRAPH.CENTER
                first = False
                

        elif line.isupper():
            if cumTu == True:
                types[len(types) - 1] += ' ' + line
                # docPara.add_run(' ' + line).bold = True
            else:
                types.append(line)
                # docPara = doc.add_paragraph('')
                # docPara.add_run(line).bold = True
                # docParaFormat = docPara.paragraph_format
                # docParaFormat.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cumTu = True
            first = True
        
        else:
            if viDu:
                exs[len(exs) - 1] += ' ' + line
            else:
                contents[len(contents) - 1] += ' ' + line
            # docPara.add_run(' ' + line)
        # for wordType in wordTypes.keys():
        #     if wordType in line:
        #         if line.find(wordType) + len(wordType) < len(line) and line[line.find(wordType) + len(wordType)] == ')':
        #             continue
        #         newPara = para[para.rfind('.') + 1:] + line[:line.find(wordType)]
        #         line = line[line.find(wordType) + len(wordType):]
        #         para = para[:para.rfind('.') + 1]
        #         # break
        #         # docPara.add_run(para)
        #         # docPara = doc.add_paragraph('')
        #         # docPara.add_run(newPara).bold = True
        #         # docPara.add_run(wordTypes[wordType]).italic = True
        #         # if len(contents) <= i:
        #         #     contents.append(para)
        #         # else:
        #         #     contents[i] += para
        #         contents.append(para)
        #         # print(contents)
        #         words.append(newPara)
        #         types.append(wordTypes[wordType])
        #         i += 1
        #         para = ''
        #         break
        
        # print(para)
exs = exs[1:]
# doc.save('result.docx')

import xml.etree.ElementTree as ET
# from lxml import etree as ET

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

tree = ET.parse('result.xml')
root = tree.getroot()
# root = ET.Element('GOC')
for i in range(len(contents)):
    element = root.makeelement('MUC_TU', {'Noi_dung': words[i], 'Loai_tu': types[i]})
    root.append(element)
    ET.SubElement(root[i], 'Y_NGHIA', {'Noi_dung': contents[i], 'Minh_hoa': exs[i]})

indent(root)
tree.write('result.xml', encoding='utf-8', xml_declaration=True)

