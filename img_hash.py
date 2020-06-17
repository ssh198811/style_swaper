import hashlib
from PIL import Image
import numpy as np

def img_hash(strA):
    fd1 = np.array(Image.open(strA)) * np.random.randint(10)
    return hashlib.md5(fd1).hexdigest()


if __name__ == '__main__':
    imageA = 'G:\\test\\style_test\\常玉.jpg'
    imageB = 'G:\\test\\style_test\\常玉2.jpg'
    res = img_hash(imageA)
    print(res)
