import pathlib
import json
import shutil
from pathlib import Path

sdv_5 = Path(fr'.\StardewValleyv1.5')
sdv_6 = Path(fr'.\StardewValleyv1.6')
en = 'English'
cn = 'Simplified Chinese'
tw = 'TraditionalChinese'

list1 = sdv_6 / en
# 檔案列表
json_list = [f for f in list1.glob('**/*.json')]


# 轉換路徑
def change_p(path, folder, lang, suffix):
    path = list(path.parts)
    path[0] = folder
    path[1] = lang
    path = Path(*path)
    path = path.with_suffix(suffix)
    return path

# 讀取 json
def readjson(path):
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
        return data

for j in json_list:
    print(j.name)
    # 轉換路徑
    j_6_en = j
    j_5_en = change_p(j, sdv_5, en, '.json')
    j_6_cn = change_p(j, sdv_6, cn, '.zh-CN.json')
    j_5_cn = change_p(j, sdv_5, cn, '.zh-CN.json')
    j_5_tw = change_p(j, sdv_5, tw, '.zh-CN.json')
    
    # 讀取 json
    j_6_en_d = readjson(j_6_en)
    j_5_en_d = readjson(j_5_en)
    j_6_cn_d = readjson(j_6_cn)
    j_5_cn_d = readjson(j_5_cn)
    # j_5_tw_d = readjson(j_5_tw)

    for key in j_6_en_d:
            try:
                j_6_en_v = j_6_en_d[key]
                j_6_cn_v = j_6_cn_d[key]
                j_5_en_v = j_5_en_d[key]
            except KeyError as e:
                print('Key:',key)
                print('Value:', j_6_en_v)
                print('Value:', j_6_cn_v)
                print('=' * 50)
            else:
                # j_5_cn_v = j_5_cn_d[key]
                # j_5_tw_v = j_5_tw_d[key]

                if j_6_en_v != j_5_en_v:
                    print('Key:', key)
                    print('英文v1.6：',j_6_en_v)
                    print('英文v1.5：',j_5_en_v)
                    print('簡中v1.6：',j_6_cn_v)
                    # print('簡中v1.5：',j_5_cn_v)
                    # print('繁中v1.5：',j_5_tw_v)
                    print('=' * 50)
    break