import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at

file_path = 'replace_text.txt'
output_txt_file_path = 'replace_text_output.txt'
lines = []

with open(file_path,'r', encoding='utf-8') as file:
        lines = file.readlines()

#print(lines)
line = ''.join(lines)

with open(output_txt_file_path,"w", encoding="utf-8") as output_file:
    output_file.write(repr(line))