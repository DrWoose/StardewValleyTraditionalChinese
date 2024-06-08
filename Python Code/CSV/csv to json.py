# 轉回 json
import re
import csv
import json
import shutil
from pathlib import Path

src_en = Path('./v1.5.4_en') # 英文路徑
dst = Path('./csv') # 工作資料夾路徑
optput = Path('./optput') # 輸出路徑

content = dst / 'Content'

# 檔案連結
file_list = content.glob('**/*.csv')

for path in file_list:
    # 轉成英文路徑
    path_en = src_en / path.relative_to(dst).with_suffix('.json')
    
    # 讀取英文 json
    with path_en.open('r', encoding='utf-8') as f:
        data =  json.load(f)
        
    # 讀取 csv
    with path.open('r', newline='', encoding='utf-8-sig') as csvfile: # Trados 匯出要用 utf-8-sig 讀取
        rows = csv.reader(csvfile, delimiter='\t')
        for row in rows:
            value_en = row[0]
            value_cn = row[1]
            key = row[2]
            data['content'][key] = data['content'][key].replace(value_en, value_cn ,1) # 用中文取代英文，並且只能取代一次

    # 轉成 json 格式
    data = json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ': ')) 
    
    # 寫入
    path = optput / path.relative_to(dst).with_suffix('.zh-CN.json')
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open('w', encoding='utf-8') as f:
        f.write(data)
        
print('done')
input('按 Enter 鍵關閉...')