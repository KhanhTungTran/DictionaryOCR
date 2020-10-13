from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import os
from docx.shared import Inches

inputsDir = 'results'
path = os.listdir(inputsDir)
# path = path[:6]
path = sorted(path, key = lambda x: len(x))

doc = Document()
para = ''
docPara = doc.add_paragraph('')

tags = {' d.': ' danh từ', 'đg.': 'động từ', ' t.': ' tính từ', 'đ.': 'đại từ', ' p.': ' phụ từ', 'k.': 'kết từ', 'tr.': 'trợ từ', ' c.': ' cảm từ', 'hoài nghi đt.': 'hoài nghi động từ'}

notes = {'(id.).': '(ít dùng)', '(kng.).': '(khẩu ngữ)', '(ph.).': '(phương ngữ)', '(vch.).': '(văn chương)'}

# tags = { 'cd.': 'ca dao', 'dt.': 'danh từ', 'đt.': 'động từ', 'gt.': 'giới từ', 'id.': 'ít dùng', 'lt.': 'liên từ', ' ng.': ' nghĩa', 'pt.': 'phụ từ', 'tht.': 'thán từ', 'tng.': 'tục ngữ', 'trt.': 'trợ từ', 'vt.': 'vị từ'}

# notes = {'(id.).': '(ít dùng)', '(kng.)': '(khẩu ngữ)' , '(thgt.)': '(thông tục)', '(ph.)': '(phương ngữ)', '(vchg.)': '(văn chương)',  '(trtr.)': '(trang trọng)', '(kc.)': '(kiểu cách)', '(chm.)': '(chuyên môn)'} # còn nữa

alphabets = {'a': ['a', 'ă', 'â', 'à', 'á', 'ã', 'ả', 'ạ', 'ắ', 'ằ', 'ẵ', 'ẳ', 'ặ', 'ấ', 'ầ', 'ẫ', 'ẩ', 'ậ'], 'b': ['b'], 'c': ['c'], 'd': ['d', 'đ'], 'e': ['e', 'ê', 'é', 'è', 'ẽ', 'ẻ', 'ẹ', 'ế', 'ề', 'ễ', 'ể', 'ệ'], 'f': ['f'], 'g': ['g'], 'h': ['h'], 'i': ['i', 'í', 'ì', 'ĩ', 'ỉ', 'ị'], 'j': ['j'], 'k': ['k'], 'l': ['l'], 'm': ['m'], 'n': ['n'], 'o': ['o', 'ô', 'ơ', 'ó', 'ò', 'õ', 'ỏ', 'ọ', 'ố', 'ồ', 'ỗ', 'ổ', 'ộ', 'ớ', 'ờ', 'ỡ', 'ở', 'ợ'], 'p': ['p'], 'q': ['q'], 'r': ['r'], 's': ['s'], 't': ['t'], 'u': ['u', 'ư', 'ú', 'ù', 'ũ', 'ủ', 'ụ', 'ứ', 'ừ', 'ữ', 'ử', 'ự'], 'v': ['v'], 'w': ['w'], 'x': ['x'], 'y': ['y'], 'z': ['z']}

extrasBeforeTag = {'cn.': '(cũng nói)', 'cv.': 'cũng viết'}  # tiếp theo sẽ là 1 từ in nghiêng có chấm cuối câu 
extrasAfterTag = {' Xem': ' Xem'}
newEntry = True
currentAlphabet = '`'
lastLine = '.'

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
    for ordNum in ['II', 'III', 'IV', 'V']:
        if text.startswith(ordNum):
            return ordNum
    return ''

for txt in path:
    print(txt)
    txtFile = open(inputsDir + '/' + txt, encoding='utf-8', errors='ignore').read()
    txtFile = re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+','', txtFile) # remove all non-XML-compatible characters
    txtFile = txtFile.replace('Ä', 'A')
    txtFile = txtFile.replace('ä', 'a')
    txtFile = txtFile.replace('“', '"')
    txtFile = txtFile.replace('”', '"')
    # txtFile = txtFile.replace('¿', 't')
    # txtFile = txtFile.replace(':.', 't.')
    # txtFile = txtFile.replace('¡(', 't')
    
    for key, value in notes.items():
        txtFile = txtFile.replace(key, value)

    for key, value in extrasBeforeTag.items():
        txtFile = txtFile.replace(key, value)
        
    contents = txtFile.split('\n')
    
    for line in contents:
        if line == '':
            newEntry = True
            continue

        # if line.lower() == chr(ord(currentAlphabet) + 1) + chr(ord(currentAlphabet) + 1):
        #     continue

        if newEntry or line.lower().startswith(chr(ord(currentAlphabet) + 1) + ',' + chr(ord(currentAlphabet) + 1)) or ((lastLine.endswith('.') or lastLine.endswith('!') or lastLine.endswith('?') or lastLine.endswith(',')) and (checkFirstWord(line, currentAlphabet, alphabets) or checkOrderNumber(line))):
            # print(line, newEntry)
            newEntry = False
            nextAlphabet = chr(ord(currentAlphabet) + 1)
            if line.lower().startswith(nextAlphabet + ',' + nextAlphabet):
                currentAlphabet = nextAlphabet
                docPara = doc.add_paragraph('')
                docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                docPara.add_run(nextAlphabet + ',' + nextAlphabet.upper() + ' ').bold = True
                docPara.add_run(line[4:])

            elif (lastLine.endswith('.') or lastLine.endswith('!') or lastLine.endswith('?') or lastLine.endswith(',')):
            # else:
                if (hasSubString(line.replace(',', '.').lower(), tags) or hasExtraTag(line.replace(',', '.'))): # mục từ mới
                    # print(line)
                    # print(line.lower(), '"' + chr(ord(currentAlphabet) + 1))
                    # print(line, line.lower().startswith('"' + currentAlphabet))
                    if line.lower().startswith(chr(ord(currentAlphabet) + 1)) or line.lower().startswith('"' + chr(ord(currentAlphabet) + 1)):
                        currentAlphabet = chr(ord(currentAlphabet) + 1)
                    
                    elif (not checkFirstWord(line, currentAlphabet, alphabets)) and checkOrderNumber(line) == '':
                        if lastLine.endswith(' '):
                            docPara.add_run(line)
                        else:
                            docPara.add_run(' ' + line)
                        continue
                    # elif not (line.lower().startswith(currentAlphabet) or line.lower().startswith('"' + currentAlphabet)):
                    #     yes = False
                    #     for ordNum in ['II', 'III', 'IV', 'V']:
                    #         if line.startswith(ordNum):
                    #             yes = True
                    #             break
                    #     if not yes:
                    #         continue
                    currentTags = {}
                    
                    tempLine = line.replace(',', '.').lower()
                    for extra in extrasAfterTag.keys():
                        if extra in line:
                            currentTags[extra] = line.find(extra)
                            # word = line[:line.find(extra)]
                            # content = line[line.find(extra):]
                    for tag in tags.keys():
                        if tag in tempLine:
                            currentTags[tag] = tempLine.find(tag)
                            # word = line[:line.find(tag)]
                            # content = line[line.find(tag):]
                    sortedCurrentTags = sorted(currentTags.items(), key=lambda kv: kv[1])
                    word = line[:sortedCurrentTags[0][1]]
                    content = line[sortedCurrentTags[len(sortedCurrentTags) - 1][1] + len(sortedCurrentTags[len(sortedCurrentTags) - 1][0]):]
                    # print(line, sortedCurrentTags)

                    docPara = doc.add_paragraph('')
                    docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    docPara.add_run(word).bold = True

                    for tagKey,_ in sortedCurrentTags:
                        # print(tagKey)
                        if tagKey in tags.keys():
                            if tagKey.startswith(' '):
                                docPara.add_run(tags[tagKey]).italic = True
                            else:
                                docPara.add_run(' ' + tags[tagKey]).italic = True
                        else:
                            docPara.add_run(' ' + extrasAfterTag[tagKey]).italic = True
                    docPara.add_run(content)
                    # for extra in extrasBeforeTag.keys():
                    #     if extra in word:
                    #         extraWord = word[word.find(extra) + len(extra):]
                    #         extraValue = extrasBeforeTag[extra]
                    #         word = word[:word.find(extra)]
                elif checkFirstWord(line, currentAlphabet, alphabets):
                    # print(line)
                    docPara = doc.add_paragraph('')
                    docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

                    for i in range(2, len(line)):
                        if (line[i].isupper() or line[i].isdigit()) and line[i - 1] == ' ' and (line[i - 2] != '.' and line[i - 2] != ',' and line[i - 2] != '!' and line[i - 2] != '?'):
                            docPara.add_run(line[:i]).bold = True
                            docPara.add_run(line[i:])
                            break
                    else:
                        docPara.add_run(line)
                elif checkOrderNumber(line) != '':
                    num = checkOrderNumber(line)
                    docPara = doc.add_paragraph('')
                    docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    docPara.add_run(num).bold = True
                    docPara.add_run(line[len(num):])
                else:
                    docPara = doc.add_paragraph('')
                    docPara.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    docPara.add_run(line)
        elif lastLine.endswith(' '):
            docPara.add_run(line)
        else:
            docPara.add_run(' ' + line)
        lastLine = line

doc.save('result.docx')
