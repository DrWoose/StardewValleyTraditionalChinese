# 轉成 xlsx
import re
import csv
import json
import demjson3
import shutil
import pandas as pd
from pathlib import Path

path_split = Path('./split')
path_en = Path('./en')
path_xlsx = Path('./xlsx')

# 讀取 json
def readjson(path):
    with path.open('r', encoding='utf-8') as f:
        json_data = f.read()
        json_data = demjson3.decode(json_data)
        return json_data

# 讀取 csv，並取代
def replace(csv_p, json_data):
    with csv_p.open('r', newline='', encoding='utf-8-sig') as csvfile: #Trados 匯出要用 utf-8-sig 讀取
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            key = row[0]
            value_en = row[1]
            value_zh = row[2]
            json_data[key] = json_data[key].replace(value_en, value_zh, 1)  # 用中文取代英文，並且只能取代一次
    return json_data

# 轉換路徑
def change_p(path, folder, suffix):
    path = list(path.parts)
    path[0] = folder
    path = Path(*path)
    path = path.with_suffix(suffix)
    return path

# 轉成 xlsx
def xlsx(xlsx_p):
    # 把 key 跟value 放進 list
    result_list = []
    for key in json_data_en:
        result_list.append([key, json_data_en[key] ,json_data_zh[key]])
    
    header = ['CONTEXT', 'EN', 'ZH']
    df = pd.DataFrame(result_list)
    writer = pd.ExcelWriter(xlsx_p, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='SVE Project', header=header, index=False)
    writer.close()

# 檔案列表
csv_list = [f for f in path_split.glob('**/*.csv')]
for csv_p in csv_list:
    # 轉換路徑
    json_p = change_p(csv_p, path_en, '.json')

    # 讀取英文 json 檔
    json_data_en = readjson(json_p)

    # 沒有中文的就跳過
    try:
        # 讀取 csv，並將英文 json 檔取代成中文（傳副本進去）
        json_data_zh = replace(csv_p, json_data_en.copy())
    except IndexError: continue

    # 顯示檔案路徑
    print(csv_p.name)

    # 轉換路徑
    xlsx_p = change_p(csv_p, path_xlsx, '.xlsx')
    
    # 建立目錄
    xlsx_p.parent.mkdir(parents=True, exist_ok=True)

    xlsx(xlsx_p)
    # # 轉成 json 格式
    # json_dump = json.dumps(json_data_zh, ensure_ascii=False, indent=4, separators=(',', ': '))

    # # 寫入
    # dump_path = Path(f'xlsx/{csv_p.name}.json')
    # with dump_path.open('w', encoding='utf-8') as f:
    #     f.write(json_dump)
