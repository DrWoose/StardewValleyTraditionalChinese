import json
import shutil
import re
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at

folder_path = Path(fr'.\StardewValleyv1.6')
file_list = [f for f in folder_path.glob('**/*.json')]
output_path = Path(fr'.\compare_output')
suffix = ".json"

def Read_json(file_path):
    with file_path.open('r+', encoding='utf-8') as file:
        data = json.load(file)
        return data

def Find_Corresponding_File():
    for file_path in file_list:
        if ".zh-TW" not in os.path.basename(file_path):
            file_name = Path(file_path).stem
            parted_path = list(file_path.parts)#split path
            parted_path[-1] = file_name + ".zh-TW" + ".json"
            Traditional_Chinese_path = Path(*parted_path)
            English_data = Read_json(file_path)
            Traditional_Chinese_data = Read_json(Traditional_Chinese_path)        
            Compare_Key(English_data,Traditional_Chinese_data,file_name)

def Compare_Key(English_data,Traditional_Chinese_data,file_name):
    added_line : dict = {}
    deleted_line : dict = {}
    update_key : set = set(English_data.keys())
    legacy_key : set = set(Traditional_Chinese_data["Changes"][0]["Entries"].keys())
    deleted_key = legacy_key - update_key
    added_key = update_key - legacy_key
    for key in added_key:
        added_line.update({key: English_data[key]})
    for key in deleted_key:
        deleted_line.update({key: Traditional_Chinese_data["Changes"][0]["Entries"][key]})

    added_key_file_path = output_path / (file_name  + "_added_output.json")
    
    with open(added_key_file_path,"w", encoding="utf-8") as output_file:
        json.dump(added_line,output_file,indent=4,ensure_ascii=False)
    
    deleted_key_file_path = output_path / (file_name  + "_deleted_output.json")
    
    with open(deleted_key_file_path,"w", encoding="utf-8") as output_file:
        json.dump(deleted_line,output_file,indent=4,ensure_ascii=False)
    


if __name__ == '__main__':
    Find_Corresponding_File()
    pass