import json
import shutil
import re
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at

output_txt_path = Path(fr'.\compare_output\all_in_one.txt')
old_version_file_path = Path(fr'.\StardewValleyv1.5')
updated_version_file_path = Path(fr'.\StardewValleyv1.6')
english_folder_name = 'English'
origin_updated_version_path =  updated_version_file_path / english_folder_name 
# 檔案列表
origin_updated_version_file_list = [f for f in origin_updated_version_path.glob('**/*.json')]

def initialize_output_txt():
    with open(output_txt_path,'w', encoding='utf-8') as output_file:
        output_file.write('')

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

def Find_New_Key(update_keys,legacy_keys):
    new_key = []
    for key in update_keys:
        if key not in legacy_keys:
            new_key.append(key)
    
    return new_key

initialize_output_txt()
for file in origin_updated_version_file_list:

    updated_english_json_file = file    
    old_english_json_file = Corresponding_Path(file, old_version_file_path, english_folder_name, '.json')
        
    updated_english_data = Read_json(updated_english_json_file)       
      
    try:
        old_english_data = Read_json(old_english_json_file)
    except FileNotFoundError:
        print(f"新檔案：{old_english_json_file}")
        isnewfile = True
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

      
    with open(output_txt_path,"a", encoding="utf-8") as output_file:
        output_file.write('\n' + str(file) + '\n\n')
        
        for key in new_key:
            output_file.write(f'"{key}": "{updated_english_data[key]}",\n')
        
        for key in modified_key:            
            output_file.write(f'"{key}": "{updated_english_data[key]}",\n')            
                        
        for key in removed_key:
            output_file.write(f'"{key}": "{old_english_data[key]}",\n')

        