
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
i = 0
for txt in path:
    print(txt)
    txtFile = open(inputsDir + '/' + txt, encoding='utf-8', errors='ignore').read()
    txtFile = re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+','', txtFile) # remove all non-XML-compatible characters
    # par = doc.add_paragraph(txtFile)
    content = txtFile.split('\n')
    for line in content:
        if line == '':
            continue
        i = 1
        while line[:i].isupper() and i <= len(line):
            i += 1
        
        i -= 2
        newWord = False
        wordType = ''
        if i == 1 and len(line) >= 4:
            if line[i + 1] == '(':
                newWord = True
            elif line[i + 1: i + 4] in wordTypes or line[i + 1: i + 5] in wordTypes or line[i + 1: i + 6] in wordTypes:
                newWord = True
        elif i > 1:
            newWord = True
        
        if newWord:
            if line[i + 1: i + 4] in wordTypes:
                wordType = line[i + 1: i + 4]
            elif line[i + 1: i + 5] in wordTypes:
                wordType = line[i + 1: i + 5]
            elif line[i + 1: i + 6] in wordTypes:
                wordType = line[i + 1: i + 6]
            newPara = line[:i]
            line = line[i:]
            contents.append(para)
            words.append(newPara)
            # docPara.add_run(para)
            # docPara = doc.add_paragraph('')
            # docPara.add_run(newPara).bold = True
            if wordType != '':
                try:
                    line = line[1 + len(wordType)]
                except Exception as e:
                    line = line[len(wordType)]
                types.append(wordTypes[wordType])
            else: types.append(' ')
            para = ''
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
        
        para += (line + ' ')
        # print(para)
# contents = contents[1:]
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
    ET.SubElement(root[i], 'Y_NGHIA', {'Noi_dung': contents[i], 'Minh_hoa': ''})

indent(root)
tree.write('result.xml', encoding='utf-8', xml_declaration=True)