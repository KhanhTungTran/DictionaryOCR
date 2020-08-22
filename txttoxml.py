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
wordTypes = {'c.': 'cảm từ', 'd.': 'danh từ', 'đ.': 'đại từ', 'đg.': 'động từ', 'k.': 'kết từ', 'p.': 'phụ từ', 't.': 'tính từ', 'tr.': 'trợ từ', 'x.': 'xem'}
# docPara = doc.add_paragraph('')
words = []
types = []
contents = []
i = 0
for txt in path:
    txtFile = open(inputsDir + '/' + txt, encoding='utf-8', errors='ignore').read()
    txtFile = re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+','', txtFile) # remove all non-XML-compatible characters
    # par = doc.add_paragraph(txtFile)
    contents = txtFile.split('\n')
    for line in contents:
        if line == '':
            continue
        
        for wordType in wordTypes.keys():
            if wordType in line:
                newPara = para[para.rfind('.') + 1:] + line[:line.find(wordType)]
                line = line[line.find(wordType) + len(wordType):]
                para = para[:para.rfind('.') + 1]
                # break
                # docPara.add_run(para)
                # docPara = doc.add_paragraph('')
                # docPara.add_run(newPara).bold = True
                # docPara.add_run(wordTypes[wordType]).italic = True
                # if len(contents) <= i:
                #     contents.append(para)
                # else:
                #     contents[i] += para
                contents.append(para)
                words.append(newPara)
                types.append(wordTypes[wordType])
                i += 1
                para = ''
                break
        
        para += (line + ' ')

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
    # word = ET.SubElement(root, 'MUC_TU')
    # word.set('Noi_dung', words[i])
    # word.set('Loai_tu' , types[i])
    # item = ET.SubElement(word, 'Y_NGHIA')
    # item.set('Noi_dung', contents[i])
    # item.set('Minh_hoa', '')

indent(root)
tree.write('result.xml', encoding='utf-8', xml_declaration=True)
# # mydata = ''
# mydata = str(ET.tostring(root, encoding='utf-8'))

# myfile = open('result.xml', 'w')
# myfile.write(mydata)

