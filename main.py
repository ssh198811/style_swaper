from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QMessageBox, QListWidgetItem, QToolTip
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QUrl, QPoint,QSize,QRect
from PyQt5 import QtGui
from combocheckbox import ComboCheckBox
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap, QFont
import Ui_test519
import os
import time
import InfoNotifier
from PIL import Image
import cv2
import glob
import json
import gen_lerp_ret
from  button_state import GlobalConfig
from path_util import PathUtils, PathTemp
from sub_threads import tab_multi_files_thread,tab_specific_pics_thread,tab_txt_thread
from gen_style_map import gen_style_map_file
import shutil
import stat
import random
import hashlib

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


class MyDelFilesThread(QThread):
    signal_ = pyqtSignal()

    def __init__(self):
        super(MyDelFilesThread, self).__init__()
        self.path = ''

    def set_para(self, path=''):
        self.path = path

    # 删除文件---delete lerp,seamless and temp files
    def readonly_handler(self, func, path, exc):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def del_temp_dir(self, path):
        if os.path.isdir(path):
            if 'lerp_output' in path or 'temp' in path or 'seamless_output' in path:
                try:
                    shutil.rmtree(path, onerror=self.readonly_handler)
                except BaseException as e:
                    print('含只读文件')
                    print(e)
                    os.chmod(path, stat.S_IWRITE)
                    os.remove(path)
                    print('已强制删除')
            else:
                for item in os.listdir(path):
                    itempath = os.path.join(path, item)
                    self.del_temp_dir(itempath)

    def run(self):
        self.del_temp_dir(self.path)
        self.signal_.emit()
class MyDeepDelThread(QThread):
    signal_=pyqtSignal()
    def __init__(self):
        super(MyDeepDelThread, self).__init__()
        self.path = ''

    def set_para(self, path=''):
        self.path = path

    def readonly_handler(self, func, path, exc):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    # 删除文件--delete style_output and dds to jpg,tga output
    def del_deep(self, path):
        if path == '':
            InfoNotifier.InfoNotifier.g_progress_info.append("没有选择工作目录！")
            return
        path = f'{path}/data/style_transfer/'
        self.del_deep_temp_dir(path)
        InfoNotifier.InfoNotifier.g_progress_info.append("已清空")

    def del_deep_temp_dir(self, path):
        if os.path.isdir(path) and 'style_output' in path and 'style_transfer' in path:
            try:
                shutil.rmtree(path, onerror=self.readonly_handler)
            except BaseException as be:
                print('存在只读文件')
                print(be)
                os.chmod(path, stat.S_IWRITE)
                os.remove(path)
                print('已强制删除')
        if os.path.isdir(path) and 'dds_output' not in path and 'style_transfer' in path:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    try:
                        os.remove(item_path)
                    except BaseException as be:
                        print('存在只读文件')
                        print(be)
                        os.chmod(item_path, stat.S_IWRITE)
                        os.remove(item_path)
                        print('已强制删除')
                else:
                    self.del_deep_temp_dir(item_path)
    def run(self):
        self.del_deep(self.path)
        self.signal_.emit()


if __name__ == '__main__':

    class MainWindow(QMainWindow):
        def __init__(self):

            super(MainWindow, self).__init__()
            self.ui = Ui_test519.Ui_MainWindow()
            self.ui.setupUi(self)

            # txt读取部分复选框
            self.combocheckBox1 = ComboCheckBox(self.ui.txt)
            self.combocheckBox1.setGeometry(QtCore.QRect(30, 160, 321, 41))
            self.combocheckBox1.setMinimumSize(QtCore.QSize(100, 20))
            self.combocheckBox1.setStyleSheet("background-color: rgb(90, 90, 90);\n"
                                    "color: rgb(0, 0, 0);")
            self.combocheckBox1.setEnabled(False)

            # 多目录读取部分复选框
            self.combocheckBox2 = ComboCheckBox(self.ui.t1)
            self.combocheckBox2.setGeometry(QtCore.QRect(30, 130, 311, 41))
            self.combocheckBox2.setMinimumSize(QtCore.QSize(100, 20))
            self.combocheckBox2.setStyleSheet("background-color: rgb(90, 90, 90);\n"
                                              "color: rgb(0, 0, 0);")
            self.combocheckBox2.setEnabled(False)



            # 预览图片数
            self.preview_num = 3

            # 预读取最后一次使用的根目录
            try:
                with open("./base_dir_log.txt", 'r') as f:
                    lines = f.readlines()
                    last_line = lines[-1].replace("\n", "")
                    self.ui.project_base_dir.setText(last_line)
            except BaseException as e:
                print(e)
                pass

            self.Thread = Mythread()
            self.Thread._signal_progress_info.connect(self.update_progress_info)
            self.Thread._signal_button_ctrl.connect(self.update_button_state)
            self.Thread.start()

            self.ui.pic_before_listWidget1.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_style_listWidget1.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_style_listWidget3.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_before_listWidget3.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_before_listWidget2.setFlow(QtWidgets.QListView.LeftToRight)
            self.ui.pic_style_listWidget2.setFlow(QtWidgets.QListView.LeftToRight)

            self.project_cwd = ''
            self.project_base = ''
            # 原图目录列表
            self.multi_dir_project = []
            # 目录相对路径
            self.multi_relative_dir = []
            # 选择风格图数组
            self.Choosed_style_pics_list = []
            self.Choosed_style_pics_list2 = []
            self.Choosed_style_pics_list3 = []
            # 点击选中风格图路径
            self.chosen_style_pic3 = ''
            self.chosen_style_pic2 = ''
            # 选中复选框
            self.chosen_file_list1 = []
            # 生成图片点击数
            self.combocheckbox2_button_clicked = 0

            # 多选图片导入tab中选中的原图数组
            self.chosen_content_list3 = []
            # 存放缩写路径和相对路径字典
            self.files_dict = {}
            # 设置第三方导出工具路径
            self.exe_dir = os.getcwd() + "\\dds_to_jpg/dds_to_jpg.exe"

            self.ui.make_project_dir_button.clicked.connect(self.make_project_dir)
            self.ui.choose_pic_multi_file_dir_button1.clicked.connect(self.choose_multi_dir_tab_files)
            self.ui.preview_content1.clicked.connect(self.show_previewed_before_pic)
            self.ui.Preview_button.clicked.connect(self.gen_dds_jpg)
            self.ui.pic_before_listWidget1.clicked.connect(self.pic_before_clicked)
            self.ui.pic_style_listWidget1.clicked.connect(self.pic_style_clicked)
            self.ui.pic_before_listWidget2.clicked.connect(self.previewed_before_clicked)
            self.ui.choose_pic_style_button1.clicked.connect(self.choose_style_pics_tab_files)
            self.ui.change_coe_horizontalSlider1.valueChanged.connect(self.preview_style_pic_in_label)
            self.ui.change_coe_horizontalSlider2.valueChanged.connect(self.preview_after_pic_in_label_tab_txt)
            self.ui.savePic_button1.clicked.connect(self.save_style)
            self.ui.choose_pic_txt_button2.clicked.connect(self.open_txt)
            self.ui.gen_jpg_tga_button2.clicked.connect(self.gen_jpg_tga_tab_txt)
            self.ui.preview_content2.clicked.connect(self.show_previewed_before_pic_tab_txt)
            self.ui.choose_pic_style_button2.clicked.connect(self.choose_style_pics_tab_txt)
            self.ui.pic_style_listWidget2.clicked.connect(self.pic_style_clicked_tab_txt)
            self.ui.savePic_button2.clicked.connect(self.save_style_tab_txt)
            self.ui.pre_bef_button3.clicked.connect(self.preview_before_in_widget_tab_pics)
            self.ui.choose_pics_button3.clicked.connect(self.choose_multi_pics)
            self.ui.pushButton.clicked.connect(self.gen_jpg_tga_tab_pics)
            self.ui.pic_before_listWidget3.clicked.connect(self.previewed_before_clicked_tab_pics)
            self.ui.choose_pic_style_button2_2.clicked.connect(self.choose_style_pics_tab_pics)
            self.ui.pic_style_listWidget3.clicked.connect(self.pic_style_clicked_tab_pics)
            self.ui.change_coe_horizontalSlider3.valueChanged.connect(self.preview_after_pic_in_label_tab_pics)
            self.ui.savePic_button3.clicked.connect(self.save_all_tab_pics)
            self.ui.reset_button.clicked.connect(self.del_data)
            self.ui.delete_files_button.clicked.connect(self.del_deep)

        # 更新日志
        def update_progress_info(self):
            try:
                for info in InfoNotifier.InfoNotifier.g_progress_info:
                    self.ui.progress_Info.append(info)
                InfoNotifier.InfoNotifier.g_progress_info.clear()
            except BaseException as e:
                print(e)

        def ui_update_progress_info(self, info=""):
            self.ui.progress_Info.append(info)

        # 控制控件
        def update_button_state(self):
            if GlobalConfig.b_sync_block_op_in_progress is True:
                # 保存图片时
                self.ui.make_project_dir_button.setEnabled(False)
                self.ui.project_base_dir.setEnabled(False)
                self.ui.choose_pic_multi_file_dir_button1.setEnabled(False)
                self.ui.Preview_button.setEnabled(False)
                self.ui.choose_pic_style_button1.setEnabled(False)
                self.ui.savePic_button1.setEnabled(False)
                self.ui.choose_pic_txt_button2.setEnabled(False)
                self.ui.gen_jpg_tga_button2.setEnabled(False)
                self.ui.choose_pic_style_button2.setEnabled(False)
                self.ui.savePic_button2.setEnabled(False)
                self.ui.choose_pics_button3.setEnabled(False)
                self.ui.pushButton.setEnabled(False)
                self.ui.choose_pic_style_button2_2.setEnabled(False)
                self.ui.savePic_button3.setEnabled(False)

            if GlobalConfig.b_sync_block_op_in_progress is False:

                self.ui.make_project_dir_button.setEnabled(True)
                self.ui.make_project_dir_button.setEnabled(True)
                self.ui.project_base_dir.setEnabled(True)
                self.ui.choose_pic_multi_file_dir_button1.setEnabled(True)
                self.ui.Preview_button.setEnabled(True)
                self.ui.choose_pic_style_button1.setEnabled(True)
                self.ui.savePic_button1.setEnabled(True)
                self.ui.choose_pic_txt_button2.setEnabled(True)
                self.ui.gen_jpg_tga_button2.setEnabled(True)
                self.ui.choose_pic_style_button2.setEnabled(True)
                self.ui.savePic_button2.setEnabled(True)
                self.ui.choose_pics_button3.setEnabled(True)
                self.ui.pushButton.setEnabled(True)
                self.ui.choose_pic_style_button2_2.setEnabled(True)
                self.ui.savePic_button3.setEnabled(True)
            if GlobalConfig.b_sync_block_in_thread_temp is True:
                # 生成预览图时
                self.ui.pic_style_listWidget1.setEnabled(False)
                self.ui.pic_style_listWidget2.setEnabled(False)
                self.ui.pic_style_listWidget3.setEnabled(False)
            if GlobalConfig.b_sync_block_in_thread_temp is False:
                self.ui.pic_style_listWidget1.setEnabled(True)
                self.ui.pic_style_listWidget2.setEnabled(True)
                self.ui.pic_style_listWidget3.setEnabled(True)

        # 清除数据
        def del_data(self):
            # self.ui.project_base_dir.clear()
            self.combocheckBox1.clearEditText()
            self.ui.pic_before_label2.clear()
            self.ui.pic_before_listWidget2.clear()
            self.ui.pic_style_label2.clear()
            self.ui.pic_style_listWidget2.clear()
            self.ui.pic_after_label2.clear()
            self.ui.progress_Info.clear()
            self.combocheckBox2.clearEditText()
            self.ui.pic_before_label1.clear()
            self.ui.pic_before_listWidget1.clear()
            self.ui.pic_style_label1.clear()
            self.ui.pic_style_listWidget1.clear()
            self.ui.pic_after_label1.clear()
            self.ui.pic_before_label3.clear()
            self.ui.pic_before_listWidget3.clear()
            self.ui.pic_style_label3.clear()
            self.ui.pic_style_listWidget3.clear()
            self.ui.pic_after_label3.clear()
            try:
                # self.del_temp_dir(self.ui.project_base_dir.text())
                self.del_thread = MyDelFilesThread()
                self.del_thread.set_para(self.ui.project_base_dir.text())
                self.del_thread.run()
                InfoNotifier.InfoNotifier.g_progress_info.append("已恢复初始界面")
            except BaseException as be:
                print(be)

            self.chosen_content_list3 = []
            # 原图目录列表
            self.multi_dir_project = []
            # 目录相对路径
            self.multi_relative_dir = []
            # 选择风格图数组
            self.Choosed_style_pics_list = []
            self.Choosed_style_pics_list2 = []
            self.Choosed_style_pics_list3 = []
            # 点击选中风格图路径
            self.chosen_style_pic3 = ''
            self.chosen_style_pic2 = ''
            # 选中复选框
            self.chosen_file_list1 = []
            # 生成图片点击数
            self.combocheckbox2_button_clicked = 0

            # 多选图片导入tab中选中的原图数组
            self.chosen_content_list3 = []
            # 存放缩写路径和相对路径字典
            self.files_dict = {}

        # deep delete
        def del_deep(self):
            self.my_deep_del = MyDeepDelThread()
            self.my_deep_del.set_para(self.ui.project_base_dir.text())
            self.my_deep_del.start()


        # 选根目录
        def make_project_dir(self):
            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
            if len(directory) == 0:
                return
            self.ui.project_base_dir.setText(directory)
            with open('./base_dir_log.txt', 'w')as f:
                f.write(f"{directory}\n")

        # 查看图片通道数
        def get_channel_num(self, img_path=''):
            if img_path != '':
                img = Image.open(img_path)
                return len(img.split())

        # tab_files
        # 多选文件导入
        def choose_multi_dir_tab_files(self):
            # 选择导入目录
            self.project_base = self.ui.project_base_dir.text()

            if self.ui.project_base_dir.text() == '':
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择根目录")
                return

            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", self.ui.project_base_dir.text())
            if len(directory) == 0:
                return
            directory_temp=directory.split('/')
            if directory_temp[-2]+'/'+directory_temp[-1] not in self.multi_dir_project:
                rela_path = directory.replace(self.ui.project_base_dir.text()+'/', "")
                self.files_dict[directory_temp[-2]+'/'+directory_temp[-1]] = rela_path
                self.multi_relative_dir.append(directory.replace(self.ui.project_base_dir.text()+'/', ""))
                self.multi_dir_project.append(directory_temp[-2]+'/'+directory_temp[-1])
                print(self.multi_dir_project)

            print(self.multi_relative_dir)
            InfoNotifier.InfoNotifier.g_progress_info.append("继续加入目录，如选择完毕则点击生成图片进行预览")

        def choose_style_pics_tab_files(self):
            # 选择风格图
            self.ui.pic_style_listWidget1.clear()
            # InfoNotifier.InfoNotifier.style_preview_pic_dir.clear()
            files, filetype = QFileDialog.getOpenFileNames(self, "选择文件", "./", "JPG文件(*.jpg)")
            #
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
                    #如果图片不是三通道，跳过
                    if self.get_channel_num(file) != 3:
                        InfoNotifier.InfoNotifier.g_progress_info.append(file+' 为四通道图片，请选择三通道jpg格式图片！')
                    elif file in self.Choosed_style_pics_list:
                        InfoNotifier.InfoNotifier.g_progress_info.append(file+' 已选过')
                    else:
                        pic_dir += file + ';;'
                # print(pic_dir)
                if pic_dir == '':
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
                    return

                pic_dir = pic_dir[:-2]

                pic_dir = pic_dir.split(";;")
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
                    item.setSizeHint(QSize(100, 100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.ui.pic_style_listWidget1.addItem(item)
                    index += 1
                iconsize = QSize(100,100)
                self.ui.pic_style_listWidget1.setIconSize(iconsize)

                QApplication.processEvents()

        def gen_dds_jpg(self):
            # 生成jpg,tga格式图片
            self.combocheckbox2_button_clicked += 1
            self.combocheckBox2.loadItems(self.multi_dir_project)
            if self.combocheckbox2_button_clicked > 1:
                self.combocheckBox2.items = self.combocheckBox2.items[self.combocheckbox2_button_clicked-1:]
                print(self.combocheckBox2.items)
            if self.ui.project_base_dir.text() == "":
                InfoNotifier.InfoNotifier.g_progress_info.append("请先为工程创建根目录")
            else:
                if len(self.multi_relative_dir)==0:
                    self.ui.progress_Info.append("请先勾选待操作文件目录")
                else:
                    self.ui.progress_Info.append("开始转换dds贴图为jpg,tga格式")
                    QApplication.processEvents()
                    self.changethread = tab_multi_files_thread.MyGenDdsJpgThreadTabFiles()
                    self.changethread.set_para(self.ui.project_base_dir.text(), self.exe_dir, self.multi_relative_dir)
                    self.changethread.start()
                    # self.ui.choose_pic_multi_file_dir_button1.setEnabled(False)
            self.combocheckBox2.setEnabled(True)

        def show_previewed_before_pic(self):
            # 预览原图
            try:
                self.ui.pic_before_listWidget1.clear()
                style_img_icon = []
                self.chosen_file_list1 = self.combocheckBox2.Selectlist()
                print(self.chosen_file_list1)
                previem_list = []
                for dire in self.chosen_file_list1:
                    tmp = glob.glob(self.ui.project_base_dir.text()+'/'+self.files_dict[dire]+'/*.dds')[0]
                    tmp = self.files_dict[dire]+'/'+os.path.basename(tmp)
                    get_path = PathUtils(_work=self.ui.project_base_dir.text(), dds_path=tmp)

                    previem_list.append(get_path.dds_to_jpg_path())
                self.show_list = previem_list
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
            except BaseException as e:
                print(e)
                InfoNotifier.InfoNotifier.g_progress_info.append("先点击生成图片")

        def pic_before_clicked(self):
            """

            点击原图事件:
            1.显示原图；2.显示风格转化后的图

            """
            if len(self.show_list) == 0:
                return
            pic_before_index=self.ui.pic_before_listWidget1.currentIndex().row()
            self.show_before_pic_in_label(pic_before_index)
            try:
                self.preview_style_pic_in_label()
            except BaseException as e:
                print(e)
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图片并进行预览")

        def pic_style_clicked(self):
            """

            点击风格图事件:
            1.预览风格图；
            2.生成预览的风格转化后的图

            """
            try:
                if len(self.Choosed_style_pics_list)==0:
                    return
                pic_style_index = self.ui.pic_style_listWidget1.currentIndex().row()
                self.show_style_pic_in_label(pic_style_index)
                InfoNotifier.InfoNotifier.g_progress_info.append("准备生成风格迁移后的预览图...")
                self.gen_preview_pic = tab_multi_files_thread.MyGenStyleTempThreadTabFiles()
                self.gen_preview_pic.set_para(self.chosen_style_pic, self.show_list, self.ui.project_base_dir.text())
                self.gen_preview_pic.start()

                self.preview_style_pic_in_label()

            except BaseException as e:
                print(e)
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一个原图目录生成风格图片")

        def show_style_pic_in_label(self, i):
            # 预览风格图
            show_list = self.Choosed_style_pics_list
            dir = show_list[i]
            self.chosen_style_pic = dir
            pix = QPixmap(dir)
            self.ui.pic_style_label1.setPixmap(pix)
            self.ui.pic_style_label1.setScaledContents(True)

        def show_before_pic_in_label(self, i):
            # 预览原图
            show_list = self.show_list
            dirs = show_list[i]
            pix = QPixmap(dirs)
            self.ui.pic_before_label1.setPixmap(pix)

        def preview_style_pic_in_label(self):
            # 预览风格后图
            try:
                content_index = self.ui.pic_before_listWidget1.currentIndex().row()
                content_pic = self.show_list[content_index]
                get_path = PathTemp(jpg_path_=content_pic, style_path_=self.chosen_style_pic)
                s_name = os.path.basename(self.chosen_style_pic).split('.')[0]
                # after_pic_dir = os.path.dirname(content_pic) + '/temp/' + s_name + '/' + os.path.basename(
                #         content_pic)
                # self.save_path1 = os.path.dirname(content_pic) + '/temp/lerp.jpg'
                self.value_slider = self.ui.change_coe_horizontalSlider1.value()
                after_pic_dir = get_path.get_temp_after_jpg_path()
                self.save_path1 = get_path.get_temp_lerp_path()
                img, _ = gen_lerp_ret.lerp_img(content_pic, after_pic_dir, float(self.value_slider))
                cv2.imwrite(self.save_path1, img)
                self.ui.pic_after_label1.clear()
                item = QListWidgetItem()
                item.setIcon(QIcon(self.save_path1))
                item.setSizeHint(QSize(291, 271))
                self.ui.pic_after_label1.setIconSize(QSize(291, 271))
                self.ui.pic_after_label1.addItem(item)
            except BaseException as e:
                print(e)
                InfoNotifier.InfoNotifier.g_progress_info.append("请等待生成预览图片")

        def is_seamless_ornot(self):
            # 是否生成无缝贴图
            if self.ui.is_seamless_ornot_comboBox1.currentText() == "否":
                b_use_expanded = False
            else:
                b_use_expanded = True
            return b_use_expanded

        def save_style(self):
            # 保存
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("开始存储风格图片·········")
                # 勾选目录
                chosen_content_file_list = self.combocheckBox2.Selectlist()
                # 映射表
                file_dict = self.files_dict

                lerp_value = self.ui.change_coe_horizontalSlider1.value()

                base = self.ui.project_base_dir.text()

                style_path=self.chosen_style_pic

                self.is_seamless = self.is_seamless_ornot()
                if self.is_seamless is False:
                    self.save_style_thread = tab_multi_files_thread.MyGenStyleThreadTabFiles()
                    self.save_style_thread.set_para(style_path, chosen_content_file_list, base, file_dict, lerp_value)
                    self.save_style_thread.start()
                elif self.is_seamless is True:
                    self.sava_sceamless_style_style = tab_multi_files_thread.MyGenSeamlessStyleThreadTabFiles()
                    self.sava_sceamless_style_style.set_para(style_path, chosen_content_file_list, base, file_dict,
                                                             lerp_value)
                    self.sava_sceamless_style_style.start()
            except BaseException as be:
                print(be)

        # tab2
        # tab_txt
        def open_txt(self):
            # 选择txt文件
            self.ui.pic_before_listWidget2.clear()
            file, filetype = QFileDialog.getOpenFileName(self, "选择文件", "./", "TXT文件(*.txt)")
            if len(file) == 0:
                return
            else:
                self.txt_path = file
                InfoNotifier.InfoNotifier.g_progress_info.append(f"选择txt文件：{file}，点击生成图片进行格式转换，如已转换过，直接点击下拉框选择目录进行预览")
                if self.ui.project_base_dir == '':
                    InfoNotifier.InfoNotifier.g_progress_info.append("请选择根目录")
                    return
                self.dirs_filter()

        def dirs_filter(self):
            """

            从TXT包含的图片路径中过滤出需要的目录；
            需要的路径的映射表部分在data.json中
            最后在复选框中显示路径的最后两级目录

            """
            with open(".\\data.json", 'r') as f:
                # print(f)
                import os
                # 以下三个表都是相对路径
                # 预览路径
                self.map_dir_omit = []

                # checkcombobox预览的路径和真实路径的映射表
                self.dir_dict = {}

                self.pics_path_array = []

                temp = json.loads(f.read())
                fw = open(self.txt_path, "r", encoding="utf-8-sig")
                for file in fw:
                    file_path = file.replace("\n", "").replace("\\", "/")
                    parent_path = os.path.dirname(file_path)
                    # print(parent_path)
                    file_split = parent_path.split("/")

                    # 过滤出 XXX/baked;XXX/env_probe;XXX/landscape/procedural 路径
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
                                self.dir_dict[f'./{file_split[-3]}/{file_split[-2]}/{file_split[-1]}']=parent_path
                    # 过滤出预先在data.json设置的路径
                    if parent_path not in temp:
                        continue
                    # 如果存在data.json中，则加入
                    self.pics_path_array.append(file_path)
                    if temp[parent_path] not in self.map_dir_omit:
                        self.map_dir_omit.append(temp[parent_path])
                        self.dir_dict[temp[parent_path]]=parent_path

                self.combocheckBox1.loadItems(self.map_dir_omit)
                self.combocheckBox1.setEnabled(True)
                print(self.map_dir_omit)
                print(self.dir_dict)
                print(self.pics_path_array)

        def gen_jpg_tga_tab_txt(self):
            try:
                file = self.txt_path
                work_ = self.ui.project_base_dir.text()+'/'
                work_ = work_.replace("/", "\\")
                # 带转换的图片列表
                dds_list = self.pics_path_array

                self.my_dds_thread = tab_txt_thread.MyGenDdsJpgThreadTabTxt()
                self.my_dds_thread.set_para(file, work_, dds_list)
                self.my_dds_thread.start()
            except BaseException as be:
                print(be)
                InfoNotifier.InfoNotifier.g_progress_info.append("请先选择txt文件")

        def show_previewed_before_pic_tab_txt(self):
            # 生成原图的略缩图
            try:
                self.ui.pic_before_listWidget2.clear()
                self.ui.pic_before_label2.clear()
                style_img_icon = []
                self.chosen_file_list = self.combocheckBox1.Selectlist()
                print(self.chosen_file_list)
                preview_list=[]
                for dire in self.chosen_file_list:
                    fw = open(self.txt_path, "r", encoding="utf-8-sig")
                    for f in fw:
                        f=f.replace("\n", "").replace("\\", "/")
                        path=self.dir_dict[dire]
                        if self.dir_dict[dire] == os.path.dirname(f):
                            preview_list.append(f)
                            break

                for i in range(len(preview_list)):
                    get_path_class = PathUtils(_work=self.ui.project_base_dir.text(), dds_path=preview_list[i])
                    dir = get_path_class.dds_to_jpg_path()
                    preview_list[i] = dir
                print(preview_list)
                self.tmp_list = preview_list
                print(self.tmp_list)
                if len(self.tmp_list) == 0:
                    InfoNotifier.InfoNotifier.g_progress_info.append("不存在对应jpg格式图片，请先转换格式")
                    return
                for pic in self.tmp_list:
                    pix = QPixmap(pic)
                    icon = QIcon()
                    icon.addPixmap(pix)
                    style_img_icon.append(icon)
                index = 0
                while index < len(self.tmp_list):
                    item = QListWidgetItem()
                    item.setIcon(style_img_icon[index])
                    item.setSizeHint(QSize(100, 100))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.ui.pic_before_listWidget2.addItem(item)
                    index += 1
                iconsize = QSize(100, 100)
                self.ui.pic_before_listWidget2.setIconSize(iconsize)
                InfoNotifier.InfoNotifier.g_progress_info.append("点击一张风格图片以进行预览")
                QApplication.processEvents()
            except BaseException as e:
                print(e)

        def previewed_before_clicked(self):
            """

            点击原图事件:1.预览原图；2.预览风格图

            """
            pic_index = self.ui.pic_before_listWidget2.currentIndex().row()
            self.show_before_pic_in_lable_tab_txt(pic_index)
            try:
                self.preview_after_pic_in_label_tab_txt()
            except BaseException as be:
                print(be)
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图片并进行预览")

        def show_before_pic_in_lable_tab_txt(self, i):
            show_list = self.tmp_list
            dirs = show_list[i]
            pix = QPixmap(dirs)
            self.ui.pic_before_label2.setPixmap(pix)

        def choose_style_pics_tab_txt(self):
            self.ui.pic_style_listWidget2.clear()
            files, filetype = QFileDialog.getOpenFileNames(self, "选择文件", "./", "JPG文件(*.jpg)")
            if len(files) == 0:
                style_img_icon = []
                for pic in self.Choosed_style_pics_list2:
                    pix = QPixmap(pic.replace("\n", ""))
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
                    # 如果图片不是三通道，跳过
                    if self.get_channel_num(file) != 3:
                        InfoNotifier.InfoNotifier.g_progress_info.append(file + ' 为四通道图片，请选择三通道jpg格式图片！')
                    elif file in self.Choosed_style_pics_list2:
                        InfoNotifier.InfoNotifier.g_progress_info.append(file + ' 已选过')
                    else:
                        pic_dir += file + ';;'
                # 如过滤后无图片需要载入，则重载之前选中的图片
                if pic_dir == '':
                    style_img_icon = []
                    for pic in self.Choosed_style_pics_list2:
                        pix = QPixmap(pic.replace("\n", ""))
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
                    return

                pic_dir = pic_dir[:-2]

                pic_dir = pic_dir.split(";;")
                for i in pic_dir:
                    self.Choosed_style_pics_list2.append(i)
                print(self.Choosed_style_pics_list2)

                style_img_icon=[]
                for pic in self.Choosed_style_pics_list2:
                    pix = QPixmap(pic.replace("\n", ""))
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
                iconsize = QSize(100,100)
                self.ui.pic_style_listWidget2.setIconSize(iconsize)

                QApplication.processEvents()

        def pic_style_clicked_tab_txt(self):
            try:
                if len(self.Choosed_style_pics_list2) == 0:
                    return
                pic_style_index = self.ui.pic_style_listWidget2.currentIndex().row()
                self.chosen_style_pic2 = self.Choosed_style_pics_list2[pic_style_index]
                self.show_style_pic_in_label_tab_txt(pic_style_index)
                self.make_temp_previewed()
                self.preview_after_pic_in_label_tab_txt()
            except BaseException as e:
                print(e)

        def make_temp_previewed(self):
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("等待生成预览图")
                base = self.ui.project_base_dir.text()
                preview_file_list = self.tmp_list
                if len(preview_file_list) == 0:
                    return
                self.mythread_temp = tab_txt_thread.MyGenStyleTempThreadTabTxt()
                self.mythread_temp.set_para(preview_file_list, self.chosen_style_pic2, self.ui.project_base_dir.text())
                self.mythread_temp.start()
            except BaseException as be:
                print(be)
                InfoNotifier.InfoNotifier.g_progress_info.append("先加入原图")
            # InfoNotifier.InfoNotifier.g_progress_info.append("预览图生成完成，点击")

        def show_style_pic_in_label_tab_txt(self, i=0):
            show_list = self.Choosed_style_pics_list2
            dirs = show_list[i]
            self.chosen_style_pic2 = dirs
            pix = QPixmap(dirs)
            self.ui.pic_style_label2.setPixmap(pix)
            self.ui.pic_style_label2.setScaledContents(True)

        def preview_after_pic_in_label_tab_txt(self):
            # 预览风格化图
            try:
                content_index = self.ui.pic_before_listWidget2.currentIndex().row()
                content_pic = self.tmp_list[content_index]
                get_path=PathTemp(jpg_path_=content_pic, style_path_=self.chosen_style_pic2)
                # s_name = os.path.basename(self.chosen_style_pic2).split('.')[0]
                # after_pic_dir = os.path.dirname(content_pic)+'/temp/'+s_name+'/'+os.path.basename(content_pic)
                # save_path2 = os.path.dirname(content_pic) + '/temp/lerp.jpg'
                after_pic_dir = get_path.get_temp_after_jpg_path()
                save_path2 = get_path.get_temp_lerp_path()
                self.value_slider = self.ui.change_coe_horizontalSlider2.value()
                img, _ = gen_lerp_ret.lerp_img(content_pic, after_pic_dir, float(self.value_slider))
                gen_lerp_ret.write_img(img, save_path2)
                self.ui.pic_after_label2.clear()
                item = QListWidgetItem()
                item.setIcon(QIcon(save_path2))
                item.setSizeHint(QSize(291, 271))
                self.ui.pic_after_label2.setIconSize(QSize(291, 271))
                self.ui.pic_after_label2.addItem(item)
            except BaseException as e:
                print('preview_after_pic_in_label_tab_txt', e)
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图或等待生成预览图片")

        def is_seamless_ornot_tab_txt(self):
            if self.ui.is_seamless_ornot_comboBox2.currentText() == "否":
                b_use_expanded = False
            else:
                b_use_expanded = True
            return b_use_expanded

        def save_style_tab_txt(self):
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("开始保存··············")
                txt_file = self.txt_path
                work_ = self.ui.project_base_dir.text()
                lerp_value = self.ui.change_coe_horizontalSlider2.value()
                seamless = self.is_seamless_ornot_tab_txt()
                chosen_style_pic = self.chosen_style_pic2
                # 被勾选的目录列表
                chosen_content_file_list = self.combocheckBox1.Selectlist()

                if seamless is False:
                    self.mythread3 = tab_txt_thread.MyGenStyleThreadTabTxt()
                    self.mythread3.set_para(txt_file, work_, lerp_value, chosen_style_pic, chosen_content_file_list,
                                            self.dir_dict)
                    self.mythread3.start()
                else:
                    self.mythread3 = tab_txt_thread.MyGenSeamlessThreadTabTxt()
                    self.mythread3.set_para(txt_file, work_, lerp_value, chosen_style_pic, chosen_content_file_list,
                                            self.dir_dict)
                    self.mythread3.start()
            except BaseException as b:
                print(b)

        # tab_pics
        def choose_multi_pics(self):
            if self.ui.project_base_dir.text() == '':
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择根目录")
                return
            files, filetype = QFileDialog.getOpenFileNames(self, "选择文件", self.ui.project_base_dir.text(),
                                                           "DDS文件(*.dds)")
            if len(files) == 0:
                return
            else:
                for file in files:
                    self.chosen_content_list3.append(file.replace(self.ui.project_base_dir.text()+'/', ""))
            InfoNotifier.InfoNotifier.g_progress_info.append(f"已选中{len(self.chosen_content_list3)}张图片")
            print(self.chosen_content_list3)

        def gen_jpg_tga_tab_pics(self):
            # self.ui.choose_pics_button3.setEnabled(False)
            self.base = self.ui.project_base_dir.text()
            self.mythread_gen = tab_specific_pics_thread.MyGenDdsJpgThreadTabPics()
            self.mythread_gen.set_para(self.chosen_content_list3, self.ui.project_base_dir.text())
            self.mythread_gen.start()

        def preview_before_in_widget_tab_pics(self):
            self.ui.pic_before_listWidget3.clear()
            style_img_icon = []
            show_before_list = []
            cnt = 3
            if len(self.chosen_content_list3) <= cnt:
                loop = range(len(self.chosen_content_list3))
            else:
                loop = random.sample(range(len(self.chosen_content_list3)), 3)
            for i in loop:
                dds_path = self.chosen_content_list3[i]
                get_path = PathUtils(_work=self.ui.project_base_dir.text(), dds_path=dds_path)
                jpg_path = get_path.dds_to_jpg_path()
                show_before_list.append(jpg_path.replace("\n", ""))
            for pic in show_before_list:
                print(pic)
                pix = QPixmap(pic)
                icon = QIcon()
                icon.addPixmap(pix)
                style_img_icon.append(icon)
            index = 0
            while index < len(show_before_list):
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

        def previewed_before_clicked_tab_pics(self):
            pic_index = self.ui.pic_before_listWidget3.currentIndex().row()
            self.show_before_pic_in_lable_tab_pics(pic_index)
            try:
                self.preview_after_pic_in_label_tab_pics()
            except BaseException as be:
                print(be)
                InfoNotifier.InfoNotifier.g_progress_info.append("请选择一张风格图片并进行预览")

        def show_before_pic_in_lable_tab_pics(self, i):
            show_list = self.tmp_before_list3
            dirs = show_list[i]
            pix = QPixmap(dirs)
            self.ui.pic_before_label3.setPixmap(pix)

        def choose_style_pics_tab_pics(self):
            self.ui.pic_style_listWidget3.clear()
            files, filetype = QFileDialog.getOpenFileNames(self, "选择文件", "./", "JPG文件(*.jpg)")
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
                    # 如果图片不是三通道，跳过
                    if self.get_channel_num(file) != 3:
                        InfoNotifier.InfoNotifier.g_progress_info.append(file + ' 为四通道图片，请选择三通道jpg格式图片！')
                    elif file in self.Choosed_style_pics_list3:
                        InfoNotifier.InfoNotifier.g_progress_info.append(file + ' 已选过')
                    else:
                        pic_dir += file + ';;'
                # 如过滤后无图片需要载入，则重载之前选中的图片
                if pic_dir == '':
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
                    return

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

        def pic_style_clicked_tab_pics(self):
            if len(self.Choosed_style_pics_list3) == 0:
                return

            pic_style_index = self.ui.pic_style_listWidget3.currentIndex().row()
            self.show_style_pic_in_label_tab_pics(pic_style_index)
            self.ui.pic_style_listWidget3.setEnabled(False)
            self.make_temp_previewed_tab_pics()
            self.preview_after_pic_in_label_tab_pics()

        def show_style_pic_in_label_tab_pics(self, i):
            # print(i)
            show_list = self.Choosed_style_pics_list3
            dirs = show_list[i]
            self.chosen_style_pic3 = dirs
            pix = QPixmap(dirs)

            # pix=pix.scaled(200, 200)
            # pix=pix.fromImage(pix)
            self.ui.pic_style_label3.setPixmap(pix)
            # self.ui.pic_style_label1.setFixedSize(QSize(250,250))
            self.ui.pic_style_label3.setScaledContents(True)

        def make_temp_previewed_tab_pics(self):
            try:
                InfoNotifier.InfoNotifier.g_progress_info.append("等待生成预览图")
                base = self.ui.project_base_dir.text()
                if base == '':
                    InfoNotifier.InfoNotifier.g_progress_info.append("请创建一个工程目录")
                else:
                    preview_file_list = self.tmp_before_list3
                    if len(preview_file_list) == 0:
                        return
                    tmp_file = preview_file_list[0]
                    get_path=PathTemp(jpg_path_=tmp_file)
                    # parent_tmp = os.path.dirname(tmp_file)
                    # tem_file = parent_tmp + '/temp/'
                    tem_file = get_path.get_temp_dir_path()
                    self.tem_file = tem_file
                    self.mythread_temp3 = tab_specific_pics_thread.MyGenStyleTempThreadTabPics()
                    self.mythread_temp3.set_para(preview_file_list, self.chosen_style_pic3, tem_file)
                    self.mythread_temp3.start()
                    self.preview_after_pic_in_label_tab_pics()
                self.ui.pic_style_listWidget3.setEnabled(True)
            except BaseException as be:
                print(be)
                InfoNotifier.InfoNotifier.g_progress_info.append("先加入原图")
            # InfoNotifier.InfoNotifier.g_progress_info.append("预览图生成完成，点击")

        def preview_after_pic_in_label_tab_pics(self):
            try:

                content_index = self.ui.pic_before_listWidget3.currentIndex().row()
                content_pic = self.tmp_before_list3[content_index]
                get_path = PathTemp(jpg_path_=content_pic,style_path_=self.chosen_style_pic3)
                # s_name = os.path.basename(self.chosen_style_pic3).split('.')[0]
                # after_pic_dir = os.path.dirname(content_pic)+'/temp/'+s_name+'/'+os.path.basename(content_pic)
                after_pic_dir = get_path.get_temp_after_jpg_path()
                # self.save_path1 = self.tem_file + 'lerp.jpg'
                self.save_path1 = get_path.get_temp_lerp_path()
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

        def is_seamless_ornot_tab_pics(self):
            if self.ui.is_seamless_ornot_comboBox3.currentText() == "否":
                return False
            return True

        def save_all_tab_pics(self):

            style_path = self.chosen_style_pic3
            content_list = self.chosen_content_list3
            lerp_value = self.ui.change_coe_horizontalSlider3.value()
            seamless = self.is_seamless_ornot_tab_pics()
            if seamless is False:
                self.mythread_save3 = tab_specific_pics_thread.MyGenStyleThreadTabPics()
                self.mythread_save3.set_para(self.ui.project_base_dir.text(), content_list, style_path, lerp_value)
                self.mythread_save3.start()
            else:
                self.mythread_save3 = tab_specific_pics_thread.MyGenSeamlessStyleThreadTabPics()
                self.mythread_save3.set_para(self.ui.project_base_dir.text(), content_list, style_path, lerp_value)
                self.mythread_save3.start()


    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
