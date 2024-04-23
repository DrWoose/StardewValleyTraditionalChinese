# 轉成 xlsx
import re
import csv
import json
import demjson3
import shutil
import pandas as pd
from pathlib import Path

path_sve_cp = Path('./default_CP.json')
path_sve_JA = Path('./default_JA.json')
path_xlsx_cp = Path(r'.\xlsx\Stardew Valley Expanded\[CP] Stardew Valley Expanded')

# 讀取 json
def readjson(path):
    with path.open('r', encoding='utf-8') as f:
        json_data = f.read()
        json_data = demjson3.decode(json_data)
        return json_data

json_data = readjson(path_sve_cp)

# 檔案列表
xlsx_list = [f for f in path_xlsx_cp.glob('**/*.xlsx')]
for xlsx_p in xlsx_list:
    # 轉成 rows 列表
    df = pd.read_excel(xlsx_p)
    rows = df.values.tolist()

    temp_dict = {}
    for row in rows:
        key = row[0]
        en  = row[1]
        zh  = row[2]
        # 如果不是空的
        if not pd.isna(zh):
            temp_dict.setdefault(key, zh)

    json_data.update(temp_dict)

# 轉成 json 格式
json_dump = json.dumps(json_data, ensure_ascii=False, indent=4, separators=(',', ': ')) 

p = Path('./zh.json')
with p.open('w', encoding='utf-8') as f:
    f.write(json_dump)
    