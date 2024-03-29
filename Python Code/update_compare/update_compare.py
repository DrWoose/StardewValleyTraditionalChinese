import json
import shutil
import re
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))

old_version_file_path = Path(fr'.\StardewValleyv1.5')
updated_version_file_path = Path(fr'.\StardewValleyv1.6')
english_folder_name = 'English'
simplified_chinese_folder_name = 'Simplified Chinese'
traditional_chinese_folder_name = 'TraditionalChinese'

origin_updated_version_path =  updated_version_file_path / english_folder_name

# 檔案列表
origin_updated_version_file_list = [f for f in origin_updated_version_path.glob('**/*.json')]

# 轉換路徑
def corresponding_path(path, version_folder_name, language, suffix): 
    path = list(path.parts)#split path
    path[0] = version_folder_name
    path[1] = language
    path = Path(*path)
    path = path.with_suffix(suffix)
    return path

# 讀取 json
def readjson(file_path):    
    with file_path.open('r', encoding='utf-8') as file:
        data = file.readlines()
        return data

def addcomma(data):
    text = []
    for i in data:
        text.append(re.sub('"\n$','",\n', i))

def Convert_To_txt(file_path):
    new_file_path = file_path.with_suffix('.txt')
    new_file_path = 'compare_output' / Path(*list(new_file_path.parts)[3:])
    return new_file_path
    #Path(*list(file.parts)[3:])

def output_to_txt_file(file,difline,update_simplified_chinese_text,old_english_text,old_key,updated_key):

    output_txt_file_path = Convert_To_txt(file)

    new_english_line = [i for i in line if i not in difline]  # 新句子
    
    with open(output_txt_file_path, "w", encoding="utf-8") as output_file:        
        output_file.write(str(file) + '\n')
        output_file.write('\n')
        for i in old_key:
            if i not in updated_key:
                output_file.write("Missing Key " + i + '\n')
        output_file.write('\n')
        if new_english_line:
            output_file.write("新句子：\n")
            for i in new_english_line:
                has_simplified_chinese_line = False
                output_file.write(i.strip() + '\n')
                key = re.sub('\\s+(".*"):.*\n?', '\\g<1>' , i)
                for j in update_simplified_chinese_text:
                    if key in j:
                        output_file.write(j.strip() + '\n')
                        has_simplified_chinese_line = True
                if not has_simplified_chinese_line:
                    output_file.write("簡中沒更新這句\n")
        
        keydif = []
        text_old = []
        text_oldt = []
        if difline != [] :
            output_file.write("\n有更動（上：英 1.5、中：英 1.6、下：簡 1.6）：\n")
            output_file.write('\n')
        for i in difline:
            keydif.append(re.sub('\\s+(".*"):.*\n?', '\\g<1>' , i))

        for i in keydif:
            for x in old_english_text:
                if i in x:
                    text_old.append(x)
            for x in update_simplified_chinese_text:
                if i in x:
                    text_oldt.append(x)

        for i in range(0,len(text_old)):
            output_file.write(text_old[i].strip() + '\n')
            output_file.write(difline[i].strip() + '\n')
            output_file.write(text_oldt[i].strip() + '\n')
        output_file.write('\n' + '=' * 65 + '\n')


def raw_output(file,difline,update_simplified_chinese_text,old_english_text,old_key,updated_key):
    for i in old_key:
        if old_key not in updated_key:
            print(f"missing key{old_key}")
    print(file)
    new_english_line = [i for i in line if i not in difline]  # 新句子


    if new_english_line:
        print("新句子：")
        for i in new_english_line:
            has_simplified_chinese_line = False
            print(i.strip())
            key = re.sub('\\s+(".*"):.*\n?', '\\g<1>' , i)
            for j in update_simplified_chinese_text:
                if key in j:
                    print(j.strip())
                    has_simplified_chinese_line = True
            if not has_simplified_chinese_line:
                print("簡中沒更新這句")
    
    keydif = []
    text_old = []
    text_oldt = []
    if difline != [] :
        print("\n有更動（上：英 1.5、中：英 1.6、下：簡 1.6）：")
    for i in difline:
        keydif.append(re.sub('\\s+(".*"):.*\n?', '\\g<1>' , i))

    for i in keydif:
        for x in old_english_text:
            if i in x:
                text_old.append(x)
        for x in update_simplified_chinese_text:
            if i in x:
                text_oldt.append(x)

    for i in range(0,len(text_old)):
        print(text_old[i].strip())
        print(difline[i].strip())
        print(text_oldt[i].strip())
        print('')

    print('=' * 65)



for file in origin_updated_version_file_list:
    isnewfile = False
    updated_english_json_file = file
    
    old_english_json_file = corresponding_path(file, old_version_file_path, english_folder_name, '.json')
    update_simplified_json_file = corresponding_path(file, updated_version_file_path, simplified_chinese_folder_name, '.zh-CN.json')
    #old_simplified_json_file = corresponding_path(file, old_version_file_path, simplified_chinese_folder_name, '.zh-CN.json')
    #old_traditional_chinese_json_file = corresponding_path(file, old_version_file_path, traditional_chinese_folder_name, '.zh-CN.json')
    
    # 讀取 json
    updated_english_data = readjson(updated_english_json_file)
    try:        
        old_english_data = readjson(old_english_json_file)
    except FileNotFoundError:
        print(f"新檔案：{old_english_json_file}")
        isnewfile = True
    update_simplified_chinese_data = readjson(update_simplified_json_file)
    #old_simplified_chinese_data = readjson(old_simplified_json_file)
    #old_traditional_chinese_data = readjson(old_traditional_chinese_json_file)
    updated_english_text = []
    old_english_text = []
    update_simplified_chinese_text = []  
    updated_key = []
    old_key = []

    for i in updated_english_data:        
        updated_english_text.append(re.sub('"\n$','",\n', i))
    if not isnewfile:
        for i in old_english_data:
            old_english_text.append(re.sub('"\n$','",\n', i))        
    for i in update_simplified_chinese_data:
        update_simplified_chinese_text.append(re.sub('"\n$','",\n', i))    
    for i in updated_english_text:
        updated_key.append(re.sub('\\s+(".*"):.*\n?', '\\g<1>' , i))
    for i in old_english_text:
        old_key.append(re.sub('\\s+(".*"):.*\n?', '\\g<1>' , i))

    # ===== 找出不同 ===== #
    line = []
    difline = []
    for i in updated_english_text:
        if i not in old_english_text:
            line.append(i) # 所有差異
            for x in old_key:
                if x in i:
                    difline.append(i) # 之前就有但有更動
    
    
    
    


    output_to_txt_file(file,difline,update_simplified_chinese_text,old_english_text,old_key,updated_key)
    #raw_output(file,difline,update_simplified_chinese_text,old_english_text,old_key,updated_key)
