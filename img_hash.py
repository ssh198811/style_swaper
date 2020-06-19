import hashlib
from PIL import Image
import numpy as np
import os

def img_hash(str):
    fd1 = np.array(Image.open(str))
    return hashlib.md5(fd1).hexdigest()
def make_pics_dict(pics_list=[],s_dict={}):
    for pic in pics_list:
        s_name = os.path.basename(pic).split('.')[0]
        s_dict[s_name] = img_hash(pic)

def search_pics_dict(pics,s_dict={},s_differ=False):
        s_name = os.path.basename(pics).split('.')[0]
        pics_hash = img_hash(pics)
        print(pics_hash)
        if s_name in s_dict:
            if s_dict[s_name] != pics_hash:
                s_differ = True
                s_dict[s_name] = pics_hash
        return s_differ


if __name__ == '__main__':
    s_list = []
    imageA = 'G:\\test\\style_test\\呐喊.jpg'
    imageB = 'G:\\test_multi_pics2\\cliff4\\呐喊1.jpg'
    imageC = 'G:\\test\\style_test\\呐喊2.jpg'
    imageD = 'C:\\Users\\Kingsoft\\Pictures\\呐喊.jpg'

    res1 = img_hash(imageA)
    res2 = img_hash(imageB)
    res3 = img_hash(imageC)
    print(res1 == res2, res1 == res3, res2 == res3)

    s_list.append(imageA)
    s_list.append(imageB)
    s_list.append(imageC)
    s_exists = False
    s_dict = {}
    make_pics_dict(s_list, s_dict)
    print(s_dict)

    a = search_pics_dict(imageD, s_dict, s_exists)
    print(a)
