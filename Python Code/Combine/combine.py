import json
import shutil
import re
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at

parent_file_path = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()    

input_old_tranditional_chinese_path = parent_file_path / ''
input_fanhuaji_path = parent_file_path / 'Fanhuaji' / 'Fanhuaji_output_json'
input_update_simplified_chinese_path = Path(fr"./")
output_path = Path()
