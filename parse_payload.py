#!/usr/bin/env python3
#https://github.com/flying1008

import json
import os
import base64
import hashlib
import datetime
import time
import sys
import argparse
import struct
from PyQt5 import QtCore, QtGui, QtWidgets

def u32(x):
    return struct.unpack('>I', x)[0]

def u64(x):
    return struct.unpack('>Q', x)[0]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(582, 420)
        self.cwd = os.getcwd()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 30, 91, 30))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 110, 521, 221))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 80, 121, 20))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 582, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "解析bin信息"))
        self.pushButton.setText(_translate("MainWindow", "选择bin文件"))
        self.label.setText(_translate("MainWindow", "bin信息："))
        self.pushButton.clicked.connect(self.slot_btn_chooseFile)

    def slot_btn_chooseFile(self):
        fileName_choose, filetype = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件",self.cwd, "bin文件 (*.bin)") 
        if fileName_choose == "":
            self.msg_info("未选择文件")
            return 
        print(fileName_choose)
        self.parse_payload(fileName_choose)

    def parse_payload(self,filename):
        file = open(filename,"rb")
        magic = file.read(4)
        try:
            assert magic == b'CrAU'
        except:
            self.msg_info("非标准bin,请重新选择")
            file.close()
            return

        file_format_version = u64(file.read(8))
        assert file_format_version == 2

        manifest_size = u64(file.read(8))

        if file_format_version > 1:
            metadata_signature_size = u32(file.read(4))

        filename = file.name
        sha256 = hashlib.sha256()
        md5 = hashlib.md5()
        with open(filename,"rb") as f:
            while True:
                chunk = f.read(16 * 1024)
                if not chunk:
                    break
                md5.update(chunk)
                sha256.update(chunk)
        payload_hash =base64.b64encode(sha256.digest()).decode()
        f.close()
        print("hash:",md5.hexdigest())
        print("FILE_HASH:",payload_hash)
        print("FILE_SIZE:",os.path.getsize(filename))
        sha2 = hashlib.sha256()
        with open(filename,"rb") as w:
            chunk = w.read(manifest_size+24)
            sha2.update(chunk)
        meta_hash =base64.b64encode(sha2.digest()).decode()
        w.close()
        print("METADATA_HASH:",meta_hash)
        print("METADATA_SIZE:",manifest_size+24)

        param={}
        other_param ={}
        param['link'] = "ADD firmware URL"
        param['hash'] = md5.hexdigest()
        other_param['FILE_HASH'] = payload_hash
        other_param['FILE_SIZE'] = str(os.path.getsize(filename))
        other_param['METADATA_HASH'] = meta_hash
        other_param['METADATA_SIZE']= str(manifest_size+24)
        param['otherParam'] = other_param
        print(json.dumps(other_param))
        json_name = os.path.basename(filename) + "_other_param.json"
        other_param_file = open(json_name,"w")
        other_param_file.write(json.dumps(param,indent=2,ensure_ascii=False))
        other_param_file.close()
        msg = "获取bin信息成功，信息已写入" +json_name + "中"
        self.msg_info(msg)
        self.textEdit.clear()
        self.textEdit.setText(json.dumps(param,indent=2,ensure_ascii=False))

    def msg_info(self,msg):
        w = QtWidgets.QWidget()
        QtWidgets.QMessageBox.information(w,"提示",msg,QtWidgets.QMessageBox.Yes)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
