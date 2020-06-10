


from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QMessageBox , QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QUrl, QPoint,QSize,QRect
from PyQt5 import QtGui
from combocheckbox import ComboCheckBox
from PyQt5.QtGui import QIcon, QDesktopServices,QPixmap
import  Ui_test519
import  os
import time
import InfoNotifier
from PIL import Image
import cv2
import glob

from  Gen_Style import style_transfer

import  gen_jpg_tga_from_dds
import json
import gen_lerp_ret

from path_util import PathUtils

#################################################tab2
class My_gen_dds_jpg_thread2(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(My_gen_dds_jpg_thread2, self).__init__()

    def set_para(self, file_='', work_='', dds_list=[]):
        self.file_ = file_
        self.work_ = work_
        self.dds_list = dds_list

    def gen_jpg_tga(self):
        gen_jpg_tga_from_dds.gen_jpg_tga(self.file_, self.work_, self.dds_list)
        InfoNotifier.InfoNotifier.g_progress_info.append("已生成jpg,tga格式图片，点击下拉框选择目录进行预览")
        self._signal.emit()

    def run(self):
        self.gen_jpg_tga()
        # self.show_previewed_before_pic2()


class My_gen_style_temp_thread2(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(My_gen_style_temp_thread2, self).__init__()

    def set_para(self, show_list=[], chosen_style_pic='', temp_file=''):
        self.show_list = show_list
        self.chosen_style_pic = chosen_style_pic
        # 根目录
        self.temp_file_name = temp_file

    def gen_style(self):
        style_pic = self.chosen_style_pic
        content_list = self.show_list
        # if os.path.exists(self.temp_file_name) is False:
        #     os.makedirs(self.temp_file_name)
        # index=0
        # for i in content_list:
        #     save_temp_dir=self.temp_file_name+str(index)+'.jpg'
        # style_name = os.path.basename(style_pic).split('.')[0]
        style_transfer.style_main2(content_list, style_pic)
        InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览")

        self._signal.emit()

    def run(self):
        self.gen_style()


class My_gen_style_thread2(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(My_gen_style_thread2, self).__init__()
        self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"

    def set_para(self, txt_path='', work_='', lerg_value=50, chosen_style_pic='', chosen_content_file_list=[],
                 dir_dict={}):
        # txt_file = self.txt_path
        # work_ = self.ui.project_base_dir.text()
        # lerp_value = self.ui.change_coe_horizontalSlider2.value()
        # seamless = self.is_seamless_ornot2()
        self.txt_path = txt_path
        self.work_ = work_
        self.lerg_value = lerg_value
        self.chosen_style_pic = chosen_style_pic
        self.chosen_content_file_list = chosen_content_file_list
        self.dir_dict = dir_dict

        # self.seamless=seamless

    def save_all(self):
        # if self.seamless is False:
        #     is_seamless=''
        # elif self.seamless is True:
        #     is_seamless='/expanded'
        style_name = os.path.basename(self.chosen_style_pic).split('.')[0]
        f = open(self.txt_path, "r", encoding='utf-8-sig')
        # f.readline()

        style_transfer.style_txt_main2(self.txt_path, self.work_, self.chosen_style_pic, self.chosen_content_file_list,
                                        self.dir_dict, False)
        # style_txt_main2(self.txt_path,self.work_,self.chosen_style_pic,self.chosen_content_file_list,self.dir_dict)
        for file in f:

            file = file.replace("\n", "").replace("\\", "/")
            get_path = PathUtils(self.work_, self.chosen_style_pic, file)
            a = False
            # 判断该图片是否在选中目录中
            for sub_file in self.chosen_content_file_list:
                if self.dir_dict[sub_file] in file:
                    a = True
                    break
            if a is True:
                # file_real_path=self.work_+'/'+file
                file_name = os.path.basename(file)
                # parent_path=os.path.dirname(file_real_path)
                # self.style_transfer_path = parent_path + "/style_transfer/"
                # # parent_path+=is_seamless
                # if os.path.exists(self.style_transfer_path) is False:
                #     InfoNotifier.InfoNotifier.g_progress_info.append("请先将dds转化为jpg,tga格式")
                #     return
                # self.style_output=parent_path+'/style_transfer/style_output/'
                #
                # self.lerp_output=parent_path+'/style_transfer/lerg_output/'
                # self.dds_output=parent_path+'/style_transfer/dds_output/'
                # if os.path.exists(self.style_output) is False:
                #     os.makedirs(self.style_output)
                # if os.path.exists(self.lerp_output) is False:
                #     os.makedirs(self.lerp_output)
                # if os.path.exists(self.dds_output) is False:
                #     os.makedirs(self.dds_output)

                jpg_path = get_path.dds_to_jpg_path()
                tga_path = get_path.dds_to_tga_path()

                # lerp
                style_out_pic_path = get_path.get_style_path()
                if os.path.exists(style_out_pic_path) is False:
                    InfoNotifier.InfoNotifier.g_progress_info.append(f"不存在对应风格化图片{style_out_pic_path}。跳过本张图片")
                    continue
                lerp_out_path = get_path.get_jpg_lerp_path()
                if os.path.exists(lerp_out_path) is False:
                    if os.path.exists(os.path.dirname(lerp_out_path)) is False:
                        os.makedirs(os.path.dirname(lerp_out_path))

                    if os.path.exists(jpg_path) is False:
                        print(jpg_path + " is not exist!")
                        continue

                    lerp_ret, _ = gen_lerp_ret.lerp_img(jpg_path, style_out_pic_path, self.lerg_value)
                    gen_lerp_ret.write_img(lerp_ret, lerp_out_path)
                    # combine alpha c
                    tga_img = Image.open(tga_path)
                    jpg_img = Image.open(lerp_out_path)
                    ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                    ir, ig, ib = jpg_img.split()
                    tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                    lerp_out_path = lerp_out_path.replace(".jpg", ".tga")
                    tga_img.save(lerp_out_path, quality=100)
                    print(f"generate tga image {lerp_out_path} after lerp op.")
                    InfoNotifier.InfoNotifier.g_progress_info.append(f"生成插值操作后的tga图片{lerp_out_path} ")
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(f"{lerp_out_path}已存在 ")
                dds_out = get_path.get_dds_output_path()
                if os.path.exists(dds_out + file_name) is False:
                    if os.path.exists(dds_out) is False:
                        os.makedirs(dds_out)
                    main_cmd = f"{self.texconv_path} -dxt5 -file {lerp_out_path} -outdir {dds_out}"
                    main_cmd.replace("\n", "")
                    try:
                        os.system(main_cmd)
                        InfoNotifier.InfoNotifier.g_progress_info.append(f"将{lerp_out_path}转化为DDS格式···")
                    except BaseException as bec:
                        InfoNotifier.InfoNotifier.g_progress_info.append(bec)
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(dds_out + file_name + '已存在，跳过')
        InfoNotifier.InfoNotifier.g_progress_info.append("保存完成")
        self._signal.emit()

    def run(self):
        self.save_all()


class My_gen_seamless_thread2(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(My_gen_seamless_thread2, self).__init__()
        self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"

    def set_para(self, txt_path='', work_='', lerg_value=50, chosen_style_pic='', chosen_content_file_list=[],
                 dir_dict={}):
        self.txt_path = txt_path
        self.work_ = work_
        self.lerg_value = lerg_value
        self.chosen_style_pic = chosen_style_pic
        self.chosen_content_file_list = chosen_content_file_list
        self.dir_dict = dir_dict

    def expanded(self):

        pad = 256
        style_name = os.path.basename(self.chosen_style_pic).split('.')[0]
        f = open(self.txt_path, "r", encoding='utf-8-sig')
        # f.readline()

        for file in f:
            file = file.replace("\n", "").replace("\\", "/")
            get_path = PathUtils(self.work_, self.chosen_style_pic, file)

            # 判断该图片是否在选中目录中
            a = False
            for sub_file in self.chosen_content_file_list:
                if self.dir_dict[sub_file] in file:
                    a = True
                    break
            if a is True:
                if os.path.exists(get_path.get_expanded_tga_path()) is False:
                    file_real_path = get_path.real_dds_path()
                    # file_name = os.path.basename(file_real_path)
                    # parent_path = os.path.dirname(file_real_path)
                    # self.style_transfer_path = parent_path + "/style_transfer/"
                    # # parent_path+=is_seamless
                    # if os.path.exists(self.style_transfer_path) is False:
                    #     InfoNotifier.InfoNotifier.g_progress_info.append("请先将dds转化为jpg,tga格式")
                    #     return
                    #
                    # parent_path += '/style_transfer/expanded'
                    # self.expanded_transfer = parent_path + '/expanded_transfer/'
                    # self.style_output = parent_path + '/style_output/'
                    # self.lerp_output = parent_path + '/lerg_output/'
                    # self.dds_output = parent_path + '/dds_output/'
                    # self.seamless_output = parent_path + '/seamless/'
                    # if os.path.exists(self.style_output) is False:
                    #     os.makedirs(self.style_output)
                    # if os.path.exists(self.lerp_output) is False:
                    #     os.makedirs(self.lerp_output)
                    # if os.path.exists(self.dds_output) is False:
                    #     os.makedirs(self.dds_output)
                    # if os.path.exists(self.expanded_transfer) is False:
                    #     os.makedirs(self.expanded_transfer)
                    # if os.path.exists(self.seamless_output) is False:
                    #     os.makedirs(self.seamless_output)

                    jpg_path = get_path.dds_to_jpg_path()
                    tga_path = get_path.dds_to_tga_path()
                    # expanded_save_path=get_path.GetEpandedPath()[0]
                    ##expand
                    img_jpg = Image.open(jpg_path)
                    img_tga = Image.open(tga_path)
                    width = img_jpg.width
                    height = img_jpg.height
                    assert width == img_tga.width and height == img_tga.height

                    img_jpg_pad = Image.new("RGB", (width * 3, height * 3))
                    img_tga_pad = Image.new("RGBA", (width * 3, height * 3))
                    for i in range(3):
                        for j in range(3):
                            img_jpg_pad.paste(img_jpg, (i * width, j * height, (i + 1) * width, (j + 1) * height))
                            img_tga_pad.paste(img_tga, (i * width, j * height, (i + 1) * width, (j + 1) * height))
                    img_jpg_crop = img_jpg_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                    if os.path.exists(os.path.dirname(get_path.get_expanded_jpg_path())) is False:
                        os.makedirs(os.path.dirname(get_path.get_expanded_jpg_path()))
                    img_jpg_crop.save(get_path.get_expanded_jpg_path(), quality=100)
                    print(get_path.get_expanded_jpg_path())
                    img_tga_crop = img_tga_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                    img_tga_crop.save(get_path.get_expanded_tga_path(), quality=100)
                    print(get_path.get_expanded_tga_path())
                    InfoNotifier.InfoNotifier.g_progress_info.append(
                        f'保存expand后图片：{get_path.get_expanded_tga_path()}，jpg')
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(get_path.get_expanded_tga_path() + ' exists')

    def save_all(self):
        pad = 256
        style_name = os.path.basename(self.chosen_style_pic).split('.')[0]

        f = open(self.txt_path, "r", encoding='utf-8-sig')
        # f.readline()
        style_transfer.style_txt_main2(self.txt_path, self.work_, self.chosen_style_pic,
                                        self.chosen_content_file_list, self.dir_dict, True)
        # gen_style_seamless_txt.style_txt_main2(self.txt_path,self.work_,self.chosen_style_pic,self.chosen_content_file_list,self.dir_dict)
        # gen_style_class.style_txt_main2(self.txt_path,self.work_,self.chosen_style_pic,self.chosen_content_file_list,self.dir_dict,True)
        for file in f:

            file = file.replace("\n", "").replace("\\", "/")
            get_path = PathUtils(self.work_, self.chosen_style_pic, file)
            # 判断该图片是否在选中目录中
            a = False
            for sub_file in self.chosen_content_file_list:
                if self.dir_dict[sub_file] in file:
                    a = True
                    break
            if a is True:
                file = file.replace("\n", "")
                file_real_path = get_path.real_dds_path()
                file_name = os.path.basename(file_real_path)
                # parent_path = os.path.dirname(file_real_path)
                # self.style_transfer_path = parent_path + "/style_transfer/"
                # # parent_path+=is_seamless
                # if os.path.exists(self.style_transfer_path) is False:
                #     InfoNotifier.InfoNotifier.g_progress_info.append("请先将dds转化为jpg,tga格式")
                #     return
                #
                # parent_path+='/style_transfer/expanded'
                # self.expanded_transfer=parent_path+'/expanded_transfer/'
                # self.style_output = parent_path + '/style_output/'
                # self.lerp_output = parent_path + '/lerg_output/'
                # self.dds_output = parent_path + '/dds_output/'
                # self.seamless_output=parent_path+'/seamless/'
                # if os.path.exists(self.style_output) is False:
                #     os.makedirs(self.style_output)
                # if os.path.exists(self.lerp_output) is False:
                #     os.makedirs(self.lerp_output)
                # if os.path.exists(self.dds_output) is False:
                #     os.makedirs(self.dds_output)
                # if os.path.exists(self.expanded_transfer) is False:
                #     os.makedirs(self.expanded_transfer)
                # if os.path.exists(self.seamless_output) is False:
                #     os.makedirs(self.seamless_output)

                jpg_path = get_path.get_expanded_jpg_path()
                tga_path = get_path.get_expanded_tga_path()
                ##expand
                # img_jpg=Image.open(jpg_path)
                # img_tga=Image.open(tga_path)
                # width = img_jpg.width
                # height = img_jpg.height
                # assert width == img_tga.width and height == img_tga.height
                #
                # img_jpg_pad = Image.new("RGB", (width * 3, height * 3))
                # img_tga_pad = Image.new("RGBA", (width * 3, height * 3))
                # for i in range(3):
                #     for j in range(3):
                #         img_jpg_pad.paste(img_jpg, (i * width, j * height, (i + 1) * width, (j + 1) * height))
                #         img_tga_pad.paste(img_tga, (i * width, j * height, (i + 1) * width, (j + 1) * height))
                # img_jpg_crop = img_jpg_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                # img_jpg_crop.save(self.expanded_transfer+os.path.basename(jpg_path),quality=100)
                # print(self.expanded_transfer+os.path.basename(jpg_path))
                # img_tga_crop = img_tga_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                # img_tga_crop.save(self.expanded_transfer+os.path.basename(tga_path),quality=100)
                # print(self.expanded_transfer+os.path.basename(tga_path))
                tmp_style_in = jpg_path

                # lerp
                style_out_pic_path = get_path.get_expanded_style_path()
                if os.path.exists(style_out_pic_path) is False:
                    InfoNotifier.InfoNotifier.g_progress_info.append("不存在对应风格化图片。跳过本张图片")
                    continue

                lerp_out_path = get_path.get_expanded_lerp_path_jpg()
                if os.path.exists(lerp_out_path) is False:
                    if os.path.exists(os.path.dirname(lerp_out_path)) is False:
                        os.makedirs(os.path.dirname(lerp_out_path))
                    lerp_ret, _ = gen_lerp_ret.lerp_img(tmp_style_in, style_out_pic_path, self.lerg_value)
                    gen_lerp_ret.write_img(lerp_ret, lerp_out_path)
                    # combine alpha c
                    tga_img = Image.open(tga_path)
                    jpg_img = Image.open(lerp_out_path)
                    ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                    ir, ig, ib = jpg_img.split()
                    tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                    lerp_out_path = lerp_out_path.replace(".jpg", ".tga")
                    tga_img.save(lerp_out_path, quality=100)
                    print(f"generate tga image {lerp_out_path} after lerp op.")
                    InfoNotifier.InfoNotifier.g_progress_info.append('生成插值操作后的tga图片' + lerp_out_path)
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(lerp_out_path + "已存在，跳过")
                # seamless
                if os.path.exists(get_path.get_seamless_path()) is False:
                    seamless_path = os.path.dirname(get_path.get_seamless_path())
                    if os.path.exists(seamless_path) is False:
                        os.makedirs(seamless_path)
                    # print("seamless:"+PathUtils.get_expanded_lerp_path_tga())

                    img = Image.open(get_path.get_expanded_lerp_path_tga())
                    width = img.width
                    height = img.height
                    pad = 256
                    img_crop = img.crop((pad, pad, width - pad, height - pad))
                    img_crop.save(get_path.get_seamless_path(), quality=100)
                    InfoNotifier.InfoNotifier.g_progress_info.append('生成无缝贴图' + get_path.get_seamless_path())
                dds_output = get_path.get_seamless_dds_path()
                if os.path.exists(dds_output + file_name) is False:
                    seamless_path = os.path.dirname(get_path.get_seamless_path())
                    if os.path.exists(dds_output) is False:
                        os.makedirs(dds_output)
                    main_cmd = f"{self.texconv_path} -dxt5 -file {get_path.get_seamless_path()} -outdir {dds_output}"
                    main_cmd.replace("\n", "")
                    os.system(main_cmd)
                    InfoNotifier.InfoNotifier.g_progress_info.append(f'将{dds_output}{file_name}转化为DDS格式···')
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(dds_output + file_name + '已存在，跳过')
        InfoNotifier.InfoNotifier.g_progress_info.append("保存完成")
        self._signal.emit()

    def run(self):
        self.expanded()
        self.save_all()