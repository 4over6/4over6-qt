# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thu4over6logviewer.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_THU4Over6LogViewer(object):
    def setupUi(self, THU4Over6LogViewer):
        THU4Over6LogViewer.setObjectName("THU4Over6LogViewer")
        THU4Over6LogViewer.resize(1000, 560)
        self.gridLayout = QtWidgets.QGridLayout(THU4Over6LogViewer)
        self.gridLayout.setObjectName("gridLayout")
        self.logViewerEdit = QtWidgets.QPlainTextEdit(THU4Over6LogViewer)
        self.logViewerEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.logViewerEdit.setObjectName("logViewerEdit")
        self.gridLayout.addWidget(self.logViewerEdit, 0, 0, 1, 3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(THU4Over6LogViewer)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.ipAddressEdit = QtWidgets.QLineEdit(THU4Over6LogViewer)
        self.ipAddressEdit.setReadOnly(True)
        self.ipAddressEdit.setObjectName("ipAddressEdit")
        self.horizontalLayout.addWidget(self.ipAddressEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.refreshButton = QtWidgets.QPushButton(THU4Over6LogViewer)
        self.refreshButton.setObjectName("refreshButton")
        self.gridLayout.addWidget(self.refreshButton, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(453, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(THU4Over6LogViewer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)

        self.retranslateUi(THU4Over6LogViewer)
        self.buttonBox.accepted.connect(THU4Over6LogViewer.accept)
        self.buttonBox.rejected.connect(THU4Over6LogViewer.reject)
        QtCore.QMetaObject.connectSlotsByName(THU4Over6LogViewer)

    def retranslateUi(self, THU4Over6LogViewer):
        _translate = QtCore.QCoreApplication.translate
        THU4Over6LogViewer.setWindowTitle(_translate("THU4Over6LogViewer", "THU4Over6 Log Viewer"))
        self.label.setText(_translate("THU4Over6LogViewer", "IP address:"))
        self.refreshButton.setText(_translate("THU4Over6LogViewer", "Refresh"))


