from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import os
from docx.shared import Inches

inputsDir = 'texts/Tu dien Nguyen Kim Than/results_new'
path = os.listdir(inputsDir)
path = sorted(path, key = lambda x: int(x[:7]) * 1000 + (int(x[8]) + 1) * 100 + int(x[10:len(x) - 4]))

doc = Document()
para = ''
docPara = doc.add_paragraph('')

# # Tags và Notes dùng cho từ điển 001 (Hoàng Phê):
# tags = {' d.': ' danh từ', 'đg.': 'động từ', ' t.': ' tính từ', 'đ.': 'đại từ', ' p.': ' phụ từ', 'k.': 'kết từ', 'tr.': 'trợ từ', ' c.': ' cảm từ', 'hoài nghi đt.': 'hoài nghi động từ'}

# notes = {'(id.).': '(ít dùng)', '(kng.).': '(khẩu ngữ)', '(ph.).': '(phương ngữ)', '(vch.).': '(văn chương)'}

# Tags và Notes dùng cho từ điển 002 (Ng Kim Than):
tags = { 'cd.': 'ca dao', 'dt.': 'danh từ', 'đt.': 'động từ', 'gt.': 'giới từ', 'id.': 'ít dùng', 'lt.': 'liên từ', ' ng.': ' nghĩa', 'pt.': 'phụ từ', 'tht.': 'thán từ', 'tng.': 'tục ngữ', 'trt.': 'trợ từ', 'vt.': 'vị từ'}

notes = {'(id.).': '(ít dùng)', '(kng.)': '(khẩu ngữ)' , '(thgt.)': '(thông tục)', '(ph.)': '(phương ngữ)', '(vchg.)': '(văn chương)',  '(trtr.)': '(trang trọng)', '(kc.)': '(kiểu cách)', '(chm.)': '(chuyên môn)'} # còn nữa

# tags = {' dt.': ' danh từ', 'đgt.': 'động từ', ' tt.': ' tính từ', ' pht.': ' phụ từ',}

# notes = {'(id.).': '(ít dùng)', '(kng.).': '(khẩu ngữ)', '(ph.).': '(phương ngữ)', '(vch.).': '(văn chương)'}

alphabets = {'a': ['a', 'ă', 'â', 'à', 'á', 'ã', 'ả', 'ạ', 'ắ', 'ằ', 'ẵ', 'ẳ', 'ặ', 'ấ', 'ầ', 'ẫ', 'ẩ', 'ậ'], 'b': ['b'], 'c': ['c'], 'd': ['d', 'đ'], 'e': ['e', 'ê', 'é', 'è', 'ẽ', 'ẻ', 'ẹ', 'ế', 'ề', 'ễ', 'ể', 'ệ'], 'f': ['f'], 'g': ['g'], 'h': ['h'], 'i': ['i', 'í', 'ì', 'ĩ', 'ỉ', 'ị'], 'j': ['j'], 'k': ['k'], 'l': ['l'], 'm': ['m'], 'n': ['n'], 'o': ['o', 'ô', 'ơ', 'ó', 'ò', 'õ', 'ỏ', 'ọ', 'ố', 'ồ', 'ỗ', 'ổ', 'ộ', 'ớ', 'ờ', 'ỡ', 'ở', 'ợ'], 'p': ['p'], 'q': ['q'], 'r': ['r'], 's': ['s'], 't': ['t'], 'u': ['u', 'ư', 'ú', 'ù', 'ũ', 'ủ', 'ụ', 'ứ', 'ừ', 'ữ', 'ử', 'ự'], 'v': ['v'], 'w': ['w'], 'x': ['x'], 'y': ['y'], 'z': ['z']}

extrasBeforeTag = {'cn.': '(cũng nói)', 'cv.': '(cũng viết)'}  # tiếp theo sẽ là 1 từ in nghiêng có chấm cuối câu 

extrasAfterTag = {' x.': ' Xem', 'Như': 'Như'}
# newEntry = True
currentAlphabet = '`'
lastLine = '.'
pages = []
lastWord = ''
lastType = ''
lastTypeKey = ''

def hasSubString(text, tags):
    for tag in tags.keys():
        if tag in text:
            return True
    return False

def hasExtraTag(text):
    for tag in extrasAfterTag.keys():
        if tag in text:
            index = text.find(tag)
            if index > 1 and text[index - 1] != '.' or text[index - 1] != '!' or text[index - 1] != '?' or text[index - 1] != ',':
                return True

    return False

def checkFirstWord(text, currAlphabet, alphabetsDict):
    for char in alphabetsDict[currAlphabet]:
        if text.lower().startswith(char) or text.lower().startswith('"' + char):
            return True
    return False

def checkOrderNumber(text):
    for ordNum in ['IV', 'III', 'II']:
        idx = text.find(ordNum)
        if idx != - 1:
            return ordNum, idx
    return None

def checkNumber(text: str):
    for num in ['1', '2', '3', '4', '5', '6']:
        idx = text.find(num)
        if idx != - 1:
            return num, idx
    return None

def spaceSplit(a):
    if a.count(" ") == 1:
        return a.split(" ")[0]
    return " ".join(a.split(" ", 2)[:2])

countNextAlphabet = 0
count = 0
for txt in path:
    print(txt)
    txtFile = open(inputsDir + '/' + txt, encoding='utf-8', errors='ignore').read()
    txtFile = re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+','', txtFile) # remove all non-XML-compatible characters
    txtFile = txtFile.replace('Ä', 'A')
    txtFile = txtFile.replace('ä', 'a')
    txtFile = txtFile.replace('“', '"')
    txtFile = txtFile.replace('”', '"')
    txtFile = txtFile.replace('¿', 't')
    txtFile = txtFile.replace(':.', 't.')
    txtFile = txtFile.replace('¡(', 't')
    
    for key, value in notes.items():
        txtFile = txtFile.replace(key, value)

    for key, value in extrasBeforeTag.items():
        txtFile = txtFile.replace(key, value)
        
    contents = txtFile.split('\n')
    contents = contents[:-1]    # bỏ đi kí tự đặc biệt luôn xuất hiện ở dòng cuối (đối với từ điển Nguyễn Kim Than)

    firstLine = True
    for line in contents:
        if line == '':
            continue
        if firstLine:
            firstLine = False
            if checkOrderNumber(line) != None:
                num, idx = checkOrderNumber(line)
                line = lastWord + line[len(num):]

            if checkNumber(line) != None:
                num, idx = checkNumber(line)
                if num != '1':
                    # docPara.add_run(line[:line.find('.') + 1])
                    # docPara = doc.add_paragraph('')
                    # docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    # docPara.add_run(line[line.find('.') + 1:idx - 1]).bold = True
                    # docPara.add_run(line[idx - 1:])
                    # lastWord = line[line.find('.') + 1:idx - 1]
                    # lastType = ''

                # else:
                    docPara.add_run(line[:idx - 1])
                    # docPara = doc.add_paragraph('')
                    # docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    # docPara.add_run(lastWord).bold = True
                    # docPara.add_run(lastType).italic = True
                    # docPara.add_run(line[idx-1:])
                    # print(line[idx+1:])
                    line = lastWord + lastTypeKey + line[idx+1:]

            if (hasSubString(line.replace(',', '.').lower(), tags) or hasExtraTag(line.replace(',', '.'))): # mục từ mới)
                # if (not checkFirstWord(line, currentAlphabet, alphabets)) and checkOrderNumber(line) == '':
                #     if lastLine.endswith(' '):
                #         docPara.add_run(line)
                #     else:
                #         docPara.add_run(' ' + line)
                #     continue
                currentTags = {}
                
                tempLine = line.replace(',', '.')
                for extra in extrasAfterTag.keys():
                    if extra in tempLine:
                        currentTags[extra] = tempLine.find(extra)
                for tag in tags.keys():
                    if tag in tempLine.lower():
                        currentTags[tag] = tempLine.lower().find(tag)
                sortedCurrentTags = sorted(currentTags.items(), key=lambda kv: kv[1])
                # print(line, sortedCurrentTags)
                word = line[:sortedCurrentTags[0][1]]
                content = line[sortedCurrentTags[-1][1] + len(sortedCurrentTags[-1][0]):]

                docPara = doc.add_paragraph('')
                docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                docPara.add_run(word).bold = True
                lastWord = word

                lastType = ''
                lastTypeKey = ''

                for tagKey,_ in sortedCurrentTags:
                    if tagKey in tags.keys():
                        if tagKey.startswith(' '):
                            docPara.add_run(tags[tagKey]).italic = True
                            lastType += tags[tagKey]
                            lastTypeKey += tagKey
                        else:
                            docPara.add_run(' ' + tags[tagKey]).italic = True
                            lastType += ' ' + tags[tagKey]
                            lastTypeKey += ' ' + tagKey
                    else:
                        docPara.add_run(' ' + extrasAfterTag[tagKey]).italic = True
                        lastType += ' ' + extrasAfterTag[tagKey]
                        lastTypeKey += ' ' + tagKey
                docPara.add_run(content)

            else:
                docPara = doc.add_paragraph('')
                docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

                for i in range(2, len(line)):
                    if line[i].isupper() and line[i - 1] == ' ' and (line[i - 2] != '.' and line[i - 2] != ',' and line[i - 2] != '!' and line[i - 2] != '?'):
                        docPara.add_run(line[:i]).bold = True
                        lastWord = line[:i]
                        docPara.add_run(line[i:])
                        lastType = ''
                        lastTypeKey = ''
                        break
                else:
                    openingBracket = line.find('(')
                    if openingBracket == -1:
                        temp = spaceSplit(line)
                    else:
                        temp = line[:openingBracket]
                    docPara.add_run(temp).bold = True
                    docPara.add_run(line[len(temp):])
                    lastWord = temp
                    lastType = ''
                    lastTypeKey = ''
        
        elif lastLine.endswith(' '):
            docPara.add_run(line)
        else:
            docPara.add_run(' ' + line)
        lastLine = line
    # count += 1
    # if count == 7:
    #     break

doc.save('result.docx')
