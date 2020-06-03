txt='E:\PycharmProject\style_swaper-master\稻香村.txt'
import os
f = open(txt, "r", encoding='utf-8-sig')
parent_dir_txt = []
for file_path in f:
    file_path = file_path.replace("\n", "")
    # file_name = os.path.basename(file_path)
    file_path =  file_path
    parent_path=os.path.dirname(file_path)

    if parent_path not in parent_dir_txt:

        parent_dir_txt.append(parent_path)
with open('./parentDirs.txt', 'w')as fs:
    for i in parent_dir_txt:
        fs.write(f"{i}\n")
fs.close()