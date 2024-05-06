import json
import shutil
import re
import os
from pathlib import Path
import csv

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

def Fanguaji_Corresponding_Path(file : Path):
    parent_file_path = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()
    splitted_path_list = list(file.parts)
    for i in range(0,len(splitted_path_list)):
        if "Content" in splitted_path_list[i]:
            file_path_in_content = Path(*splitted_path_list[i+1:len(splitted_path_list)])
            break
    fanhuaji_path = parent_file_path / 'Fanhuaji' / 'Fanhuaji_output_json' /file_path_in_content
    return fanhuaji_path

# 讀取 json
def Read_json(file_path):  
    with file_path.open('r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def write_new_file(file,updated_english_data,update_simplified_chinese_data):
    output_csv_file_path = Convert_To_csv(file)   
    with open(output_csv_file_path,"w",encoding='utf-8', newline='') as output_file: 
        csv_writer = csv.writer(output_file)
        for key in updated_english_data.keys():
            csv_writer.writerow([key,updated_english_data[key],update_simplified_chinese_data[key],'New line from v1.6'])

def Find_Key(input_string):
    key =  re.sub('\\s+(".*"):.*\n?', '\\g<1>' , input_string)
    return key

def Convert_To_csv(file_path):
    new_file_path = file_path.with_suffix('.csv')
    new_file_path = 'compare_output_csv' / Path(*list(new_file_path.parts)[3:])
    return new_file_path
    #Path(*list(file.parts)[3:])

def write_csv(csv_writer,key,updated_english_data,update_simplified_chinese_data,old_english_data):
    #cause sometimes they don't have it :(
    try:
        old_english_value = old_english_data[key]
    except KeyError:
        old_english_value = 'New line from v1.6'
    try:
        update_simplified_chinese_value = update_simplified_chinese_data[key]
    except KeyError:
        update_simplified_chinese_value = "Simplified Chinese didn't update"
    
    csv_writer.writerow([key,updated_english_data[key],update_simplified_chinese_value,old_english_value])
    

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
    fanhuaji_json_file = Fanguaji_Corresponding_Path(file)

    #old_traditional_chinese_json_file = Corresponding_Path(file, old_version_file_path, traditional_chinese_folder_name, '.zh-CN.json')
    
    updated_english_data = Read_json(updated_english_json_file)       
    update_simplified_chinese_data = Read_json(update_simplified_json_file)    
    try:
        fanhuaji_data = Read_json(fanhuaji_json_file)   
    except FileNotFoundError:
        print(fanhuaji_json_file)
        continue

    try:
        old_english_data = Read_json(old_english_json_file)
        old_simplified_chinese_data = Read_json(old_simplified_json_file)       
    except FileNotFoundError:
        print(f"新檔案：{old_english_json_file}")
        write_new_file(file,updated_english_data,update_simplified_chinese_data)
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

    output_csv_file_path = Convert_To_csv(file)   
    with open(output_csv_file_path,"w",encoding='utf-8', newline='') as output_file: 
        #output_file.write('\ufeff') #convert to utf-8 bom
        csv_writer = csv.writer(output_file)
        for key in new_key:#new line
            #write_csv(csv_writer,key,updated_english_data,update_simplified_chinese_data,old_english_data)
            write_csv(csv_writer,key,updated_english_data,fanhuaji_data,old_english_data)
            
        for key in modified_key:#modified line      
            #write_csv(csv_writer,key,updated_english_data,update_simplified_chinese_data,old_english_data)
            write_csv(csv_writer,key,updated_english_data,fanhuaji_data,old_english_data)
        
            
    
