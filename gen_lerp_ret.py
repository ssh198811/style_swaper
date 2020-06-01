import cv2
import numpy as np
import os
from PIL import Image


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def read_img(img_path):
    if is_contain_chinese(img_path) is True:
        return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
    else:
        return cv2.imread(img_path)


def write_img(img, img_path=""):
    if os.path.exists(img_path):
        os.unlink(img_path)

    if img is None:
        return

    if is_contain_chinese(img_path) is True:
        if img_path.endswith('.jpg') is True:
            cv2.imencode('.jpg', img)[1].tofile(img_path)
        elif img_path.endswith('.png') is True:
            cv2.imencode('.png', img)[1].tofile(img_path)
    else:
        cv2.imwrite(img_path, img)


def lerp_img(src_path, dst_path, lerp_value):
    # 进行lerp操作
    alpha = 1.0 - float(lerp_value) / 100.0
    beta = float(lerp_value) / 100.0
    gamma = 0

    img_src = read_img(src_path)
    img_dst = read_img(dst_path)

    h_src, w_src, c_src = img_src.shape
    h_dst, w_dst, c_dst = img_dst.shape
    if h_src != h_dst or w_src != w_dst:
        return None, -1

    img_add = cv2.addWeighted(img_src, alpha, img_dst, beta, gamma)
    return img_add, 0


def gen_lerp_ret(base_dir='', content_name=None, style_dir='', lerp_value=50, b_use_expanded=False):
    content_d = base_dir
    style_d = base_dir + "style_output/"

    if b_use_expanded is True:
        content_d += "expanded/"
        style_d += "expanded/"

    for file in os.listdir(content_d):
        if file.endswith(".jpg") is False:
            continue
        if content_name is not None and content_name != file:
            continue

        # 得到原始图片路径
        content_path = content_d + file
        # 得到完全风格化后图片路径
        s_name = os.path.splitext(os.path.basename(style_dir))[0]
        styled_path = style_d + f"{s_name}/" + file

        output_path = base_dir + "lerp_output/" + file
        if os.path.exists(base_dir + "lerp_output/") is False:
            os.makedirs(base_dir + "lerp_output/")

        # lerp
        lerp_ret, ret = lerp_img(content_path, styled_path, lerp_value)
        write_img(lerp_ret, output_path)

        # combine alpha channel
        split_file = os.path.splitext(file)
        assert os.path.exists(content_d + split_file[0] + ".tga")

        tga_img = Image.open(content_d + split_file[0] + ".tga")
        jpg_img = Image.open(output_path)
        assert len(tga_img.getbands()) == 4
        ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
        ir, ig, ib = jpg_img.split()
        tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
        output_path = output_path.replace(".jpg", ".tga")
        tga_img.save(output_path, quality=100)
        print(f"generate tga image {output_path} after lerp op.")


if __name__ == '__main__':
    set_base_dir = 'H:/sword3-products-head/client/data/source/maps_source/foliage/Texture/style_transfer/'

    set_content_name = 'gm_aglaiaodorata001_billboards.jpg'

    set_style_dir = 'E:/Users/shishaohua.SHISHAOHUA1/PycharmProjects/Pytorch_Style_Swap-master/style_test/8.jpeg'

    set_lerp_value = 50

    set_b_use_expended = False

    gen_lerp_ret(set_base_dir, set_content_name, set_style_dir, set_lerp_value, set_b_use_expended)
