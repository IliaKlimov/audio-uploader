# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(450, 300)
        Dialog.setStyleSheet("QMainWindow{"
                            "  background-color: #9ebcec;"
                            "}"
                            "QPushButton{\n"
                            "    background-color: #fff;\n"
                            "    border:none;\n"
                            "    border-radius: 20px;"
                             "   "     
                            "}"
                             "QComboBox:!editable, QComboBox::drop-down:editable {background: white; border: none;}"
                            "QComboBox QAbstractItemView { border: none; selection-background-color: #2f4e7e; }"
                             # "QComboBox::down-arrow {image: url(downwards-arrow-key.png);border: none;    width: 15px;}"
                            "QComboBox::drop-down {subcontrol-origin: padding;subcontrol-position: top right;width: 15px;}"
                             "QOpenGLWidget{color: white}"
                             )
        Dialog.setWindowFilePath("")
        font = QtGui.QFont()
        font.setPointSize(10)

        self.msgBox = QtWidgets.QMessageBox()


        self.fileTextLine = QtWidgets.QLineEdit(Dialog)
        self.fileTextLine.setGeometry(QtCore.QRect(150, 90, 190, 22))
        self.fileTextLine.setObjectName("fileTextBox")

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(150, 130, 190, 22))
        self.comboBox.setObjectName("comboBox")

        self.DateTextLine = QtWidgets.QLineEdit(Dialog)
        self.DateTextLine.setGeometry(QtCore.QRect(150, 170, 190, 22))
        self.DateTextLine.setObjectName("lineDate")
        self.DateTextLine.setPlaceholderText(" dd.mm.yy / dd.mm.yyyy")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(315, 225, 90, 40))
        self.pushButton.setObjectName("pushButton")

        self.fileButton = QtWidgets.QPushButton(Dialog)
        self.fileButton.setGeometry(QtCore.QRect(345, 91, 25, 20))
        self.fileButton.setObjectName("fileButton")

        self.label_file = QtWidgets.QLabel(Dialog)
        self.label_file.setGeometry(QtCore.QRect(70, 90, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_file.setFont(font)
        self.label_file.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_file.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_file.setObjectName("label_file")


        self.label_sermoner = QtWidgets.QLabel(Dialog)
        self.label_sermoner.setGeometry(QtCore.QRect(30, 130, 111, 20))
        self.label_sermoner.setFont(font)
        self.label_sermoner.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_sermoner.setObjectName("label_sermoner")

        self.label_date = QtWidgets.QLabel(Dialog)
        self.label_date.setGeometry(QtCore.QRect(30, 170, 111, 20))
        self.label_date.setFont(font)
        self.label_date.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_date.setObjectName("label_date")


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Загрузка записи", None, -1))
        self.msgBox.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "ERR", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Dialog", "Отправить", None, -1))
        self.label_file.setText(QtWidgets.QApplication.translate("Dialog", "Файл:", None, -1))
        self.label_sermoner.setText(QtWidgets.QApplication.translate("Dialog", "Спикер:", None, -1))
        self.label_date.setText(QtWidgets.QApplication.translate("Dialog", "Дата:", None, -1))
        self.fileButton.setText(QtWidgets.QApplication.translate("Dialog", "...", None, -1))





