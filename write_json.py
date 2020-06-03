import  json
def store(data):
    with open('data.json', 'w') as fw:
        # 将字典转化为字符串
        # json_str = json.dumps(data)
        # fw.write(json_str)
        # 上面两句等同于下面这句
        json.dump(data,fw)
# load json data from file
def load():
    with open('data.json','r') as f:
        data = json.load(f)
        return data

if __name__ == "__main__":
    # json_data = '{"map":[{"path":"data\source\maps_source\\texture","name":".\\maps_source\\texture"},' \
    #             '{"path":"data\source\maps_source\\foliage\\texture","name":".\\foliage\\texture"},' \
    #             '{}]}'
    # dict={}
    # dict["data\source\maps_source\\texture"]=".\\maps_source\\texture"
    # dict["data\source\maps_source\\foliage\\texture"]=".\\foliage\\texture"
    # dict["data\source\maps_source\\background\\texture"]=".\\background\\texture"
    # dict["data\source\maps_source\\texture\skytexture"]=".\\texture\skytexture"
    # dict["data\source\maps_source\\texture\\terraintexture\soil"]=".\\terraintexture\soil"
    # dict["data\source\maps_source\\texture\\terraintexture\moss"]=".\\terraintexture\moss"
    # dict["data\source\maps_source\\texture\\terraintexture\grass"]=".\\terraintexture\grass"
    # dict["data\source\combitextures"]=".\combitextures"
    # dict["data\source\maps_source\\texture\\terraintexture\stone"]=".\\terraintexture\stone"
    # dict["data\source\maps_source\\texture\\terraintexture\cliff"]=".\\terraintexture\cliff"
    # dict["data\source\maps_source\\texture\\terraintexture\\noise"]=".\\terraintexture\\noise"
    # dict["data\source\\texture"]=".\\texture"
    # dict["data\source\maps\XXXX\\baked"]="baked"
    # dict["data\source\maps\XXXX\env_probe"]="env_probe"
    # dict["data\source\maps\XXXX\landscape\procedural"]=".\landscape\procedural"
    # # j=json.dumps(dict)
    # with open('data.json', 'w') as fw:
    #     # 将字典转化为字符串
    #     # json_str = json.dumps(data)
    #     # fw.write(json_str)
    #     # 上面两句等同于下面这句
    #     json.dump(dict, fw,sort_keys=True,indent=4,separators=(',', ':'))
    # # 函数是将json格式数据转换为字典
    # # data = json.loads(json_data)
    # # store(data)
    #
    # # data = load()
    # # print(data)
    with open(".\data.json", 'r') as f:
        # print(f)
        import os
        a=[]
        temp=json.loads(f.read())
        fw = open('E:\PycharmProject\style_swaper-master\稻香村.txt', "r", encoding="utf-8-sig")
        for file in fw:
            file_path = file.replace("\n", "").replace("\\","/")
            parent_path = os.path.dirname(file_path)
            # print(parent_path)
            file_split=parent_path.split("/")
            if len(file_split)>=3:
                if file_split[-1]=='baked' and file_split[-3]=='maps' and f'./{file_split[-2]}/{file_split[-1]}' not in a:
                    a.append(f'./{file_split[-2]}/{file_split[-1]}')
                if file_split[-1]=='env_probe' and file_split[-3]=='maps' and f'./{file_split[-2]}/{file_split[-1]}' not  in a :
                    a.append(f'./{file_split[-2]}/{file_split[-1]}')
                if file_split[-1]=='procedural' and file_split[-2]=='landscape' and f'./{file_split[-2]}/{file_split[-1]}' not  in a :
                    a.append(f'./{file_split[-2]}/{file_split[-1]}')
            # if file_split[-1]
            if  parent_path not in temp:
                continue
            if temp[parent_path] not in a:
                a.append(temp[parent_path])
        for i in a:
            print(i)
        print(len(a))
    # js_obj=json.loads('.\landscape\procedural')
    # print(js_obj)