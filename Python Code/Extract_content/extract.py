import json
import shutil
import re
import os
import glob
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at

input_folder_path = Path(fr"./Input")
file_name = ''
new_dict : dict = {}

def Output_json(output_data,file_name):
    output_folder_path = Path(fr'./Output')
    output_folder_path = output_folder_path / file_name
    print(output_folder_path)
    with open(output_folder_path,'w', encoding='utf-8') as file:
        json.dump(output_data,file,indent=4,ensure_ascii=False)

def Extract_content(data,file_name):
    data_dict : dict = data['content']
    key_list = list(data_dict.keys())
    for key in key_list:
        string : str = data_dict[key]
        splitted_string = string.split('/')
        temp_dict = {
            splitted_string[0].strip() + "_Name": splitted_string[4],
            splitted_string[0].strip() + "_Description": splitted_string[5]
        }        
        new_dict.update(temp_dict)
    data['content'] = new_dict
    Output_json(data,file_name)
        

def json_Data(file_path,file_name):  
    with open(file_path,'r', encoding='utf-8') as file_data:
        data = json.load(file_data) 
        Extract_content(data,file_name)       
    
    
def Get_File_List():
    input_file_list = [f for f in input_folder_path.glob('**/*.json')]   
    for file_path in input_file_list:
        head,tail = os.path.split(file_path)
        file_name = tail
        json_Data(file_path,file_name)                


if __name__ == '__main__':
    Get_File_List()
    pass