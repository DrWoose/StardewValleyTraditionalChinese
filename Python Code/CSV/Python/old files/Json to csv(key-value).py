# 轉成 csv
import re
import csv
import demjson3
import shutil
from pathlib import Path

files = Path("default.json")
csv_split = Path("key-value.csv")

# 讀取 json
with files.open('r', encoding='utf-8') as f:
    data = f.read()
    data = demjson3.decode(data)

# 把 key 跟value 放進 list
result_list = []
for key in data:
    result_list.append([key, data[key]])

# 寫入 csv
with csv_split.open('w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_ALL)
    # 寫入二維表格
    writer.writerows(result_list)
