import hashlib
from PIL import Image
import numpy as np


def img_hash(str):
    fd1 = np.array(Image.open(str))
    return hashlib.md5(fd1).hexdigest()


if __name__ == '__main__':
    imageA = 'G:\\test\\style_test\\呐喊1.jpg'
    imageB = 'G:\\test_multi_pics2\\cliff4\\呐喊1.jpg'
    imageC = 'G:\\test\\style_test\\呐喊2.jpg'
    res1 = img_hash(imageA)
    res2 = img_hash(imageB)
    res3 = img_hash(imageC)
    print(res1 == res2, res1 == res3, res2 == res3)
