
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QMessageBox , QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QUrl, QPoint,QSize,QRect
from PyQt5 import QtGui
from combocheckbox import ComboCheckBox
from PyQt5.QtGui import QIcon, QDesktopServices,QPixmap
import  Ui_test519
import  glob
import  os
import time
import InfoNotifier
from PIL import Image
import cv2
import glob
from gen_style_tex import main
from gen_style_files import  style_main
from gen_expanded_style_files import  expanded_style_main
from gen_style_file2 import style_main2
from gen_style_file3 import  style_main3
import gen_style_all
import  gen_jpg_tga_from_dds
import json
import gen_lerp_ret
import gen_style_seamless_txt
from  gen_style_txt import style_txt_main2
import  gen_style_batch3
import  gen_seamless_style_batch3
from path_util import PathUtils
from Gen_Style import  gen_style_class
# from  threading import Thread
# class MySignals(QObject):
#     定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # text_print = Signal(QTextBrowser,str)
    # 还可以定义其他信号
    # update_table = Signal(str)
class Mythread(QThread):
    _signal_progress_info = pyqtSignal()

    _signal_button_ctrl = pyqtSignal()

    def __init__(self):
        super(Mythread, self).__init__()

    def run(self):
        while True:
            # 发出信号
            self._signal_progress_info.emit()
            self._signal_button_ctrl.emit()
            # 让程序休眠
            time.sleep(1.5)
if __name__=='__main__':

    ##################################################tab1
    class My_gen_dds_jpg_thread(QThread):
        _signal_trigger=pyqtSignal()
        def __init__(self):
            super(My_gen_dds_jpg_thread, self).__init__()

        def set_para(self,project_base="",exe_dir="",multi_dir_project=[]):
            # self.dir=dir
            self.multi_dir_project=multi_dir_project
            self.exe_dir=exe_dir
            self.project_base=project_base
        def run(self):
            self.gen_jpg_tga_from_dds_from_files()
        def gen_jpg_tga_from_dds_from_file(self,dir):
            try:
                gd=self.project_base
                file_name=dir.split('/')[-1]
                if gd=='':
                    print("请先创建根目录")
                    return
                # dds_list=[]
                #
                dds_list=glob.glob(dir+'/'+'*.dds')
                savp_path = dir+ '/style_transfer/'
                if os.path.exists(savp_path) is False:
                    os.makedirs(savp_path)
                for file in dds_list:
                    file_base_name=os.path.basename(file)
                    jpg_path=savp_path+file_base_name.replace(".dds",".jpg")
                    tga_path=savp_path+file_base_name.replace(".dds",".tga")
                    if os.path.exists(jpg_path) is True:
                        continue
                    if os.path.exists(jpg_path) is False:
                        main_cmd=f"{self.exe_dir} {file} {jpg_path} {tga_path}"
                        main_cmd=main_cmd.replace("\n","")
                        os.system(main_cmd)

            except BaseException as e:
                print(e)


        # def gen_jpg_tga_from_dds_from_files_Thread(self):
        #     thread = Thread(target=self.gen_jpg_tga_from_dds_from_files())
        #     thread.start()

        def gen_jpg_tga_from_dds_from_files(self):
                if len(self.multi_dir_project) == 0:
                    print('请先选择文件')
                else:

                    files_list = self.multi_dir_project
                    for file_dir in files_list:
                        self.gen_jpg_tga_from_dds_from_file(file_dir)
                InfoNotifier.InfoNotifier.g_progress_info.append("转化完成,勾选一个目录进行预览")

                self._signal_trigger.emit()
    class My_gen_style_temp_thread(QThread):
        _signal_trigger=pyqtSignal()
        def __init__(self):
            super(My_gen_style_temp_thread,self).__init__()
        def set_para(self,chosen_style_pic='',show_list=[],project_base=''):
            self.chosen_style_pic=chosen_style_pic
            self.show_list=show_list
            self.project_base=project_base
        def preview_lerg_pics(self):
            style_pic = self.chosen_style_pic
            content_list = self.show_list
            parent_path=os.path.dirname(content_list[0])
            filename = content_list[0].split("/")[-2]
            self.temp_file_name = parent_path + '/temp/'

            if os.path.exists(self.temp_file_name) is False:
                os.makedirs(self.temp_file_name)
            style_name=os.path.basename(style_pic)
            # index=0
            # for i in content_list:
            #     save_temp_dir=self.temp_file_name+str(index)+'.jpg'

            """
                        if os.path.exists(self.temp_file_name + style_name + '/') is False:
                style_main2(content_list, style_pic, self.temp_file_name)
                InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览，并滑动微调栏杆调整插值参数")
            else:
                for file_path in content_list:
                    file = os.path.basename(file_path)
                    # style_path=
                    InfoNotifier.InfoNotifier.style_preview_pic_dir2.append(
                        f'{self.temp_file_name}{style_name}/' + file)
                InfoNotifier.InfoNotifier.g_progress_info.append(self.temp_file_name + style_name + '已存在，点击一张原图进行预览')
            """

            if os.path.exists(self.temp_file_name+style_name+'/') is True:
                for pic in content_list:
                    file=os.path.basename(pic)
                    InfoNotifier.InfoNotifier.style_preview_pic_dir.append(self.temp_file_name+style_name+'/'+file)
                InfoNotifier.InfoNotifier.g_progress_info.append("点击一张原图进行预览")
            else:
                style_main(content_list, style_pic, self.temp_file_name)
                InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览，并滑动微调栏杆调整插值参数")
            # main(pics_dir=[], style_dir='', save_dir='')
            self._signal_trigger.emit()


        def run(self):
            self.preview_lerg_pics()
    class My_gen_seamless_style_thread(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_seamless_style_thread, self).__init__()
            self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"

            self.pad=256
        def set_para(self,chosen_style_pic='',show_list=[],project_base='',multi_files=[],lerp_value=50):
            self.chosen_style_pic = chosen_style_pic
            self.show_list = show_list
            self.pre_project_bse=project_base
            self.project_base = project_base+'/expanded'
            self.multi_files = multi_files
            self.lerp_value = lerp_value
            self.seamless_file = self.project_base + 'seamless/'
        def gen_expanded_pic(self):
            # if os.path.exists(self.project_base) is False:
            #     os.makedirs(self.project_base)
            # expand_base=self.project_base+'/style_transfer/'
            # if os.path.exists(expand_base) is False:
            #     os.makedirs(expand_base)
            # input_file=self.pre_project_bse+'/style_transfer/'
            pad=256
            #遍历文件目录
            for loc in self.multi_files:
                #当前文件名
                file_name=loc.split('/')[-1]
                # parent_path=os.path.dirname(loc)

                # sub_file=input_file+file_name+'/'
                sub_expand_dir=loc+'/style_transfer/expanded/expanded_output/'
                if os.path.exists(sub_expand_dir) is False:
                    os.makedirs(sub_expand_dir)
                pic_list=glob.glob(loc+'/style_transfer/*.jpg')
                for file_jpg in pic_list:
                    if os.path.exists(sub_expand_dir + os.path.basename(file_jpg)) is False:
                        split_text = os.path.splitext(file_jpg)
                        file_tga = split_text[0] + '.tga'
                        if os.path.exists(sub_expand_dir + os.path.basename(file_jpg)) is False:
                            img_jpg = Image.open(file_jpg)
                            img_tga = Image.open( file_tga)
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
                            img_jpg_crop.save(sub_expand_dir + os.path.basename(file_jpg), quality=100)
                            print(sub_expand_dir+ os.path.basename(file_jpg))

                            img_tga_crop = img_tga_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                            img_tga_crop.save(sub_expand_dir + os.path.basename(file_tga), quality=100)
                            print(sub_expand_dir + os.path.basename(file_tga))
            # self._signal.emit()
        def gen_style(self):
            style_pic=self.chosen_style_pic
            style_name=os.path.basename(style_pic).split('.')[0]
            # content_path=self.project_base+'/style_transfer/'
            # style_output=self.project_base+'/style_output/'
            for loc in self.multi_files:
                file_name=loc.split('/')[-1]

                # sub_file=content_path+file_name+'/'
                # sub_style_file=style_output+style_name+'/'+file_name+'/'
                # if os.path.exists(sub_style_file) is False:
                #     os.makedirs(sub_style_file)
                # sub_save_dir=style_output+
                # content_list=glob.glob(sub_file+'*.jpg')
                # print(content_list)
                content_path=loc+'/style_transfer/expanded/expanded_output/'
                content_list=glob.glob(content_path+'*.jpg')
                sub_style_file=loc+'/style_transfer/expanded/style_output/'+style_name+'/'
                if os.path.exists(sub_style_file) is False:
                    os.makedirs(sub_style_file)
                expanded_style_main(content_list,style_pic,sub_style_file)
        def gen_lerp_pic(self):
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("开始生成DDS贴图············")
                # style_path=self.project_base+'/style_output/'
                # self.lerp_output=self.project_base+'/lerp_output/'
                # dds_output=self.project_base+'/dds_output/'
                # if os.path.exists(self.lerp_output) is False:
                #     os.makedirs(self.lerp_output)
                # if os.path.exists(style_path) is False:
                #     os.makedirs(style_path)
                style_pic = self.chosen_style_pic
                style_name = os.path.basename(style_pic).split('.')[0]
                # content_path=self.project_base+'/style_transfer/'
                for loc in self.multi_files:
                    file_name=loc.split('/')[-1]

                    sub_content_file=loc+'/style_transfer/expanded/expanded_output/'
                    sub_style_file=loc+'/style_transfer/expanded/style_output/'+style_name+'/'
                    sub_save_path=loc+'/style_transfer/expanded/lerg_out/'+style_name+'/'
                    # dds_output=
                    if os.path.exists(sub_save_path) is False:
                        os.makedirs(sub_save_path)

                    content_list=glob.glob(sub_content_file+'*.jpg')
                    for content_pic in content_list:
                        pic_name=os.path.basename(content_pic)
                        style_pic=sub_style_file+pic_name
                        if os.path.exists(style_pic) is False:
                            InfoNotifier.InfoNotifier.g_progress_info.append(style_pic+' not exists')
                            continue

                        save_pic_path=sub_save_path+pic_name
                        if os.path.exists(save_pic_path) is False:
                            lerp_ret,ret=gen_lerp_ret.lerp_img(content_pic,style_pic,self.lerp_value)
                            gen_lerp_ret.write_img(lerp_ret,save_pic_path)
                            tga_img=Image.open(sub_content_file+pic_name.split('.')[0]+'.tga')
                            jpg_img=Image.open(save_pic_path)
                            ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                            ir, ig, ib = jpg_img.split()
                            tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                            save_pic_path=save_pic_path.replace(".jpg",".tga")
                            tga_img.save(save_pic_path,quality=100)
                            print(f"generate tga image {save_pic_path} after lerp op.")
                        dds_save_path=loc+'/style_transfer/expanded/dds_output/'+style_name+'/'

                        if os.path.exists(dds_save_path) is False:
                            os.makedirs(dds_save_path)
                        ###生成无缝贴图（.tga）
                        seamless_path=loc+f'/style_transfer/expanded/seamless/{style_name}/'
                        if os.path.exists(seamless_path) is False:
                            os.makedirs(seamless_path)
                        img=Image.open(save_pic_path)
                        width = img.width
                        height = img.height
                        pad=256
                        img_crop = img.crop((pad, pad, width - pad, height - pad))
                        img_crop.save(seamless_path+os.path.basename(save_pic_path),quality=100)



                        main_cmd=f"{self.texconv_path} -dxt5 -file {seamless_path+os.path.basename(save_pic_path)} -outdir {dds_save_path}"
                        main_cmd=main_cmd.replace("\n","")
                        os.system(main_cmd)
                InfoNotifier.InfoNotifier.g_progress_info.append("dds图片已转化完毕，保存在工程文件dds_output中")
            except BaseException as be:
                print(be)


        def run(self):
            self.gen_expanded_pic()
            self.gen_style()
            self.gen_lerp_pic()
            self._signal.emit()








        # self.expanded_jpg_tga_output=self.project_base+'/style_transfer/expanded/'

        #     jpg_dds_dir=self.project_base+'/style_transfer/'
        #     self.jpg_dds_dir = jpg_dds_dir
        #     for sub_file in os.listdir(jpg_dds_dir):
        #         file_name=sub_file.split('/')[-1]
        #         expanded_jpg_tga_output = self.project_base + '/style_transfer/'+file_name+'/expanded/'
        #         self.expanded_jpg_tga_output=expanded_jpg_tga_output
        #         if os.path.exists(expanded_jpg_tga_output) is False:
        #             os.makedirs(expanded_jpg_tga_output)
        #         sub_file_dir=jpg_dds_dir+file_name+'/'
        #         for file_jpg in os.listdir(sub_file_dir):
        #             if file_jpg.endswith(".jpg") is True:
        #                 split_text = os.path.splitext(file_jpg)
        #                 file_tga = split_text[0] + '.tga'
        #                 img_jpg = Image.open(jpg_dds_dir+sub_file + '/'+file_jpg)
        #                 img_tga = Image.open(jpg_dds_dir+sub_file + '/' + file_tga)
        #                 width = img_jpg.width
        #                 height = img_jpg.height
        #                 if(width == img_tga.width and height == img_tga.height):
        #                     img_jpg_pad = Image.new("RGB", (width * 3, height * 3))
        #                     img_tga_pad = Image.new("RGBA", (width * 3, height * 3))
        #                     for i in range(3):
        #                         for j in range(3):
        #                             img_jpg_pad.paste(img_jpg, (i * width, j * height, (i + 1) * width, (j + 1) * height))
        #                             img_tga_pad.paste(img_tga, (i * width, j * height, (i + 1) * width, (j + 1) * height))
        #                     if os.path.exists(expanded_jpg_tga_output) is False:
        #                         os.makedirs(expanded_jpg_tga_output)
        #                     img_jpg_crop = img_jpg_pad.crop((width - self.pad, height - self.pad, 2 * width + self.pad, 2 * height + self.pad))
        #                     img_jpg_crop.save(expanded_jpg_tga_output + file_jpg, quality=100)
        #                     print("saveing " + expanded_jpg_tga_output+ file_jpg)
        #
        #                     img_tga_crop = img_tga_pad.crop((width - self.pad, height - self.pad, 2 * width + self.pad, 2 * height + self.pad))
        #                     img_tga_crop.save(expanded_jpg_tga_output+file_tga, quality=100)
        #                     print("saveing " +expanded_jpg_tga_output+ file_tga)
        #
        # def gen_style_pics(self):
        #     self.gen_expanded_pic()
        #     input=self.jpg_dds_dir
        #     style_pic=self.chosen_style_pic
        #     self.temp_file_name = self.project_base + '/style_output/'
        #     if os.path.exists(self.temp_file_name) is False:
        #         os.makedirs(self.temp_file_name)
        #     for file_single in self.multi_files:
        #         file_name=file_single.split('/')[-1]
        #         content_list=glob.glob(input+'/'+file_name+'/*.jpg')
        #         # filename = content_list[0].split("/")[-2]
        #
        #
        #
        #         # index=0
        #         # for i in content_list:
        #         #     save_temp_dir=self.temp_file_name+str(index)+'.jpg'
        #         expanded_style_main(content_list, style_pic, self.temp_file_name)
        #     # InfoNotifier.InfoNotifier.g_progress_info.append("完成")
        #     # main(pics_dir=[], style_dir='', save_dir='')
        #     self.gen_lerg()
        #     self._signal.emit()
        # def gen_lerg(self):
        #     InfoNotifier.InfoNotifier.g_progress_info.append("开始生成DDS贴图")
        #     self.lerg_save_path = self.project_base + '/lerp_output/'
        #     style_jpg_dir = self.temp_file_name
        #     content_dir = self.expanded_jpg_tga_output
        #     style_dds = self.project_base + '/dds_output/'
        #     style_name = os.path.basename(self.chosen_style_pic).split('.')[0]
        #     self.style_name = style_name
        #     for i in self.multi_files:
        #         # 文件名
        #         file_name = i.split('/')[-1]
        #         sub_content_file = content_dir
        #         sub_style_file=self.temp_file_name+style_name+'/expanded/'+file_name+'/'
        #         sub_save_path = self.lerg_save_path + style_name + '/expanded/' + file_name + '/'
        #         sub_dds_path = style_dds + style_name + '/expanded/' + file_name + '/'
        #         for f in os.listdir(sub_content_file):
        #             if f.endswith(".jpg") is False:
        #                 continue
        #             content_pic_path = sub_content_file + f
        #             style_pic_path = sub_style_file + f
        #             out_pic_path = sub_save_path + f
        #             if os.path.exists(self.lerg_save_path) is False:
        #                 os.makedirs(self.lerg_save_path)
        #             if os.path.exists(self.lerg_save_path + style_name) is False:
        #                 os.makedirs(self.lerg_save_path + style_name)
        #             if os.path.exists(self.lerg_save_path + style_name + '/expanded/' + file_name) is False:
        #                 os.makedirs(self.lerg_save_path + style_name + '/expanded/' + file_name)
        #             if os.path.exists(style_dds) is False:
        #                 os.makedirs(style_dds)
        #             if os.path.exists(style_dds + style_name) is False:
        #                 os.makedirs(style_dds + style_name)
        #             if os.path.exists(style_dds + style_name + '/expanded/' + file_name) is False:
        #                 os.makedirs(style_dds + style_name + '/expanded/' + file_name)
        #             ##########Lerp
        #             try:
        #                 lerp_ret, ret = gen_lerp_ret.lerp_img(content_pic_path, style_pic_path, self.lerp_value)
        #
        #                 gen_lerp_ret.write_img(lerp_ret, out_pic_path)
        #             except BaseException as bec:
        #                 print(bec)
        #                 # combine alpha channel
        #             split_f = os.path.splitext(f)
        #             try:
        #                 tga_img = Image.open(sub_content_file + split_f[0] + ".tga")
        #                 jpg_img = Image.open(out_pic_path)
        #                 if len(tga_img.getbands()) == 4:
        #                     ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
        #                     ir, ig, ib = jpg_img.split()
        #                     tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
        #                     out_pic_path = out_pic_path.replace(".jpg", ".tga")
        #                     tga_img.save(out_pic_path, quality=100)
        #                     print(f"generate tga image {out_pic_path} after lerp op.")
        #                     img=Image.open(out_pic_path)
        #                     pad=self.pad
        #                     width = img.width
        #                     height = img.height
        #
        #                     img_crop = img.crop((pad, pad, width - pad, height - pad))
        #                     if os.path.exists(self.seamless_file) is False:
        #                         os.makedirs(self.seamless_file)
        #                     img_crop.save(self.seamless_file + style_name+'/'+file_name+'/'+os.path.basename(out_pic_path), quality=100)
        #                     # dds_output=sub_dds_path+os.path.basename(out_pic_path).split('.')[0]+'.dds'
        #                     dds_output = sub_dds_path
        #                     main_cmd = f"{self.texconv_path} -dxt5 -file  {self.seamless_file + style_name+'/'+file_name+'/'+os.path.basename(out_pic_path)} -outdir {dds_output} "
        #                     main_cmd = main_cmd.replace("\n", "")
        #                     print(main_cmd)
        #                     os.system(main_cmd)
        #
        #
        #             except BaseException as be:
        #                 print(be)
        #     InfoNotifier.InfoNotifier.g_progress_info.append("dds图片已转化完毕，保存在工程文件dds_output中")
        #
        #             # def gen_dds_from_tga(self):
        #             #     input_tga_path=
        # def run(self):
        #     self.gen_style_pics()
        # # def gen_seamless_files(self):
        # #     seamless_file=self.project_base+'seamless/'
        # #     if os.path.exists(seamless_file) is False:
        # #         os.makedirs(seamless_file)
        # #     for file in self.show_list:
        # #         file=file.replace('.jpg','.tga')
        # #         if file.endswith('.tga') is True:
        # #             img=Image.open(file)
        # #         width = img.width
        # #         height = img.height
        # #
        # #         img_crop = img.crop((self.pad, self.pad, width - self.pad, height - self.pad))
        # #         img_crop.save(seamless_file+os.path.basename(file),quality=100)
        # #     self.seamless_file=seamless_file
        ###???###
    class My_gen_style_thread(QThread):
        _signal_trigger=pyqtSignal()
        def __init__(self):
            super(My_gen_style_thread,self).__init__()
            self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"
        def set_para(self,chosen_style_pic='',show_list=[],project_base='',multi_files=[],lerp_value=50):
            self.chosen_style_pic=chosen_style_pic
            self.show_list=show_list
            self.project_base=project_base
            self.multi_files=multi_files
            self.lerp_value=lerp_value
            # self.is_seamless=is_seamless

        def preview_lerg_pics(self):
            style_pic = self.chosen_style_pic
            content_list = self.show_list
            filename = content_list[0].split("/")[-2]
            parent_path=os.path.dirname(content_list[0])
            self.parent_path=parent_path
            self.temp_file_name = parent_path+ '/style_output/'

            if os.path.exists(self.temp_file_name) is False:
                os.makedirs(self.temp_file_name)
            # index=0
            # for i in content_list:
            #     save_temp_dir=self.temp_file_name+str(index)+'.jpg'
            style_main(content_list, style_pic, self.temp_file_name)
            # InfoNotifier.InfoNotifier.g_progress_info.append("完成")
            # main(pics_dir=[], style_dir='', save_dir='')
            self.gen_lerg()
            self._signal_trigger.emit()
        def gen_lerg(self):
            InfoNotifier.InfoNotifier.g_progress_info.append("开始生成DDS贴图···········")
            self.lerg_save_path=self.parent_path+'/lerp_output/'
            if os.path.exists(self.lerg_save_path) is False:
                os.makedirs(self.lerg_save_path)
            style_jpg_dir=self.temp_file_name
            content_dir=self.parent_path+'/'
            style_dds=self.parent_path+'/dds_output/'
            if os.path.exists(style_dds) is False:
                os.makedirs(style_dds)
            style_name=os.path.basename(self.chosen_style_pic).split('.')[0]
            self.style_name=style_name
            for file_path in self.show_list:
                file_name=os.path.basename(file_path)
                #原图
                content_real_path=content_dir+file_name
                content_tga_path=content_dir+file_name.replace(".jpg",".tga")
                #风格后图片
                style_real_path=self.temp_file_name+file_name
                #待保存-lerg
                lerp_real_path=self.lerg_save_path+style_name+'/'+file_name
                #待保存-dds
                dds_real_path=style_dds+style_name+'/'

                #######################################################
                if os.path.exists(content_real_path) is False:
                    # os.makedirs(self.lerg_save_path)
                    print("dds not transfered")
                if os.path.exists(self.lerg_save_path+style_name+'/') is False:
                    os.makedirs(self.lerg_save_path+style_name+'/')
                if os.path.exists(style_dds+style_name+'/') is False:
                    os.makedirs(style_dds+style_name+'/')
                try:
                    lerp_ret, ret = gen_lerp_ret.lerp_img(content_real_path, style_real_path, self.lerp_value)
                    gen_lerp_ret.write_img(lerp_ret, lerp_real_path)
                except BaseException as be:
                    print(be)
                # combine alpha channel
                tga_img = Image.open(content_tga_path)
                jpg_img = Image.open(content_real_path)
                ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                ir, ig, ib = jpg_img.split()
                tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                lerp_real_path = lerp_real_path.replace(".jpg", ".tga")
                tga_img.save(lerp_real_path, quality=100)
                print(f"generate tga image {lerp_real_path} after lerp op.")
                # dds_out = self.dds_output + style_name + '/'
                # if os.path.exists(dds_out) is False:
                #     os.makedirs(dds_out)
                main_cmd = f"{self.texconv_path} -dxt5 -file {lerp_real_path} -outdir {dds_real_path}"
                main_cmd.replace("\n", "")
                os.system(main_cmd)




            # for i in self.multi_files:
            #     #文件名
            #     file_name=i.split('/')[-1]
            #     sub_content_file=content_dir+file_name+'/'
            #     #风格后路径
            #     sub_style_file=self.temp_file_name+style_name+'/'+file_name+'/'
            #     sub_save_path=self.lerg_save_path+style_name+'/'+file_name+'/'
            #     sub_dds_path=style_dds+style_name+'/'+file_name+'/'
            #     for f in os.listdir(sub_content_file):
            #         if f.endswith(".jpg") is False:
            #             continue
            #         content_pic_path=sub_content_file+f
            #         style_pic_path=sub_style_file+f
            #         out_pic_path=sub_save_path+f
            #         if os.path.exists(self.lerg_save_path) is False:
            #             os.makedirs(self.lerg_save_path)
            #         if os.path.exists(self.lerg_save_path+style_name) is False:
            #             os.makedirs(self.lerg_save_path+style_name)
            #         if os.path.exists(self.lerg_save_path+style_name+'/'+file_name) is False:
            #             os.makedirs(self.lerg_save_path + style_name + '/' + file_name)
            #         if os.path.exists(style_dds) is False:
            #             os.makedirs(style_dds)
            #         if os.path.exists(style_dds+style_name) is False:
            #             os.makedirs(style_dds+style_name)
            #         if os.path.exists(style_dds+style_name+'/'+file_name) is False:
            #             os.makedirs(style_dds+style_name+'/'+file_name)
            #         ##########Lerp
            #         try:
            #             lerp_ret,ret=gen_lerp_ret.lerp_img(content_pic_path,style_pic_path,self.lerp_value)
            #
            #             gen_lerp_ret.write_img(lerp_ret,out_pic_path)
            #         except BaseException as bec:
            #             print(bec)
            #
            #         #combine alpha channel
            #         split_f=os.path.splitext(f)
            #         try:
            #             tga_img=Image.open(sub_content_file+split_f[0]+".tga")
            #             jpg_img=Image.open(out_pic_path)
            #             if len(tga_img.getbands())==4:
            #                 ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
            #                 ir, ig, ib = jpg_img.split()
            #                 tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
            #                 out_pic_path = out_pic_path.replace(".jpg", ".tga")
            #                 tga_img.save(out_pic_path, quality=100)
            #                 print(f"generate tga image {out_pic_path} after lerp op.")
            #                 # dds_output=sub_dds_path+os.path.basename(out_pic_path).split('.')[0]+'.dds'
            #                 dds_output = sub_dds_path
            #                 main_cmd=f"{self.texconv_path} -dxt5 -file  {out_pic_path} -outdir {dds_output} "
            #                 main_cmd = main_cmd.replace("\n", "")
            #                 print(main_cmd)
            #                 os.system(main_cmd)
            #
            #
            #         except BaseException as be:
            #             print(be)
            InfoNotifier.InfoNotifier.g_progress_info.append("dds图片已转化完毕，保存在工程文件dds_output中")

        # def gen_dds_from_tga(self):
        #     input_tga_path=
        def run(self):
            self.preview_lerg_pics()

    #################################################tab2
    class My_gen_dds_jpg_thread2(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_dds_jpg_thread2, self).__init__()
        def set_para(self,file_='',work_='',dds_list=[]):
            self.file_=file_
            self.work_=work_
            self.dds_list=dds_list
        def gen_jpg_tga(self):
            gen_jpg_tga_from_dds.gen_jpg_tga(self.file_,self.work_,self.dds_list)
            InfoNotifier.InfoNotifier.g_progress_info.append("已生成jpg,tga格式图片，点击下拉框选择目录进行预览")
            self._signal.emit()
        def run(self):
            self.gen_jpg_tga()
            # self.show_previewed_before_pic2()
    class My_gen_style_temp_thread2(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_style_temp_thread2, self).__init__()
        def set_para(self,show_list=[],chosen_style_pic='',temp_file=''):
            self.show_list=show_list
            self.chosen_style_pic=chosen_style_pic
            #根目录
            self.temp_file_name=temp_file
        def gen_style(self):
            style_pic=self.chosen_style_pic
            content_list = self.show_list
            # if os.path.exists(self.temp_file_name) is False:
            #     os.makedirs(self.temp_file_name)
                # index=0
                # for i in content_list:
                #     save_temp_dir=self.temp_file_name+str(index)+'.jpg'
            # style_name = os.path.basename(style_pic).split('.')[0]
            style_main2(content_list, style_pic, self.temp_file_name)
            InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览")
            # if os.path.exists(self.temp_file_name + style_name + '/') is False:
            #     style_main2(content_list, style_pic, self.temp_file_name)
            #     InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览，并滑动微调栏杆调整插值参数")
            # else:
            #     for file_path in content_list:
            #         file = os.path.basename(file_path)
            #         # style_path=
            #         InfoNotifier.InfoNotifier.style_preview_pic_dir2.append(
            #             f'{self.temp_file_name}{style_name}/' + file)
            #     InfoNotifier.InfoNotifier.g_progress_info.append(self.temp_file_name + style_name + '已存在，点击一张原图进行预览')
            # main(pics_dir=[], style_dir='', save_dir='')
            self._signal.emit()

        def run(self):
            self.gen_style()
    class My_gen_style_thread2(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_style_thread2, self).__init__()
            self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"
        def set_para(self,txt_path='',work_='',lerg_value=50,chosen_style_pic='',chosen_content_file_list=[],dir_dict={}):
            # txt_file = self.txt_path
            # work_ = self.ui.project_base_dir.text()
            # lerp_value = self.ui.change_coe_horizontalSlider2.value()
            # seamless = self.is_seamless_ornot2()
            self.txt_path=txt_path
            self.work_=work_
            self.lerg_value=lerg_value
            self.chosen_style_pic=chosen_style_pic
            self.chosen_content_file_list=chosen_content_file_list
            self.dir_dict=dir_dict

            # self.seamless=seamless
        def save_all(self):
            # if self.seamless is False:
            #     is_seamless=''
            # elif self.seamless is True:
            #     is_seamless='/expanded'
            style_name=os.path.basename(self.chosen_style_pic).split('.')[0]
            f=open(self.txt_path,"r",encoding='utf-8-sig')
            # f.readline()




            style_txt_main2(self.txt_path,self.work_,self.chosen_style_pic,self.chosen_content_file_list,self.dir_dict)
            for file in f:

                file=file.replace("\n","").replace("\\","/")
                get_path = PathUtils(self.work_, self.chosen_style_pic,file)
                a = False
                # 判断该图片是否在选中目录中
                for sub_file in self.chosen_content_file_list:
                    if self.dir_dict[sub_file] in file:
                        a = True
                        break
                if a is True:
                    # file_real_path=self.work_+'/'+file
                    file_name=os.path.basename(file)
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
                    # pic_list=[jpg_path]
                    # style_main2(pic_list,self.chosen_style_pic,self.style_output)
                    #lerp
                    style_out_pic_path=get_path.get_style_path()
                    if os.path.exists(style_out_pic_path) is False:
                        InfoNotifier.InfoNotifier.g_progress_info.append(f"不存在对应风格化图片{style_out_pic_path}。跳过本张图片")
                        continue
                    lerp_out_path=get_path.get_jpg_lerp_path()
                    if os.path.exists(lerp_out_path) is False:
                        if os.path.exists(os.path.dirname(lerp_out_path)) is False:
                            os.makedirs(os.path.dirname(lerp_out_path))

                        if os.path.exists(jpg_path) is False:
                            print(jpg_path + " is not exist!")
                            continue

                        lerp_ret,_=gen_lerp_ret.lerp_img(jpg_path,style_out_pic_path,self.lerg_value)
                        gen_lerp_ret.write_img(lerp_ret,lerp_out_path)
                        #combine alpha c
                        tga_img=Image.open(tga_path)
                        jpg_img=Image.open(lerp_out_path)
                        ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                        ir, ig, ib = jpg_img.split()
                        tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                        lerp_out_path = lerp_out_path.replace(".jpg", ".tga")
                        tga_img.save(lerp_out_path, quality=100)
                        print(f"generate tga image {lerp_out_path} after lerp op.")
                        InfoNotifier.InfoNotifier.g_progress_info.append(f"生成插值操作后的tga图片{lerp_out_path} ")
                    else:
                        InfoNotifier.InfoNotifier.g_progress_info.append(f"{lerp_out_path}已存在 ")
                    dds_out=get_path.get_dds_output_path()
                    if os.path.exists(dds_out+file_name) is False:
                        if os.path.exists(dds_out) is False:
                            os.makedirs(dds_out)
                        main_cmd=f"{self.texconv_path} -dxt5 -file {lerp_out_path} -outdir {dds_out}"
                        main_cmd.replace("\n","")
                        try:
                            os.system(main_cmd)
                            InfoNotifier.InfoNotifier.g_progress_info.append(f"将{lerp_out_path}转化为DDS格式···")
                        except BaseException as bec:
                            InfoNotifier.InfoNotifier.g_progress_info.append(bec)
                    else:
                        InfoNotifier.InfoNotifier.g_progress_info.append(dds_out+file_name+'已存在，跳过')
            InfoNotifier.InfoNotifier.g_progress_info.append("保存完成")
            self._signal.emit()
        def run(self):
            self.save_all()
    class My_gen_seamless_thread2(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_seamless_thread2, self).__init__()
            self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"
        def set_para(self,txt_path='',work_='',lerg_value=50,chosen_style_pic='',chosen_content_file_list=[],dir_dict={}):
            self.txt_path = txt_path
            self.work_ = work_
            self.lerg_value = lerg_value
            self.chosen_style_pic = chosen_style_pic
            self.chosen_content_file_list=chosen_content_file_list
            self.dir_dict=dir_dict
        def expanded(self):

            pad = 256
            style_name = os.path.basename(self.chosen_style_pic).split('.')[0]
            f = open(self.txt_path, "r", encoding='utf-8-sig')
            # f.readline()

            for file in f:
                file = file.replace("\n", "").replace("\\","/")
                get_path = PathUtils(self.work_,self.chosen_style_pic,file)

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
                        tga_path =  get_path.dds_to_tga_path()
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
                        img_jpg_crop.save( get_path.get_expanded_jpg_path(), quality=100)
                        print( get_path.get_expanded_jpg_path())
                        img_tga_crop = img_tga_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                        img_tga_crop.save( get_path.get_expanded_tga_path(), quality=100)
                        print(get_path.get_expanded_tga_path())
                        InfoNotifier.InfoNotifier.g_progress_info.append(f'保存expand后图片：{get_path.get_expanded_tga_path()}，jpg')
                    else:
                        InfoNotifier.InfoNotifier.g_progress_info.append(get_path.get_expanded_tga_path()+' exists')
        def save_all(self):
            pad=256
            style_name = os.path.basename(self.chosen_style_pic).split('.')[0]

            f = open(self.txt_path, "r", encoding='utf-8-sig')
            # f.readline()
            gen_style_seamless_txt.style_txt_main2(self.txt_path,self.work_,self.chosen_style_pic,self.chosen_content_file_list,self.dir_dict)
            # gen_style_class.style_txt_main2(self.txt_path,self.work_,self.chosen_style_pic,self.chosen_content_file_list,self.dir_dict,True)
            for file in f:

                file = file.replace("\n", "").replace("\\", "/")
                get_path = PathUtils(self.work_,self.chosen_style_pic,file)
                # 判断该图片是否在选中目录中
                a = False
                for sub_file in self.chosen_content_file_list:
                    if self.dir_dict[sub_file] in file:
                        a = True
                        break
                if a is True:
                    file = file.replace("\n", "")
                    file_real_path =get_path.real_dds_path()
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

                    jpg_path =get_path.get_expanded_jpg_path()
                    tga_path =get_path.get_expanded_tga_path()
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
                    tmp_style_in=jpg_path
                    # style_out=self.style_output+style_name+'/'
                    # tmp_style_list=[tmp_style_in]
                    # style_main2(tmp_style_list,self.chosen_style_pic,self.style_output)

                    #lerp
                    style_out_pic_path=get_path.get_expanded_style_path()
                    if os.path.exists(style_out_pic_path) is False:
                        InfoNotifier.InfoNotifier.g_progress_info.append("不存在对应风格化图片。跳过本张图片")
                        continue

                    lerp_out_path=get_path.get_expanded_lerp_path_jpg()
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
                        InfoNotifier.InfoNotifier.g_progress_info.append('生成插值操作后的tga图片'+lerp_out_path)
                    else:
                        InfoNotifier.InfoNotifier.g_progress_info.append(lerp_out_path+"已存在，跳过")
                    #seamless
                    if os.path.exists(get_path.get_seamless_path()) is False:
                        seamless_path=os.path.dirname(get_path.get_seamless_path())
                        if os.path.exists(seamless_path) is False:
                            os.makedirs(seamless_path)
                        # print("seamless:"+PathUtils.get_expanded_lerp_path_tga())

                        img=Image.open(get_path.get_expanded_lerp_path_tga())
                        width = img.width
                        height = img.height
                        pad = 256
                        img_crop = img.crop((pad, pad, width - pad, height - pad))
                        img_crop.save(get_path.get_seamless_path(), quality=100)
                        InfoNotifier.InfoNotifier.g_progress_info.append('生成无缝贴图'+get_path.get_seamless_path())
                    dds_output=get_path.get_seamless_dds_path()
                    if os.path.exists(dds_output+file_name) is False:
                        seamless_path = os.path.dirname(get_path.get_seamless_path())
                        if os.path.exists(dds_output) is False:
                            os.makedirs(dds_output)
                        main_cmd=f"{self.texconv_path} -dxt5 -file {get_path.get_seamless_path()} -outdir {dds_output}"
                        main_cmd.replace("\n","")
                        os.system(main_cmd)
                        InfoNotifier.InfoNotifier.g_progress_info.append(f'将{dds_output}{file_name}转化为DDS格式···')
                    else:
                        InfoNotifier.InfoNotifier.g_progress_info.append(dds_output+file_name+'已存在，跳过')
            InfoNotifier.InfoNotifier.g_progress_info.append("保存完成")
            self._signal.emit()
        def run(self):
            self.expanded()
            self.save_all()


    #################################################tab3
    class My_gen_dds_jpg_thread3(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_dds_jpg_thread3, self).__init__()
            self.exe_dir=os.getcwd() + "\\dds_to_jpg/dds_to_jpg.exe"
        def set_para(self,content_list=[]):
            self.show_list=content_list
        def gen_jpg(self):
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("开始将贴图格式转换为jpg和tga····")
                for file in self.show_list:
                    file_real_path=file

                    file_name = os.path.basename(file_real_path)

                    # 创建style_transfer目录
                    parent_path = os.path.dirname(file_real_path)
                    style_transfer_path = parent_path + "/style_transfer/"
                    if os.path.exists(style_transfer_path) is False:
                        os.makedirs(style_transfer_path)

                    # 创建 jpg tga
                    jpg_path = style_transfer_path + file_name.replace(".dds", ".jpg")
                    tga_path = style_transfer_path + file_name.replace(".dds", ".tga")
                    if os.path.exists(jpg_path) is False:
                        main_cmd = f"{self.exe_dir} {file_real_path} {jpg_path} {tga_path}"
                        main_cmd = main_cmd.replace("\n", "")
                        print(main_cmd)

                        # do real job
                        os.system(main_cmd)
                    else:
                        print(jpg_path+' exists')

                InfoNotifier.InfoNotifier.g_progress_info.append("已生成jpg,tga格式图片")
                self._signal.emit()
            except BaseException as e:
                print(e)
        def run(self):
            self.gen_jpg()
    class My_gen_style_temp_thread3(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_style_temp_thread3, self).__init__()
        def set_para(self,show_list=[],chosen_style_pic='',temp_file=''):
            self.show_list = show_list
            self.chosen_style_pic = chosen_style_pic
            self.temp_file_name = temp_file

        def gen_style(self):
            style_pic = self.chosen_style_pic
            content_list = self.show_list
            file_name=os.path.basename(content_list[0])
            style_name=os.path.basename(style_pic).split('.')[0]
            if os.path.exists(self.temp_file_name) is False:
                os.makedirs(self.temp_file_name)
            #
            # style_main3(content_list, style_pic, self.temp_file_name)
            # InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览，并滑动微调栏杆调整插值参数")

            """让生成过的临时文件不再重新生成"""
            if os.path.exists(self.temp_file_name + style_name + '/'+file_name) is False:
                style_main3(content_list, style_pic, self.temp_file_name)
                InfoNotifier.InfoNotifier.g_progress_info.append("完成，点击一张原图进行预览，并滑动微调栏杆调整插值参数")
            else:
                for file_path in content_list:
                    file = os.path.basename(file_path)
                    # style_path=
                    InfoNotifier.InfoNotifier.style_preview_pic_dir3.append(f'{self.temp_file_name}{style_name}/' + file)
                InfoNotifier.InfoNotifier.g_progress_info.append(self.temp_file_name + style_name + '已存在，点击一张原图进行预览')


            # main(pics_dir=[], style_dir='', save_dir='')
            self._signal.emit()

        def run(self):
            self.gen_style()
    class My_gen_style_thread3(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_style_thread3, self).__init__()
            self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"
        def set_para(self,content_list=[],style_path='',lerg_value=50):
            self.content_list=content_list
            self.chosen_style_pic=style_path
            self.lerg_value=lerg_value
        def save_all(self):

            style_name=os.path.basename(self.chosen_style_pic).split('.')[0]
            InfoNotifier.InfoNotifier.g_progress_info.append("开始保存图片··············")
            gen_style_batch3.style_main3(self.content_list,self.chosen_style_pic)
            for file in self.content_list:
                file = file.replace("\n", "")
                file_name = os.path.basename(file)
                parent_path = os.path.dirname(file)
                self.style_transfer_path = parent_path + "/style_transfer/"
                if os.path.exists(self.style_transfer_path) is False:
                    InfoNotifier.InfoNotifier.g_progress_info.append("请先将dds转化为jpg,tga格式")
                    return

                self.style_output = parent_path + '/style_transfer/style_output/'
                self.lerp_output = parent_path + '/style_transfer/lerg_output/'
                self.dds_output = parent_path + '/style_transfer/dds_output/'
                if os.path.exists(self.style_output) is False:
                    os.makedirs(self.style_output)
                if os.path.exists(self.lerp_output) is False:
                    os.makedirs(self.lerp_output)
                if os.path.exists(self.dds_output) is False:
                    os.makedirs(self.dds_output)
                jpg_path = self.style_transfer_path + file_name.replace(".dds", ".jpg")
                tga_path = self.style_transfer_path + file_name.replace(".dds", ".tga")
                pic_list=[jpg_path]
                # gen_style_all.style_main3(pic_list,self.chosen_style_pic,self.style_output)

                #lerp
                style_out_pic_path = self.style_output + style_name + '/' + file_name.replace(".dds", ".jpg")
                if os.path.exists(style_out_pic_path) is False:
                    InfoNotifier.InfoNotifier.g_progress_info.append(f"不存在对应风格化图片{style_out_pic_path}。跳过本张图片")
                    continue
                lerp_out_path = self.lerp_output + style_name + '/' + file_name.replace(".dds", ".jpg")
                if os.path.exists(lerp_out_path) is False:
                    if os.path.exists(self.lerp_output + style_name + '/') is False:
                        os.makedirs(self.lerp_output + style_name + '/')
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
                    InfoNotifier.InfoNotifier.g_progress_info.append(f"generate tga image {lerp_out_path} after lerp op.")
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(lerp_out_path+' exists')
                #dds
                dds_out = self.dds_output + style_name + '/'
                if os.path.exists(dds_out+file_name) is False:
                    if os.path.exists(dds_out) is False:
                        os.makedirs(dds_out)
                    main_cmd = f"{self.texconv_path} -dxt5 -file {lerp_out_path} -outdir {dds_out}"
                    main_cmd.replace("\n", "")
                    os.system(main_cmd)
                    InfoNotifier.InfoNotifier.g_progress_info.append('生成DDS贴图：'+dds_out+file_name)
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(dds_out+file_name+' exists')

            InfoNotifier.InfoNotifier.g_progress_info.append("保存完成，DDS贴图保存在各原始图片目录下dds_output文件中")
            self._signal.emit()
        def run(self):
            self.save_all()
    class My_gen_seamless_style_thread3(QThread):
        _signal=pyqtSignal()
        def __init__(self):
            super(My_gen_seamless_style_thread3, self).__init__()
            self.texconv_path = os.getcwd() + "\\result_moss/texconv.exe"
        def set_para(self,content_list=[],style_path='',lerg_value=50):
            self.content_list=content_list
            self.chosen_style_pic=style_path
            self.lerg_value=lerg_value
        def expanded(self):
            InfoNotifier.InfoNotifier.g_progress_info.append("开始保存图片··············")
            pad = 256
            style_name = os.path.basename(self.chosen_style_pic).split('.')[0]
            for file in self.content_list:
                file = file.replace("\n", "")
                file_real_path = file
                file_name = os.path.basename(file_real_path)
                parent_path = os.path.dirname(file_real_path)
                self.style_transfer_path = parent_path + "/style_transfer/"
                # parent_path+=is_seamless
                if os.path.exists(self.style_transfer_path) is False:
                    InfoNotifier.InfoNotifier.g_progress_info.append("请先将dds转化为jpg,tga格式")
                    return

                parent_path += '/style_transfer/expanded'
                self.expanded_transfer = parent_path + '/expanded_transfer/'
                self.style_output = parent_path + '/style_output/'
                self.lerp_output = parent_path + '/lerg_output/'
                self.dds_output = parent_path + '/dds_output/'
                self.seamless_output = parent_path + '/seamless/'
                if os.path.exists(self.style_output) is False:
                    os.makedirs(self.style_output)
                if os.path.exists(self.lerp_output) is False:
                    os.makedirs(self.lerp_output)
                if os.path.exists(self.dds_output) is False:
                    os.makedirs(self.dds_output)
                if os.path.exists(self.expanded_transfer) is False:
                    os.makedirs(self.expanded_transfer)
                if os.path.exists(self.seamless_output) is False:
                    os.makedirs(self.seamless_output)

                jpg_path = self.style_transfer_path + file_name.replace(".dds", ".jpg")
                tga_path = self.style_transfer_path + file_name.replace(".dds", ".tga")
                #expand
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
                img_jpg_crop.save(self.expanded_transfer + os.path.basename(jpg_path), quality=100)
                print(self.expanded_transfer + os.path.basename(jpg_path))
                img_tga_crop = img_tga_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                img_tga_crop.save(self.expanded_transfer + os.path.basename(tga_path), quality=100)
                print(self.expanded_transfer + os.path.basename(tga_path))
                InfoNotifier.InfoNotifier.g_progress_info.append(f'保存expand后图片：{self.expanded_transfer}{os.path.basename(tga_path)}，jpg')

        def save_all(self):
            pad = 256
            style_name = os.path.basename(self.chosen_style_pic).split('.')[0]
            gen_seamless_style_batch3.style_main3(self.content_list,self.chosen_style_pic)
            for file in self.content_list:
                file = file.replace("\n", "")
                file_real_path = file
                file_name = os.path.basename(file_real_path)
                parent_path = os.path.dirname(file_real_path)
                self.style_transfer_path = parent_path + "/style_transfer/"
                # parent_path+=is_seamless
                if os.path.exists(self.style_transfer_path) is False:
                    InfoNotifier.InfoNotifier.g_progress_info.append("请先将dds转化为jpg,tga格式")
                    return

                parent_path += '/style_transfer/expanded'
                self.expanded_transfer = parent_path + '/expanded_transfer/'
                self.style_output = parent_path + '/style_output/'
                self.lerp_output = parent_path + '/lerg_output/'
                self.dds_output = parent_path + '/dds_output/'
                self.seamless_output = parent_path + '/seamless/'
                if os.path.exists(self.style_output) is False:
                    os.makedirs(self.style_output)
                if os.path.exists(self.lerp_output) is False:
                    os.makedirs(self.lerp_output)
                if os.path.exists(self.dds_output) is False:
                    os.makedirs(self.dds_output)
                if os.path.exists(self.expanded_transfer) is False:
                    os.makedirs(self.expanded_transfer)
                if os.path.exists(self.seamless_output) is False:
                    os.makedirs(self.seamless_output)

                jpg_path = self.style_transfer_path + file_name.replace(".dds", ".jpg")
                tga_path = self.style_transfer_path + file_name.replace(".dds", ".tga")
                #expand
                # img_jpg = Image.open(jpg_path)
                # img_tga = Image.open(tga_path)
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
                # img_jpg_crop.save(self.expanded_transfer + os.path.basename(jpg_path), quality=100)
                # print(self.expanded_transfer + os.path.basename(jpg_path))
                # img_tga_crop = img_tga_pad.crop((width - pad, height - pad, 2 * width + pad, 2 * height + pad))
                # img_tga_crop.save(self.expanded_transfer + os.path.basename(tga_path), quality=100)
                # print(self.expanded_transfer + os.path.basename(tga_path))

                tmp_style_in = self.expanded_transfer + os.path.basename(jpg_path)
                # style_out=self.style_output+style_name+'/'
                # tmp_style_list = [tmp_style_in]
                # gen_style_all.style_main3(tmp_style_list,self.chosen_style_pic,self.style_output)


                # lerp
                style_out_pic_path = self.style_output + style_name + '/' + file_name.replace(".dds", ".jpg")

                if os.path.exists(style_out_pic_path) is False:
                    InfoNotifier.InfoNotifier.g_progress_info.append(f"不存在对应风格化图片{style_out_pic_path}。跳过本张图片")
                    continue
                lerp_out_path = self.lerp_output + style_name + '/' + file_name.replace(".dds", ".jpg")
                if os.path.exists(lerp_out_path) is False:
                    if os.path.exists(self.lerp_output + style_name + '/') is False:
                        os.makedirs(self.lerp_output + style_name + '/')
                    lerp_ret, _ = gen_lerp_ret.lerp_img(tmp_style_in, style_out_pic_path, self.lerg_value)
                    gen_lerp_ret.write_img(lerp_ret, lerp_out_path)
                    # combine alpha c
                    tga_img = Image.open(self.expanded_transfer + os.path.basename(tga_path))
                    jpg_img = Image.open(lerp_out_path)
                    ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                    ir, ig, ib = jpg_img.split()
                    tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                    lerp_out_path = lerp_out_path.replace(".jpg", ".tga")
                    tga_img.save(lerp_out_path, quality=100)
                    print(f"generate tga image {lerp_out_path} after lerp op.")
                    InfoNotifier.InfoNotifier.g_progress_info.append(f"generate tga image {lerp_out_path} after lerp op.")
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(lerp_out_path+'  exists')
                # seamless
                seamless_path = self.seamless_output + style_name + '/'
                if os.path.exists(seamless_path + os.path.basename(lerp_out_path)) is False :

                    if os.path.exists(seamless_path) is False:
                        os.makedirs(seamless_path)
                    img = Image.open(lerp_out_path)
                    width = img.width
                    height = img.height
                    pad = 256
                    img_crop = img.crop((pad, pad, width - pad, height - pad))
                    img_crop.save(seamless_path + os.path.basename(lerp_out_path), quality=100)
                    InfoNotifier.InfoNotifier.g_progress_info.append("生成无缝贴图："+seamless_path + os.path.basename(lerp_out_path))
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(seamless_path + os.path.basename(lerp_out_path)+'   exists')

                dds_output = self.dds_output + style_name + '/'
                if os.path.exists(dds_output+file_name) is False:
                    if os.path.exists(dds_output) is False:
                        os.makedirs(dds_output)
                    main_cmd = f"{self.texconv_path} -dxt5 -file {seamless_path + os.path.basename(lerp_out_path)} -outdir {dds_output}"
                    main_cmd.replace("\n", "")
                    os.system(main_cmd)
                    InfoNotifier.InfoNotifier.g_progress_info.append('生成DDS贴图：'+dds_output+file_name)
                else:
                    InfoNotifier.InfoNotifier.g_progress_info.append(dds_output+file_name+'   exists')


            InfoNotifier.InfoNotifier.g_progress_info.append("dds图片已转化完毕，保存在工程文件dds_output中")
            self._signal.emit()
        def run(self):
            self.expanded()
            self.save_all()








    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.ui=Ui_test519.Ui_MainWindow()
            self.ui.setupUi(self)
            #实例化下拉复选框类
            self.combocheckBox1 = ComboCheckBox(self.ui.txt)
            self.combocheckBox1.setGeometry(QtCore.QRect(30, 160, 321, 41))
            self.combocheckBox1.setMinimumSize(QtCore.QSize(100, 20))
            self.combocheckBox1.setStyleSheet("background-color: rgb(90, 90, 90);\n"
                                    "color: rgb(0, 0, 0);")
            # items = ["\\terraintexture\grass", "\稻香村\\baked\\", "\maps_source\\texture\\"]
            # self.comboBox1.loadItems(items)
            self.combocheckBox1.setEnabled(False)


            self.preview_num=3
            # self.ui.pic_before_listWidget1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            # self.ui.pic_before_listWidget1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # self.threads=Mythread()
            # self.threads._signal_progress_info.connect()
            try:
                with open("./base_dir_log.txt",'r') as f:
                    lines=f.readlines()
                    last_line=lines[-1].replace("\n","")
                    self.ui.project_base_dir.setText(last_line)



            except:
                pass
            self.Thread=Mythread()
            self.Thread._signal_progress_info.connect(self.update_progress_info)
            self.Thread.start()
            self.ui.pic_before_listWidget1.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_style_listWidget1.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_style_listWidget3.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_before_listWidget3.setFlow(QtWidgets.QListView.LeftToRight)

            self.ui.pic_before_listWidget2.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_style_listWidget2.setFlow(QtWidgets.QListView.LeftToRight)
            self.project_cwd=''
            self.project_base=''
            #原图目录列表
            self.multi_dir_project=[]
            self.Choosed_style_pics_list = []
            self.Choosed_style_pics_list2=[]
            self.Choosed_style_pics_list3=[]
            self.chosen_style_pic3=''
            self.chosen_style_pic2=''
            self.chosen_content_list3=[]


            # 设置第三方导出工具路径
            self.exe_dir = os.getcwd() + "\\dds_to_jpg/dds_to_jpg.exe"
            self.ui.make_project_dir_button.clicked.connect(self.Make_Project_dir)
            self.ui.choose_pic_multi_file_dir_button1.clicked.connect(self.Choose_multi_dir_tab1)
            self.ui.multi_file_combobox.activated[int].connect(self.show_previewed_before_pic)
            self.ui.Preview_button.clicked.connect(self.gen_dds_jpg)
            self.ui.pic_before_listWidget1.clicked.connect(self.pic_before_clicked)
            self.ui.pic_style_listWidget1.clicked.connect(self.pic_style_clicked)
            self.ui.pic_before_listWidget2.clicked.connect(self.previewed_before_clicked)
            self.ui.choose_pic_style_button1.clicked.connect(self.Choose_style_pics)
            self.ui.change_coe_horizontalSlider1.valueChanged.connect(self.preview_style_pic_in_label)
            self.ui.change_coe_horizontalSlider2.valueChanged.connect(self.preview_style_pic_in_label2)
            self.ui.savePic_button1.clicked.connect(self.save_style)

            # self.ui.choose_before_pic_base.clicked.connect(self.choose_before_pic_base_dir)
            self.ui.choose_pic_txt_button2.clicked.connect(self.open_txt)
            self.ui.gen_jpg_tga_button2.clicked.connect(self.gen_jpg_tga2)

            # self.ui.preview_before_button2.clicked.connect(self.show_previewed_before_pic2)
            self.ui.preview_content2.clicked.connect(self.show_previewed_before_pic2)

            self.ui.choose_pic_style_button2.clicked.connect(self.Choose_style_pics2)
            self.ui.pic_style_listWidget2.clicked.connect(self.pic_style_clicked2)
            self.ui.savePic_button2.clicked.connect(self.save_style2)

            self.ui.pre_bef_button3.clicked.connect(self.preview_before_inWidget3)
            self.ui.choose_pics_button3.clicked.connect(self.choose_pics3)
            self.ui.pushButton.clicked.connect(self.gen_jpg_tga3)
            self.ui.pic_before_listWidget3.clicked.connect(self.previewed_before_clicked3)
            self.ui.choose_pic_style_button2_2.clicked.connect(self.Choose_style_pics3)
            self.ui.pic_style_listWidget3.clicked.connect(self.pic_style_clicked3)
            self.ui.change_coe_horizontalSlider3.valueChanged.connect(self.preview_after_pic_in_label3)
            self.ui.savePic_button3.clicked.connect(self.save_all3)

            # self.ui.picpath_bef_comboBox.highlighted[int].connect(self.highlighted_text)
        def update_progress_info(self):
            for info in InfoNotifier.InfoNotifier.g_progress_info:
                self.ui.progress_Info.append(info)
            InfoNotifier.InfoNotifier.g_progress_info.clear()
        def ui_update_progress_info(self,info=""):
            self.ui.progress_Info.append(info)



        #tab1
        def Make_Project_dir(self):
            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
            if len(directory)==0:
                return

            self.ui.project_base_dir.setText(directory)
            #
            with open('./base_dir_log.txt','w')as f:
                f.write(f"{directory}\n")
        def Choose_multi_dir_tab1(self):
            self.project_base = self.ui.project_base_dir.text()

            if self.ui.project_base_dir.text() =='':
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择根目录")
                return

            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", self.ui.project_base_dir.text())
            if len(directory)==0:
                return
            directory_temp=directory.split('/')
            if directory not in self.multi_dir_project:
                self.ui.multi_file_combobox.addItem(directory_temp[-2]+'/'+directory_temp[-1])
                # print(self.ui.multi_file_combobox.currentIndex())
                self.multi_dir_project.append(directory)
                print(self.multi_dir_project)
        def Choose_style_pics(self):
            self.ui.pic_style_listWidget1.clear()
            # InfoNotifier.InfoNotifier.style_preview_pic_dir.clear()
            files, filetype = QFileDialog.getOpenFileNames(self, "选择文件", "./", "JPG文件(*.jpg);;PNG文件(*.png)")
            if len(files) == 0:
                style_img_icon = []
                for pic in self.Choosed_style_pics_list:
                    pix = QPixmap(pic)
                    icon = QIcon()
                    icon.addPixmap(pix)
                    style_img_icon.append(icon)
                index = 0
                while index < len(self.Choosed_style_pics_list):
                    item = QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100, 100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.pic_style_listWidget1.addItem(item)
                    index += 1
                iconsize = QSize(100, 100)
                self.ui.pic_style_listWidget1.setIconSize(iconsize)

                QApplication.processEvents()
            else:
                pic_dir = ""
                for file in files:
                    pic_dir += file + ';;'
                pic_dir = pic_dir[:-2]

                pic_dir=pic_dir.split(";;")
                for i in pic_dir:
                    self.Choosed_style_pics_list.append(i)
                print(self.Choosed_style_pics_list)

                style_img_icon=[]
                for pic in self.Choosed_style_pics_list:
                    pix = QPixmap(pic)
                    icon = QIcon()
                    icon.addPixmap(pix)
                    style_img_icon.append(icon)
                index = 0
                while index < len(self.Choosed_style_pics_list):
                    item = QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100,100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.pic_style_listWidget1.addItem(item)
                    index += 1
                iconsize = QSize(100,100)
                self.ui.pic_style_listWidget1.setIconSize(iconsize)

                QApplication.processEvents()
        # def ShowImage_multi_pic(self,idx):
        #     dir=self.multi_dir_project[idx]
        def gen_dds_jpg(self):
            if self.ui.project_base_dir.text()=="":
                InfoNotifier.InfoNotifier.g_progress_info.append("请先为工程创建根目录")
            else:
                if len(self.multi_dir_project)==0:
                    self.ui.progress_Info.append("请先勾选待操作文件目录")
                else:
                    self.ui.progress_Info.append("开始转换dds贴图为jpg,tga格式")
                    QApplication.processEvents()
                    self.changethread=My_gen_dds_jpg_thread()
                    #set_para(self,project_base="",exe_dir="",multi_dir_project=[])
                    self.changethread.set_para(self.ui.project_base_dir.text(),self.exe_dir,self.multi_dir_project)
                    self.changethread.start()
                    self.ui.choose_pic_multi_file_dir_button1.setEnabled(False)
        def show_previewed_before_pic(self,i):
            self.ui.pic_before_listWidget1.clear()
            InfoNotifier.InfoNotifier.style_preview_pic_dir.clear()
            style_img_icon = []
            dirs = self.multi_dir_project[i]
            file_name = dirs.split('/')[-1]
            previem_list = glob.glob(dirs + '/style_transfer/'+'*.jpg')
            if len(previem_list) > self.preview_num:
                previem_list = previem_list[:self.preview_num]
            self.show_list=previem_list
            for pic in previem_list:
                pix = QPixmap(pic)
                icon = QIcon()
                icon.addPixmap(pix)
                style_img_icon.append(icon)
            index = 0
            while index < len(previem_list):
                item = QListWidgetItem()
                item.setIcon(style_img_icon[index])
                item.setSizeHint(QSize(100, 100))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ui.pic_before_listWidget1.addItem(item)
                index += 1
            iconsize = QSize(100, 100)
            self.ui.pic_before_listWidget1.setIconSize(iconsize)

            QApplication.processEvents()

                #     # pic=QtWidgets.QListWidgetItem(QtGui.QIcon(pic),cnt)
                #     # pix=piexif.load(pic)
                #     pix=QPixmap(pic)
                #     icon=QIcon()
                #     icon.addPixmap(pix)
                #     self.style_img_icon.append(icon)
                # idx=0
                # while idx<len(self.style_img_icon):
                #     item=QListWidgetItem()
                #     item.setIcon(previem_list[idx])
                #     item.setSizeHint(QSize(80,80))
                #     self.ui.pic_before_listWidget1.setIconSize(QSize(80,80))
                #     self.ui.pic_before_listWidget1.addItem(item)
                #     idx+=1

                # print(pic)
                # self.ui.pic_before_listWidget1.addItem(pix)
                # self.ui.pic_before_listWidget1.setIconSize()
        def pic_before_clicked(self):
            if len(self.show_list)==0:
                return
            pic_before_index=self.ui.pic_before_listWidget1.currentIndex().row()
            self.show_before_pic_in_label(pic_before_index)
            try:
                self.preview_style_pic_in_label()
            except BaseException as e:
                print(e)
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图片并进行预览")
        def pic_style_clicked(self):
            try:
                # self.ui.change_coe_horizontalSlider1.setEnabled(False)
                InfoNotifier.InfoNotifier.style_preview_pic_dir.clear()
                if len(self.Choosed_style_pics_list)==0:
                    return
                pic_style_index=self.ui.pic_style_listWidget1.currentIndex().row()
                self.show_style_pic_in_label(pic_style_index)
                # self.preview_lerg_pics()
                InfoNotifier.InfoNotifier.g_progress_info.append("准备生成风格迁移后的预览图...")

                self.gen_preview_pic=My_gen_style_temp_thread()
                #set_para(self,chosen_style_pic='',show_list=[],project_base='')
                self.gen_preview_pic.set_para(self.chosen_style_pic,self.show_list,self.ui.project_base_dir.text())
                self.gen_preview_pic.start()
            except:
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一个原图目录生成风格图片")
            # self.ui.change_coe_horizontalSlider1.setEnabled(True)
        def show_style_pic_in_label(self,i):
            # print(i)
            show_list=self.Choosed_style_pics_list
            dir=show_list[i]
            self.chosen_style_pic=dir
            pix=QPixmap(dir)

            # pix=pix.scaled(200, 200)
            # pix=pix.fromImage(pix)
            self.ui.pic_style_label1.setPixmap(pix)
            # self.ui.pic_style_label1.setFixedSize(QSize(250,250))
            self.ui.pic_style_label1.setScaledContents(True)
        def show_before_pic_in_label(self,i):
            show_list=self.show_list
            dir=show_list[i]
            pix=QPixmap(dir)
            self.ui.pic_before_label1.setPixmap(pix)
        # def preview_lerg_pics(self):
        #     style_pic=self.chosen_style_pic
        #     content_list=self.show_list
        #     filename=content_list[0].split("/")[-2]
        #     self.temp_file_name=self.project_base+'/temp/'+filename+'/'
        #     if os.path.exists(self.temp_file_name) is False:
        #         os.makedirs(self.temp_file_name)
        #     # index=0
        #     # for i in content_list:
        #     #     save_temp_dir=self.temp_file_name+str(index)+'.jpg'
        #     style_main(content_list,style_pic,self.temp_file_name)
        #         # main(pics_dir=[], style_dir='', save_dir='')
        def preview_style_pic_in_label(self):
            try:
                # self.ui.pic_after_label1.clear()
                # style_index=self.ui.pic_style_listWidget1.currentIndex().row()
                # style_pic=self.chosen_style_pic[style_index]
                # style_name=os.path.basename(style_pic).replace(".jpg","")
                # combobox_index=self.ui.multi_file_combobox.currentIndex()
                # current_content_file=self.multi_dir_project[combobox_index].split('/')[-1]
                content_index=self.ui.pic_before_listWidget1.currentIndex().row()
                content_pic=self.show_list[content_index]
                # content_fileName=os.path.basename(content_pic)
                # thread=My_gen_style_temp_thread()
                # temp_path=thread.temp_file_name
                # temp_path= self.project_base + '/temp/'
                # after_pic_dir=temp_path+style_name+'/'+style_name+current_content_file+'/'+content_fileName
                after_pic_dir=InfoNotifier.InfoNotifier.style_preview_pic_dir[content_index]
                # pix = QPixmap(after_pic_dir)
                # self.ui.pic_after_label1.setPixmap(pix)
                # lerp_value=self.ui.change_coe_horizontalSlider1
                self.save_path1 = os.path.dirname(content_pic)+ '/temp/lerp.jpg'
                self.value_slider=self.ui.change_coe_horizontalSlider1.value()
                img, _ = gen_lerp_ret.lerp_img(content_pic, after_pic_dir, float(self.value_slider))
                # gen_lerp_ret.write_img(img,save_path)
                cv2.imwrite(self.save_path1, img)
                self.ui.pic_after_label1.clear()
                item=QListWidgetItem()
                item.setIcon(QIcon(self.save_path1))
                item.setSizeHint(QSize(291,271))
                self.ui.pic_after_label1.setIconSize(QSize(291,271))
                self.ui.pic_after_label1.addItem(item)
                # time.sleep(0.5)
                # self.ui.pic_after_label1.clear()
                """
                print(save_path1)
                pix1 = QPixmap(save_path1)
                self.ui.pic_after_label1.setPixmap(pix1)
                # self.ui.pic_after_label1.clear()
    
                # QApplication.processEvents()
                """
            except BaseException as e:
                print(e)
                InfoNotifier.InfoNotifier.g_progress_info.append("请等待生成预览图片")
        def is_seamless_ornot(self):
            if self.ui.is_seamless_ornot_comboBox1.currentText()=="否":
                b_use_expanded=False
            else:
                b_use_expanded=True
            return  b_use_expanded
        def save_style(self):
            try:
                is_slemness=self.is_seamless_ornot()
                # if is_slemness is False
                InfoNotifier.InfoNotifier.g_progress_info.append("开始存储风格图片·········")
                base_dir=self.ui.project_base_dir.text()
                content_dir=base_dir
                # save_dir=base_dir+'/style_output/'
                file_list=self.multi_dir_project
                style_index=self.ui.pic_style_listWidget1.currentIndex().row()
                show_style_list=self.chosen_style_pic
                # chosen_style_pic=show_style_list[style_index]
                # style_name=os.path.basename(chosen_style_pic).split(".")[0]
                # save_dir+=style_name+'/'
                for file in file_list:
                    file_name=file.split("/")[-1]
                    # print(file_name)
                    pic_dir=file+'/style_transfer/'
                    # sub_save_dir=save_dir+file_name+'/'
                    img_list=glob.glob(pic_dir+'/'+'*.jpg')
                    print('原图列表:')
                    print(img_list)
                    print(show_style_list)
                    self.is_seamless=self.is_seamless_ornot()
                    if self.is_seamless is False:
                        self.save_style_thread=My_gen_style_thread()
                        # set_para(self,                chosen_style_pic='', show_list=[], project_base='', multi_files=[], lerp_value=50):
                        self.save_style_thread.set_para(show_style_list,img_list,base_dir,self.multi_dir_project,self.ui.change_coe_horizontalSlider1.value())
                        self.save_style_thread.start()
                    elif self.is_seamless is True:
                        self.sava_sceamless_style_style=My_gen_seamless_style_thread()
                        self.sava_sceamless_style_style.set_para(show_style_list,img_list,base_dir,self.multi_dir_project,self.ui.change_coe_horizontalSlider1.value())
                        # set_para(self, chosen_style_pic='', show_list=[], project_base='', multi_files=[], lerp_value=50):
                        self.sava_sceamless_style_style.start()
            # def  save_lerp(self):
            except BaseException as be:
                print(be)





        #tab2
        def open_txt(self):
            self.ui.pic_before_listWidget2.clear()
            file,filetype=QFileDialog.getOpenFileName(self, "选择文件", "./", "TXT文件(*.txt)")
            if len(file)==0:
                return
            else:
                self.txt_path=file
                # self.parent_dir_txt=[]
                InfoNotifier.InfoNotifier.g_progress_info.append(f"选择txt文件：{file}，点击生成图片进行格式转换，如已转换过，直接点击下拉框选择目录进行预览")
                if self.ui.project_base_dir=='':
                    InfoNotifier.InfoNotifier.g_progress_info.append("请选择根目录")
                    return

                # self.parent_dir_txt.clear()
                # self.show_dirs_in_combobox2()
                self.dirs_filter()
        def dirs_filter(self):
            # fw=open(self.txt_path,"r",encoding="utf-8-sig")
            #
            # self.checkcombobox_dir_array=[]
            # with open(".\data.json", 'r') as f:
            #     temp = json.loads(f.read())
            #     for file_path in fw:
            #         file_path=file_path.replace("\n","")
            #         parent_path=os.path.dirname(file_path)
            #         try:
            #             tmp=temp[parent_path]
            #             self.checkcombobox_dir_array.append(parent_path)
            #         except:
            #             pass
            #         parent_path.split("\\")
            #         if
            with open(".\data.json", 'r') as f:
                # print(f)
                import os
                #以下三个表都是相对路径
                #预览路径
                self.map_dir_omit = []

                # self.map_full_dir=[]
                #checkcombobox预览的路径和真实路径的映射表
                self.dir_dict={}
                self.pics_path_array=[]
                temp = json.loads(f.read())
                fw = open(self.txt_path, "r", encoding="utf-8-sig")
                for file in fw:
                    file_path = file.replace("\n", "").replace("\\", "/")
                    parent_path = os.path.dirname(file_path)
                    # print(parent_path)
                    file_split = parent_path.split("/")
                    if len(file_split) >= 3:
                        if file_split[-1] == 'baked' and file_split[-3] == 'maps':
                            self.pics_path_array.append(file_path)
                            if f'./{file_split[-2]}/{file_split[-1]}' not in self.map_dir_omit:
                                self.map_dir_omit.append(f'./{file_split[-2]}/{file_split[-1]}')
                                # self.map_full_dir.append(parent_path)
                                self.dir_dict[f'./{file_split[-2]}/{file_split[-1]}']=parent_path
                        if file_split[-1] == 'env_probe' and file_split[-3] == 'maps':
                            self.pics_path_array.append(file_path)
                            if f'./{file_split[-2]}/{file_split[-1]}' not in self.map_dir_omit:
                                self.map_dir_omit.append(f'./{file_split[-2]}/{file_split[-1]}')
                                # self.map_full_dir.append(parent_path)
                                self.dir_dict[f'./{file_split[-2]}/{file_split[-1]}']=parent_path
                        if file_split[-1] == 'procedural' and file_split[-2] == 'landscape':
                            self.pics_path_array.append(file_path)
                            if f'./{file_split[-3]}/{file_split[-2]}/{file_split[-1]}' not in self.map_dir_omit:
                                self.map_dir_omit.append(f'./{file_split[-3]}/{file_split[-2]}/{file_split[-1]}')
                                # self.map_full_dir.append(parent_path)
                                self.dir_dict[f'./{file_split[-3]}/{file_split[-2]}/{file_split[-1]}']=parent_path
                    # if file_split[-1]
                    if parent_path not in temp:
                        continue
                    self.pics_path_array.append(file_path)
                    if temp[parent_path] not in self.map_dir_omit:
                        self.map_dir_omit.append(temp[parent_path])
                        # self.map_full_dir.append(parent_path)
                        self.dir_dict[temp[parent_path]]=parent_path

                self.combocheckBox1.loadItems(self.map_dir_omit)
                self.combocheckBox1.setEnabled(True)
                print(self.map_dir_omit)
                # print(self.map_full_dir)
                print(self.dir_dict)
                print(self.pics_path_array)
        def gen_jpg_tga2(self):
            try:
                file=self.txt_path
                work_=self.ui.project_base_dir.text()+'/'
                work_=work_.replace("/","\\")
                #带转换的图片列表
                dds_list=self.pics_path_array
                # print(self.combocheckBox1.Selectlist())
                # SelectList=self.combocheckBox1.Selectlist()

                self.my_dds_thread=My_gen_dds_jpg_thread2()
                self.my_dds_thread.set_para(file,work_,dds_list)
                self.my_dds_thread.start()
                # time.sleep(1)
            except:
                InfoNotifier.InfoNotifier.g_progress_info.append("请先选择txt文件")
        def show_previewed_before_pic2(self,i):
            try:
                self.ui.pic_before_listWidget2.clear()
                self.ui.pic_before_label2.clear()
                InfoNotifier.InfoNotifier.style_preview_pic_dir2.clear()
                style_img_icon = []
                # dirs=self.parent_dir_txt[i]
                self.chosen_file_list=self.combocheckBox1.Selectlist()
                print(self.chosen_file_list)
                preview_list=[]
                for dire in self.chosen_file_list:
                    fw = open(self.txt_path, "r", encoding="utf-8-sig")
                    for f in fw:
                        f=f.replace("\n","").replace("\\","/")
                        path=self.dir_dict[dire]
                        if self.dir_dict[dire] in f:
                            preview_list.append(f)
                            break

                for i in range(len(preview_list)):
                    # dir=preview_list[i].replace(".dds",".jpg")
                    # dir=f'{self.ui.project_base_dir.text()}/{dir}'
                    # parent=os.path.dirname(dir)
                    # file_name=os.path.basename(dir)
                    # dir=f'{parent}/style_transfer/{file_name}'
                    # 实例化获取路径的类
                    get_path_class = PathUtils(_work=self.ui.project_base_dir.text(),dds_path=preview_list[i])
                    # self.get_path_class.work_=self.ui.project_base_dir.text()
                    # self.get_path_class.dds_path=preview_list[i]
                    dir=get_path_class.dds_to_jpg_path()
                    preview_list[i]=dir
                print(preview_list)

                # dirs = self.txt_path
                # work_=self.ui.project_base_dir.text()+'/'
                # real_parent_path=f'{work_}{dirs}'
                # preview_list=glob.glob(f'{real_parent_path}/style_transfer/*.jpg')
                # if len(preview_list)>self.preview_num:
                #     preview_list=preview_list[:self.preview_num]
                self.tmp_list=preview_list
                print(self.tmp_list)
                if len(self.tmp_list) == 0:
                    InfoNotifier.InfoNotifier.g_progress_info.append("不存在对应jpg格式图片，请先转换格式")
                    return
                for pic in self.tmp_list:
                    pix=QPixmap(pic)
                    icon=QIcon()
                    icon.addPixmap(pix)
                    style_img_icon.append(icon)
                index=0
                while index<len(self.tmp_list):
                    item=QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100, 100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.ui.pic_before_listWidget2.addItem(item)
                    index += 1
                iconsize=QSize(100,100)
                self.ui.pic_before_listWidget2.setIconSize(iconsize)
                InfoNotifier.InfoNotifier.g_progress_info.append("点击一张风格图片以进行预览")
                QApplication.processEvents()
            except BaseException as e:
                print(e)
        def previewed_before_clicked(self):
            # pre_list=self.tmp_list
            pic_index=self.ui.pic_before_listWidget2.currentIndex().row()
            self.show_before_pic_in_lable2(pic_index)
            # print("显示")
            try:
                self.preview_style_pic_in_label2()
            except:
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图片并进行预览")
        def show_before_pic_in_lable2(self,i):
            show_list=self.tmp_list
            dir=show_list[i]
            pix=QPixmap(dir)
            self.ui.pic_before_label2.setPixmap(pix)
            # print('111')
        def Choose_style_pics2(self):
            self.ui.pic_style_listWidget2.clear()
            # InfoNotifier.InfoNotifier.style_preview_pic_dir.clear()
            files, filetype = QFileDialog.getOpenFileNames(self, "选择文件", "./", "JPG文件(*.jpg);;PNG文件(*.png)")
            if len(files) == 0:
                style_img_icon = []
                for pic in self.Choosed_style_pics_list2:
                    pix = QPixmap(pic.replace("\n",""))
                    icon = QIcon()
                    icon.addPixmap(pix)
                    style_img_icon.append(icon)
                index = 0
                while index < len(self.Choosed_style_pics_list2):
                    item = QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100, 100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.pic_style_listWidget2.addItem(item)
                    index += 1
                iconsize = QSize(100, 100)
                self.ui.pic_style_listWidget2.setIconSize(iconsize)

                QApplication.processEvents()
            else:
                pic_dir = ""
                for file in files:
                    pic_dir += file + ';;'
                pic_dir = pic_dir[:-2]

                pic_dir=pic_dir.split(";;")
                for i in pic_dir:
                    self.Choosed_style_pics_list2.append(i)
                print(self.Choosed_style_pics_list2)

                style_img_icon=[]
                for pic in self.Choosed_style_pics_list2:
                    pix = QPixmap(pic.replace("\n",""))
                    icon = QIcon()
                    icon.addPixmap(pix)
                    style_img_icon.append(icon)
                index = 0
                while index < len(self.Choosed_style_pics_list2):
                    item = QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100,100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.pic_style_listWidget2.addItem(item)
                    index += 1
                iconsize = QSize(100,100)
                self.ui.pic_style_listWidget2.setIconSize(iconsize)

                QApplication.processEvents()
        def pic_style_clicked2(self):
            try:
                # self.ui.change_coe_horizontalSlider1.setEnabled(False)
                InfoNotifier.InfoNotifier.style_preview_pic_dir2.clear()
                if len(self.Choosed_style_pics_list2) == 0:
                    return
                pic_style_index = self.ui.pic_style_listWidget2.currentIndex().row()
                self.chosen_style_pic2=self.Choosed_style_pics_list2[pic_style_index]
                self.show_style_pic_in_label2(pic_style_index)
                self.make_temp_previewed()
            except BaseException as e:
                print(e)

            # self.preview_lerg_pics()
            # InfoNotifier.InfoNotifier.g_progress_info.append("准备生成风格迁移后的预览图...")
            # try:
            #     self.gen_preview_pic = My_gen_style_temp_thread()
            #     # set_para(self,chosen_style_pic='',show_list=[],project_base='')
            #     self.gen_preview_pic.set_para(self.chosen_style_pic, self.show_list, self.project_base)
            #     self.gen_preview_pic.start()
            # except:
            #     InfoNotifier.InfoNotifier.g_progress_info.append("请选择一个原图目录生成风格图片")
            # self.ui.change_coe_horizontalSlider1.setEnabled(True)
        def make_temp_previewed(self):
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("等待生成预览图")
                base = self.ui.project_base_dir.text()
                preview_file_list = self.tmp_list
                #self.tmp_list:f'{parent}/style_transfer/{file_name}'

                # tem_file = f'{os.path.dirname(os.path.dirname(preview_file_list[0]))}/style_transfer/temp/'
                # print(tem_file)
                # if os.path.exists(tem_file) is False:
                #     os.makedirs(tem_file)

                if len(preview_file_list) == 0:
                    return
                self.mythread_temp=My_gen_style_temp_thread2()
                self.mythread_temp.set_para(preview_file_list, self.chosen_style_pic2, self.ui.project_base_dir.text())
                self.mythread_temp.start()
            except BaseException as be:
                print(be)
                InfoNotifier.InfoNotifier.g_progress_info.append("先加入原图")
            # InfoNotifier.InfoNotifier.g_progress_info.append("预览图生成完成，点击")
        def show_style_pic_in_label2(self,i=0):

            # print(i)
            show_list=self.Choosed_style_pics_list2
            dir=show_list[i]
            self.chosen_style_pic2=dir
            pix=QPixmap(dir)

            # pix=pix.scaled(200, 200)
            # pix=pix.fromImage(pix)
            self.ui.pic_style_label2.setPixmap(pix)
            # self.ui.pic_style_label1.setFixedSize(QSize(250,250))
            self.ui.pic_style_label2.setScaledContents(True)
        def preview_style_pic_in_label2(self):
            try:

                content_index = self.ui.pic_before_listWidget2.currentIndex().row()
                content_pic = self.tmp_list[content_index]
                if self.chosen_style_pic2 != '':
                    s_name=os.path.basename(self.chosen_style_pic2).split('.')[0]

                    after_pic_dir=os.path.dirname(content_pic)+'/temp/'+s_name+'/'+os.path.basename(content_pic)

                # after_pic_dir = InfoNotifier.InfoNotifier.style_preview_pic_dir2[content_index]

                save_path2 = os.path.dirname(content_pic) + '/temp/lerp.jpg'
                self.value_slider = self.ui.change_coe_horizontalSlider2.value()
                img, _ = gen_lerp_ret.lerp_img(content_pic, after_pic_dir, float(self.value_slider))
                # cv2.imwrite(save_path2, img)
                gen_lerp_ret.write_img(img,save_path2)
                self.ui.pic_after_label2.clear()
                item = QListWidgetItem()
                item.setIcon(QIcon(save_path2))
                item.setSizeHint(QSize(291, 271))
                self.ui.pic_after_label2.setIconSize(QSize(291, 271))
                self.ui.pic_after_label2.addItem(item)

            except BaseException as e:
                print('preview_style_pic_in_label2',e)
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图或等待生成预览图片")
        def is_seamless_ornot2(self):
            if self.ui.is_seamless_ornot_comboBox2.currentText() == "否":
                b_use_expanded = False
            else:
                b_use_expanded = True
            return b_use_expanded
        def save_style2(self):
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("开始保存··············")
                txt_file=self.txt_path
                work_=self.ui.project_base_dir.text()
                lerp_value=self.ui.change_coe_horizontalSlider2.value()
                seamless=self.is_seamless_ornot2()
                chosen_style_pic=self.chosen_style_pic2
                #被勾选的目录列表
                chosen_content_file_list=self.combocheckBox1.Selectlist()

                if seamless is False:
                    self.mythread3=My_gen_style_thread2()
                    self.mythread3.set_para(txt_file,work_,lerp_value,chosen_style_pic,chosen_content_file_list,self.dir_dict)
                    self.mythread3.start()
                else:
                    self.mythread3=My_gen_seamless_thread2()
                    self.mythread3.set_para(txt_file,work_,lerp_value,chosen_style_pic,chosen_content_file_list,self.dir_dict)
                    self.mythread3.start()

                # set_para(self, txt_path='', work_='', lerg_value=50, chosen_style_pic=''):
            except BaseException as b:
                print(b)









        #tab3
        # self.chosen_style_pic3 = ''
        # self.chosen_content_list3 = []
        def choose_pics3(self):
            if self.ui.project_base_dir.text()=='':
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择根目录")
                return
            files, filetype = QFileDialog.getOpenFileNames(self, "选择文件", self.ui.project_base_dir.text(), "DDS文件(*.dds)")
            if len(files)==0:
                return
            else:
                for file in files:
                    self.chosen_content_list3.append(file)
            InfoNotifier.InfoNotifier.g_progress_info.append(f"已选中{len(self.chosen_content_list3)}张图片")
        def gen_jpg_tga3(self):
            self.base=self.ui.project_base_dir.text()
            self.mythread_gen=My_gen_dds_jpg_thread3()
            self.mythread_gen.set_para(self.chosen_content_list3)
            self.mythread_gen.start()
            # self.ui.choose_pics_button3.setEnabled(False)
        def preview_before_inWidget3(self):
            self.ui.pic_before_listWidget3.clear()
            InfoNotifier.InfoNotifier.style_preview_pic_dir3.clear()
            style_img_icon = []
            show_before_list=[]

            cnt=3
            if len(self.chosen_content_list3)<3:
                cnt=len(self.chosen_content_list3)
            for i in range(cnt):
                dds_path=self.chosen_content_list3[i]
                file_name = os.path.basename(dds_path)
                parent_path = os.path.dirname(dds_path)
                style_transfer_path = parent_path + "/style_transfer/"
                ipg_path = style_transfer_path + file_name.replace(".dds", ".jpg")
                show_before_list.append(ipg_path.replace("\n",""))
            for pic in show_before_list:
                print(pic)
                pix = QPixmap(pic)
                icon = QIcon()
                icon.addPixmap(pix)
                style_img_icon.append(icon)
            index = 0
            while index < cnt:
                try:
                    item = QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100, 100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.ui.pic_before_listWidget3.addItem(item)
                    index += 1
                except BaseException as be:
                    print(be)
            self.tmp_before_list3 = show_before_list
            iconsize = QSize(100, 100)
            self.ui.pic_before_listWidget3.setIconSize(iconsize)
            QApplication.processEvents()
        def previewed_before_clicked3(self):
            # pre_list=self.tmp_list
            pic_index = self.ui.pic_before_listWidget3.currentIndex().row()
            self.show_before_pic_in_lable3(pic_index)
            # print("显示")
            try:
                self.preview_after_pic_in_label3()
            except:
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图片并进行预览")
        def show_before_pic_in_lable3(self,i):
            show_list = self.tmp_before_list3
            dir = show_list[i]
            pix = QPixmap(dir)
            self.ui.pic_before_label3.setPixmap(pix)
        def Choose_style_pics3(self):
            self.ui.pic_style_listWidget3.clear()
            InfoNotifier.InfoNotifier.style_preview_pic_dir3.clear()
            files, filetype = QFileDialog.getOpenFileNames(self, "选择文件", "./", "JPG文件(*.jpg);;PNG文件(*.png)")
            if len(files) == 0:
                style_img_icon = []
                for pic in self.Choosed_style_pics_list3:
                    pix = QPixmap(pic.replace("\n", ""))
                    icon = QIcon()
                    icon.addPixmap(pix)
                    style_img_icon.append(icon)
                index = 0
                while index < len(self.Choosed_style_pics_list3):
                    item = QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100, 100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.pic_style_listWidget3.addItem(item)
                    index += 1
                iconsize = QSize(100, 100)
                self.ui.pic_style_listWidget3.setIconSize(iconsize)

                QApplication.processEvents()
            else:
                pic_dir = ""
                for file in files:
                    pic_dir += file + ';;'
                pic_dir = pic_dir[:-2]

                pic_dir = pic_dir.split(";;")
                for i in pic_dir:
                    self.Choosed_style_pics_list3.append(i)
                print(self.Choosed_style_pics_list3)

                style_img_icon = []
                for pic in self.Choosed_style_pics_list3:
                    pix = QPixmap(pic.replace("\n", ""))
                    icon = QIcon()
                    icon.addPixmap(pix)
                    style_img_icon.append(icon)
                index = 0
                while index < len(self.Choosed_style_pics_list3):
                    item = QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100, 100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.pic_style_listWidget3.addItem(item)
                    index += 1
                iconsize = QSize(100, 100)
                self.ui.pic_style_listWidget3.setIconSize(iconsize)

                QApplication.processEvents()
        def pic_style_clicked3(self):
            # self.ui.change_coe_horizontalSlider1.setEnabled(False)
            InfoNotifier.InfoNotifier.style_preview_pic_dir3.clear()
            if len(self.Choosed_style_pics_list3) == 0:
                return
            pic_style_index = self.ui.pic_style_listWidget3.currentIndex().row()
            self.show_style_pic_in_label3(pic_style_index)
            self.make_temp_previewed3()
        def show_style_pic_in_label3(self, i):
            # print(i)
            show_list = self.Choosed_style_pics_list3
            dir = show_list[i]
            self.chosen_style_pic3 = dir
            pix = QPixmap(dir)

            # pix=pix.scaled(200, 200)
            # pix=pix.fromImage(pix)
            self.ui.pic_style_label3.setPixmap(pix)
            # self.ui.pic_style_label1.setFixedSize(QSize(250,250))
            self.ui.pic_style_label3.setScaledContents(True)
        def make_temp_previewed3(self):
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("等待生成预览图")
                base = self.ui.project_base_dir.text()
                if base=='':
                    InfoNotifier.InfoNotifier.g_progress_info.append("请创建一个工程目录")
                else:


                    preview_file_list = self.tmp_before_list3

                    if len(preview_file_list) == 0:
                        return
                    tmp_file=preview_file_list[0]
                    parent_tmp=os.path.dirname(tmp_file)
                    tem_file = parent_tmp+ '/temp/'
                    self.tem_file=tem_file
                    self.mythread_temp3 = My_gen_style_temp_thread3()
                    self.mythread_temp3.set_para(preview_file_list, self.chosen_style_pic3, tem_file)
                    self.mythread_temp3.start()
            except BaseException as be:
                print(be)
                InfoNotifier.InfoNotifier.g_progress_info.append("先加入原图")
            # InfoNotifier.InfoNotifier.g_progress_info.append("预览图生成完成，点击")
        def preview_after_pic_in_label3(self):
            try:

                content_index = self.ui.pic_before_listWidget3.currentIndex().row()
                content_pic = self.tmp_before_list3[content_index]

                after_pic_dir = InfoNotifier.InfoNotifier.style_preview_pic_dir3[content_index]

                self.save_path1 = self.tem_file + 'lerp.jpg'
                self.value_slider = self.ui.change_coe_horizontalSlider3.value()
                img, _ = gen_lerp_ret.lerp_img(content_pic, after_pic_dir, float(self.value_slider))

                cv2.imwrite(self.save_path1, img)
                self.ui.pic_after_label3.clear()
                item = QListWidgetItem()
                item.setIcon(QIcon(self.save_path1))
                item.setSizeHint(QSize(291, 271))
                self.ui.pic_after_label3.setIconSize(QSize(291, 271))
                self.ui.pic_after_label3.addItem(item)

            except BaseException as e:
                print(e)
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图片，再等待生成预览图片")
        def is_seamless_ornot3(self):
            if self.ui.is_seamless_ornot_comboBox3.currentText()=="否":
                return False
            return True
        def save_all3(self):
            style_path=self.chosen_style_pic3
            content_list=self.chosen_content_list3
            lerp_value=self.ui.change_coe_horizontalSlider3.value()
            seamless=self.is_seamless_ornot3()
            if seamless is False:
                self.mythread_save3=My_gen_style_thread3()
                self.mythread_save3.set_para(content_list,style_path,lerp_value)
                self.mythread_save3.start()
            else:
                self.mythread_save3=My_gen_seamless_style_thread3()
                self.mythread_save3.set_para(content_list,style_path,lerp_value)
                self.mythread_save3.start()


    import  sys
    app=QApplication(sys.argv)
    window=MainWindow()
#     comboBox1 = ComboCheckBox(window.ui.txt)
#     comboBox1.setGeometry(QtCore.QRect(30, 160, 321, 41))
#     comboBox1.setMinimumSize(QtCore.QSize(100, 20))
#     comboBox1.setStyleSheet("background-color: rgb(90, 90, 90);\n"
# "color: rgb(212, 212, 212);")
#     items = ["\\terraintexture\grass", "\稻香村\\baked\\", "\maps_source\\texture\\"]
#     comboBox1.loadItems(items)
    window.show()
    sys.exit(app.exec_())