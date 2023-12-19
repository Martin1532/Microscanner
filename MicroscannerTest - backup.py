import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QCheckBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
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


class MicroscannerTest(QMainWindow):
    def __init__(self):
        super(MicroscannerTest, self).__init__()
        os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python')
        # os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python')
        loadUi('MicroscannerTest.ui', self)

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
        self.namaSlide_btn.clicked.connect(self.createwsiconnect)
        self.prepare_btn.clicked.connect(self.prepareconnect)
        # self.prepare_btn.clicked.connect(self.confirmation)
        self.openCam_btn.clicked.connect(self.openCamconnect)
        self.setArea_btn.clicked.connect(self.setAreaconnect)
        self.comRefresh_btn.clicked.connect(self.addComboItem)
        self.setHomeSlide_btn.clicked.connect(self.setHomeSlideconnect)

        self.connect_btn.clicked.connect(self.portconnect)

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

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(5)

        self.thread = QThread()
        self.createwsi = False
        self.wsi = wsiThread()
        self.wsi.finishWsi.connect(self.wsiFinish)

        self.video = VideoThread()
        self.video.rescale_factor = 25
        self.video.update_frame.connect(self.update_frame)

        self.ser = None
        # self.serConnect("COM3")
        # self.wsi

        # try:
        #     # self.ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
        #     self.ser = serial.Serial('COM4', baudrate=9600)
        # except:
        #     self.status_txt.setText('Port Serial Tidak Tersambung')

        # self.serialcheck()
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
            print(datetime.datetime.now())
            self.status_txt.setText('Start')
            self.start_btn.setText('Stop')
            self.start = not self.start
            self.currImage = 0
            self.tempdirectory = "temp"+str(round(time.time() * 1000))
            self.ser.write(str("S"+"\n").encode('utf-8'))
            # self.ser.write(str("S").encode())
        else:
            self.status_txt.setText('Stop')
            self.start_btn.setText('Start')
            # self.ser.write(str("0").encode())
            self.ser.write(str("0"+"\n").encode('utf-8'))
            self.start = not self.start

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

    def prepareconnect(self):
        self.status_txt.setText('Prepare')
        self.ser.write(str(0).encode())

    def saveimage(self, column, row):
        self.currImage += 1
        if not os.path.exists("image/"+self.tempdirectory):
            os.makedirs("image/"+self.tempdirectory)

        # cv2.imwrite(self.directory[self.currslide]+'/'+ str(self.countcolumn) + ".jpg", self.image)
        # cv2.imwrite(self.tempdirectory+'/' + str(column) + "_"+str(row) + ".jpg", self.image)
        self.video.saveimage("image/" + self.tempdirectory +
                             '/' + str(column) + "_"+str(row))

        # self.ser.write(str("C").encode())
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(str("C"+"\n").encode('utf-8'))
        self.onCapture = True
        self.lastCapture = self.getMillis()
        # self.ser.write(str(perintah).encode())

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
        self.video.setExposure(40000)
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
                self.ser.flushInput()
                self.ser.flushOutput()
                self.ser.write(str("C"+"\n").encode('utf-8'))

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
                    self.namaSlide_btn.setText("WAIT")
                    self.wsi.setDirectory(self.tempdirectory)
                    self.status_txt.setText('Stop')
                    self.start_btn.setText('Start')
                    # self.ser.write(str("0").encode())
                    self.start = not self.start
                    self.wsi.start()

                elif text_serial == "!" and not self.popup:
                    self.popup = True
                    self.confirmation()

                elif text_serial == "O":
                    self.onCapture = False

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
        self.ser.write(str("A:" + width+":"+height + "\n").encode('utf-8'))

    def setHomeSlideconnect(self):
        xx = self.xHomeSlide_text.text()
        yy = self.yHomeSlide_text.text()
        self.ser.write(str("s:" + xx+":"+yy + "\n").encode('utf-8'))

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
            self.ser.write(str("Y" + "\n").encode('utf-8'))
            # self.ser.write(str("Y").encode())
            print("YA")
        if i.text() == '&No':
            self.ser.write(str("N" + "\n").encode('utf-8'))
            # self.ser.write(str("N").encode())
            print("No")

        self.popup = False

    def createwsiconnect(self):
        self.createwsi = True
        self.namaSlide_btn.setText("WAIT")
        self.wsi.setDirectory(self.tempdirectory)
        # self.wsi.makedir()
        self.wsi.start()

    def wsiFinish(self):
        self.createwsi = False
        self.namaSlide_btn.setText("Create WSI")

    def sendSerial(self, command):


class wsiThread(QThread):
    # updatewsi = pyqtSignal(bool)
    finishWsi = pyqtSignal()

    def __init__(self):
        super(wsiThread, self).__init__()
        self._isRunning = True
        self.startrow = 0
        self.endrow = 4
        self.startcolumn = 0
        self.endcolumn = 7
        self.directory = ""

    def run(self):
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

    def setDirectory(self, dir):
        self.directory = dir

    def makedir(self):
        os.mkdir("slide/dzi/temp1641364530021")


class VideoThread(QThread):
    update_frame = pyqtSignal(np.ndarray)

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
            img = self.cam.stream()
            # if self.rescale_factor != 0:
            #     img = rescale_frame(img, self.rescale_factor)
            cv2.imwrite(dir + ".jpg", img)

    def cekfile(self, name):
        if os.path.isfile(name+".jpg"):
            # if os.path.isfile("D:/Neurabot/Microscanner/V2/Pemrograman/Python/" + name):
            return True
        else:
            return False

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
