import json
import requests

url = "https://api.zhconvert.org/convert"
headers = {
	# 指定 Content-Type 為 application/json
    # 必須培養手動設定的習慣，不然有時候沒注意到，會帶了前一支 API 的 Content-Type，會傻傻的不知道為什麼打不通
	"Content-Type": "application/json"
}

def zhconvert(text):
    request_body = {
        "text": text,
        "converter": "Taiwan",
        "EllipsisMark": 1,
        "QuotationMark": 1,
        "RemoveSpaces":1,
        "trimTrailingWhiteSpaces" : True
    }

    # 以 post method 發出 request
    response = requests.get(url, json=request_body, headers=headers)

    # 由於知道 response 的 Content-Type 是 application/json
    # 可用 json() 讀取 Response 內容
    # 應用 json 套件作排版顯示，不然資料量大的時候，閱讀會比較困難
    # 使用 indent 參數設定縮排為 4 個空格
    text = response.json()['data']['text']
    return text
    # print("Response:", json.dumps(response.json(), ensure_ascii=False, indent=4))

if __name__ == '__main__':
    zh_cn = '视频好好看'
    print(f'原句子：{zh_cn}')
    print(f'台灣化：{zhconvert(zh_cn)}')