from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QMessageBox , QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QUrl, QPoint,QSize,QRect
from PyQt5 import QtGui
from combocheckbox import ComboCheckBox
from PyQt5.QtGui import QIcon, QDesktopServices,QPixmap
import Ui_test519
import os
import time
import InfoNotifier
from PIL import Image
import cv2
import glob
import gen_jpg_tga_from_dds
import json
import gen_lerp_ret
from Gen_Style import style_transfer
from path_util import PathUtils
from gen_style_map import gen_style_map_file
from button_state import GlobalConfig

# TabFiles
class MyGenDdsJpgThreadTabFiles(QThread):
        _signal_trigger = pyqtSignal()

        def __init__(self):
            super(MyGenDdsJpgThreadTabFiles, self).__init__()
            self.multi_dir_project = []
            self.exe_dir = ""
            self.project_base = ""

        def set_para(self, project_base="", exe_dir="", multi_dir_project=None):
            # self.dir=dir
            if multi_dir_project is None:
                self.multi_dir_project=[]
            self.multi_dir_project = multi_dir_project
            self.exe_dir = exe_dir
            self.project_base = project_base

        def run(self):
            self.gen_jpg_tga_from_dds_from_file()

        def gen_jpg_tga_from_dds_from_file(self):
            try:
                content_list = []
                for file in self.multi_dir_project:
                    real_file_path = self.project_base+'/'+file
                    dds_list = glob.glob(real_file_path+'/*.dds')
                    for i in range(len(dds_list)):
                        dds_list[i] = dds_list[i].replace(self.project_base+'/', "").replace("\\", "/")
                    content_list += dds_list
                gen_jpg_tga_from_dds.gen_jpg_tga(work_=self.project_base, dds_list=content_list)
                InfoNotifier.InfoNotifier.g_progress_info.append("转化完成,勾选一个目录进行预览")
                self._signal_trigger.emit()
            except BaseException as e:
                print(e)


class MyGenStyleTempThreadTabFiles(QThread):
        _signal_trigger=pyqtSignal()

        def __init__(self):
            super(MyGenStyleTempThreadTabFiles,self).__init__()
            self.chosen_style_pic = ""
            self.show_list = []
            self.project_base = ""

        def set_para(self, chosen_style_pic='', show_list=None, project_base=''):
            if show_list is None:
                self.show_list = show_list
            self.chosen_style_pic = chosen_style_pic
            self.show_list = show_list
            self.project_base = project_base

        def preview_lerg_pics(self):
            GlobalConfig.b_sync_block_in_thread_temp = True
            QApplication.processEvents()
            style_transfer.style_main_temp(self.show_list, self.chosen_style_pic)
            InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览，并滑动微调栏杆调整插值参数")
            GlobalConfig.b_sync_block_in_thread_temp = False
            self._signal_trigger.emit()

        def run(self):
            self.preview_lerg_pics()


class MyGenSeamlessStyleThreadTabFiles(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(MyGenSeamlessStyleThreadTabFiles, self).__init__()
            self.texconv_path = os.getcwd() + "/texconv.exe"
            self.pad = 256
            self.chosen_style_pic = ''
            self.chosen_content_file_list = []
            self.project_base = ''
            self.file_dict = {}
            self.lerp_value = 50

        def set_para(self, style_path='', chosen_content_file_list=None, base='', file_dict=None, lerp_value=50):
            # set_para(style_path,chosen_content_file_list,base,file_dict,lerp_value)
            if chosen_content_file_list is None:
                self.chosen_content_file_list = []
            if file_dict is None:
                self.file_dict = {}
            self.chosen_style_pic = style_path
            self.chosen_content_file_list = chosen_content_file_list
            self.project_base = base
            self.file_dict = file_dict
            self.lerp_value = lerp_value

        def gen_expanded_pic(self):
            InfoNotifier.InfoNotifier.g_progress_info.append("开始生成DDS贴图············")
            GlobalConfig.b_sync_block_op_in_progress = True
            QApplication.processEvents()
            pad = 256

            # 存放被选中的目录中图片的相对路径到pic_list中
            pic_list = []
            for file in self.chosen_content_file_list:
                file_path = self.file_dict[file]
                tmp = glob.glob(self.project_base + '/' + file_path + '/*.dds')
                for i in range(len(tmp)):
                    tmp[i] = tmp[i].replace(self.project_base + '/', "")
                pic_list += tmp

            # 遍历文件目录
            for file in pic_list:

                # 当前文件名
                get_path = PathUtils(self.project_base, self.chosen_style_pic, file)
                expanded_jpg = get_path.get_expanded_jpg_path()
                expanded_tga = get_path.get_expanded_tga_path()

                if os.path.exists(expanded_jpg) is False:
                    jpg_path = get_path.dds_to_jpg_path()
                    tga_path = get_path.dds_to_tga_path()
                    # expand
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

                    if os.path.exists(os.path.dirname(expanded_jpg)) is False:
                        os.makedirs(os.path.dirname(expanded_jpg))

                    img_jpg_crop.save(expanded_jpg, quality=100)
                    print(expanded_jpg)
                    img_tga_crop = img_tga_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                    img_tga_crop.save(expanded_tga, quality=100)
                    print(expanded_tga)
                    InfoNotifier.InfoNotifier.g_progress_info.append(
                        f'保存expand后图片：{expanded_tga}，jpg')
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(expanded_tga + ' exists')

            # self._signal.emit()
        def gen_style(self):
            style_pic = self.chosen_style_pic
            file_list = self.chosen_content_file_list
            # 存放被选中的目录中图片的相对路径
            pic_list = []
            for file in file_list:
                file_path = self.file_dict[file]
                tmp = glob.glob(self.project_base + '/' + file_path + '/*.dds')
                for i in range(len(tmp)):
                    tmp[i] = tmp[i].replace(self.project_base + '/', "")
                pic_list += tmp

            style_transfer.style_main(pic_list, style_pic, self.project_base, True)

        def gen_lerp_pic(self):
            try:
                file_list = self.chosen_content_file_list
                # 存放被选中的目录中图片的相对路径
                pic_list = []
                for file in file_list:
                    file_path = self.file_dict[file]
                    tmp = glob.glob(self.project_base + '/' + file_path + '/*.dds')
                    for i in range(len(tmp)):
                        tmp[i] = tmp[i].replace(self.project_base + '/', "")
                    pic_list += tmp

                for file in pic_list:
                    file_name = os.path.basename(file)
                    get_path = PathUtils(self.project_base, self.chosen_style_pic, file)
                    jpg_path = get_path.get_expanded_jpg_path()
                    tga_path = get_path.get_expanded_tga_path()
                    tmp_style_in = jpg_path

                    # lerp
                    style_out_pic_path = get_path.get_expanded_style_path()

                    if os.path.exists(style_out_pic_path) is False:
                        InfoNotifier.InfoNotifier.g_progress_info.append("不存在对应风格化图片。跳过本张图片")
                        continue
                    lerp_out_path = get_path.get_expanded_lerp_path_jpg()

                    if os.path.exists(os.path.dirname(lerp_out_path)) is False:
                        os.makedirs(os.path.dirname(lerp_out_path))
                    lerp_ret, _ = gen_lerp_ret.lerp_img(tmp_style_in, style_out_pic_path, self.lerp_value)
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
                    # seamless
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
                    # dds
                    dds_output = get_path.get_dds_output_path()
                    if os.path.exists(dds_output) is False:
                        os.makedirs(dds_output)
                    main_cmd = f"{self.texconv_path} -dxt5 -file {get_path.get_seamless_path()} -outdir {dds_output}"
                    main_cmd.replace("\n", "")
                    os.system(main_cmd)
                    InfoNotifier.InfoNotifier.g_progress_info.append(f'将{dds_output}{file_name}转化为DDS格式···')
                InfoNotifier.InfoNotifier.g_progress_info.append("保存完成")
                # InfoNotifier.InfoNotifier.g_progress_info.append("dds图片已转化完毕")
            except BaseException as be:
                print(be)


        def run(self):
            self.gen_expanded_pic()
            self.gen_style()
            self.gen_lerp_pic()
            GlobalConfig.b_sync_block_op_in_progress = False
            self._signal.emit()


class MyGenStyleThreadTabFiles(QThread):
        _signal_trigger=pyqtSignal()

        def __init__(self):
            super(MyGenStyleThreadTabFiles, self).__init__()
            self.texconv_path = os.getcwd() + "/texconv.exe"
            self.chosen_style_pic = ''
            self.chosen_content_file_list = None
            self.project_base = ''
            self.file_dict = None
            self.lerp_value = 50

        def set_para(self,chosen_style_pic='', chosen_content_file_list=None, project_base='', file_dict=None,
                     lerp_value=50):
            if chosen_content_file_list is None:
                self.chosen_content_file_list = []
            if file_dict is None:
                self.file_dict = {}
            # set_para(style_path,chosen_content_file_list,base,file_dict,lerp_value)
            self.chosen_style_pic = chosen_style_pic
            self.chosen_content_file_list = chosen_content_file_list
            self.project_base = project_base
            self.file_dict = file_dict
            self.lerp_value = lerp_value
            # self.is_seamless=is_seamless

        def preview_lerg_pics(self):
            GlobalConfig.b_sync_block_op_in_progress = True
            QApplication.processEvents()
            style_pic = self.chosen_style_pic
            file_list = self.chosen_content_file_list
            #存放被选中的目录中图片的相对路径
            pic_list=[]
            for file in file_list:
                file_path = self.file_dict[file]
                tmp = glob.glob(self.project_base+'/'+file_path+'/*.dds')
                for i in range(len(tmp)):
                    tmp[i]=tmp[i].replace(self.project_base+'/', "")
                pic_list += tmp

            style_transfer.style_main(pic_list, style_pic, self.project_base, False)
            self.gen_lerg(pic_list)
            GlobalConfig.b_sync_block_op_in_progress = False
            self._signal_trigger.emit()

        def gen_lerg(self, pic_list):
            InfoNotifier.InfoNotifier.g_progress_info.append("开始生成DDS贴图···········")
            for file_path in pic_list:
                file_name = os.path.basename(file_path)
                get_path = PathUtils(self.project_base, self.chosen_style_pic, file_path)

                # 原图
                jpg_path = get_path.dds_to_jpg_path()
                tga_path = get_path.dds_to_tga_path()
                # 风格后图片
                style_real_path = get_path.get_style_path()
                # 待保存-lerg
                lerp_real_path = get_path.get_jpg_lerp_path()
                # 待保存-dds
                dds_real_path = get_path.get_dds_output_path()

                #######################################################
                if os.path.exists(jpg_path) is False:
                    print("dds not transfered")
                    continue
                if os.path.exists(style_real_path) is False:
                    print('img not stylized')
                    continue
                if os.path.exists(os.path.dirname(lerp_real_path)) is False:
                    os.makedirs(os.path.dirname(lerp_real_path))
                if os.path.exists(dds_real_path) is False:
                    os.makedirs(dds_real_path)
                try:
                    lerp_ret, ret = gen_lerp_ret.lerp_img(jpg_path, style_real_path, self.lerp_value)
                    gen_lerp_ret.write_img(lerp_ret, lerp_real_path)
                except BaseException as be:
                    print(be)
                # combine alpha channel
                tga_img = Image.open(tga_path)
                jpg_img = Image.open(lerp_real_path)
                ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                ir, ig, ib = jpg_img.split()
                tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                lerp_real_path = lerp_real_path.replace(".jpg", ".tga")
                tga_img.save(lerp_real_path, quality=100)
                print(f"generate tga image {lerp_real_path} after lerp op.")
                InfoNotifier.InfoNotifier.g_progress_info.append(f"生成插值操作后的tga图片 {lerp_real_path} ")
                # dds
                main_cmd = f"{self.texconv_path} -dxt5 -file {lerp_real_path} -outdir {dds_real_path}"
                main_cmd.replace("\n", "")
                os.system(main_cmd)
                InfoNotifier.InfoNotifier.g_progress_info.append(f'将{dds_real_path}{file_name}转化为DDS格式···')
            InfoNotifier.InfoNotifier.g_progress_info.append("保存完成")

        def run(self):
            self.preview_lerg_pics()