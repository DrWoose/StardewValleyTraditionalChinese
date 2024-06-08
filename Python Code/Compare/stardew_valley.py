import re, os
from pathlib import Path

subfolder_path = r'\Characters\Dialogue' 
updated_folder_path  = r'D:\StardewValley\StardewValleyTranslation\StardewValleyEnglish\Unpacked_v1.6\Content(unpacked)' + subfolder_path
old_folder_path  = r'D:\StardewValley\StardewValleyTranslation\StardewValleyEnglish\Unpack_v1.5\Content (unpacked)' + subfolder_path
correspond_folder_path = r'D:\StardewValley\StardewValleyTranslation\StardewValleySimplifiedChinese\unpack_v1.6\Content(unpacked)' + subfolder_path
correspond_file_suffix = '.zh-CN'
file_name = []

# ===== 檔案列表 ===== #
try:
    for i in os.listdir(updated_folder_path):        
        file_name.append(i)

except FileNotFoundError:
    print('資料夾不存在！')

for i in file_name:
    # ===== text ===== #
    with open(f"{updated_folder_path}\{i}", encoding='utf-8') as f:
        updated_data = f.readlines()

    with open(f"{old_folder_path}\{i}", encoding='utf-8') as f:
        old_data = f.readlines()
    
    with open(f"{correspond_folder_path}\{i[:-5] + correspond_file_suffix + i[-5:]}", encoding='utf-8') as f:
        correspond_data = f.readlines()

    updated_text = []
    old_text = []
    correspond_text = []  
    for i in updated_data:
        print(re.sub('"$\n?','",\n', i))
        updated_text.append(re.sub('"$\n?','",\n', i))

    for i in old_data:
        old_text.append(re.sub('"$\n?','",\n', i))
    for i in correspond_data:
        correspond_text.append(re.sub('"$\n?','",\n', i))

    # ===== json key ===== #
    key145 = []

    for i in old_text:
        key145.append(re.sub('\s+(".*"):.*\n?', '\g<1>' , i))

    # ===== 找出不同 ===== #
    line = []
    difline = []
    for i in updated_text:
        if i not in old_text:
            line.append(i) # 所有差異
            for x in key145:
                if x in i:
                    difline.append(i) # 之前就有但有更動

    newline = [i for i in line if i not in difline]  # 新句子

    print(y) # file name

    print("新句子：")
    for i in newline:
        print(i.strip())

    keydif = []
    text_old = []
    text_oldt = []
    if difline != [] :
        print("\n有更動（上：簡 1.4、中：簡 1.5、下：繁 1.4）：")
    for i in difline:
        keydif.append(re.sub('\s+(".*"):.*\n?', '\g<1>' , i))

    for i in keydif:
        for x in old_text:
            if i in x:
                text_old.append(x)
        for x in correspond_text:
            if i in x:
                text_oldt.append(x)

    for i in range(0,len(text_old)):
        print(text_old[i].strip())
        print(difline[i].strip())
        print(text_oldt[i].strip())
        print('')

    print('=' * 65)
