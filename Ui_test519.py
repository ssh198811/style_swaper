# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_test519.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 1000)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 1000))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 1000))
        MainWindow.setStyleSheet("color: rgb(0, 0, 91);\n"
"background-color: rgb(0, 59, 89);\n"
"font: 12pt \"Arial\";")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SpecPic = QtWidgets.QTabWidget(self.centralwidget)
        self.SpecPic.setEnabled(True)
        self.SpecPic.setGeometry(QtCore.QRect(0, 50, 1200, 700))
        self.SpecPic.setMinimumSize(QtCore.QSize(1200, 700))
        self.SpecPic.setMaximumSize(QtCore.QSize(1200, 700))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SpecPic.setFont(font)
        self.SpecPic.setToolTip("")
        self.SpecPic.setStatusTip("")
        self.SpecPic.setStyleSheet("background-color: rgb(0, 59, 89);")
        self.SpecPic.setObjectName("SpecPic")
        self.txt = QtWidgets.QWidget()
        self.txt.setEnabled(True)
        self.txt.setObjectName("txt")
        self.is_seamless_ornot_text2 = QtWidgets.QLabel(self.txt)
        self.is_seamless_ornot_text2.setGeometry(QtCore.QRect(860, 520, 131, 31))
        self.is_seamless_ornot_text2.setStyleSheet("color: rgb(255, 248, 249);\n"
"font: 12pt \"Arial\";")
        self.is_seamless_ornot_text2.setObjectName("is_seamless_ornot_text2")
        self.savePic_button2 = QtWidgets.QPushButton(self.txt)
        self.savePic_button2.setGeometry(QtCore.QRect(950, 580, 161, 51))
        self.savePic_button2.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 251, 252);")
        self.savePic_button2.setObjectName("savePic_button2")
        self.pic_style_text2 = QtWidgets.QLabel(self.txt)
        self.pic_style_text2.setGeometry(QtCore.QRect(400, 20, 71, 21))
        self.pic_style_text2.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.pic_style_text2.setObjectName("pic_style_text2")
        self.line_19 = QtWidgets.QFrame(self.txt)
        self.line_19.setGeometry(QtCore.QRect(380, 40, 20, 521))
        self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.pic_before_label2 = QtWidgets.QLabel(self.txt)
        self.pic_before_label2.setGeometry(QtCore.QRect(40, 220, 301, 251))
        self.pic_before_label2.setStyleSheet("color: rgb(203, 203, 203);")
        self.pic_before_label2.setText("")
        self.pic_before_label2.setObjectName("pic_before_label2")
        self.pic_after_text2 = QtWidgets.QLabel(self.txt)
        self.pic_after_text2.setGeometry(QtCore.QRect(820, 20, 71, 21))
        self.pic_after_text2.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.pic_after_text2.setObjectName("pic_after_text2")
        self.line_20 = QtWidgets.QFrame(self.txt)
        self.line_20.setGeometry(QtCore.QRect(353, 40, 20, 521))
        self.line_20.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.choose_pic_txt_button2 = QtWidgets.QPushButton(self.txt)
        self.choose_pic_txt_button2.setEnabled(True)
        self.choose_pic_txt_button2.setGeometry(QtCore.QRect(30, 60, 321, 41))
        self.choose_pic_txt_button2.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.choose_pic_txt_button2.setObjectName("choose_pic_txt_button2")
        self.line_21 = QtWidgets.QFrame(self.txt)
        self.line_21.setGeometry(QtCore.QRect(770, 30, 20, 521))
        self.line_21.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.line_22 = QtWidgets.QFrame(self.txt)
        self.line_22.setGeometry(QtCore.QRect(730, 30, 20, 521))
        self.line_22.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.pic_before_text2 = QtWidgets.QLabel(self.txt)
        self.pic_before_text2.setGeometry(QtCore.QRect(30, 20, 71, 21))
        self.pic_before_text2.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.pic_before_text2.setObjectName("pic_before_text2")
        self.line_23 = QtWidgets.QFrame(self.txt)
        self.line_23.setGeometry(QtCore.QRect(450, 20, 291, 21))
        self.line_23.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_23.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.line_24 = QtWidgets.QFrame(self.txt)
        self.line_24.setGeometry(QtCore.QRect(110, 30, 251, 21))
        self.line_24.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_24.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_24.setObjectName("line_24")
        self.is_seamless_ornot_comboBox2 = QtWidgets.QComboBox(self.txt)
        self.is_seamless_ornot_comboBox2.setEnabled(True)
        self.is_seamless_ornot_comboBox2.setGeometry(QtCore.QRect(1020, 520, 91, 31))
        self.is_seamless_ornot_comboBox2.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 252, 253);")
        self.is_seamless_ornot_comboBox2.setObjectName("is_seamless_ornot_comboBox2")
        self.is_seamless_ornot_comboBox2.addItem("")
        self.is_seamless_ornot_comboBox2.addItem("")
        self.pic_style_label2 = QtWidgets.QLabel(self.txt)
        self.pic_style_label2.setGeometry(QtCore.QRect(400, 220, 301, 251))
        self.pic_style_label2.setToolTip("")
        self.pic_style_label2.setToolTipDuration(1)
        self.pic_style_label2.setStyleSheet("color: rgb(203, 203, 203);")
        self.pic_style_label2.setText("")
        self.pic_style_label2.setObjectName("pic_style_label2")
        self.line_31 = QtWidgets.QFrame(self.txt)
        self.line_31.setGeometry(QtCore.QRect(900, 30, 271, 21))
        self.line_31.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_31.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.line_32 = QtWidgets.QFrame(self.txt)
        self.line_32.setGeometry(QtCore.QRect(1160, 40, 20, 521))
        self.line_32.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.pic_before_listWidget2 = QtWidgets.QListWidget(self.txt)
        self.pic_before_listWidget2.setGeometry(QtCore.QRect(30, 510, 311, 121))
        self.pic_before_listWidget2.setStyleSheet("")
        self.pic_before_listWidget2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_before_listWidget2.setObjectName("pic_before_listWidget2")
        self.pic_style_listWidget2 = QtWidgets.QListWidget(self.txt)
        self.pic_style_listWidget2.setGeometry(QtCore.QRect(410, 510, 311, 121))
        self.pic_style_listWidget2.setStyleSheet("")
        self.pic_style_listWidget2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_style_listWidget2.setObjectName("pic_style_listWidget2")
        self.choose_pic_style_button2 = QtWidgets.QPushButton(self.txt)
        self.choose_pic_style_button2.setGeometry(QtCore.QRect(410, 110, 301, 41))
        self.choose_pic_style_button2.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.choose_pic_style_button2.setObjectName("choose_pic_style_button2")
        self.change_coe_horizontalSlider2 = QtWidgets.QSlider(self.txt)
        self.change_coe_horizontalSlider2.setGeometry(QtCore.QRect(820, 70, 301, 22))
        self.change_coe_horizontalSlider2.setStyleSheet("\n"
"color: rgb(212, 212, 212);")
        self.change_coe_horizontalSlider2.setMaximum(100)
        self.change_coe_horizontalSlider2.setSingleStep(1)
        self.change_coe_horizontalSlider2.setProperty("value", 50)
        self.change_coe_horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.change_coe_horizontalSlider2.setObjectName("change_coe_horizontalSlider2")
        self.pic_after_label2 = QtWidgets.QListWidget(self.txt)
        self.pic_after_label2.setGeometry(QtCore.QRect(820, 210, 301, 271))
        self.pic_after_label2.setToolTip("")
        self.pic_after_label2.setStyleSheet("border-color: rgb(0, 85, 127);")
        self.pic_after_label2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_after_label2.setObjectName("pic_after_label2")
        self.gen_jpg_tga_button2 = QtWidgets.QPushButton(self.txt)
        self.gen_jpg_tga_button2.setGeometry(QtCore.QRect(30, 110, 321, 41))
        self.gen_jpg_tga_button2.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.gen_jpg_tga_button2.setObjectName("gen_jpg_tga_button2")
        self.picpath_bef_comboBox = QtWidgets.QComboBox(self.txt)
        self.picpath_bef_comboBox.setEnabled(True)
        self.picpath_bef_comboBox.setGeometry(QtCore.QRect(30, 160, 321, 41))
        self.picpath_bef_comboBox.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.picpath_bef_comboBox.setModelColumn(0)
        self.picpath_bef_comboBox.setObjectName("picpath_bef_comboBox")
        self.preview_content2 = QtWidgets.QPushButton(self.txt)
        self.preview_content2.setGeometry(QtCore.QRect(270, 480, 75, 23))
        self.preview_content2.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.preview_content2.setObjectName("preview_content2")
        self.SpecPic.addTab(self.txt, "TXT路径导入")
        self.t1 = QtWidgets.QWidget()
        self.t1.setAccessibleName("")
        self.t1.setObjectName("t1")
        self.choose_pic_multi_file_dir_button1 = QtWidgets.QPushButton(self.t1)
        self.choose_pic_multi_file_dir_button1.setGeometry(QtCore.QRect(30, 70, 151, 41))
        self.choose_pic_multi_file_dir_button1.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.choose_pic_multi_file_dir_button1.setObjectName("choose_pic_multi_file_dir_button1")
        self.Pic_before_text1 = QtWidgets.QLabel(self.t1)
        self.Pic_before_text1.setGeometry(QtCore.QRect(30, 30, 71, 21))
        self.Pic_before_text1.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.Pic_before_text1.setObjectName("Pic_before_text1")
        self.pic_before_label1 = QtWidgets.QLabel(self.t1)
        self.pic_before_label1.setGeometry(QtCore.QRect(30, 210, 301, 251))
        self.pic_before_label1.setStyleSheet("color: rgb(203, 203, 203);")
        self.pic_before_label1.setText("")
        self.pic_before_label1.setObjectName("pic_before_label1")
        self.pic_style_label1 = QtWidgets.QLabel(self.t1)
        self.pic_style_label1.setGeometry(QtCore.QRect(410, 210, 301, 251))
        self.pic_style_label1.setStyleSheet("color: rgb(203, 203, 203);")
        self.pic_style_label1.setText("")
        self.pic_style_label1.setObjectName("pic_style_label1")
        self.change_coe_horizontalSlider1 = QtWidgets.QSlider(self.t1)
        self.change_coe_horizontalSlider1.setGeometry(QtCore.QRect(820, 90, 301, 22))
        self.change_coe_horizontalSlider1.setStyleSheet("\n"
"color: rgb(212, 212, 212);")
        self.change_coe_horizontalSlider1.setMaximum(100)
        self.change_coe_horizontalSlider1.setSingleStep(1)
        self.change_coe_horizontalSlider1.setProperty("value", 50)
        self.change_coe_horizontalSlider1.setOrientation(QtCore.Qt.Horizontal)
        self.change_coe_horizontalSlider1.setObjectName("change_coe_horizontalSlider1")
        self.savePic_button1 = QtWidgets.QPushButton(self.t1)
        self.savePic_button1.setGeometry(QtCore.QRect(950, 580, 161, 51))
        self.savePic_button1.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 251, 252);")
        self.savePic_button1.setObjectName("savePic_button1")
        self.is_seamless_ornot_comboBox1 = QtWidgets.QComboBox(self.t1)
        self.is_seamless_ornot_comboBox1.setGeometry(QtCore.QRect(1010, 490, 91, 31))
        self.is_seamless_ornot_comboBox1.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 252, 253);")
        self.is_seamless_ornot_comboBox1.setObjectName("is_seamless_ornot_comboBox1")
        self.is_seamless_ornot_comboBox1.addItem("")
        self.is_seamless_ornot_comboBox1.addItem("")
        self.is_seamless_ornot_text1 = QtWidgets.QLabel(self.t1)
        self.is_seamless_ornot_text1.setGeometry(QtCore.QRect(860, 490, 131, 31))
        self.is_seamless_ornot_text1.setStyleSheet("color: rgb(255, 248, 249);\n"
"font: 12pt \"Arial\";")
        self.is_seamless_ornot_text1.setObjectName("is_seamless_ornot_text1")
        self.pic_style_text1 = QtWidgets.QLabel(self.t1)
        self.pic_style_text1.setGeometry(QtCore.QRect(400, 30, 71, 21))
        self.pic_style_text1.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.pic_style_text1.setObjectName("pic_style_text1")
        self.pic_after_text1 = QtWidgets.QLabel(self.t1)
        self.pic_after_text1.setGeometry(QtCore.QRect(820, 30, 71, 21))
        self.pic_after_text1.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.pic_after_text1.setObjectName("pic_after_text1")
        self.line = QtWidgets.QFrame(self.t1)
        self.line.setGeometry(QtCore.QRect(110, 40, 251, 21))
        self.line.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.t1)
        self.line_2.setGeometry(QtCore.QRect(353, 50, 20, 521))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.t1)
        self.line_3.setGeometry(QtCore.QRect(380, 50, 20, 521))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.t1)
        self.line_4.setGeometry(QtCore.QRect(450, 30, 291, 21))
        self.line_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.t1)
        self.line_5.setGeometry(QtCore.QRect(730, 40, 20, 521))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.t1)
        self.line_6.setGeometry(QtCore.QRect(770, 40, 20, 521))
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self.t1)
        self.line_7.setGeometry(QtCore.QRect(890, 30, 261, 21))
        self.line_7.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self.t1)
        self.line_8.setGeometry(QtCore.QRect(780, 30, 31, 20))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(self.t1)
        self.line_9.setGeometry(QtCore.QRect(0, 0, 261, 21))
        self.line_9.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.choose_pic_style_button1 = QtWidgets.QPushButton(self.t1)
        self.choose_pic_style_button1.setGeometry(QtCore.QRect(410, 70, 301, 41))
        self.choose_pic_style_button1.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.choose_pic_style_button1.setObjectName("choose_pic_style_button1")
        self.pic_before_listWidget1 = QtWidgets.QListWidget(self.t1)
        self.pic_before_listWidget1.setGeometry(QtCore.QRect(30, 500, 311, 121))
        self.pic_before_listWidget1.setStyleSheet("")
        self.pic_before_listWidget1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_before_listWidget1.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.pic_before_listWidget1.setObjectName("pic_before_listWidget1")
        self.pic_style_listWidget1 = QtWidgets.QListWidget(self.t1)
        self.pic_style_listWidget1.setGeometry(QtCore.QRect(410, 500, 311, 121))
        self.pic_style_listWidget1.setStyleSheet("")
        self.pic_style_listWidget1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_style_listWidget1.setObjectName("pic_style_listWidget1")
        self.multi_file_combobox = QtWidgets.QComboBox(self.t1)
        self.multi_file_combobox.setGeometry(QtCore.QRect(30, 130, 311, 41))
        self.multi_file_combobox.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.multi_file_combobox.setObjectName("multi_file_combobox")
        self.Preview_button = QtWidgets.QPushButton(self.t1)
        self.Preview_button.setGeometry(QtCore.QRect(210, 70, 121, 41))
        self.Preview_button.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.Preview_button.setObjectName("Preview_button")
        self.pic_after_label1 = QtWidgets.QListWidget(self.t1)
        self.pic_after_label1.setGeometry(QtCore.QRect(830, 200, 291, 271))
        self.pic_after_label1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_after_label1.setObjectName("pic_after_label1")
        self.preview_content1 = QtWidgets.QPushButton(self.t1)
        self.preview_content1.setGeometry(QtCore.QRect(260, 470, 75, 23))
        self.preview_content1.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);\n"
"\n"
"")
        self.preview_content1.setObjectName("preview_content1")
        self.SpecPic.addTab(self.t1, "多目录导入")
        self.pics = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pics.setFont(font)
        self.pics.setAccessibleName("")
        self.pics.setObjectName("pics")
        self.is_seamless_ornot_text3 = QtWidgets.QLabel(self.pics)
        self.is_seamless_ornot_text3.setGeometry(QtCore.QRect(870, 470, 131, 31))
        self.is_seamless_ornot_text3.setStyleSheet("color: rgb(255, 248, 249);\n"
"font: 12pt \"Arial\";")
        self.is_seamless_ornot_text3.setObjectName("is_seamless_ornot_text3")
        self.savePic_button3 = QtWidgets.QPushButton(self.pics)
        self.savePic_button3.setGeometry(QtCore.QRect(960, 570, 161, 51))
        self.savePic_button3.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 251, 252);")
        self.savePic_button3.setObjectName("savePic_button3")
        self.pic_style_text3 = QtWidgets.QLabel(self.pics)
        self.pic_style_text3.setGeometry(QtCore.QRect(410, 20, 71, 21))
        self.pic_style_text3.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.pic_style_text3.setObjectName("pic_style_text3")
        self.line_25 = QtWidgets.QFrame(self.pics)
        self.line_25.setGeometry(QtCore.QRect(390, 40, 20, 521))
        self.line_25.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_25.setObjectName("line_25")
        self.pic_before_label3 = QtWidgets.QLabel(self.pics)
        self.pic_before_label3.setGeometry(QtCore.QRect(40, 180, 301, 251))
        self.pic_before_label3.setStyleSheet("color: rgb(203, 203, 203);")
        self.pic_before_label3.setText("")
        self.pic_before_label3.setObjectName("pic_before_label3")
        self.pic_after_text3 = QtWidgets.QLabel(self.pics)
        self.pic_after_text3.setGeometry(QtCore.QRect(830, 20, 71, 21))
        self.pic_after_text3.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.pic_after_text3.setObjectName("pic_after_text3")
        self.line_26 = QtWidgets.QFrame(self.pics)
        self.line_26.setGeometry(QtCore.QRect(363, 40, 20, 521))
        self.line_26.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.choose_pics_button3 = QtWidgets.QPushButton(self.pics)
        self.choose_pics_button3.setGeometry(QtCore.QRect(40, 60, 151, 41))
        self.choose_pics_button3.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.choose_pics_button3.setObjectName("choose_pics_button3")
        self.line_27 = QtWidgets.QFrame(self.pics)
        self.line_27.setGeometry(QtCore.QRect(780, 30, 20, 521))
        self.line_27.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.line_28 = QtWidgets.QFrame(self.pics)
        self.line_28.setGeometry(QtCore.QRect(740, 30, 20, 521))
        self.line_28.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_28.setObjectName("line_28")
        self.pic_before_text3 = QtWidgets.QLabel(self.pics)
        self.pic_before_text3.setGeometry(QtCore.QRect(40, 20, 71, 21))
        self.pic_before_text3.setStyleSheet("background-color: rgb(0, 59, 89);\n"
"font: 14pt \"Arial\";\n"
"\n"
"color: rgb(212, 212, 212);")
        self.pic_before_text3.setObjectName("pic_before_text3")
        self.line_29 = QtWidgets.QFrame(self.pics)
        self.line_29.setGeometry(QtCore.QRect(460, 20, 291, 21))
        self.line_29.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_29.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_29.setObjectName("line_29")
        self.line_30 = QtWidgets.QFrame(self.pics)
        self.line_30.setGeometry(QtCore.QRect(120, 30, 251, 21))
        self.line_30.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_30.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")
        self.is_seamless_ornot_comboBox3 = QtWidgets.QComboBox(self.pics)
        self.is_seamless_ornot_comboBox3.setGeometry(QtCore.QRect(1030, 470, 91, 31))
        self.is_seamless_ornot_comboBox3.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 252, 253);")
        self.is_seamless_ornot_comboBox3.setObjectName("is_seamless_ornot_comboBox3")
        self.is_seamless_ornot_comboBox3.addItem("")
        self.is_seamless_ornot_comboBox3.addItem("")
        self.pic_style_label3 = QtWidgets.QLabel(self.pics)
        self.pic_style_label3.setGeometry(QtCore.QRect(420, 190, 301, 251))
        self.pic_style_label3.setStyleSheet("color: rgb(203, 203, 203);")
        self.pic_style_label3.setText("")
        self.pic_style_label3.setObjectName("pic_style_label3")
        self.line_33 = QtWidgets.QFrame(self.pics)
        self.line_33.setGeometry(QtCore.QRect(1160, 40, 20, 511))
        self.line_33.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_33.setObjectName("line_33")
        self.line_34 = QtWidgets.QFrame(self.pics)
        self.line_34.setGeometry(QtCore.QRect(890, 30, 281, 21))
        self.line_34.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"Arial\";")
        self.line_34.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_34.setObjectName("line_34")
        self.pic_style_listWidget3 = QtWidgets.QListWidget(self.pics)
        self.pic_style_listWidget3.setGeometry(QtCore.QRect(410, 510, 311, 121))
        self.pic_style_listWidget3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_style_listWidget3.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.pic_style_listWidget3.setObjectName("pic_style_listWidget3")
        self.pic_before_listWidget3 = QtWidgets.QListWidget(self.pics)
        self.pic_before_listWidget3.setGeometry(QtCore.QRect(40, 510, 311, 121))
        self.pic_before_listWidget3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_before_listWidget3.setObjectName("pic_before_listWidget3")
        self.choose_pic_style_button2_2 = QtWidgets.QPushButton(self.pics)
        self.choose_pic_style_button2_2.setGeometry(QtCore.QRect(420, 60, 301, 41))
        self.choose_pic_style_button2_2.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.choose_pic_style_button2_2.setObjectName("choose_pic_style_button2_2")
        self.change_coe_horizontalSlider3 = QtWidgets.QSlider(self.pics)
        self.change_coe_horizontalSlider3.setGeometry(QtCore.QRect(820, 70, 321, 22))
        self.change_coe_horizontalSlider3.setStyleSheet("\n"
"color: rgb(212, 212, 212);")
        self.change_coe_horizontalSlider3.setMaximum(100)
        self.change_coe_horizontalSlider3.setSingleStep(1)
        self.change_coe_horizontalSlider3.setProperty("value", 50)
        self.change_coe_horizontalSlider3.setOrientation(QtCore.Qt.Horizontal)
        self.change_coe_horizontalSlider3.setObjectName("change_coe_horizontalSlider3")
        self.pic_after_label3 = QtWidgets.QListWidget(self.pics)
        self.pic_after_label3.setGeometry(QtCore.QRect(820, 180, 301, 271))
        self.pic_after_label3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pic_after_label3.setObjectName("pic_after_label3")
        self.pushButton = QtWidgets.QPushButton(self.pics)
        self.pushButton.setGeometry(QtCore.QRect(220, 60, 131, 41))
        self.pushButton.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.pushButton.setObjectName("pushButton")
        self.pre_bef_button3 = QtWidgets.QPushButton(self.pics)
        self.pre_bef_button3.setGeometry(QtCore.QRect(290, 470, 75, 23))
        self.pre_bef_button3.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.pre_bef_button3.setObjectName("pre_bef_button3")
        self.SpecPic.addTab(self.pics, "多选贴图导入")
        self.make_project_dir_button = QtWidgets.QPushButton(self.centralwidget)
        self.make_project_dir_button.setGeometry(QtCore.QRect(0, 20, 500, 31))
        self.make_project_dir_button.setMaximumSize(QtCore.QSize(500, 16777215))
        self.make_project_dir_button.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.make_project_dir_button.setObjectName("make_project_dir_button")
        self.project_base_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.project_base_dir.setGeometry(QtCore.QRect(510, 20, 671, 31))
        self.project_base_dir.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(212, 212, 212);")
        self.project_base_dir.setObjectName("project_base_dir")
        self.progress_Info = QtWidgets.QTextBrowser(self.centralwidget)
        self.progress_Info.setGeometry(QtCore.QRect(0, 790, 1181, 151))
        self.progress_Info.setToolTip("")
        self.progress_Info.setStyleSheet("color: rgb(212, 212, 212);")
        self.progress_Info.setObjectName("progress_Info")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 760, 121, 21))
        self.label.setStyleSheet("color: rgb(212, 212, 212);")
        self.label.setObjectName("label")
        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setEnabled(False)
        self.reset_button.setGeometry(QtCore.QRect(990, 950, 81, 31))
        self.reset_button.setToolTipDuration(-1)
        self.reset_button.setStatusTip("")
        self.reset_button.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 251, 252);\n"
"")
        self.reset_button.setObjectName("reset_button")
        self.delete_files_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_files_button.setEnabled(False)
        self.delete_files_button.setGeometry(QtCore.QRect(1100, 950, 81, 31))
        self.delete_files_button.setToolTipDuration(-1)
        self.delete_files_button.setStatusTip("")
        self.delete_files_button.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 251, 252);")
        self.delete_files_button.setObjectName("delete_files_button")
        self.make_project_dir_button.raise_()
        self.project_base_dir.raise_()
        self.progress_Info.raise_()
        self.label.raise_()
        self.reset_button.raise_()
        self.delete_files_button.raise_()
        self.SpecPic.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action3 = QtWidgets.QAction(MainWindow)
        self.action3.setObjectName("action3")

        self.retranslateUi(MainWindow)
        self.SpecPic.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "风格迁移-jw3"))
        self.is_seamless_ornot_text2.setText(_translate("MainWindow", "是否输出无缝贴图："))
        self.savePic_button2.setText(_translate("MainWindow", "保存图片"))
        self.pic_style_text2.setText(_translate("MainWindow", "风格"))
        self.pic_after_text2.setText(_translate("MainWindow", "微调"))
        self.choose_pic_txt_button2.setText(_translate("MainWindow", "选择含图片路径的TXT文件"))
        self.pic_before_text2.setText(_translate("MainWindow", "原图"))
        self.is_seamless_ornot_comboBox2.setItemText(0, _translate("MainWindow", "否"))
        self.is_seamless_ornot_comboBox2.setItemText(1, _translate("MainWindow", "是"))
        self.choose_pic_style_button2.setText(_translate("MainWindow", "导入风格图片"))
        self.gen_jpg_tga_button2.setText(_translate("MainWindow", "生成图片"))
        self.preview_content2.setText(_translate("MainWindow", "预览"))
        self.choose_pic_multi_file_dir_button1.setText(_translate("MainWindow", "选择待转换图片目录"))
        self.Pic_before_text1.setText(_translate("MainWindow", "原图"))
        self.savePic_button1.setText(_translate("MainWindow", "保存图片"))
        self.is_seamless_ornot_comboBox1.setItemText(0, _translate("MainWindow", "否"))
        self.is_seamless_ornot_comboBox1.setItemText(1, _translate("MainWindow", "是"))
        self.is_seamless_ornot_text1.setText(_translate("MainWindow", "是否输出无缝贴图："))
        self.pic_style_text1.setText(_translate("MainWindow", "风格"))
        self.pic_after_text1.setText(_translate("MainWindow", "微调"))
        self.choose_pic_style_button1.setText(_translate("MainWindow", "导入风格图片"))
        self.Preview_button.setText(_translate("MainWindow", "生成图片"))
        self.preview_content1.setText(_translate("MainWindow", "预览"))
        self.is_seamless_ornot_text3.setText(_translate("MainWindow", "是否输出无缝贴图："))
        self.savePic_button3.setText(_translate("MainWindow", "保存图片"))
        self.pic_style_text3.setText(_translate("MainWindow", "风格"))
        self.pic_after_text3.setText(_translate("MainWindow", "微调"))
        self.choose_pics_button3.setText(_translate("MainWindow", "选择待转换图片"))
        self.pic_before_text3.setText(_translate("MainWindow", "原图"))
        self.is_seamless_ornot_comboBox3.setItemText(0, _translate("MainWindow", "否"))
        self.is_seamless_ornot_comboBox3.setItemText(1, _translate("MainWindow", "是"))
        self.choose_pic_style_button2_2.setText(_translate("MainWindow", "导入风格图片"))
        self.pushButton.setText(_translate("MainWindow", "生成图片"))
        self.pre_bef_button3.setText(_translate("MainWindow", "预览"))
        self.make_project_dir_button.setText(_translate("MainWindow", "选择工程目录"))
        self.label.setText(_translate("MainWindow", "进度信息："))
        self.reset_button.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-family:\'宋体\'; color:#242424;\">1. 对页面初始化，保留工作目录。</span></p><p align=\"justify\"><span style=\" font-family:\'宋体\'; color:#242424;\">2. 删除保存过程中生成的lerp_output，</span><span style=\" font-family:\'Calibri\'; color:#242424;\">temp</span><span style=\" font-family:\'宋体\'; color:#242424;\">和</span><span style=\" font-family:\'Calibri\'; color:#242424;\">seamless_output</span><span style=\" font-family:\'宋体\'; color:#242424;\">文件</span></p></body></html>"))
        self.reset_button.setText(_translate("MainWindow", "复位"))
        self.delete_files_button.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-family:\'宋体\'; color:#1e1e1e;\">1. 删除 style_output 文件</span></p><p align=\"justify\"><span style=\" font-family:\'宋体\'; color:#1e1e1e;\">2. 删除由DDS贴图转化的</span><span style=\" font-family:\'Calibri\'; color:#1e1e1e;\">JPG</span><span style=\" font-family:\'宋体\'; color:#1e1e1e;\">，</span><span style=\" font-family:\'Calibri\'; color:#1e1e1e;\">TGA</span><span style=\" font-family:\'宋体\'; color:#1e1e1e;\">图片</span></p><p align=\"justify\"><span style=\" font-family:\'宋体\'; color:#1e1e1e;\">3. 删除经Exapnd操作产生的图片</span></p><p align=\"justify\"><span style=\" font-family:\'Calibri\'; color:#1e1e1e;\"/></p></body></html>"))
        self.delete_files_button.setText(_translate("MainWindow", "清空缓存"))
        self.action3.setText(_translate("MainWindow", "3"))
