import json
import shutil
import re
import os
import glob
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at

Python_Code_folder_path = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()
master_folder_path = Python_Code_folder_path.parent.absolute()
Replace_Version_folder_path = master_folder_path / 'Replace Version' / 'Content'
Content_Patcher_Version_folder_path = master_folder_path / 'Content Patcher Version' / 'assets'


def json_Data(file_path):  
    with open(file_path,'r', encoding='utf-8') as file_data:
        data = json.load(file_data) 
        Convert_to_Content_Patcher(data,file_path)

def Correspoding_File_Path(splitted_flie_list):
    for i in range(0,len(splitted_flie_list)):
        if "Content" in splitted_flie_list[i]:
            master_branch_file_path = master_folder_path / Path(*splitted_flie_list[i+1:])
            file_name_parts = splitted_flie_list[-1].split('.zh-CN') 
            file_name_parts.insert(1,'.zh-TW')
            file_name = ''.join(file_name_parts)
            Content_Patcher_Version_file_path =  Content_Patcher_Version_folder_path / Path(*splitted_flie_list[i+1:-1]) / file_name
            break
    return Content_Patcher_Version_file_path

def Convert_to_Content_Patcher(data,file_path):
    splitted_flie_list = list(file_path.parts)
    output_file_path = Correspoding_File_Path(splitted_flie_list)
    
    print(output_file_path)
    with open(output_file_path,'r+', encoding='utf-8') as file:
        output_data = json.load(file)
        output_data["Changes"][0]["Entries"].update(data["content"])
        json.dump(output_data,file,indent=4,ensure_ascii=False)
        file.seek(0)
        # Write the updated data
        json.dump(output_data, file, indent=4, ensure_ascii=False)
        # Truncate the file to remove any remaining old content
        file.truncate()
    pass
    
    
def Get_File_List():
    input_file_list = [f for f in Replace_Version_folder_path.glob('**/*.json')]      
    folders_to_skip = ["LooseSprites", "Maps", "Minigames","TileSheets"]
    for file_path in input_file_list:
        if any(folder_name in str(file_path.parts) for folder_name in folders_to_skip):
            continue  
        if "credits.zh-CN.json" in str(file_path):
            continue
        json_Data(file_path)


if __name__ == '__main__':
    Get_File_List()
    pass