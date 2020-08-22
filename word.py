def save_word(image, path):
  with PyTessBaseAPI(lang = 'vie', psm = PSM.SINGLE_BLOCK, oem = OEM.LSTM_ONLY) as api:
    api.SetImage(Image.fromarray(cv.bitwise_not(image)))
    contents = api.GetUTF8Text()
    header = False
    lines = contents.split('\n')
    for i in range(10):
      if str(i) in contents[0]:
        header = True
        break
    if header:
      lines = lines[1:]
    word = ''
    document = Document()
    p = document.add_paragraph('')
    new_word = False
    example = False
    type_flag = False
    is_diff = False
    diff_example = False
    for line in lines:
      # print(line)
      line = line.strip()
      c = line.replace('-', '').split()
      if len(c) == 0:
        continue
      if all([w.isupper() for w in c]):
        t = p.add_run(f'\t\t\t{line}')
        t.bold = True
        t.alignment = 1
        new_word = True
        type_flag = False
        is_diff = False
        diff_example = False
        p.add_run('\n')
        continue
      elif new_word and line[0].islower():
        for item in c:
          t = p.add_run(f'\t\t\t{item}')
          t.bold = True
          t.alignment = 1
          p.add_run('\n')
        continue
      if line[0].isupper() and line[1].isupper():
        new_word = False
        example = False
        type_flag = True
        word, words = line.split('-')
        p.add_run(f'{word} - ').bold = True
        for item in words:
          p.add_run(f'{item}')
      elif line[0].isupper() and 'trái' in line:
        t = p.add_run(f'\t{line}')
        t.bold = True
        t.italic = True
        is_diff = True
      elif is_diff:
        if 'Ví dụ' in line or diff_example:
          diff_example = True
          colon = True
          for i, item in enumerate(line.split()):
            if colon and 'Ví dụ' in line:
              p.add_run(item + ' ')
            else:
              t = p.add_run(item + ' ')
              t.italic = True
              item = item.replace(',', '').replace(';', '').replace('.', '')
              if item.lower() in diff_ls:
                t.bold = True
            if colon:
              colon = item[-1] != ':'
        else:
          diff_ls = line.replace(',', ' ').replace('-', ' ').split()
          t = p.add_run(f'{line}')
          t.bold = True
          t.italic = True
      elif 'Ví dụ' in line or example:
        type_flag = False
        words = line.split()
        flag = word.lower() in line.lower()
        for i, item in enumerate(words):
          if i < 3 and not example:
            p.add_run(f'{item} ')
          else:
            if not flag:
              p.add_run(f'{item} ').italic = True
            else:
              c = word.split()
              if c and item.lower() == c[0].lower():
                t = p.add_run(f'{item} ')
                t.bold = True
                t.italic = True
                c = c[1:]
              else:
                p.add_run(f'{item} ').italic = True
        example = True
      elif not example and type_flag:
        p.add_run(f'{line}')
      p.add_run('\n')     
    document.save(path)
    print('[Finished]', path)
