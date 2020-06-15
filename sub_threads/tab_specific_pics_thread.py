
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QMessageBox , QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QUrl, QPoint,QSize,QRect
import  os
import time
import InfoNotifier
from PIL import Image
import cv2
import glob
from Gen_Style import style_transfer
import gen_jpg_tga_from_dds
import json
import gen_lerp_ret
from path_util import PathUtils
from button_state import GlobalConfig

# tab3
class MyGenDdsJpgThreadTabPics(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(MyGenDdsJpgThreadTabPics, self).__init__()
        self.exe_dir = os.getcwd() + "\\dds_to_jpg/dds_to_jpg.exe"
        self.show_list = []
        self.project_base = ''

    def set_para(self, content_list=None, project_base=''):
        if content_list is None:
            self.show_list = []
        self.show_list = content_list
        self.project_base = project_base

    def gen_jpg(self):
        try:
            InfoNotifier.InfoNotifier.g_progress_info.append("开始将贴图格式转换为jpg和tga····")

            gen_jpg_tga_from_dds.gen_jpg_tga(work_=self.project_base, dds_list=self.show_list)
            InfoNotifier.InfoNotifier.g_progress_info.append("已生成jpg,tga格式图片")
            self._signal.emit()
        except BaseException as e:
            print(e)

    def run(self):
        self.gen_jpg()


class MyGenStyleTempThreadTabPics(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(MyGenStyleTempThreadTabPics, self).__init__()
        self.show_list = None
        self.chosen_style_pic = ''
        self.temp_file_name = ''

    def set_para(self, show_list=None, chosen_style_pic='', temp_file=''):
        if show_list is None:
            self.show_list = []
        self.show_list = show_list
        self.chosen_style_pic = chosen_style_pic
        self.temp_file_name = temp_file

    def gen_style(self):
        GlobalConfig.b_sync_block_in_thread_temp = True
        QApplication.processEvents()
        style_pic = self.chosen_style_pic
        content_list = self.show_list
        style_name = os.path.basename(style_pic).split('.')[0]
        if os.path.exists(self.temp_file_name) is False:
            os.makedirs(self.temp_file_name)

        """让生成过的临时文件不再重新生成"""
        flag = True
        for i in range(len(content_list)):
            file_name = os.path.basename(content_list[i])
            if os.path.exists(self.temp_file_name + style_name + '/' + file_name) is False:
                flag = False
                break
            # style_main3(content_list, style_pic, self.temp_file_name)
        if flag is False:
            style_transfer.style_main_temp(content_list, style_pic)
        InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览，并滑动微调栏杆调整插值参数")
        GlobalConfig.b_sync_block_in_thread_temp = False
        self._signal.emit()

    def run(self):
        self.gen_style()


class MyGenStyleThreadTabPics(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(MyGenStyleThreadTabPics, self).__init__()
        self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"
        self.project_base = ''
        self.content_list = []
        self.chosen_style_pic = ''
        self.lerg_value = 50

    def set_para(self, project_base='', content_list=None, style_path='', lerg_value=50):
        if content_list is None:
            self.content_list = []
        self.project_base = project_base
        self.content_list = content_list
        self.chosen_style_pic = style_path
        self.lerg_value = lerg_value

    def save_all(self):
        GlobalConfig.b_sync_block_op_in_progress = True
        QApplication.processEvents()
        InfoNotifier.InfoNotifier.g_progress_info.append("开始保存图片··············")
        # gen_style_batch3.style_main3(self.content_list,self.chosen_style_pic)
        style_transfer.style_main(self.content_list, self.chosen_style_pic, self.project_base, False)
        for file in self.content_list:
            file_name = os.path.basename(file)
            get_path = PathUtils(self.project_base, self.chosen_style_pic, file)
            jpg_path = get_path.dds_to_jpg_path()
            tga_path = get_path.dds_to_tga_path()

            # lerp
            style_out_pic_path = get_path.get_style_path()
            if os.path.exists(style_out_pic_path) is False:
                InfoNotifier.InfoNotifier.g_progress_info.append(f"不存在对应风格化图片{style_out_pic_path}。跳过本张图片")
                continue
            lerp_out_path = get_path.get_jpg_lerp_path()
            if os.path.exists(os.path.dirname(lerp_out_path)) is False:
                os.makedirs(os.path.dirname(lerp_out_path))
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
            InfoNotifier.InfoNotifier.g_progress_info.append(f"生成插值操作后的tga图片: {lerp_out_path} ")
            # dds
            # 图片目录路径
            dds_out = get_path.get_dds_output_path()
            if os.path.exists(dds_out) is False:
                os.makedirs(dds_out)
            main_cmd = f"{self.texconv_path} -dxt5 -file {lerp_out_path} -outdir {dds_out}"
            main_cmd.replace("\n", "")
            os.system(main_cmd)
            InfoNotifier.InfoNotifier.g_progress_info.append('生成DDS贴图：' + dds_out + file_name)
        InfoNotifier.InfoNotifier.g_progress_info.append("保存完成")
        GlobalConfig.b_sync_block_op_in_progress = False
        self._signal.emit()

    def run(self):
        self.save_all()


class MyGenSeamlessStyleThreadTabPics(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(MyGenSeamlessStyleThreadTabPics, self).__init__()
        self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"
        self.project_base = ''
        self.content_list = []
        self.chosen_style_pic = ''
        self.lerg_value = 50

    def set_para(self, project_base='', content_list=None, style_path='', lerg_value=50):
        if content_list is None:
            self.content_list = []
        self.project_base = project_base
        self.content_list = content_list
        self.chosen_style_pic = style_path
        self.lerg_value = lerg_value

    def expanded(self):
        InfoNotifier.InfoNotifier.g_progress_info.append("开始保存图片··············")
        GlobalConfig.b_sync_block_op_in_progress = True
        QApplication.processEvents()
        pad = 256
        for file in self.content_list:
            get_path = PathUtils(self.project_base, self.chosen_style_pic, file)

            jpg_path = get_path.dds_to_jpg_path()
            tga_path = get_path.dds_to_tga_path()
            expanded_jpg = get_path.get_expanded_jpg_path()
            expanded_tga = get_path.get_expanded_tga_path()
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
            InfoNotifier.InfoNotifier.g_progress_info.append(f'保存expand后图片：{expanded_jpg}，jpg')

    def save_all(self):
        # gen_seamless_style_batch3.style_main3(self.content_list,self.chosen_style_pic)
        style_transfer.style_main(self.content_list, self.chosen_style_pic, self.project_base, True)
        for file in self.content_list:
            file = file.replace("\n", "")
            file_name = os.path.basename(file)

            get_path = PathUtils(self.project_base, self.chosen_style_pic, file)
            jpg_path = get_path.get_expanded_jpg_path()
            tga_path = get_path.get_expanded_tga_path()

            tmp_style_in = jpg_path

            # lerp
            style_out_pic_path = get_path.get_expanded_style_path()

            if os.path.exists(style_out_pic_path) is False:
                InfoNotifier.InfoNotifier.g_progress_info.append(f"不存在对应风格化图片{style_out_pic_path}。跳过本张图片")
                continue
            lerp_out_path = get_path.get_expanded_lerp_path_jpg()
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
            InfoNotifier.InfoNotifier.g_progress_info.append(f"生成插值操作后的tga图片 {lerp_out_path} ")
            # seamless
            seamless_path = get_path.get_seamless_path()
            if os.path.exists(os.path.dirname(seamless_path)) is False:
                os.makedirs(os.path.dirname(seamless_path))
            img = Image.open(get_path.get_expanded_tga_path())
            width = img.width
            height = img.height
            pad = 256
            img_crop = img.crop((pad, pad, width - pad, height - pad))
            img_crop.save(seamless_path, quality=100)
            InfoNotifier.InfoNotifier.g_progress_info.append("生成无缝贴图：" + seamless_path)
            dds_output = get_path.get_seamless_dds_path()
            if os.path.exists(dds_output) is False:
                os.makedirs(dds_output)
            main_cmd = f"{self.texconv_path} -dxt5 -file {seamless_path} -outdir {dds_output}"
            main_cmd.replace("\n", "")
            os.system(main_cmd)
            InfoNotifier.InfoNotifier.g_progress_info.append('生成DDS贴图：' + dds_output + file_name)

        InfoNotifier.InfoNotifier.g_progress_info.append("保存完成")
        GlobalConfig.b_sync_block_op_in_progress = False
        self._signal.emit()

    def run(self):
        self.expanded()
        self.save_all()