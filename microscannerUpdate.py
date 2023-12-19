# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scannerUpdate.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MicroscannerTest(object):
    def setupUi(self, MicroscannerTest):
        MicroscannerTest.setObjectName("MicroscannerTest")
        MicroscannerTest.resize(1366, 915)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setKerning(True)
        MicroscannerTest.setFont(font)
        MicroscannerTest.setWindowTitle("Microscanner Test")
        MicroscannerTest.setLayoutDirection(QtCore.Qt.LeftToRight)
        MicroscannerTest.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MicroscannerTest)
        self.centralwidget.setObjectName("centralwidget")
        self.capturelbl = QtWidgets.QLabel(self.centralwidget)
        self.capturelbl.setGeometry(QtCore.QRect(280, 30, 800, 561))
        self.capturelbl.setFrameShape(QtWidgets.QFrame.Box)
        self.capturelbl.setFrameShadow(QtWidgets.QFrame.Plain)
        self.capturelbl.setLineWidth(1)
        self.capturelbl.setText("")
        self.capturelbl.setObjectName("capturelbl")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(1090, 0, 260, 851))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.openCam_btn = QtWidgets.QPushButton(self.groupBox_2)
        self.openCam_btn.setGeometry(QtCore.QRect(0, 30, 261, 30))
        self.openCam_btn.setObjectName("openCam_btn")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setGeometry(QtCore.QRect(0, 70, 260, 101))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setFlat(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.exposureMode = QtWidgets.QComboBox(self.groupBox_4)
        self.exposureMode.setGeometry(QtCore.QRect(10, 30, 241, 30))
        self.exposureMode.setObjectName("exposureMode")
        self.exposure_slider = QtWidgets.QSlider(self.groupBox_4)
        self.exposure_slider.setGeometry(QtCore.QRect(10, 70, 241, 22))
        self.exposure_slider.setProperty("value", 40)
        self.exposure_slider.setOrientation(QtCore.Qt.Horizontal)
        self.exposure_slider.setObjectName("exposure_slider")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setGeometry(QtCore.QRect(0, 170, 260, 161))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setFlat(True)
        self.groupBox_5.setObjectName("groupBox_5")
        self.WBMode = QtWidgets.QComboBox(self.groupBox_5)
        self.WBMode.setGeometry(QtCore.QRect(10, 30, 241, 30))
        self.WBMode.setObjectName("WBMode")
        self.R_slider = QtWidgets.QSlider(self.groupBox_5)
        self.R_slider.setGeometry(QtCore.QRect(29, 70, 221, 22))
        self.R_slider.setOrientation(QtCore.Qt.Horizontal)
        self.R_slider.setObjectName("R_slider")
        self.G_slider = QtWidgets.QSlider(self.groupBox_5)
        self.G_slider.setGeometry(QtCore.QRect(29, 100, 221, 22))
        self.G_slider.setOrientation(QtCore.Qt.Horizontal)
        self.G_slider.setObjectName("G_slider")
        self.B_slider = QtWidgets.QSlider(self.groupBox_5)
        self.B_slider.setGeometry(QtCore.QRect(30, 130, 221, 22))
        self.B_slider.setOrientation(QtCore.Qt.Horizontal)
        self.B_slider.setObjectName("B_slider")
        self.label_4 = QtWidgets.QLabel(self.groupBox_5)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 16, 16))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        self.label_6.setGeometry(QtCore.QRect(10, 100, 16, 16))
        self.label_6.setObjectName("label_6")
        self.label_9 = QtWidgets.QLabel(self.groupBox_5)
        self.label_9.setGeometry(QtCore.QRect(10, 130, 16, 16))
        self.label_9.setObjectName("label_9")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setGeometry(QtCore.QRect(0, 340, 260, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setFlat(True)
        self.groupBox_6.setObjectName("groupBox_6")
        self.brightness_slider = QtWidgets.QSlider(self.groupBox_6)
        self.brightness_slider.setGeometry(QtCore.QRect(10, 30, 241, 22))
        self.brightness_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brightness_slider.setObjectName("brightness_slider")
        self.digitalShift_slider = QtWidgets.QSlider(self.groupBox_6)
        self.digitalShift_slider.setGeometry(QtCore.QRect(10, 90, 241, 22))
        self.digitalShift_slider.setOrientation(QtCore.Qt.Horizontal)
        self.digitalShift_slider.setObjectName("digitalShift_slider")
        self.label_3 = QtWidgets.QLabel(self.groupBox_6)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 131, 20))
        self.label_3.setObjectName("label_3")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_7.setGeometry(QtCore.QRect(0, 460, 260, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setFlat(True)
        self.groupBox_7.setObjectName("groupBox_7")
        self.gainRaw_slider = QtWidgets.QSlider(self.groupBox_7)
        self.gainRaw_slider.setGeometry(QtCore.QRect(10, 40, 241, 22))
        self.gainRaw_slider.setOrientation(QtCore.Qt.Horizontal)
        self.gainRaw_slider.setObjectName("gainRaw_slider")
        self.gamma_slider = QtWidgets.QSlider(self.groupBox_7)
        self.gamma_slider.setGeometry(QtCore.QRect(10, 100, 241, 22))
        self.gamma_slider.setOrientation(QtCore.Qt.Horizontal)
        self.gamma_slider.setObjectName("gamma_slider")
        self.label_5 = QtWidgets.QLabel(self.groupBox_7)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 131, 20))
        self.label_5.setObjectName("label_5")
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_8.setGeometry(QtCore.QRect(0, 600, 260, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setFlat(True)
        self.groupBox_8.setObjectName("groupBox_8")
        self.denoising_slider = QtWidgets.QSlider(self.groupBox_8)
        self.denoising_slider.setGeometry(QtCore.QRect(10, 90, 241, 22))
        self.denoising_slider.setOrientation(QtCore.Qt.Horizontal)
        self.denoising_slider.setObjectName("denoising_slider")
        self.denoising_lbl = QtWidgets.QLabel(self.groupBox_8)
        self.denoising_lbl.setGeometry(QtCore.QRect(10, 60, 131, 20))
        self.denoising_lbl.setObjectName("denoising_lbl")
        self.denoising_cb = QtWidgets.QCheckBox(self.groupBox_8)
        self.denoising_cb.setGeometry(QtCore.QRect(10, 30, 70, 17))
        self.denoising_cb.setObjectName("denoising_cb")
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_9.setGeometry(QtCore.QRect(0, 730, 260, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_9.setFont(font)
        self.groupBox_9.setFlat(True)
        self.groupBox_9.setObjectName("groupBox_9")
        self.sharpness_slider = QtWidgets.QSlider(self.groupBox_9)
        self.sharpness_slider.setGeometry(QtCore.QRect(10, 100, 241, 22))
        self.sharpness_slider.setOrientation(QtCore.Qt.Horizontal)
        self.sharpness_slider.setObjectName("sharpness_slider")
        self.denoising_slider_3 = QtWidgets.QLabel(self.groupBox_9)
        self.denoising_slider_3.setGeometry(QtCore.QRect(10, 70, 131, 20))
        self.denoising_slider_3.setObjectName("denoising_slider_3")
        self.sharpness_cb = QtWidgets.QCheckBox(self.groupBox_9)
        self.sharpness_cb.setGeometry(QtCore.QRect(10, 40, 70, 17))
        self.sharpness_cb.setObjectName("sharpness_cb")
        self.AreaScan = QtWidgets.QGroupBox(self.centralwidget)
        self.AreaScan.setGeometry(QtCore.QRect(10, 400, 260, 151))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.AreaScan.setFont(font)
        self.AreaScan.setAlignment(QtCore.Qt.AlignCenter)
        self.AreaScan.setFlat(True)
        self.AreaScan.setObjectName("AreaScan")
        self.widthScan_text = QtWidgets.QLineEdit(self.AreaScan)
        self.widthScan_text.setGeometry(QtCore.QRect(90, 30, 161, 30))
        self.widthScan_text.setObjectName("widthScan_text")
        self.heightScan_text = QtWidgets.QLineEdit(self.AreaScan)
        self.heightScan_text.setGeometry(QtCore.QRect(90, 70, 161, 30))
        self.heightScan_text.setObjectName("heightScan_text")
        self.setArea_btn = QtWidgets.QPushButton(self.AreaScan)
        self.setArea_btn.setGeometry(QtCore.QRect(10, 110, 241, 30))
        self.setArea_btn.setObjectName("setArea_btn")
        self.label = QtWidgets.QLabel(self.AreaScan)
        self.label.setGeometry(QtCore.QRect(10, 30, 61, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.AreaScan)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 71, 30))
        self.label_2.setObjectName("label_2")
        self.AreaScan_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.AreaScan_2.setGeometry(QtCore.QRect(10, 240, 260, 161))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.AreaScan_2.setFont(font)
        self.AreaScan_2.setAlignment(QtCore.Qt.AlignCenter)
        self.AreaScan_2.setFlat(True)
        self.AreaScan_2.setObjectName("AreaScan_2")
        self.xHomeSlide_text = QtWidgets.QLineEdit(self.AreaScan_2)
        self.xHomeSlide_text.setGeometry(QtCore.QRect(40, 30, 211, 30))
        self.xHomeSlide_text.setObjectName("xHomeSlide_text")
        self.yHomeSlide_text = QtWidgets.QLineEdit(self.AreaScan_2)
        self.yHomeSlide_text.setGeometry(QtCore.QRect(40, 70, 211, 30))
        self.yHomeSlide_text.setObjectName("yHomeSlide_text")
        self.setHomeSlide_btn = QtWidgets.QPushButton(self.AreaScan_2)
        self.setHomeSlide_btn.setGeometry(QtCore.QRect(10, 120, 241, 30))
        self.setHomeSlide_btn.setObjectName("setHomeSlide_btn")
        self.label_7 = QtWidgets.QLabel(self.AreaScan_2)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 21, 30))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.AreaScan_2)
        self.label_8.setGeometry(QtCore.QRect(10, 70, 21, 30))
        self.label_8.setObjectName("label_8")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 20, 260, 221))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.status_txt = QtWidgets.QTextEdit(self.groupBox_3)
        self.status_txt.setEnabled(True)
        self.status_txt.setGeometry(QtCore.QRect(0, 110, 261, 60))
        self.status_txt.setAutoFillBackground(False)
        self.status_txt.setReadOnly(True)
        self.status_txt.setObjectName("status_txt")
        self.comCombo = QtWidgets.QComboBox(self.groupBox_3)
        self.comCombo.setGeometry(QtCore.QRect(0, 30, 261, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comCombo.setFont(font)
        self.comCombo.setToolTip("")
        self.comCombo.setWhatsThis("")
        self.comCombo.setCurrentText("")
        self.comCombo.setObjectName("comCombo")
        self.connect_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.connect_btn.setGeometry(QtCore.QRect(100, 70, 161, 30))
        self.connect_btn.setObjectName("connect_btn")
        self.comRefresh_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.comRefresh_btn.setGeometry(QtCore.QRect(0, 70, 91, 30))
        self.comRefresh_btn.setObjectName("comRefresh_btn")
        self.fokus_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.fokus_btn.setGeometry(QtCore.QRect(140, 180, 121, 30))
        self.fokus_btn.setObjectName("fokus_btn")
        self.prepare_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.prepare_btn.setGeometry(QtCore.QRect(0, 180, 121, 30))
        self.prepare_btn.setObjectName("prepare_btn")
        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(180, 740, 55, 16))
        self.time_label.setObjectName("time_label")
        self.total_label = QtWidgets.QLabel(self.centralwidget)
        self.total_label.setGeometry(QtCore.QRect(20, 740, 91, 20))
        self.total_label.setObjectName("total_label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 560, 260, 101))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")
        self.namaSlide_text = QtWidgets.QLineEdit(self.groupBox)
        self.namaSlide_text.setGeometry(QtCore.QRect(0, 30, 261, 30))
        self.namaSlide_text.setObjectName("namaSlide_text")
        self.namaSlide_btn = QtWidgets.QPushButton(self.groupBox)
        self.namaSlide_btn.setGeometry(QtCore.QRect(10, 70, 241, 30))
        self.namaSlide_btn.setObjectName("namaSlide_btn")
        self.groupBox_10 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_10.setGeometry(QtCore.QRect(280, 610, 381, 111))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(12)
        self.groupBox_10.setFont(font)
        self.groupBox_10.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_10.setFlat(True)
        self.groupBox_10.setObjectName("groupBox_10")
        self.currRow_lbl = QtWidgets.QLabel(self.groupBox_10)
        self.currRow_lbl.setGeometry(QtCore.QRect(10, 60, 80, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.currRow_lbl.setFont(font)
        self.currRow_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.currRow_lbl.setObjectName("currRow_lbl")
        self.label_15 = QtWidgets.QLabel(self.groupBox_10)
        self.label_15.setGeometry(QtCore.QRect(10, 30, 80, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.currCol_lbl = QtWidgets.QLabel(self.groupBox_10)
        self.currCol_lbl.setGeometry(QtCore.QRect(120, 60, 80, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.currCol_lbl.setFont(font)
        self.currCol_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.currCol_lbl.setObjectName("currCol_lbl")
        self.label_16 = QtWidgets.QLabel(self.groupBox_10)
        self.label_16.setGeometry(QtCore.QRect(120, 30, 80, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.currImg_lbl = QtWidgets.QLabel(self.groupBox_10)
        self.currImg_lbl.setGeometry(QtCore.QRect(220, 60, 140, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.currImg_lbl.setFont(font)
        self.currImg_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.currImg_lbl.setObjectName("currImg_lbl")
        self.label_19 = QtWidgets.QLabel(self.groupBox_10)
        self.label_19.setGeometry(QtCore.QRect(220, 30, 140, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.groupBox_11 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_11.setGeometry(QtCore.QRect(710, 610, 381, 111))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(12)
        self.groupBox_11.setFont(font)
        self.groupBox_11.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_11.setFlat(True)
        self.groupBox_11.setObjectName("groupBox_11")
        self.sumRow_lbl = QtWidgets.QLabel(self.groupBox_11)
        self.sumRow_lbl.setGeometry(QtCore.QRect(10, 60, 80, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.sumRow_lbl.setFont(font)
        self.sumRow_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.sumRow_lbl.setObjectName("sumRow_lbl")
        self.label_23 = QtWidgets.QLabel(self.groupBox_11)
        self.label_23.setGeometry(QtCore.QRect(10, 30, 80, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.sumCol_lbl = QtWidgets.QLabel(self.groupBox_11)
        self.sumCol_lbl.setGeometry(QtCore.QRect(120, 60, 80, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.sumCol_lbl.setFont(font)
        self.sumCol_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.sumCol_lbl.setObjectName("sumCol_lbl")
        self.label_25 = QtWidgets.QLabel(self.groupBox_11)
        self.label_25.setGeometry(QtCore.QRect(120, 30, 80, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_25.setFont(font)
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.sumImg_lbl = QtWidgets.QLabel(self.groupBox_11)
        self.sumImg_lbl.setGeometry(QtCore.QRect(220, 60, 140, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.sumImg_lbl.setFont(font)
        self.sumImg_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.sumImg_lbl.setObjectName("sumImg_lbl")
        self.label_27 = QtWidgets.QLabel(self.groupBox_11)
        self.label_27.setGeometry(QtCore.QRect(220, 30, 140, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setObjectName("label_27")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(10, 680, 261, 30))
        self.start_btn.setObjectName("start_btn")
        self.groupBox_12 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_12.setGeometry(QtCore.QRect(500, 720, 341, 141))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.groupBox_12.setFont(font)
        self.groupBox_12.setObjectName("groupBox_12")
        self.rightButton = QtWidgets.QPushButton(self.groupBox_12)
        self.rightButton.setGeometry(QtCore.QRect(220, 70, 93, 28))
        self.rightButton.setObjectName("rightButton")
        self.upButton = QtWidgets.QPushButton(self.groupBox_12)
        self.upButton.setGeometry(QtCore.QRect(120, 40, 93, 28))
        self.upButton.setObjectName("upButton")
        self.downButton = QtWidgets.QPushButton(self.groupBox_12)
        self.downButton.setGeometry(QtCore.QRect(120, 100, 93, 28))
        self.downButton.setObjectName("downButton")
        self.leftButton = QtWidgets.QPushButton(self.groupBox_12)
        self.leftButton.setGeometry(QtCore.QRect(20, 70, 93, 28))
        self.leftButton.setObjectName("leftButton")
        MicroscannerTest.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MicroscannerTest)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 26))
        self.menubar.setObjectName("menubar")
        MicroscannerTest.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MicroscannerTest)
        self.statusbar.setObjectName("statusbar")
        MicroscannerTest.setStatusBar(self.statusbar)

        self.retranslateUi(MicroscannerTest)
        QtCore.QMetaObject.connectSlotsByName(MicroscannerTest)

    def retranslateUi(self, MicroscannerTest):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox_2.setTitle(_translate("MicroscannerTest", "Camera Setting"))
        self.openCam_btn.setText(_translate("MicroscannerTest", "Open Cam"))
        self.groupBox_4.setTitle(_translate("MicroscannerTest", "Exposure"))
        self.groupBox_5.setTitle(_translate("MicroscannerTest", "White Balance"))
        self.label_4.setText(_translate("MicroscannerTest", "R"))
        self.label_6.setText(_translate("MicroscannerTest", "G"))
        self.label_9.setText(_translate("MicroscannerTest", "B"))
        self.groupBox_6.setTitle(_translate("MicroscannerTest", "Brightness"))
        self.label_3.setText(_translate("MicroscannerTest", "DigitalShift"))
        self.groupBox_7.setTitle(_translate("MicroscannerTest", "GainRaw"))
        self.label_5.setText(_translate("MicroscannerTest", "Gamma"))
        self.groupBox_8.setTitle(_translate("MicroscannerTest", "Denoising"))
        self.denoising_lbl.setText(_translate("MicroscannerTest", "Value"))
        self.denoising_cb.setText(_translate("MicroscannerTest", "Open"))
        self.groupBox_9.setTitle(_translate("MicroscannerTest", "Sharpeness"))
        self.denoising_slider_3.setText(_translate("MicroscannerTest", "Value"))
        self.sharpness_cb.setText(_translate("MicroscannerTest", "Open"))
        self.AreaScan.setTitle(_translate("MicroscannerTest", "Area Scan"))
        self.setArea_btn.setText(_translate("MicroscannerTest", "Set Area Scan"))
        self.label.setText(_translate("MicroscannerTest", "Lebar"))
        self.label_2.setText(_translate("MicroscannerTest", "Panjang"))
        self.AreaScan_2.setTitle(_translate("MicroscannerTest", "Koordinat Awal Slide"))
        self.setHomeSlide_btn.setText(_translate("MicroscannerTest", "Set Koordinat Awal"))
        self.label_7.setText(_translate("MicroscannerTest", "X"))
        self.label_8.setText(_translate("MicroscannerTest", "Y"))
        self.groupBox_3.setTitle(_translate("MicroscannerTest", "Setup Serial"))
        self.connect_btn.setText(_translate("MicroscannerTest", "Connect"))
        self.comRefresh_btn.setText(_translate("MicroscannerTest", "Refresh"))
        self.fokus_btn.setText(_translate("MicroscannerTest", "Set Fokus"))
        self.prepare_btn.setText(_translate("MicroscannerTest", "Persiapan"))
        self.time_label.setText(_translate("MicroscannerTest", "TextLabel"))
        self.total_label.setText(_translate("MicroscannerTest", "TextLabel"))
        self.groupBox.setTitle(_translate("MicroscannerTest", "Nama Slide"))
        self.namaSlide_btn.setText(_translate("MicroscannerTest", "Set Nama Slide"))
        self.groupBox_10.setTitle(_translate("MicroscannerTest", "Posisi"))
        self.currRow_lbl.setText(_translate("MicroscannerTest", "-"))
        self.label_15.setText(_translate("MicroscannerTest", "Baris"))
        self.currCol_lbl.setText(_translate("MicroscannerTest", "-"))
        self.label_16.setText(_translate("MicroscannerTest", "Kolom"))
        self.currImg_lbl.setText(_translate("MicroscannerTest", "-"))
        self.label_19.setText(_translate("MicroscannerTest", "Gambar"))
        self.groupBox_11.setTitle(_translate("MicroscannerTest", "Total"))
        self.sumRow_lbl.setText(_translate("MicroscannerTest", "-"))
        self.label_23.setText(_translate("MicroscannerTest", "Baris"))
        self.sumCol_lbl.setText(_translate("MicroscannerTest", "-"))
        self.label_25.setText(_translate("MicroscannerTest", "Kolom"))
        self.sumImg_lbl.setText(_translate("MicroscannerTest", "-"))
        self.label_27.setText(_translate("MicroscannerTest", "Gambar"))
        self.start_btn.setText(_translate("MicroscannerTest", "Start"))
        self.groupBox_12.setTitle(_translate("MicroscannerTest", "_____________________ calibration ____________________"))
        self.rightButton.setText(_translate("MicroscannerTest", "RIGHT"))
        self.upButton.setText(_translate("MicroscannerTest", "UP"))
        self.downButton.setText(_translate("MicroscannerTest", "DOWN"))
        self.leftButton.setText(_translate("MicroscannerTest", "LEFT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MicroscannerTest = QtWidgets.QMainWindow()
    ui = Ui_MicroscannerTest()
    ui.setupUi(MicroscannerTest)
    MicroscannerTest.show()
    sys.exit(app.exec_())