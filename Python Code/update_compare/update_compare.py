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

    newline = [i for i in line if i not in difline]  # 新句子
    print(file.name) # file name

    print("新句子：")
    for i in newline:
        print(i.strip())

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


    # for key in updated_english_data:
    #         try:
    #             j_6_en_v = updated_english_data[key]
    #             j_6_cn_v = update_simplified_chinese_data[key]
    #             j_5_en_v = old_english_data[key]
    #         except KeyError as e:
    #             print('Key:',key)
    #             print('Value:', j_6_en_v)
    #             print('Value:', j_6_cn_v)
    #             print('=' * 50)
    #         else:
    #             # j_5_cn_v = old_simplified_chinese_data[key]
    #             # j_5_tw_v = old_traditional_chinese_data[key]

    #             if j_6_en_v != j_5_en_v:
    #                 print('Key:', key)
    #                 print('英文v1.6：',j_6_en_v)
    #                 print('英文v1.5：',j_5_en_v)
    #                 print('簡中v1.6：',j_6_cn_v)
    #                 # print('簡中v1.5：',j_5_cn_v)
    #                 # print('繁中v1.5：',j_5_tw_v)
    #                 print('=' * 50)
    break