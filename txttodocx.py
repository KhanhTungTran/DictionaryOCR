from docx import Document
import re
import os

inputsDir = 'results'
path = os.listdir(inputsDir)
# Đi từng dòng, dòng nào là '' thì bỏ qua
# Tìm những cụm như ' ph.', ' vch.', ... => quay ngược lại tìm dấu chấm trước đó, in đậm từ dấu chấm đến trước cụm,
# và thêm '\n' trước dấu chấm vừa tìm được
doc = Document()
para = ''
wordTypes = {'c.': 'cảm từ', 'd.': 'danh từ', 'đ.': 'đại từ', 'đg.': 'động từ', 'k.': 'kết từ', 'p.': 'phụ từ', 't.': 'tính từ', 'tr.': 'trợ từ', 'x.': 'xem'}
docPara = doc.add_paragraph('')
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
                docPara.add_run(para)
                docPara = doc.add_paragraph('')
                docPara.add_run(newPara).bold = True
                docPara.add_run(wordTypes[wordType]).italic = True
                para = ''
                break
        
        para += (line + ' ')

doc.save('result.docx')