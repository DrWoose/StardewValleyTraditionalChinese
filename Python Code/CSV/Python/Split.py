# 拆開句子
import re
import csv
import demjson3
import shutil
from pathlib import Path

path = Path('./en')
path_split = Path('./split')

# 檔案列表
json__list = [f for f in path.glob('**/*.json')]

# 處理文本中的程式碼
def split(key, value):
    value = re.sub('^#?\$c ..#', '', value)  # 開頭的「#$c .5#」、「$c .5#」等等
    value = re.sub('#?(\$.)?#\$c ..#', '\n', value)  # 中間的 $h#$c .5#
    # 開頭的「#$1 AbigailHAND#」、「#$1 LeahBug#」、「#$1 Abigail1#」、「"#$e#%」等等
    value = re.sub('^#?\$[a-zA-Z\d\$# ]+#%?', '', value)

    if not key == "3917626/f Harvey 3500/O Harvey/t 2000 2400/p Harvey/L" and not key == "4325434/f Penny 3500/O Penny/t 1500 1900/p Penny":
        # 選項的「#$q 25/26 summer_Sun_old#」、「$u#$e#$q 5/6 Wed_01_old#」等等
        value = re.sub(
            '(\$.{1,2})?(#\$.)?#?\$([a-zA-Z\d /_-]){3,}#', '\n', value)

    # 中間的「#$e#」、「$h#$b#」、「$h%revealtasteEmily207#$e#」、「#$b#$y '」等等
    value = re.sub(
        "(\$.{1,2}){0,2}(%revealtasteEmily207)?#\$.#%?(\$y ')?", '\n', value)
    value = re.sub('#e#', '\n', value)  # Alex 的 #e#
    value = re.sub('(\$.{1,2})?\|', '\n', value)  # 符號 |
    value = re.sub('(%fork)?(\$.{1,2})?\^{1,2}',
                   '\n', value)  # 符號 ^、「^^」、「%fork$a^」等等
    # 結尾的「$h」、「$8%fork」、「%fork$a」等等
    value = re.sub('(%fork)?\$.{1,2}(%fork)?$', '', value)
    value = re.sub('^%(?!k)', '', value)  # 開頭的 %
    value = re.sub("^\$y '", '', value)  # 開頭的 $y '

    # $y 針對某個 key 個別處理
    if key == "Phone_Ring_Lewis":
        value = re.sub("(\$.)?\*", '\n', value)  # 中間的 * 號

    # 寫在最後，避免錯誤取代
    value = re.sub('(\$.)?_', '\n', value)  # 中間的 _
    value = re.sub('^ ?#', '', value)  # 開頭的 #、前面可能有空白
    value = re.sub('#', '\n', value)  # 中間的 #
    value = re.sub('\$.', '\n', value)  # 中間的 $h 等等

    # 物品
    value = re.sub('\[[\d ]+\]', '', value)  # 物品

    # 分割成 list
    split_lst = value.split('\n')

    # 回傳 list
    return split_lst

# 讀取 json
def readjson(path):
    with path.open('r', encoding='utf-8') as f:
        json_data = f.read()
        json_data = demjson3.decode(json_data)
        return json_data

# 轉成 key 和 value(列表)，放進 temp_dict
def key_split(json_data, dic):
    for key in json_data:
        value = json_data[key]
        split_lst = split(key, value)
        # 加入 dic
        dic.setdefault(key, split_lst)

# 儲存成 csv
def save_to_csv(temp_dict, file_path):
    # 把中英文的 value 跟 key 放進 list
    result_list = []
    for key in temp_dict:
        for n in range(len(temp_dict[key])):
            # 如果不是空的
            if temp_dict[key][n]:
                result_list.append([key, temp_dict[key][n]])

    with file_path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        # 寫入二維表格
        writer.writerows(result_list)

# 轉換路徑
def change_p(path):
    path = list(path.parts)
    path[0] = path_split
    path = Path(*path)
    path = path.with_suffix('.csv')
    return path

# main
for json_p in json__list:
    # 轉換路徑
    csv_p = change_p(json_p)

    # 有了就跳過
    if csv_p.exists():
        continue
    
    # 顯示檔案路徑
    print(json_p.name)

    # 讀取 json 檔
    json_data = readjson(json_p)

    # 建立暫存字典
    temp_dict = {}

    # 轉成 key 和 value(列表)，放進 temp_dict
    key_split(json_data, temp_dict)

    # 建立目錄
    csv_p.parent.mkdir(parents=True, exist_ok=True)

    # 儲存 csv
    save_to_csv(temp_dict, csv_p)

print('Done!')