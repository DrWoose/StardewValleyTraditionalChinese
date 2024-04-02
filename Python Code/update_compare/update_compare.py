import json
import shutil
import re
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at

old_version_file_path = Path(fr'.\StardewValleyv1.5')
updated_version_file_path = Path(fr'.\StardewValleyv1.6')
english_folder_name = 'English'
simplified_chinese_folder_name = 'Simplified Chinese'
traditional_chinese_folder_name = 'TraditionalChinese'
origin_updated_version_path =  updated_version_file_path / english_folder_name
# 檔案列表
origin_updated_version_file_list = [f for f in origin_updated_version_path.glob('**/*.json')]

# 轉換路徑
def Corresponding_Path(path, version_folder_name, language, suffix): 
    parted_path = list(path.parts)#split path
    parted_path[0] = version_folder_name
    parted_path[1] = language
    path = Path(*parted_path)
    path = path.with_suffix(suffix)
    return path

# 讀取 json
def Read_json(file_path):  
    with file_path.open('r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def Find_Key(input_string):
    key =  re.sub('\\s+(".*"):.*\n?', '\\g<1>' , input_string)
    return key

def Convert_To_txt(file_path):
    new_file_path = file_path.with_suffix('.txt')
    new_file_path = 'compare_output' / Path(*list(new_file_path.parts)[3:])
    return new_file_path
    #Path(*list(file.parts)[3:])

def is_key_in_simplified_chinese(update_simplified_chinese_data,key):#cause sometimes they don't have it :(
    try:
        output_file.write(f'"{key}": "{update_simplified_chinese_data[key]}",\n')
    except KeyError:
        output_file.write(f'簡中沒更新這句\n')

def Find_New_Key(update_keys,legacy_keys):
    new_key = []
    for key in update_keys:
        if key not in legacy_keys:
            new_key.append(key)
    
    return new_key

def simplified_chinese_didnot_update(output_file,modified_key,update_simplified_chinese_data,old_simplified_chinese_data):
    #英文有更新簡中卻沒變
    unchange_key = {
        key: (update_simplified_chinese_data, old_simplified_chinese_data)
        for key in modified_key 
        if update_simplified_chinese_data[key].lower() == old_simplified_chinese_data[key].lower()
    }
    for key in unchange_key:
        output_file.write(f'"{key}": "{old_simplified_chinese_data[key]}",\n')
    


for file in origin_updated_version_file_list:

    updated_english_json_file = file    
    old_english_json_file = Corresponding_Path(file, old_version_file_path, english_folder_name, '.json')
    update_simplified_json_file = Corresponding_Path(file, updated_version_file_path, simplified_chinese_folder_name, '.zh-CN.json')
    old_simplified_json_file = Corresponding_Path(file, old_version_file_path, simplified_chinese_folder_name, '.zh-CN.json')
    #old_traditional_chinese_json_file = Corresponding_Path(file, old_version_file_path, traditional_chinese_folder_name, '.zh-CN.json')
    
    updated_english_data = Read_json(updated_english_json_file)       
    update_simplified_chinese_data = Read_json(update_simplified_json_file)    
    
    try:
        old_english_data = Read_json(old_english_json_file)
        old_simplified_chinese_data = Read_json(old_simplified_json_file)       
    except FileNotFoundError:
        print(f"新檔案：{old_english_json_file}")
        continue
    #old_traditional_chinese_data = Read_json(old_traditional_chinese_json_file)
    try:
        update_key = set(updated_english_data.keys())
        legacy_key = set(old_english_data.keys())
    except AttributeError:
        print(f"{file} 怪怪ㄉ")
        continue
    new_key = update_key - legacy_key
    removed_key = legacy_key - update_key

    shared_key = update_key & legacy_key
    modified_key = {
        key: (updated_english_data, old_english_data)
        for key in shared_key 
        if updated_english_data[key].lower() != old_english_data[key].lower()
    }

    #print(file)

    output_txt_file_path = Convert_To_txt(file)   
    with open(output_txt_file_path,"w", encoding="utf-8") as output_file:
        output_file.write(str(file) + '\n\n')
        output_file.write('新句子（上：英 1.6、下：簡 1.6）：\n')
    
        for key in new_key:
            output_file.write(f'"{key}": "{updated_english_data[key]}",\n')
            is_key_in_simplified_chinese(update_simplified_chinese_data,key)
        output_file.write('\n有更動（上：英 1.5、中：英 1.6、下：簡 1.6）：\n')

        for key in modified_key:            
            output_file.write(f'"{key}": "{old_english_data[key]}",\n')
            output_file.write(f'"{key}": "{updated_english_data[key]}",\n')            
            output_file.write(f'"{key}": "{update_simplified_chinese_data[key]}",\n')
            
        output_file.write('\n移除的句子\n')
        for key in removed_key:
            output_file.write(f'"{key}": "{old_english_data[key]}",\n')

        output_file.write('\n簡中沒更新到的句子：\n')
        simplified_chinese_didnot_update(output_file,modified_key,update_simplified_chinese_data,old_simplified_chinese_data)
