import json
import shutil
import re
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at

parent_file_path = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()    
input_simplified_chinese_folder_path = parent_file_path.parent.absolute() / 'Content'

def Output_json(output_file_path,output_data):
    with output_file_path.open('w', encoding='utf-8') as file:
        json.dump(output_data,file,indent=4,ensure_ascii=False)

def Correspoding_File_Path(splitted_flie_list):
    master_branch_path = Path(fr"./master_Branch")
    fanhuaji_folder_path = parent_file_path / 'Fanhuaji' / 'Fanhuaji_output_json'
    for i in range(0,len(splitted_flie_list)):
        if "Content" in splitted_flie_list[i]:
            master_branch_file_path = master_branch_path / Path(*splitted_flie_list[i+1:])
            file_name_parts = splitted_flie_list[-1].split('.zh-CN')
            file_name = ''.join(file_name_parts)
            fanhuaji_file_path =  fanhuaji_folder_path / Path(*splitted_flie_list[i+1:-1]) / file_name
            break
    return fanhuaji_file_path,master_branch_file_path

def Combine_json(input_simplified__chinese_file_path):
    input_simplified__chinese_data = json_Data(input_simplified__chinese_file_path)
    splitted_flie_list = list(input_simplified__chinese_file_path.parts)
    fanhuaji_file_file_path,master_branch_file_path = Correspoding_File_Path(splitted_flie_list)
    fanhuaji_data = json_Data(fanhuaji_file_file_path)
    try:
        master_branch_data = json_Data(master_branch_file_path)
    except FileNotFoundError:#new file
        master_branch_data = input_simplified__chinese_data
        return
    input_simplified__chinese_data['content'] = master_branch_data['content']
    input_simplified__chinese_data['content'].update(fanhuaji_data)
    Output_json(input_simplified__chinese_file_path,input_simplified__chinese_data)



def json_Data(file_path):  
    with file_path.open('r', encoding='utf-8') as file_data:
        data = json.load(file_data)        
        return data

def Get_File_List():
    input_simplified_chinese_file_list = [f for f in input_simplified_chinese_folder_path.glob('**/*.json')]
    
    folders_to_skip = ["LooseSprites", "Maps", "Minigames","TileSheets"]
    
    for file_path in input_simplified_chinese_file_list:
        if any(folder_name in str(file_path.parts) for folder_name in folders_to_skip):
            continue  # Skip this iteration and move to the next file
        
        if "credits.zh-CN.json" in str(file_path):
            continue

        Combine_json(file_path)                


if __name__ == '__main__':
    Get_File_List()
    pass