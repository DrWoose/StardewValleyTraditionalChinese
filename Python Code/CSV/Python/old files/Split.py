# 轉成 csv
import re
import csv
import demjson3
import shutil
from pathlib import Path

files = Path("default.json")
csv_split = Path("Split.csv")


def split(key, value):
    value = re.sub('^#?\$c ..#', '', value)  # 開頭的「#$c .5#」、「$c .5#」等等
    value = re.sub('#?(\$.)?#\$c ..#', '\n', value)  # 中間的 $h#$c .5#
    # 開頭的「#$1 AbigailHAND#」、「#$1 LeahBug#」、「#$1 Abigail1#」、「"#$e#%」等等
    value = re.sub('^#?\$[a-zA-Z\d\$# ]+#%?', '', value)

    if not key == "3917626/f Harvey 3500/O Harvey/t 2000 2400/p Harvey/L" and not key == "4325434/f Penny 3500/O Penny/t 1500 1900/p Penny":
        # 選項的「#$q 25/26 summer_Sun_old#」、「$u#$e#$q 5/6 Wed_01_old#」等等
        value = re.sub(
            '(\$.{1,2})?(#\$.)?#\$([a-zA-Z\d /_-]){3,}#', '\n', value)

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

    # 分割成 list
    lst = value.split('\n')
    print(lst)
    # 回傳 list
    return lst

# Dialogue、Strings


def Dialogue(data, dic):
    for key in data:
        value = data[key]

        lst = split(key, value)

        # 加入 dic
        dic.setdefault(key, lst)


temp_dict = {}

# 讀取 json
with files.open('r', encoding='utf-8') as f:
    data = f.read()
    data = demjson3.decode(data)

Dialogue(data, temp_dict)

# 把中英文的 value 跟 key 放進 list
result_list = []
for key in temp_dict:
    for n in range(len(temp_dict[key])):
        result_list.append([temp_dict[key][n], key])

with csv_split.open('w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t',
                        quotechar='"', quoting=csv.QUOTE_ALL)
    # 寫入二維表格
    writer.writerows(result_list)
