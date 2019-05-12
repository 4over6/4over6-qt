# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thu4over6settings.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_THU4Over6Settings(object):
    def setupUi(self, THU4Over6Settings):
        THU4Over6Settings.setObjectName("THU4Over6Settings")
        THU4Over6Settings.resize(300, 200)
        self.gridLayout = QtWidgets.QGridLayout(THU4Over6Settings)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(THU4Over6Settings)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.vpnNameComboBox = QtWidgets.QComboBox(THU4Over6Settings)
        self.vpnNameComboBox.setObjectName("vpnNameComboBox")
        self.gridLayout.addWidget(self.vpnNameComboBox, 0, 1, 1, 2)
        self.warningCheckBox = QtWidgets.QCheckBox(THU4Over6Settings)
        self.warningCheckBox.setObjectName("warningCheckBox")
        self.gridLayout.addWidget(self.warningCheckBox, 1, 0, 1, 3)
        self.line_2 = QtWidgets.QFrame(THU4Over6Settings)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 3)
        self.sudoCheckBox = QtWidgets.QCheckBox(THU4Over6Settings)
        self.sudoCheckBox.setObjectName("sudoCheckBox")
        self.gridLayout.addWidget(self.sudoCheckBox, 3, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(THU4Over6Settings)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 2)
        self.sudoCommandEdit = QtWidgets.QLineEdit(THU4Over6Settings)
        self.sudoCommandEdit.setObjectName("sudoCommandEdit")
        self.gridLayout.addWidget(self.sudoCommandEdit, 4, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(THU4Over6Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)

        self.retranslateUi(THU4Over6Settings)
        self.buttonBox.accepted.connect(THU4Over6Settings.accept)
        self.buttonBox.rejected.connect(THU4Over6Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(THU4Over6Settings)
        THU4Over6Settings.setTabOrder(self.vpnNameComboBox, self.warningCheckBox)
        THU4Over6Settings.setTabOrder(self.warningCheckBox, self.sudoCheckBox)
        THU4Over6Settings.setTabOrder(self.sudoCheckBox, self.sudoCommandEdit)
        THU4Over6Settings.setTabOrder(self.sudoCommandEdit, self.buttonBox)

    def retranslateUi(self, THU4Over6Settings):
        _translate = QtCore.QCoreApplication.translate
        THU4Over6Settings.setWindowTitle(_translate("THU4Over6Settings", "4Over6 Settings"))
        self.label.setText(_translate("THU4Over6Settings", "VPN name:"))
        self.warningCheckBox.setText(_translate("THU4Over6Settings", "Show warning when disconnected"))
        self.sudoCheckBox.setText(_translate("THU4Over6Settings", "Use sudo"))
        self.label_2.setText(_translate("THU4Over6Settings", "Sudo command:"))


