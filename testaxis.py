# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testaxis.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import time
import serial
from PyQt5.QtCore import *


class Ui_testAxis(object):
    def setupUi(self, testAxis):
        testAxis.setObjectName("testAxis")
        testAxis.resize(480, 360)
        self.centralwidget = QtWidgets.QWidget(testAxis)
        self.centralwidget.setObjectName("centralwidget")
        self.Axis_text = QtWidgets.QLineEdit(self.centralwidget)
        self.Axis_text.setGeometry(QtCore.QRect(180, 120, 113, 20))
        self.Axis_text.setObjectName("Axis_text")
        self.x_btn = QtWidgets.QPushButton(self.centralwidget)
        self.x_btn.setGeometry(QtCore.QRect(130, 180, 75, 23))
        self.x_btn.setObjectName("x_btn")
        self.x_btn.clicked.connect(self.btn_x_klik)
        self.y_btn = QtWidgets.QPushButton(self.centralwidget)
        self.y_btn.setGeometry(QtCore.QRect(260, 180, 75, 23))
        self.y_btn.setObjectName("y_btn")
        self.y_btn.clicked.connect(self.btn_y_klik)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 120, 47, 13))
        self.label.setObjectName("label")
        testAxis.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(testAxis)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menubar.setObjectName("menubar")
        testAxis.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(testAxis)
        self.statusbar.setObjectName("statusbar")
        testAxis.setStatusBar(self.statusbar)

        self.retranslateUi(testAxis)
        QtCore.QMetaObject.connectSlotsByName(testAxis)
        self.ser = serial.Serial('COM15', baudrate=9600)
        self.run()


    def retranslateUi(self, testAxis):
        _translate = QtCore.QCoreApplication.translate
        testAxis.setWindowTitle(_translate("testA"
                                           "xis", "Test Axis"))
        self.x_btn.setText(_translate("testAxis", "X AXIS"))
        self.y_btn.setText(_translate("testAxis", "Y AXIS"))
        self.label.setText(_translate("testAxis", "mm"))

    def btn_x_klik(self):
        xx = self.Axis_text.text()
        self.ser.write(str("X:"+xx+"\n").encode('utf-8'))

        # self.label.setText(xx)

    def btn_y_klik(self):
        # i = 1
        yy = self.Axis_text.text()
        self.ser.write(str("Y:" + yy+"\n").encode('utf-8'))
        # self.label.setText(yy)

    def run(self):
        QTimer.singleShot(1, self.run)
        # time_str = time.strftime("%H:%M:%S")
        # self.label_time.setText(time_str)
        while self.ser.inWaiting():
            text_serial = self.ser.readline().decode('ascii').strip()
            self.label.setText(text_serial)
        #     # ser.read


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_testAxis()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


