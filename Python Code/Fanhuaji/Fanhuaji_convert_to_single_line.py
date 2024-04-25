import os
import glob
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at
file_list = [f for f in glob.glob('Tranlation_Rule/*.txt')]
print(file_list)

for file_path in file_list:        
        lines = []
        with open(file_path,'r', encoding='utf-8') as file:
                lines = file.readlines()        
        line = ''.join(lines)

        output_txt_file_path = 'Tranlation_Rule_Single_Line/' + Path(file_path).stem + '_single_line.txt'
        print(output_txt_file_path)
        with open(output_txt_file_path,"w", encoding="utf-8") as output_file:
                output_file.write(repr(line))