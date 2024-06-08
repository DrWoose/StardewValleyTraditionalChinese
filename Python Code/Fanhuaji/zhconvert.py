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

single_line_txt = {}

def output_to_json(output_json_data,file : Path):
    
    splitted_path_list = list(file.parts)
    for i in range(0,len(splitted_path_list)):
        if "compare" in splitted_path_list[i]:
            splitted_path_list[i] = "Fanhuaji"
            splitted_path_list[i+1] = "Fanhuaji_output_json"
            break
    output_file_path = Path(*splitted_path_list)
    
    with open(output_file_path,"w", encoding='utf8') as output_file:
        json.dump(output_json_data,output_file,indent=4,ensure_ascii=False)

def Convert_to_single_line(json_data):
    simplified_chinese_line = ""
    key_list = json_data.keys()
    for key in key_list:
        simplified_chinese_line += "Fanhuaji" + json_data.get(key)    
    traditional_chinese_single_line : str = Zhconvert(simplified_chinese_line)
    traditional_chinese_line = traditional_chinese_single_line.split("Fanhuaji")
    return traditional_chinese_line

def Read_json_line(file):
    
    output_json_data = {}
    json_data : dict = Read_json(file)
    key_list = list(json_data.keys())
    traditional_chinese_line_list = Convert_to_single_line(json_data)
    
    for index in range(len(key_list)):
        output_json_data.update({key_list[index]:traditional_chinese_line_list[index+1]})

    output_to_json(output_json_data,file)


def Get_json_list():
    parent_file_path = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()
    file_path = parent_file_path / 'update_compare' / 'compare_output_json'
    file_list = [f for f in file_path.glob('**/*.json')]
    for index, file in enumerate(file_list):
        progress : float = round((index / len(file_list)) * 100,1)
        print(f"Progress:{progress}%")
        Read_json_line(file)
        print(f"{file.stem} Completed!")
        


def Read_txt():
    file_list = [f for f in glob.glob('Tranlation_Rule/*.txt')]

    for file_path in file_list:        
        line = ''               
        lines = []
        with open(file_path,'r', encoding='utf-8') as file:
                lines = file.readlines()        
        line = ''.join(lines)
        single_line_txt.update({Path(file_path).stem: line})


                    
def Zhconvert(text):

    request_body = {
        "text": text,
        "converter": "Taiwan",
        "userPostReplace":single_line_txt['post_replace'],
        "userPreReplace":single_line_txt['pre_replace'],
        "userProtectReplace":single_line_txt['protect'],
        # don't have this parameter
        # "EllipsisMark": 1,
        # "QuotationMark": 1,
        # "RemoveSpaces":1,
        # "trimTrailingWhiteSpaces" : True
    }

    # 以 post method 發出 request
    response = requests.get(url, json=request_body)
    # 由於知道 response 的 Content-Type 是 application/json
    # 可用 json() 讀取 Response 內容
    # 應用 json 套件作排版顯示，不然資料量大的時候，閱讀會比較困難
    # 使用 indent 參數設定縮排為 4 個空格
    text = response.json()['data']['text']
    return text
    # print("Response:", json.dumps(response.json(), ensure_ascii=False, indent=4))

def Read_json(json_file_path):  
    with json_file_path.open('r', encoding='utf-8') as file:
        data = json.load(file)
        return data

if __name__ == '__main__':
    Read_txt()
    Get_json_list()

    # zh_cn = '山洞蘿蔔'
    # print(f'原句子：{zh_cn}')
    # print(f'台灣化：{Zhconvert(zh_cn)}')