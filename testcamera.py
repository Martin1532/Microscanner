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


class MicroscannerTest(QMainWindow):
    def __init__(self):
        super(MicroscannerTest, self).__init__()
        # os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python')
        dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir)
        # os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python')
        loadUi('scannerUpdate.ui', self)
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
        self.directory = ['preparat 0',
                          'preparat 1', 'preparat 2', 'preparat 3']
        self.start_btn.clicked.connect(self.startconnect)
        self.namaSlide_btn.clicked.connect(self.setNamaSlide)
        self.fokus_btn.clicked.connect(self.setfokusconnect)
        self.prepare_btn.clicked.connect(self.prepareconnect)
        self.openCam_btn.clicked.connect(self.openCamconnect)
        self.setArea_btn.clicked.connect(self.setAreaconnect)
        self.comRefresh_btn.clicked.connect(self.addComboItem)
        self.setHomeSlide_btn.clicked.connect(self.setHomeSlideconnect)

        self.calibrationButton.addItems(['Off', 'On'])
        self.calibrationButton.currentIndexChanged.connect(
            self.statusCalibration)
        self.calibrationButton.activated.connect(self.modeCalibrate)

        self.openIfDone.toggled.connect(self.openDone)
        self.openIfDone.setChecked(False)
        self.rightButton.clicked.connect(self.rightConnect)
        self.downButton.clicked.connect(self.downConnect)
        self.leftButton.clicked.connect(self.leftConnect)
        self.upButton.clicked.connect(self.upConnect)
        self.homeButton.clicked.connect(self.homeConnect)
        self.connect_btn.clicked.connect(self.portconnect)

        self.openBrowsur.clicked.connect(self.open_file_dialog)
        self.file_list = QLineEdit()

        self.tiffButton.clicked.connect(self.tif_file_dialog)
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

        self.preparateButton.clicked.connect(self.toglePreparateOpen)
        self.closePreparate.clicked.connect(self.toglePreparateClose)
        # self.brignesLamp.valueChanged.connect(self. brightness_led)
        # self.brignesLamp.setMinimum(0)
        # self.brignesLamp.setMaximum(100)

        self.currslide = 0

        # self.capture = cv2.VideoCapture(1)
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        # self.cam = marscam.marscam()
        # self.cam.setCamera(0)
        # self.cam.openCamera()

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
        self.pathTif = r'Python\image'

        self.gotif = CreatTiff()
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(5)

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
        # self.serConnect("COM3")
        # self.wsi

        # try:
        #     # self.ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
        #     self.ser = serial.Serial('COM4', baudrate=9600)
        # except:
        #     self.status_txt.setText('Port Serial Tidak Tersambung')

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
            # print(datetime.datetime.now())
            # self.status_txt.setText('Start')
            # self.start_btn.setText('Stop')
            # self.start = not self.start
            self.currImage = 0

            if (self.tempdirectory == ""):
                self.tempdirectory = "temp"+str(round(time.time() * 1000))
            self.heightScan_text.text()
            # self.ser.write(str("S"+"\n").encode('utf-8'))
            # self.ser.write(str("S").encode())
            self.sendSerial("S")

        else:
            # self.status_txt.setText('Stop')
            # self.start_btn.setText('Start')
            # self.ser.write(str("0").encode())
            # self.ser.write(str("0"+"\n").encode('utf-8'))
            self.sendSerial("0")
            # self.start = not self.start

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
            # self.ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
            self.ser = serial.Serial(com, baudrate=9600)
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
        try:
            self.gotif.generateTiff(self.folder[0], maxRow, maxCol)
            self.status_txt.setText(f'Success save {self.gotif.nameSlide}.tif')
        except ValueError:
            print(ValueError)
            self.status_txt.setText(f'Failed save {self.gotif.nameSlide}.tif')

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

    def openDone(self):
        openIfDone = self.sender()
        if openIfDone.isChecked():
            self.openFile = True
        else:
            self.openFile = False

    def toglePreparateOpen(self):
        try:
            self.sendSerial("PO")
        except:
            print("arduino not connect")
            self.status_txt.setText("arduino not connect")
        else:
            self.status_txt.setText('Sukses Open Preparate')
            print("open preparate")

    def toglePreparateClose(self):
        try:
            self.sendSerial("PC")
        except:
            print("arduino not connect")
            self.status_txt.setText("arduino not connect")
        else:
            self.status_txt.setText('Sukses Close Preparate')
            print("open preparate")

    def statusCalibration(self, i):
        for stt in range(self.calibrationButton.count()):
            self.calibrationButton.itemText(stt)
            # print(self.calibrationButton.currentIndex())
            print(self.calibrationButton.itemText(stt))

    def modeCalibrate(self):
        if self.calibrationButton.currentIndex() == 1:
            try:
                self.sendSerial('CL')
            except:
                print("arduino not connect")
                self.status_txt.setText("arduino not connect")
            else:
                print("calibration mode")
                self.status_txt.setText("calibration mode")
                self.modeCalibration = True
        else:
            self.modeCalibration = False

    def homeConnect(self):
        # self.countRight = self.countRight-1
        try:
            self.sendSerial("H")
        except:
            print("arduino not connect")
            self.status_txt.setText("arduino not connect")
        else:
            self.status_txt.setText('kembali ke HOME')

    def rightConnect(self):
        # self.countLeft = self.countLeft-1
        if self.modeCalibration == True:
            try:
                self.sendSerial("SR")
            except:
                print("arduino not connect")
                self.status_txt.setText("arduino not connect")
            else:
                self.countRight = self.countRight+1
                val = str(self.countRight)
                self.status_txt.setText('shift right'+" "+val)
                print("shift right")

    def leftConnect(self):
        # self.countRight = self.countRight-1
        if self.modeCalibration == True:
            try:
                self.sendSerial("SL")
            except:
                print("arduino not connect")
                self.status_txt.setText("arduino not connect")
            else:
                self.countLeft = self.countLeft+1
                val = str(self.countLeft)
                self.status_txt.setText('shift left'+" "+val)
                print("shift left")

    def upConnect(self):
        # self.countUp = self.countUp+1
        if self.modeCalibration == True:
            try:
                self.sendSerial("SU")
            except:
                print("arduino not connect")
                self.status_txt.setText("arduino not connect")
            else:
                self.countUp = self.countUp+1
                val = str(self.countUp)
                self.status_txt.setText('shift up'+" "+val)
                print("shift up")

    def downConnect(self):
        if self.modeCalibration == True:
            try:
                self.sendSerial("SD")
            except:
                print("arduino not connect")
                self.status_txt.setText("arduino not connect")
            else:
                self.countDown = self.countDown+1
                val = str(self.countDown)
                self.status_txt.setText('shift down'+" "+val)
                print("shift down")

    def setfokusconnect(self):
        self.status_txt.setText('Set Fokus')
        # self.ser.write(str(0).encode())
        self.sendSerial("f")

    def prepareconnect(self):
        self.sendSerial("P")

    def saveimage(self, column, row):
        self.currImage += 1
        if not os.path.exists("image/"+self.tempdirectory):
            os.makedirs("image/"+self.tempdirectory)

        # cv2.imwrite(self.directory[self.currslide]+'/'+ str(self.countcolumn) + ".jpg", self.image)
        # cv2.imwrite(self.tempdirectory+'/' + str(column) + "_"+str(row) + ".jpg", self.image)
        self.video.saveimage("image/" + self.tempdirectory +
                             '/' + str(column) + "_"+str(row))

        # self.ser.write(str("C").encode())
        # self.ser.flushInput()
        # self.ser.flushOutput()
        # self.ser.write(str("C"+"\n").encode('utf-8'))

        # self.sendSerial("C")
        # self.onCapture = True
        # self.lastCapture = self.getMillis()

        # self.ser.write(str(perintah).encode())

    def fileReady(self):
        self.sendSerial("C")
        self.onCapture = True
        self.lastCapture = self.getMillis()

    def update_frame(self, img):
        if self.opencam:
            # ret, self.image = self.capture.read()
            # self.image = cv2.flip(self.image, 1)
            # self.image = self.cam.stream()
            self.displayImage(img)

    # def update_frame(self):
    #     if self.opencam:
    #         # ret, self.image = self.capture.read()
    #         # self.image = cv2.flip(self.image, 1)
    #         self.image = self.cam.stream()
    #         self.displayImage(self.image)

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
            self.time_label.setText(
                str(self.currRow) + ", " + str(self.currCol) + ", " + str(self.currImage))

            self.currRow_lbl.setText(str(self.currRow))
            self.currCol_lbl.setText(str(self.currCol))
            self.currImg_lbl.setText(str(self.currImage))

            if self.onCapture and now - self.lastCapture > 800:
                # self.ser.flushInput()
                # self.ser.flushOutput()
                # self.ser.write(str("C"+"\n").encode('utf-8'))
                self.sendSerial("C")

            while self.ser.inWaiting():
                text_serial = self.ser.readline().decode('ascii').strip()
                self.status_txt.setText(text_serial)
                if ';' in text_serial:
                    split = text_serial.split(';')
                    if (split[0] == "C"):
                        # self.label_arduino.setText(split[1])
                        self.currRow = split[2]
                        self.currCol = split[1]
                        # self.ser.flushInput()
                        # self.ser.flushOutput()
                        # self.ser.write(str("C"+"\n").encode('utf-8'))

                        # self.sendSerial("C")

                        self.saveimage(split[1], split[2])

                    elif (split[0] == "T"):
                        row = split[2]
                        col = split[1]
                        self.total_label.setText(
                            str(col) + ", " + str(row) + ", " + str(int(col) * int(row)))

                        self.sumRow_lbl.setText(str(row))
                        self.sumCol_lbl.setText(str(col))
                        self.sumImg_lbl.setText(str(int(col) * int(row)))

                        # self.saveimage(split[1],split[2])

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

    def setAreaconnect(self):
        width = self.widthScan_text.text()
        height = self.heightScan_text.text()
        # self.ser.write(str("A:" + width+":"+height + "\n").encode('utf-8'))
        command = str("A:" + width+":"+height)
        print(command)
        self.sendSerial(command)

    def setHomeSlideconnect(self):
        xx = self.xHomeSlide_text.text()
        yy = self.yHomeSlide_text.text()
        # self.ser.write(str("s:" + xx+":"+yy + "\n").encode('utf-8'))
        command = str("s:" + xx+":"+yy)
        self.sendSerial(command)

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
                    time.sleep(.2)
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
        self.listRow = []
        self.listCol = []
        self.allData = []
        self.allRowCol = []

    def generateTiff(self, title, col, row):
        os.chdir(r'python\image')
        print(datetime.datetime.now())
        tiles = [pyvips.Image.new_from_file(f"{title}/{x}_{y}.jpg", access="sequential")
                 for y in range(self.startrow_tif, row) for x in range(self.startcolumn_tif, col)]

        image = pyvips.Image.arrayjoin(
            tiles, across=col-row)
        image.write_to_file(f"{title}.tif",
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
        # self.opencam = True

    # def opencam(self):
    #     self.cam = marscam.marscam()
    #     self.cam.setCamera(0)
    #     self.cam.openCamera()

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
