# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serial.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import time
from cv2 import split
# from PyQt5.QtCore import pyqtSlot
# from PyQt5.QtWidgets import QApplication, QDialog
# from PyQt5.uic import loadUi
import serial
from PyQt5.QtCore import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 300)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_arduino = QtWidgets.QLabel(self.centralwidget)
        self.label_arduino.setGeometry(QtCore.QRect(340, 130, 61, 16))
        self.label_arduino.setScaledContents(True)
        self.label_arduino.setWordWrap(False)
        self.label_arduino.setObjectName("label_arduino")
        self.label_time = QtWidgets.QLabel(self.centralwidget)
        self.label_time.setGeometry(QtCore.QRect(340, 90, 47, 13))
        self.label_time.setScaledContents(True)
        self.label_time.setWordWrap(False)
        self.label_time.setObjectName("Time")
        self.btn_ccw = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ccw.setGeometry(QtCore.QRect(150, 70, 75, 23))
        self.btn_ccw.setObjectName("btn_ccw")
        self.btn_ccw.clicked.connect(self.btn_ccw_klik)
        self.btn_cw = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cw.setGeometry(QtCore.QRect(150, 130, 75, 23))
        self.btn_cw.setObjectName("btn_cw")
        self.btn_cw.clicked.connect(self.btn_cw_klik)
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(150, 190, 75, 23))
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.clicked.connect(self.btn_stop_klik)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.ser = serial.Serial('COM15', baudrate=9600)
        self.run()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cek Serial"))
        self.label_arduino.setText(_translate("MainWindow", "Serial Read"))
        self.btn_ccw.setText(_translate("MainWindow", "X AXIS"))
        self.btn_cw.setText(_translate("MainWindow", "Y AXIS "))
        self.btn_stop.setText(_translate("MainWindow", "STOP"))

    def btn_ccw_klik(self):
        i = 1
        self.ser.write(str(i).encode())
        # self.label_arduino.setText('CCW')

    def btn_cw_klik(self):
        i = 2
        self.ser.write(str(i).encode())
        # self.label_arduino.setText('CW')

    def btn_stop_klik(self):
        i = 3
        self.ser.write(str(i).encode())
        # self.label_arduino.setText('Stop')

    def run(self):
        QTimer.singleShot(1, self.run)
        # time_str = time.strftime("%H:%M:%S")
        # self.label_time.setText(time_str)
        while self.ser.inWaiting():
            text_serial = self.ser.readline().decode('ascii').strip()
            if ';' in text_serial:                
                split = text_serial.split(';')
                if(split[0] == "S"):
                    self.label_arduino.setText(split[1])
                else:
                    self.label_arduino.setText(split[0])
            else:
                self.label_arduino.setText(text_serial)
            # ser.read


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

