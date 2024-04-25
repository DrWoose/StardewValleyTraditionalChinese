import json
import requests
import glob
import os
from pathlib import Path

url = "https://api.zhconvert.org/convert"
headers = {
	# 指定 Content-Type 為 application/json
    # 必須培養手動設定的習慣，不然有時候沒注意到，會帶了前一支 API 的 Content-Type，會傻傻的不知道為什麼打不通
	"Content-Type": "application/json"
}

os.chdir(os.path.dirname(os.path.realpath(__file__)))#set working path to where .py file at
file_list = [f for f in glob.glob('Tranlation_Rule_Single_Line/*.txt')]
#print(file_list)


single_line_txt = {}
post_replace_txt = ''
pre_replace_txt = ''
protect_txt = ''


for file_path in file_list:        
        line = ''
        with open(file_path,'r', encoding='utf-8') as file:
                line = file.readline()        
        single_line_txt.update({Path(file_path).stem: line})

                    
def zhconvert(text):
    request_body = {
        "text": text,
        "converter": "Taiwan",
        "userPostReplace":single_line_txt['post_replace_single_line'],
        "userPreReplace":single_line_txt['pre_replace_single_line'],
        "userProtectReplace":single_line_txt['protect_single_line'],
        # don't have this parameter
        # "EllipsisMark": 1,
        # "QuotationMark": 1,
        # "RemoveSpaces":1,
        # "trimTrailingWhiteSpaces" : True
    }

    # 以 post method 發出 request
    response = requests.get(url, json=request_body)
    print(response.json())
    # 由於知道 response 的 Content-Type 是 application/json
    # 可用 json() 讀取 Response 內容
    # 應用 json 套件作排版顯示，不然資料量大的時候，閱讀會比較困難
    # 使用 indent 參數設定縮排為 4 個空格
    text = response.json()['data']['text']
    return text
    # print("Response:", json.dumps(response.json(), ensure_ascii=False, indent=4))

def Read_json(file_path):  
    with file_path.open('r', encoding='utf-8') as file:
        data = json.load(file)
        return data

if __name__ == '__main__':
    zh_cn = '衣衫襤褸'
    print(f'原句子：{zh_cn}')
    print(f'台灣化：{zhconvert(zh_cn)}')