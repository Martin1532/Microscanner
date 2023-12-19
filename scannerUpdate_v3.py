# D:\Python\Scripts\activate
# D:\Python\Scripts

import sys
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QCheckBox, QWidget, QShortcut, QLabel, QHBoxLayout, QPushButton, QFileDialog, QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QKeySequence
from click import command
import cv2
from numpy.lib.function_base import select
import serial
import serial.tools.list_ports
import pyvips
import os
import gc
# from Python.slide.dzi.rescale import rescale_frame
import marscam
import time
import datetime
import numpy as np
import shutil
import re
from pathlib import Path
import webbrowser
import re
import pathlib


class MicroscannerTest(QMainWindow):
    def __init__(self):
        super(MicroscannerTest, self).__init__()
        os.chdir(r'D:\KP\Github\neurabotMicroscanner-main\Python')
        dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir)
        # os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python')
        loadUi('scannerV3.ui', self)
        self.setWindowIcon(QIcon("neurabot-favicon.png"))
        self.image = None
        self.start = False
        self.popup = False
        self.opencam = False
        self.onCapture = False
        self.lastCapture = 0
        self.currRow = 0
        self.currCol = 0
        self.currImage = 0
        self._Row=0
        self._Col=0
        # self.koordinatStart=[0,0] #koordinat (x,y)
        # self.koordinatEnd=[0,0] #koordinat (x,y)
        self.koordinat=[0,0] #koordinat (x,y)
        self.zPosition=10100
        self.startPoint=[0,0]  #koordinat (x,y)
        self.endPoint=[0,0]  #koordinat (x,y)

        self.directory = ['preparat 0',
                          'preparat 1', 'preparat 2', 'preparat 3']
        self.start_btn.clicked.connect(self.startconnect)
        self.stop_btn.clicked.connect(self.stopScan)
        self.namaSlide_btn.clicked.connect(self.setNamaSlide)
        # self.auto_btn.clicked.connect(self.setfokusconnect)
        self.openCam_btn.clicked.connect(self.openCamconnect)
        self.comRefresh_btn.clicked.connect(self.addComboItem)
        self.startPoint_btn.clicked.connect(self.setPointStart)
        self.endPoint_btn.clicked.connect(self.setPointEnd)
        self.auto_btn.clicked.connect(self.autoFocus)
       

        self.delayCapture.valueChanged.connect(self.setDelayCapture)
        self.delayCapture.setMinimum(0.0)
        self.delayCapture.setMaximum(100)
        self.delayCapture.valueChanged.connect(self.brightness_value)

        self.speedScan.valueChanged.connect(self.setSpeedScan)
        self.speedScan.setMinimum(0)
        self.speedScan.setMaximum(100)
        self.speedScan.valueChanged.connect(self.brightness_value)

        self.over.addItems(['10', '15','30'])
        self.over.currentIndexChanged.connect(self.itemOver)
        self.over.activated.connect(self.setOver)
        

        self.openIfDone.toggled.connect(self.openDone)
        self.openIfDone.setChecked(False)
        
        # Connect click button 
        self.r_btn.clicked.connect(self.rightConnect)
        self.d_btn.clicked.connect(self.downConnect)
        self.l_btn.clicked.connect(self.leftConnect)
        self.u_btn.clicked.connect(self.upConnect)
        
        self.ru_btn.clicked.connect(self.RightUpConnect)
        self.rd_btn.clicked.connect(self.RightDownConnect)
        self.lu_btn.clicked.connect(self.LeftUpConnect)
        self.ld_btn.clicked.connect(self.LeftDownConnect)
        
        
        self.t_btn.clicked.connect(self.zUpConnect)
        self.b_btn.clicked.connect(self.zDownConnect)
        self.home_btn.clicked.connect(self.homeConnect)
        self.connect_btn.clicked.connect(self.portconnect)
        
        # Create timers for each button
        self.up_timer = QTimer(self)
        self.down_timer = QTimer(self)
        self.left_timer = QTimer(self)
        self.right_timer = QTimer(self)
        
        self.Rightup_timer = QTimer(self)
        self.Rightdown_timer = QTimer(self)
        self.Leftup_timer = QTimer(self)
        self.Leftdown_timer = QTimer(self)
        
        self.zup_timer = QTimer(self)
        self.zdown_timer = QTimer(self)
        
        # Connect the timer timeouts to functions
        self.up_timer.timeout.connect(self.upConnect)
        self.down_timer.timeout.connect(self.downConnect)
        self.left_timer.timeout.connect(self.leftConnect)
        self.right_timer.timeout.connect(self.rightConnect)
        
        self.Rightup_timer.timeout.connect(self.RightUpConnect)
        self.Rightdown_timer.timeout.connect(self.RightDownConnect)
        self.Leftup_timer.timeout.connect(self.LeftUpConnect)
        self.Leftdown_timer.timeout.connect(self.LeftDownConnect)
        
        self.zup_timer.timeout.connect(self.zUpConnect)
        self.zdown_timer.timeout.connect(self.zDownConnect)
        
        # Connect button pressed and released events to start/stop timers
        self.u_btn.pressed.connect(self.up_timer.start) 
        self.u_btn.released.connect(self.up_timer.stop)
        
        self.d_btn.pressed.connect(self.down_timer.start)
        self.d_btn.released.connect(self.down_timer.stop)

        self.l_btn.pressed.connect(self.left_timer.start)
        self.l_btn.released.connect(self.left_timer.stop)

        self.r_btn.pressed.connect(self.right_timer.start)
        self.r_btn.released.connect(self.right_timer.stop)
        
        self.ru_btn.pressed.connect(self.Rightup_timer.start)
        self.ru_btn.released.connect(self.Rightup_timer.stop)

        self.rd_btn.pressed.connect(self.Rightdown_timer.start)
        self.rd_btn.released.connect(self.Rightdown_timer.stop)

        self.lu_btn.pressed.connect(self.Leftup_timer.start)
        self.lu_btn.released.connect(self.Leftup_timer.stop)

        self.ld_btn.pressed.connect(self.Leftdown_timer.start)
        self.ld_btn.released.connect(self.Leftdown_timer.stop)
        
        self.t_btn.pressed.connect(self.zup_timer.start)
        self.t_btn.released.connect(self.zup_timer.stop)

        self.b_btn.pressed.connect(self.zdown_timer.start)
        self.b_btn.released.connect(self.zdown_timer.stop)
        

        self.open_btn.clicked.connect(self.open_file_dialog)
        self.file_list = QLineEdit()

        self.tiff_btn.clicked.connect(self.tif_file_dialog)
        self.dir_tif_edit = QLineEdit()

        self.denoising_cb.stateChanged.connect(self.denoising_connect)
        self.sharpness_cb.stateChanged.connect(self.sharpness_connect)

        self.exposure_slider.valueChanged.connect(self.exposure_value)
        self.exposure_slider.setMinimum(16)
        self.exposure_slider.setMaximum(10000000)
        self.exposure_slider.setTickInterval(1)
        self.brightness_slider.valueChanged.connect(self.brightness_value)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(100)
        self.digitalShift_slider.valueChanged.connect(self.digitalShift_value)
        self.digitalShift_slider.setMinimum(0)
        self.digitalShift_slider.setMaximum(4)
        self.digitalShift_slider.setTickInterval(0.1)
        self.gainRaw_slider.valueChanged.connect(self.gainRaw_value)
        self.gainRaw_slider.setMinimum(0)
        self.gainRaw_slider.setMaximum(320)
        self.gainRaw_slider.setTickInterval(1)
        self.gamma_slider.valueChanged.connect(self.gamma_value)
        self.gamma_slider.setMinimum(0)
        self.gamma_slider.setMaximum(4)
        self.gamma_slider.setTickInterval(0.01)
        self.denoising_slider.valueChanged.connect(self.denoising_value)
        self.denoising_slider.setMinimum(0)
        self.denoising_slider.setMaximum(100)
        self.sharpness_slider.valueChanged.connect(self.sharpness_value)
        self.sharpness_slider.setMinimum(0)
        self.sharpness_slider.setMaximum(100)
        self.R_slider.valueChanged.connect(self.R_value)
        self.R_slider.setMinimum(0)
        self.R_slider.setMaximum(150)
        self.R_slider.setTickInterval(0.1)
        self.G_slider.valueChanged.connect(self.G_value)
        self.G_slider.setMinimum(0)
        self.G_slider.setMaximum(150)
        self.G_slider.setTickInterval(0.1)
        self.B_slider.valueChanged.connect(self.B_value)
        self.B_slider.setMinimum(0)
        self.B_slider.setMaximum(150)
        self.B_slider.setTickInterval(0.1)

        self.exposureMode.addItems(['Off', 'Once', 'Continuous'])
        self.exposureMode.currentIndexChanged.connect(self.exposureModeChange)
        self.WBMode.addItems(['Off', 'Once', 'Continuous'])
        self.WBMode.currentIndexChanged.connect(self.WBModeChange)
        self.tempdirectory = ""

        # even keyboard
        self.shortcut_right = QShortcut(QKeySequence('Ctrl+RIGHT'), self)
        self.shortcut_right.activated.connect(self.rightConnect)

        self.shortcut_left = QShortcut(QKeySequence('Ctrl+LEFT'), self)
        self.shortcut_left.activated.connect(self.leftConnect)

        self.shortcut_up = QShortcut(QKeySequence('Ctrl+UP'), self)
        self.shortcut_up.activated.connect(self.upConnect)

        self.shortcut_down = QShortcut(QKeySequence('Ctrl+DOWN'), self)
        self.shortcut_down.activated.connect(self.downConnect)

        self.currslide = 0
        self.countcolumn = 0
        self.countrow = 0
        self.startrow = 0
        self.endrow = 15
        self.startcolumn = 0
        self.endcolumn = 14
        self.XX = 0

        # TAMBAHAN
        self.countRight = 0
        self.countLeft = 0
        self.countUp = 0
        self.countDown = 0
        self.modeCalibration = False
        self.sttPreparate = True
        self.openFile = False
        self.pathTif = r'D:\Neurabot\Microscanner\V2\Pemrograman\Python\image'

        self.gotif = CreatTiff()

        self.thread = QThread()
        self.createwsi = False
        self.wsi = wsiThread()
        self.wsi.finishWsi.connect(self.wsiFinish)
        self.wsi.errorWsi.connect(self.wsiError)

        self.video = VideoThread()
        self.video.rescale_factor = 25
        self.video.update_frame.connect(self.update_frame)
        self.video.fileExist.connect(self.fileReady)

        self.ser = None
        self.serialcheck()
        self.addComboItem()
        self.comCombo.currentIndexChanged.connect(self.comComboChanged)

    def addComboItem(self):
        self.comCombo.clear()
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            print("{}: {}".format(port, desc))
            self.comCombo.addItem("{}: {}".format(port, desc))

    def comComboChanged(self, i):
        print(self.comCombo.currentText())

    def startconnect(self):
        if not self.start:
            self.currImage = 0

            if (self.tempdirectory == ""):
                self.tempdirectory = "temp"+str(round(time.time() * 1000))
            self.scanConfirmation()
            
        else:
            self.sendSerial("0")
        self.serialcheck()

    def portconnect(self):
        # port = self.port_txt.text()
        # print(self.comCombo.itemText(i).split(':')[0])
        print(self.comCombo.currentText().split(':')[0])
        port = self.comCombo.currentText().split(':')[0]
        # print(port)
        self.serConnect(port)

    def serConnect(self, com):
        try:
            self.ser = serial.Serial(com, baudrate=115200)
            self.status_txt.setText('Serial OK')
        except:
            self.status_txt.setText('Port Serial Tidak Tersambung')

    def tif_file_dialog(self):
        tifFolder = QFileDialog.getExistingDirectory(
            self, ("open Folder"), "image")

        if tifFolder:
            self.path_folder = Path(tifFolder)
            self.folder_name = os.path.basename(self.path_folder)
            self.folder = os.path.splitext(self.folder_name)

        cc = []
        vv = []
        lk = []
        self.dir_list = os.listdir(self.pathTif + "\\" + self.folder[0])

        pj = ''.join(map(str, self.dir_list))
        pp = pj.split(".jpg")
        for o in pp:
            kk = o.split("_")
            cd = np.array(kk)
            lk.append(cd)

        i = 0
        while i < len(self.dir_list):
            cc.append(lk[i][0])
            vv.append(lk[i][1])
            i += 1

        res = [eval(i) for i in cc]
        ros = [eval(i) for i in vv]

        maxRow = res[0]
        for i in range(1, len(res)):
            if res[i] > maxRow:
                maxRow = res[i]

        maxCol = ros[0]
        for i in range(1, len(ros)):
            if ros[i] > maxCol:
                maxCol = ros[i]
        maxRow = maxRow-1
        maxCol = maxCol-1
        try:
            self.gotif.generateTiff(self.folder[0], maxRow, maxCol)
        except ValueError:
            print("error")
        else:
            self.status_txt.clear()
            self.status_txt.setText(
                'successful saving ' + self.folder[0]+'.tif')
            # self.gotif.deleteFile(self.folder[0])

    def open_file_dialog(self):
        self.creatUrl = 'localhost/slide/?slide='
        filenames, ok = QFileDialog.getOpenFileName(self, ("Open File"),
                                                    "slide\\dzi\\",
                                                    ("Images (*.dzi)"))
        if filenames:
            self.path = str(Path(filenames))
            self.file_name = os.path.basename(self.path)
            self.file = os.path.splitext(self.file_name)
            self.creatUrl = self.creatUrl+self.file[0]
            webbrowser.open(self.creatUrl)

    

    def setDelayCapture(self):
        size=self.delayCapture.value()
        print(size)
        command = str("P:" + size)
        self.sendSerial(command)
        
        
    def setSpeedScan(self):
        size=self.speedScan.value()
        print(size)
        command = str("E:" + size)
        self.sendSerial(command)

    def itemOver(self, i):
        for stt in range(self.over.count()):
            self.over.itemText(stt)

    def setOver(self):
        if self.over.currentIndex() == 0:
            print("10")
        elif self.over.currentIndex() ==1:
            print("15")
        elif self.over.currentIndex() ==2:
            print("30")

    def openDone(self):
        openIfDone = self.sender()
        if openIfDone.isChecked():
            self.openFile = True
        else:
            self.openFile = False

    def homeConnect(self):
        try:
            self.sendSerial("H")
        except:
            print("Device not connect!")
            self.status_txt.setText("Device not connect!")
        else:
            self.koordinat[0]=0
            self.koordinat[1]=0
            self.status_txt.setText('HOME')

    def rightConnect(self):
            try:
                self.sendSerial("R")
            except:
                print("Device not connect!")
                self.status_txt.setText("Device not connect!")
            else:
                self.koordinat[0] +=1
                self.status_txt.setText("KOORDINAT: {},{}".format(self.koordinat[0], self.koordinat[1]))

    def leftConnect(self):
            try:
                self.sendSerial("L")
            except:
                print("Device not connect!")
                self.status_txt.setText("Device not connect!")
            else:
                self.koordinat[0] -=1
                self.status_txt.setText("KOORDINAT: {},{}".format(self.koordinat[0], self.koordinat[1]))

    def upConnect(self):
            try:
                self.sendSerial("U")
            except:
                print("Device not connected!")
                self.status_txt.setText("Device not connected!")
            else:
                self.koordinat[1] += 1
                self.status_txt.setText("KOORDINAT: {},{}".format(self.koordinat[0], self.koordinat[1]))

    def downConnect(self):
            try:
                self.sendSerial("D")
            except:
                print("Device not connect!")
                self.status_txt.setText("Device not connect!")
            else:
                self.koordinat[1] -=1
                self.status_txt.setText("KOORDINAT: {},{}".format(self.koordinat[0], self.koordinat[1]))
                
    def RightUpConnect(self):
            try:
                self.sendSerial("RU")
            except:
                print("Device not connect!")
                self.status_txt.setText("Device not connect!")
            else:
                self.koordinat[0] += 1
                self.koordinat[1] += 1
                self.status_txt.setText("KOORDINAT: {},{}".format(self.koordinat[0], self.koordinat[1]))

    def LeftUpConnect(self):
            try:
                self.sendSerial("LU")
            except:
                print("Device not connect!")
                self.status_txt.setText("Device not connect!")
            else:
                self.koordinat[0] -= 1
                self.koordinat[1] += 1
                self.status_txt.setText("KOORDINAT: {},{}".format(self.koordinat[0], self.koordinat[1]))       
                
    def RightDownConnect(self):
            try:
                self.sendSerial("RD")
            except:
                print("Device not connect!")
                self.status_txt.setText("Device not connect!")
            else:
                self.koordinat[0] += 1
                self.koordinat[1] -= 1
                self.status_txt.setText("KOORDINAT: {},{}".format(self.koordinat[0], self.koordinat[1]))

    def LeftDownConnect(self):
            try:
                self.sendSerial("LD")
            except:
                print("Device not connect!")
                self.status_txt.setText("Device not connect!")
            else:
                self.koordinat[0] -= 1
                self.koordinat[1] -= 1
                self.status_txt.setText("KOORDINAT: {},{}".format(self.koordinat[0], self.koordinat[1]))          
                
                
    def zUpConnect(self):
        try:
            self.sendSerial("T")
        except:
            print("Device not connect!")
            self.status_txt.setText("Device not connect!")
        else:
            self.zPosition +=1
            self.status_txt.setText("Z Position : " + str(self.zPosition))

    def zDownConnect(self):
        try:
            if self.zPosition > 0:
                self.sendSerial("B")
            else:
                # self.status_txt.setText("Limit Button")
                print("limit")
        except:
            print("Device not connect!")
            self.status_txt.setText("Device not connect!")
        else:
            if self.zPosition < 1:
                self.zPosition=0
            else:
                self.zPosition -=1
            self.status_txt.setText("Z Position : " + str(self.zPosition))
            
    # def sendSerial(self, command):
    #     # Implementasi untuk mengirim perintah serial
    #     pass

    def setfokFusconnect(self):
       pass


    def saveimage(self):
        self.currImage += 1
        pading=5
        file_number=str(self.currImage).zfill(pading)
        if not os.path.exists("image/"+self.tempdirectory):
            os.makedirs("image/"+self.tempdirectory)

        # cv2.imwrite(self.directory[self.currslide]+'/'+ str(self.countcolumn) + ".jpg", self.image)
        # cv2.imwrite(self.tempdirectory+'/' + str(column) + "_"+str(row) + ".jpg", self.image)
        self.video.saveimage("image/" + self.tempdirectory +
                             '/' + str(file_number))

    def fileReady(self):
        # self.sendSerial("S")
        self.onCapture = True
        self.lastCapture = self.getMillis()

    def update_frame(self, img):
        if self.opencam:
            # ret, self.image = self.capture.read()
            # self.image = cv2.flip(self.image, 1)
            # self.image = self.cam.stream()
            self.displayImage(img)

    def openCamconnect(self):
        # self.cam = marscam.marscam()
        # self.cam.setCamera(0)
        # self.cam.openCamera()
        self.video.opencam()
        self.video.start()

        # self.exposure_slider.setValue(1000)

        self.video.setExposureAuto("Off")
        # self.video.setExposure(40000)
        self.video.setExposure(13159.5)
        self.video.setGainRaw(1.8)
        self.video.setGamma(1)
        self.video.setBrightness(50)
        self.video.setWhiteBalance("Off")
        self.video.setWBRatio("Red", 3.52)
        self.video.setWBRatio("Green", 1)
        self.video.setWBRatio("Blue", 1.47)
        self.opencam = True

    def displayImage(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:  # [0]=rows, [1]=cols, [2]=channels
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outImage = QImage(img, img.shape[1],
                          img.shape[0], img.strides[0], qformat)
        # BGR to RGB
        outImage = outImage.rgbSwapped()

        self.capturelbl.setPixmap(QPixmap.fromImage(outImage))
        self.capturelbl.setScaledContents(True)

    def exposureModeChange(self, i):

        # for count in range(self.exposureMode.count()):
        #     print(self.exposureMode.itemText(count))
        # print ("Current index",i,"selection changed ",self.exposureMode.currentText())
        # self.cam.setExposureAuto(self.exposureMode.currentText())
        self.video.setExposureAuto(self.exposureMode.currentText())

    def WBModeChange(self, i):

        # for count in range(self.exposureMode.count()):
        #     print(self.exposureMode.itemText(count))
        # print ("Current index",i,"selection changed ",self.exposureMode.currentText())
        # self.cam.setWBAuto(self.WBMode.currentText())
        self.video.setWhiteBalance(self.WBMode.currentText())

    def exposure_value(self):
        size = self.exposure_slider.value() / 10
        if self.opencam:
            # self.cam.setExposureTime(size)
            self.video.setExposure(size)

    def brightness_value(self):
        size = self.brightness_slider.value()
        if self.opencam:
            # self.cam.setBrightness(size)
            self.video.setBrightness(size)

    def digitalShift_value(self):
        size = self.digitalShift_slider.value()
        print("digital shift = " + str(size))
        if self.opencam:
            # self.cam.setdigitalShiftTime(size)
            self.video.setdigitalShift(size)

    def R_value(self):
        size = self.R_slider.value() / 10
        print("digital shift = " + str(size))
        if self.opencam:
            # self.cam.setdigitalShiftTime(size)
            self.video.setWBRatio("Red", size)

    def G_value(self):
        size = self.G_slider.value() / 10
        print("digital shift = " + str(size))
        if self.opencam:
            # self.cam.setdigitalShiftTime(size)
            self.video.setWBRatio("Green", size)

    def B_value(self):
        size = self.B_slider.value() / 10
        print("digital shift = " + str(size))
        if self.opencam:
            # self.cam.setdigitalShiftTime(size)
            self.video.setWBRatio("Blue", size)

    def gainRaw_value(self):
        size = self.gainRaw_slider.value() / 10
        # print("gainRaw = "+ str(size))
        if self.opencam:
            # self.cam.setgainRawTime(size)
            self.video.setGainRaw(size)

    def gamma_value(self):
        size = self.gamma_slider.value()
        # print("gamma = "+ str(size))
        if self.opencam:
            # self.cam.setgammaTime(size)
            self.video.setGamma(size)

    def denoising_value(self):
        size = self.denoising_slider.value()
        print("denoising = " + str(size))
        if self.opencam:
            # self.cam.setdenoisingTime(size)
            self.video.setdenoising(size)

    def sharpness_value(self):
        size = self.sharpness_slider.value()
        # print("sharpness shift = "+ str(size))
        if self.opencam:
            # self.cam.setsharpnessTime(size)
            self.video.setSharpness(size)

    def getMillis(self):
        time = datetime.datetime.now()
        milis = time.microsecond
        return milis

    def serialcheck(self):
        QTimer.singleShot(1, self.serialcheck)
        # time_str = time.strftime("%H:%M:%S")

        # now = self.getMillis()
        # self.time_label.setText(str(now))
        # if now - self.lastCapture > 1000:
        #     self.ser.write(str("C"+"\n").encode('utf-8'))

        try:
            now = self.getMillis()
            # self.time_label.setText(str(now))
            # self.time_label.setText(
            #     str(self.currRow) + ", " + str(self.currCol) + ", " + str(self.currImage))

            # self.currRow_lbl.setText(str(self.currRow))
            # self.currCol_lbl.setText(str(self.currCol))
            # self.currImg_lbl.setText(str(self.currImage))

            if self.onCapture and now - self.lastCapture > 800:
                # self.ser.flushInput()
                # self.ser.flushOutput()
                # self.ser.write(str("C"+"\n").encode('utf-8'))
                # self.sendSerial("m")
                pass

            while self.ser.inWaiting():
                text_serial = self.ser.readline().decode('ascii').strip()
                self.status_txt.setText(text_serial)
                if ';' in text_serial:
                    split = text_serial.split(';')
                    if (split[0] == "3"):
                        pass

                    elif (split[0] == "T"):
                        row = split[2]
                        col = split[1]
                        self.total_label.setText(
                            str(col) + ", " + str(row) + ", " + str(int(col) * int(row)))

                        self.sumRow_lbl.setText(str(row))
                        self.sumCol_lbl.setText(str(col))
                        self.sumImg_lbl.setText(str(int(col) * int(row)))

                        self.saveimage(split[1],split[2])

                elif text_serial == "N":
                    self.countcolumn = 0
                    self.currslide += 1
                    if self.currslide == 4:
                        self.currslide = 0
                        #     # ser.read

                elif text_serial == "F":
                    print("finish")
                    self.createwsi = True
                    # self.namaSlide_btn.setText("WAIT")
                    self.wsi.setDirectory(self.tempdirectory)
                    # self.wsi.setSlideNumber(self.tempdirectory)
                    self.status_txt.setText('Stop')
                    self.start_btn.setText('Start')
                    # self.ser.write(str("0").encode())
                    # self.start = not self.start
                    self.start = False
                    try:
                        self.wsi.start()
                    except:
                        None

                elif text_serial == "!" and not self.popup:
                    self.popup = True
                    self.confirmation()

                elif text_serial == "O":
                    self.onCapture = False

                elif text_serial == "0":
                    self.status_txt.setText('Stop')
                    self.start_btn.setText('Start')
                    self.start = False

                elif text_serial == "R":
                    print(datetime.datetime.now())
                    self.status_txt.setText('Start')
                    self.start_btn.setText('Stop')
                    self.start = True
                
                elif text_serial=="V":
                    print("active jos")

                    try:
                        self.saveimage()           
                    except Exception as err:
                        print(err)

                    # self.currRow=self.currRow+1
                    # self.currCol=self.currCol+1
                    gc.collect()
                # penambahan perintah
        except:
            None

    def denoising_connect(self, state):
        if state == QtCore.Qt.Checked:
            print("denoising on")
        else:
            print("denoising off")

    def sharpness_connect(self, state):
        if state == QtCore.Qt.Checked:
            # print("denoising on")
            self.video.setSharpnessEnable("On")
        else:
            # print("denoising off")
            self.video.setSharpnessEnable("Off")

    def setPointStart(self):
        try:
            self.sendSerial("<")
        except:
            print("Device not connect!")
            self.status_txt.setText("Device not connect!")
        else:
            self.startPoint[0]=self.koordinat[0]
            self.startPoint[1]=self.koordinat[1]
            self.status_txt.setText("SET START : " + str(self.startPoint[0])+ ","+ str(self.startPoint[1]))

    def setPointEnd(self):
        try:
            self.sendSerial(">")
        except:
            print("Device not connect!")
            self.status_txt.setText("Device not connect!")
        else:
            self.endPoint[0]=self.koordinat[0]
            self.endPoint[1]=self.koordinat[1]
            self.setRow(self.startPoint[0],self.endPoint[0])
            self.setCol(self.startPoint[1],self.endPoint[1])
            self.status_txt.setText("SET END : " + str(self.endPoint[0])+ ","+ str(self.endPoint[1]))
            print(self.getRow())
            print(self.getCol())

    def getRow(self):
        return self._Row

    def setRow(self,valX,valY):
        if valX<1:
            valX=valX*-1
        if valY<1:
            valY=valY*-1
        self._Row=valX + valY

    def getCol(self):
        return self._Col
    
    def setCol(self,valX,valY):
        if valX<1:
            valX=valX*-1
        if valY<1:
            valY=valY*-1
        self._Col=valX + valY
        
    def autoFocus():
       pass

    def stopScan(self):
        self.sendSerial("!")
      
                
    def setHomeSlideconnect(self):
        xx = self.xHomeSlide_text.text()
        yy = self.yHomeSlide_text.text()
        # self.ser.write(str("s:" + xx+":"+yy + "\n").encode('utf-8'))
        command = str("s:" + xx+":"+yy)
        self.sendSerial(command)

    def scanConfirmation(self):
        msg = QMessageBox()
        msg.setWindowTitle("Scan Confirmation")
        msg.setText("Scan Area "+"row :" +str(self.getRow()) +" Coloum :"+str(self.getCol())+" mulai scan?")
        # msg.setText("Scan row :" + self.getRow +" Coloum :"+self.getCol)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)

        msg.buttonClicked.connect(self.start_confirmation_btn)
        x = msg.exec_()
        
    def start_confirmation_btn(self, i):
        if i.text() == '&Yes':
            self.sendSerial("S")
            print("YA")

        if i.text() == '&No':
            self.sendSerial("N")
            print("No")
        self.popup = False

    def confirmation(self):
        msg = QMessageBox()
        msg.setWindowTitle("Lanjutkan Scanning")
        msg.setText("Apakah Scanning akan dilanjutkan ?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)

        msg.buttonClicked.connect(self.confirmation_btn)
        x = msg.exec_()

    def confirmation_btn(self, i):
        if i.text() == '&Yes':
            # self.ser.write(str("Y" + "\n").encode('utf-8'))
            self.sendSerial("Y")
            # self.ser.write(str("Y").encode())
            print("YA")
        if i.text() == '&No':
            # self.ser.write(str("N" + "\n").encode('utf-8'))
            self.sendSerial("N")
            # self.ser.write(str("N").encode())
            print("No")

        self.popup = False


    def setNamaSlide(self):
        judul = self.namaSlide_text.text()
        judul = judul.strip()
        judul = re.sub('[^a-zA-Z0-9 \n\.]', '', judul)
        judul = judul.replace(" ", "-")

        # print(judul)
        self.tempdirectory = judul

        self.wsi.setDirectory(self.tempdirectory)
        self.status_txt.setText('Save '+self.tempdirectory)

    def createwsiconnect(self):
        self.createwsi = True
        # self.namaSlide_btn.setText("WAIT")
        self.wsi.setDirectory(self.tempdirectory)
        # self.wsi.makedir()
        self.wsi.start()

    def wsiFinish(self):
        self.createwsi = False
        self.creatUrl = 'localhost/slide/?slide='

        msg = QMessageBox()
        msg.setWindowTitle("Scanning Selesai")
        msg.setText("Slide " + self.tempdirectory + " berhasil di-Scan")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.buttonClicked.connect(self.confirmation_btn)
        self.sendSerial("J")

        try:
            if self.openFile == True:
                self.creatUrl = self.creatUrl+self.tempdirectory
                webbrowser.open(self.creatUrl)
        except:
            "Gagal open Slide "

        x = msg.exec_()

        # self.namaSlide_btn.setText("Create WSI")

    def wsiError(self):
        self.createwsi = False

        msg = QMessageBox()
        msg.setWindowTitle("Scanning Gagaal")
        msg.setText("Slide " + self.tempdirectory + " gagal di-Scan")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)

        msg.buttonClicked.connect(self.confirmation_btn)
        x = msg.exec_()

        # self.namaSlide_btn.setText("Create WSI")

    def sendSerial(self, command):
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(str(command+"\n").encode('utf-8'))


class wsiThread(QThread):
    # updatewsi = pyqtSignal(bool)
    finishWsi = pyqtSignal()
    errorWsi = pyqtSignal()

    def __init__(self):
        super(wsiThread, self).__init__()
        self._isRunning = True
        self.startrow = 0
        self.endrow = 4
        self.startcolumn = 0
        self.endcolumn = 7
        self.directory = ""

    def run(self):
        try:
            os.mkdir("slide/dzi/"+self.directory)
            mypath = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "image\\"+self.directory)
            onlyfiles = [f for f in os.listdir(
                mypath) if os.path.isfile(os.path.join(mypath, f))]

            col = []
            row = []
            for file in onlyfiles:
                file = file.split(".")[0]
                split = file.split('_')
                col.append(int(split[0]))
                row.append(int(split[1]))

            self.endcolumn = int(max(col))+1
            self.endrow = int(max(row))+1

            self.cekFile()

            tiles = [pyvips.Image.new_from_file(f"image/{self.directory}/{x}_{y}.jpg", access="sequential")
                     for y in range(self.startrow, self.endrow) for x in range(self.startcolumn, self.endcolumn)]
            image = pyvips.Image.arrayjoin(
                tiles, across=self.endcolumn - self.startcolumn)
            # image.write_to_file(self.directory+".tif", compression="jpeg", tile=True)
            image.dzsave("slide/dzi/"+self.directory)

            shutil.move("slide/dzi/"+self.directory+".dzi",
                        "slide/dzi/"+self.directory+"/"+self.directory+".dzi")
            shutil.move("slide/dzi/"+self.directory+"_files",
                        "slide/dzi/"+self.directory+"/"+self.directory + "_files")
            # print("wait")
            # time.sleep(10)
            self.finishWsi.emit()
            self._isRunning = False

        except Exception as e:
            self._isRunning = True
            self.errorWsi.emit()
            print(e)

    def setDirectory(self, dir):
        self.directory = dir

    def cekFile(self):
        col = 0
        # row = 0
        while (col < self.endcolumn + 1):
            # while (row < self.endrow + 1):
            for row in range(self.endrow + 1):
                # self.endcolumn, self.endrow
                # path = Path("image/"+ self.directory + '/' + col +"_"+row +"".jpg")
                path = Path("image/" + self.directory +
                            '/' + str(col) + "_"+str(row) + ".jpg")
                while not path.is_file():
                    img = np.zeros((2048, 2448, 3), dtype=np.uint8)
                    img.fill(255)
                    cv2.imwrite("image/" + self.directory +
                                '/' + str(col) + "_"+str(row) + ".jpg", img)
                    # time.sleep(.2)
                # row += 1
            # row = 0
            col += 1

    def makedir(self):
        os.mkdir("slide/dzi/temp1641364530021")


class CreatTiff():
    def __init__(self) -> None:
        super().__init__()
        self.startrow_tif = 0
        self.endrow_tif = 0
        self.startcolumn_tif = 0
        self.endcolumn_tif = 0
        self.nameSlide = ""

    def generateTiff(self, title, col, row):
        titleResult = title
        title = 'D:\\Neurabot\\Microscanner\\V2\\Pemrograman\\Python\\image\\'+title
        destination = 'D:\\Neurabot\\Microscanner\\V2\\Pemrograman\\Python\\image'
        os.chdir(title)
        # os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python\image')
        print(datetime.datetime.now())

        print(os.getcwd())
        print(col)
        print(row)

        tiles = [pyvips.Image.new_from_file(f"{x}_{y}.jpg", access="sequential")
                 for y in range(self.startrow_tif, row) for x in range(self.startcolumn_tif, col)]

        image = pyvips.Image.arrayjoin(
            tiles, across=col-self.startcolumn_tif)

        image.write_to_file(f"{titleResult}.tif",
                            compression="jpeg", tile=True)


class VideoThread(QThread):
    update_frame = pyqtSignal(np.ndarray)
    fileExist = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.cam = None
        self.rescale_factor = 0

    def run(self):
        # capture from web cam
        # cap = cv2.VideoCapture(0)
        while self._run_flag:
            self.image = self.cam.stream()
            self.update_frame.emit(self.image)
        # shut down capture system
        # cap.release()

    def opencam(self):
        self.cam = marscam.marscam()
        self.cam.setCamera(0)
        self.cam.openCamera()
        
    def setExposureAuto(self, mode):
        self.cam.setExposureAuto(mode)

    def setWhiteBalance(self, mode):
        self.cam.setWBAuto(mode)

    def setBrightness(self, val):
        self.cam.setBrightness(val)

    def setExposure(self, val):
        self.cam.setExposureTime(val)

    def setGainRaw(self, val):
        self.cam.setGainRaw(val)

    def setGamma(self, val):
        self.cam.setGamma(val)

    def setSharpnessEnable(self, val):
        self.cam.setSharpnessEnable(str(val))

    def setSharpness(self, val):
        self.cam.setSharpness(val)

    def setWBRatio(self, channel, dval):
        self.cam.setWBRatio(channel, dval)

    def rescale_frame(self, frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def saveimage(self, dir):
        # while True:
        #     if cv2.imwrite(dir + ".jpg", self.cam.stream()):
        #         break

        while not self.cekfile(dir):
            print("save image : " + dir)
            # img = np.zeros((100, 100, 3), dtype=np.uint8)
            img = self.cam.stream()
            # if self.rescale_factor != 0:
            #     img = rescale_frame(img, self.rescale_factor)
            cv2.imwrite(dir + ".jpg", img)
            # time.sleep(.2)
            # self.cam.stream()

        self.fileExist.emit()

    def cekfile(self, name):

        # image = cv2.imread(name)

        # Checking if the image is empty or not
        # if image is None:
        #     return False
        # else:
        #     return True

        # os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python')
        dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir)

        # path = Path(name + ".jpg")

        # if path.is_file():

        #     # if os.path.isfile(name+".jpg"):
        #     # if os.path.isfile("D:/Neurabot/Microscanner/V2/Pemrograman/Python/" + name):
        #     return True
        # else:
        #     return False

        cap = cv2.imread(name + ".jpg")
        if (cap is None):
            return False
        else:
            return True

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MicroscannerTest()
    window.setWindowTitle('Microscanner Test')
    window.show()
    sys.exit(app.exec_())
