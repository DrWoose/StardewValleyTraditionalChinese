import json
import shutil
import re
import os
import glob
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at



def Output_json(output_data,file_name):
    output_folder_path = Path(fr'./Output')
    output_folder_path = output_folder_path / file_name
    print(output_folder_path)
    with open(output_folder_path,'w', encoding='utf-8') as file:
        json.dump(output_data,file,indent=4,ensure_ascii=False)

def json_Data(file_path,file_name):  
    with open(file_path,'r', encoding='utf-8') as file_data:
        data = json.load(file_data) 
        Convert_to_Content_Patcher(data,file_name)

def Convert_to_Content_Patcher():
    
    pass
    
    
def Get_File_List():
    input_folder_path = Path(fr"./Input")
    input_file_list = [f for f in input_folder_path.glob('**/*.json')]   
    for file_path in input_file_list:
        head,tail = os.path.split(file_path)
        file_name = tail
        json_Data(file_path,file_name)                


if __name__ == '__main__':
    Get_File_List()
    pass