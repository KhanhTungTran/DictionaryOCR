### 0: từ bình thường, không nghiêng, không in đậm
### 1: từ in đậm 
### 2: từ nghiêng

def split_by_meaning(d, ls, is_has_digit = True):
    if not ls:
        return [('','')]
    n_tmp = []
    if is_has_digit:
        s, rs = [], []
        ls.append(('22', 1))
        for item in ls:
            if item[1] == 1:
                if item[0].isdigit() and int(item[0]) > 1:
                    s.append(n_tmp)
                    n_tmp = []
            else:
                n_tmp.append((item[0], item[1]))
        for item in s:
            rs.append(split_by_meaning(d, item, False)[0])
        return rs
    else:
        i_tmp = []
        size = len(ls)
        no_italic = False
        for i in range(size):
            if ls[i][1] != 2:
                n_tmp.append(ls[i][0])
                no_italic = True
            else:
                break
        if i != size - 1:
            while i < size:
                i_tmp.append(ls[i][0])
                i += 1
        elif not no_italic:
            for item in ls:
                n_tmp.append(item[0])
        # else:
        #     n_tmp.append(ls[-1][0])
        n_tmp = [d.get(i, i) for i in n_tmp]
        i_tmp = [d.get(i, i) for i in i_tmp]
        return [(' '.join(n_tmp), ' '.join(i_tmp))]
def split_by_type_word(ls):
    size, idx, count = len(ls), [], 1
    for i in range(size):
        if ls[i][0] == 'I' * count:
            idx.append(i)
            count += 1
    size_i, s = len(idx), []
    for i in range(size_i - 1):
        temp = ls[idx[i] + 1 : idx[i + 1]]
        s.append(temp)
    s.append(ls[idx[-1] + 1:])
    return ls[:idx[0]], s
def save_xml(tree, noi_dung_list, loai_tu_list, y_nghia_list):
    size = len(noi_dung_list)
    for i in range(size):
        muctu = ET.SubElement(tree, 'MUC_TU')
        muctu.set('Noi_dung', noi_dung_list[i])
        muctu.set('Loai_tu', loai_tu_list[i])
        for item in y_nghia_list[i]:
            ynghia = ET.SubElement(muctu, 'Y_NGHIA')
            ynghia.set('Noi_dung', item[0])
            ynghia.set('Minh_hoa', item[1])
def is_many_meanings(ls, isHomophoneWord = True):
    flag_1, flag_2 = False, False
    if isHomophoneWord:
        pt_1, pt_2 = 'I', 'II'
    else:
        pt_1, pt_2 = '1', '2'
    for l in ls:
        if l[0] == pt_1:
            flag_1 = True
        elif l[0] == pt_2:
            flag_2 = True
        if flag_1 & flag_2:
            return True
    return False


def readjust_italic_text(ls):
    # print(ls)
    size = len(ls)
    idx = 0
    # for l in ls:
    #     idx += 1
    #     if l[1] == 2:
    #         break
    for i in range(idx, size - 2):
        if ls[i][1] == 2 and ls[i + 1][1] != 2 and ls[i + 2][1] == 2:
            ls[i + 1][1] = 2
    if len(ls) > 3:
        if ls[-3][1] == 2 and ls[-2][1] == 2 and ls[-1][1] != 2:
            ls[-1][1] = 2
    # for i in range(3, size - 2):
    #     if ls[i][1] == 2 and ls[i + 1][1] == 2 and ls[i + 2][1] == 2:
    #         if ls[i - 2][0][-1] == '.' and ls[i - 1][0][0].isupper():
    #             ls[i - 1][1] = 2
    #         if ls[i - 3][0][-1] == '.' and ls[i - 2][0][0].isupper():
    #             ls[i - 2][1] = ls[i - 1][1] = 2

    for i in range(size - 3, idx, -1):
        if ls[i][1] == 0 and ls[i + 1][1] == 2 and ls[i + 2][1] == 2:
            if ls[i - 1][0][-1] == '.' and ls[i][0][0].isupper():
                ls[i][1] = 2
        if i > 1 and ls[i + 1][1] == 2 and ls[i + 2][1] == 2 and ls[i - 1][0][0].isupper() and ls[i - 2][0][-1] == '.':
            ls[i - 1][1] = ls[i][1] = 2
        if i < size - 3 and ls[i][1] == 2 and ls[i + 3][1] == 2:
            if ls[i + 1][1] == 2:
                ls[i + 2][1] = 2
            elif ls[i + 2][1] == 2:
                ls[i + 1][1] = 2
    for i in range(idx, size - 1):
        if ls[i + 1][1] == 2 and ls[i][0][-1] == '.' and ls[i + 1][0][0].isupper():
            break
        if ls[i + 1][1] == 2:
            ls[i + 1][1] = 0
    # print(ls)
def isOtherMeaning(s, d):
    if s in d:
        return True
    return False
def parseargument():
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--source', required = True, type = str, help = 'path to source of (an) image(s)')
    args = vars(ap.parse_args())
    return args
dt = Manager().dict()
def parseimage(img_path, d, d_fn, clf, sc):
    global dt
    dt['end'] =False
    # d_values = list(d.values())
    d_keys = list(d.keys())
    d_om = {'cv.':'cũng viết', 'cn.':'cũng nói'}
    d_t_om = generate_type_word(d_om)
    d_om = list(d_t_om.keys())
    # img = cv.imread(img_path)
    # # img = cv.imread(img_path)
    # # thresh = preprocessing(img)
    # pages = split_page(img)
    # p_pages = [preprocessing(page) for page in pages]
    # p_pages = [remove_border(page) for page in p_pages]
    # p_pages = [remove_num_page(page) for page in p_pages]
    # is_character = p_pages[1][:, -63: -61].sum() > 2000
    # if is_character:
    #     p_pages[1] = remove_character(p_pages[1])
    # pages, p_pages = skew(pages, p_pages)
    # if is_character:
    #     p_pages[1] = remove_character(p_pages[1], 12)
    img = cv.imread(img_path)
    thresh = preprocessing(img)
    thresh = deskew(thresh)[0]
    has_remove_alpha = int(img_path.split('.')[0][-1]) % 2 == 1
    prefix_name = img_path.split(os.path.sep)[-1].split('.')[0]
    if has_remove_alpha:
      thresh = remove_alpha(thresh)
    columns = split_column(thresh)
    new_columns = []
    for col in columns:
      col = deskew(col)[0]
      col = np.pad(col, ((10, 10), (0, 0)))
      new_columns.append(col)
    cols = new_columns
    del new_columns
    flag = True
    num = False
    isSaveO = False
    new_page = True
    ls_content, ls_typeword, ls_meaning = [], [], []
    with PyTessBaseAPI(lang = 'vie+eng+fra', psm = PSM.SINGLE_LINE, oem = OEM.LSTM_ONLY) as api:
          first = True
          ls = []
          for col in cols:
              # new_col = True
              if col is None:
                  continue
              rows = split_line(col)
              if len(rows) == 0:
                  continue
              for row in rows:
                  l_i = []
                  api.SetImage(Image.fromarray(cv.bitwise_not(row)))
                  text = api.GetUTF8Text().strip()
                  if not text:
                      continue
                  # print(text)
                  if text[0] == '"':
                      text = text.replace('"', ' ', 2)
                  tus = split_word(row)
                  for tu in tus:
                      c = split_character(tu)
                      api.SetImage(Image.fromarray(cv.bitwise_not(tu)))
                      t_c = api.GetUTF8Text()
                      l_i.extend([is_italic(clf, sc, c)[0]] * len(t_c.split()))
                  ls_words = typeofword(text, d)
                  if flag and not num:
                      if len(ls_words) == 1:
                          n_o = int(img_path.split(os.path.sep)[-1].split('.')[0][-4:])
                          path_o = os.path.join('xml', 'PAGEPAGE{:04}.xml'.format(n_o - 1))
                          if os.path.exists(path_o):
                              if not isSaveO:
                                  root_o = ET.parse(path_o).getroot()
                                  last_child_o = root_o[-1][-1] 
                                  isSaveO = True
                                        
                              last_child_o.attrib['Noi_dung'] += ' '.join(ls_words[0])
              
                              num = isEndOfDefine(text, row)
                              continue
                  if isSaveO:
                   
                      tree_o = ET.ElementTree(root_o)
                      tree_o.write(path_o, encoding = 'utf-8')
                      isSaveO = False
                  flag = False
                  if num or first:
                      if first and new_page:
                          if num:
                              if ls:
                                  if not is_many_meanings(ls):
                                      i, size = 0, len(ls)
                                      content_t = ''
                                      while i < size and ls[i][1] == 1 and not ls[i][0].isdigit():
                                          content_t += '{} '.format(d_t_om.get(ls[i][0], ls[i][0]))
                                          i += 1
                                      content_t = content_t.strip()#.replace('"','')
                                      typeword_t = ''
                                      if i < size:
                                          if ls[i][0] in d_keys:
                                              typeword_t = d_fn.get(ls[i][0], ls[i][0])
                                              typeword_t = d.get(typeword_t, typeword_t)
                                              ls = ls[i + 1 :]
                                              size -= i + 1
                                          else:
                                              ls = ls[i : ]
                                              size -= i
                                      else:
                                          ls = []
                                      readjust_italic_text(ls)
                                      meanings = split_by_meaning(d, ls, is_many_meanings(ls, False))
                                      ls_content.append(content_t)
                                      ls_typeword.append(typeword_t)
                                      ls_meaning.append(meanings)
                                  else:
                                      content, ls_w = split_by_type_word(ls)
                                      content_t = ''
                                      for c in content:
                                          content_t += '{} '.format(d_t_om.get(c[0], c[0]))
                                      content_t = content_t.strip()#.replace('"','')
                                      for s in ls_w:
                                          typeword_t = ''
                                          if s[0][0] in d_keys:
                                              typeword_t = d_fn.get(s[0][0],s[0][0])
                                              typeword_t = d.get(typeword_t, typeword_t)
                                              s.pop(0)
                                          readjust_italic_text(s)
                                          meanings = split_by_meaning(d, s, is_many_meanings(s, False))
                                          ls_content.append(content_t)
                                          ls_typeword.append(typeword_t)
                                          ls_meaning.append(meanings)
                                  ls = []
                              new_page = False
                          else:
                              words = text.split()
                              words = [d.get(i, i) for i in words]
                              for word in words:
                                  try:
                                      if int(word) < 20:
                                          ls.append([word, 1])
                                  except:
                                      if len(l_i) and l_i[0] == 1:
                                          ls.append([word, 2])
                                      else:
                                          ls.append([word, 0])          
                                  if len(l_i):
                                      l_i.pop(0)
                              num = isEndOfDefine(text, row)
                              continue
                      if ls:
                          # print(ls)
                          if not is_many_meanings(ls):
                              i, size = 0, len(ls)
                              content_t = ''
                              while i < size and ls[i][1] == 1 and not ls[i][0].isdigit():
                                  content_t += '{} '.format(d_t_om.get(ls[i][0], ls[i][0]))
                                  i += 1
                              content_t = content_t.strip()#.replace('"','')
                              typeword_t = ''
                              if i < size:
                                  if ls[i][0] in d_keys:
                                      typeword_t = d_fn.get(ls[i][0], ls[i][0])
                                      typeword_t = d.get(typeword_t, typeword_t)
                                      ls = ls[i + 1 :]
                                      size -= i + 1
                                  else:
                                      ls = ls[i : ]
                                      size -= i
                              else:
                                  ls = []
                              # print('Before: {}'.format(ls))
                              readjust_italic_text(ls)
                              # print('After: {}'.format(ls))
                              meanings = split_by_meaning(d, ls, is_many_meanings(ls, False))
                              ls_content.append(content_t)
                              ls_typeword.append(typeword_t)
                              ls_meaning.append(meanings)
                          else:
                              content, ls_w = split_by_type_word(ls)
                              content_t = ''
                              for c in content:
                                  content_t += '{} '.format(d_t_om.get(c[0], c[0]))
                              content_t = content_t.strip().replace('"','')
                              for s in ls_w:
                                  typeword_t = ''
                                  if s[0][0] in d_keys:
                                      typeword_t = d_fn.get(s[0][0],s[0][0])
                                      typeword_t = d.get(typeword_t, typeword_t)
                                      s.pop(0)
                                  readjust_italic_text(s)
                                  meanings = split_by_meaning(d, s, is_many_meanings(s, False))
                                  ls_content.append(content_t)
                                  ls_typeword.append(typeword_t)
                                  ls_meaning.append(meanings)
                      ls = []
                      if len(ls_words) > 1:
                          for b_word in ls_words[0]:
                              ls.append([b_word, 1])
                              if len(l_i):
                                  l_i.pop(0)
                          ls.append([ls_words[1], 2])
                          if len(l_i):
                              l_i.pop(0)
                          ls_words = (ls_words[2], )
                      else:
                          size = len(ls_words[0])
                          i = 0
                          nfound = False
                          f_word = True
                          for i in range(size):
                              item = ls_words[0][i]
                              if f_word or (item[0] != '[' and item[0] != '(' and not item[0].isupper()) or (len(item) == 1 and item[0].isalpha()):
                                  ls.append([item, 1])
                              else:
                                  nfound = True
                                  break
                              f_word = False
                              if len(l_i):
                                  l_i.pop(0)
                          if nfound:
                              ls_words = (ls_words[0][i:], )
                          else:
                              ls_words = ([], )
                  else:
                      if len(ls_words) > 1:
                          temp = [ls_words[1]]
                          temp.extend(ls_words[2])
                          ls_words[0].extend(temp)
                  for item in ls_words[0]:
                      try:
                          if int(item) < 20:
                              ls.append([item, 1])
                      except:
                          if len(l_i) and l_i[0] == 1:
                              ls.append([item, 2])
                          else:
                              ls.append([item, 0])
                      if len(l_i):
                          l_i.pop(0) 
                  num = isEndOfDefine(text, row)
                  first = False
          if ls:
              if not is_many_meanings(ls):
                  i, size = 0, len(ls)
                  content_t = ''
                  while i < size and ls[i][1] == 1 and not ls[i][0].isdigit():
                      content_t += '{} '.format(d_t_om.get(ls[i][0], ls[i][0]))
                      i += 1
                  content_t = content_t.strip()#.replace('"','')
                  typeword_t = ''
                  if i < size:
                      if ls[i][0] in d_keys:
                          typeword_t = d_fn.get(ls[i][0], ls[i][0])
                          typeword_t = d.get(typeword_t, typeword_t)
                          ls = ls[i + 1 :]
                          size -= i + 1
                      else:
                          ls = ls[i : ]
                          size -= i
                  else:
                      ls = []
                  # print(ls)
                  readjust_italic_text(ls)
                  meanings = split_by_meaning(d, ls, is_many_meanings(ls, False))
                  ls_content.append(content_t)
                  ls_typeword.append(typeword_t)
                  ls_meaning.append(meanings)
              else:
                  content, ls_w = split_by_type_word(ls)
                  content_t = ''
                  for c in content:
                      content_t += '{} '.format(d_t_om.get(c[0], c[0]))
                  content_t = content_t.strip().replace('"','')
                  for s in ls_w:
                      typeword_t = ''
                      if s[0][0] in d_keys:
                          typeword_t = d_fn.get(s[0][0],s[0][0])
                          typeword_t = d.get(typeword_t, typeword_t)
                          s.pop(0)
                      readjust_italic_text(s)
                      meanings = split_by_meaning(d, s, is_many_meanings(s, False))
                      ls_content.append(content_t)
                      ls_typeword.append(typeword_t)
                      ls_meaning.append(meanings)
              ls = []
    dt['data'] = [ls_content, ls_typeword, ls_meaning]
    dt['end'] = True


def main(args):
    global dt
    d = {'cd.': 'ca dao', 'chm.': 'chuyên môn', 'dt.': 'danh từ', 'đt.': 'đại từ', 'gt.': 'giới từ', 'id.': 'ít dùng', 
          'kc.': 'kiểu cách', 'kng.': 'khẩu ngữ', 'lt.': 'liên từ', 'ng.': 'nghĩa', 'ph.': 'phương ngữ', 'pt.': 'phụ từ',
          'thgt.': 'thông tục', 'tht.': 'thán từ', 'tng.': 'tục ngữ', 'trt.': 'trợ từ', 'trtr.': 'trang trọng', 'vch.': 'văn chương', 'vt.': 'vị từ', 'u£.': 'vị từ', 'dz.': 'danh từ.'}
    d = generate_type_word(d)
    d_fn = {'đợ.': 'đg.', 'đẹ.':'đg.'}
    d_fn = generate_type_word(d_fn)
    xmls = glob.glob("xml/*.xml")
    clf, sc = load_model()
    img_paths = args['source']
    print('[INFO] Starting ...')
    count = 0

   
    for img_path in img_paths:
        start = time.time()
        count += 1
        # try:
        img_name = img_path.split(os.path.sep)[-1]
        xml_name = img_name.split('.')[0]
        xml_name = f'xml/PAGE{xml_name}.xml'
        if xml_name in xmls:
          continue
        t = Process(target=parseimage, args=[img_path, d, d_fn, clf, sc])
        t.start()
        t.join(timeout = 180)
        t.terminate()
        if dt['end'] == False:
          print('failed')
          with open("log_xml", 'a') as f:
            f.write(img_path + "\n")
          continue
        ls_content, ls_typeword, ls_meaning = dt['data']
        root = ET.Element('GOC')
        save_xml(root, ls_content, ls_typeword, ls_meaning)
        format_xml(root)
        tree = ET.ElementTree(root)
        output_path = "xml/PAGE{}.xml".format(img_path.split(os.path.sep)[-1].split('.')[0])
        print(output_path)
        tree.write(output_path, encoding = 'utf-8')
        end = time.time()
        print('[INFO] Processed {} image: {} - Time: {:.4f}'.format(count, img_name, end - start))
    print('[INFO] Finished.')
