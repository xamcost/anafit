# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customFitDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_customFitDialog(object):
    def setupUi(self, customFitDialog):
        customFitDialog.setObjectName("customFitDialog")
        customFitDialog.resize(400, 276)
        customFitDialog.setWindowOpacity(4.0)
        customFitDialog.setSizeGripEnabled(False)
        self.customFitButtonBox = QtWidgets.QDialogButtonBox(customFitDialog)
        self.customFitButtonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.customFitButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.customFitButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.customFitButtonBox.setCenterButtons(True)
        self.customFitButtonBox.setObjectName("customFitButtonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(customFitDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.customFitNameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.customFitNameLabel.setObjectName("customFitNameLabel")
        self.verticalLayout.addWidget(self.customFitNameLabel)
        self.customFitName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.customFitName.setObjectName("customFitName")
        self.verticalLayout.addWidget(self.customFitName)
        self.customFitDefLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.customFitDefLabel.setObjectName("customFitDefLabel")
        self.verticalLayout.addWidget(self.customFitDefLabel)
        self.customFitDef = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.customFitDef.setObjectName("customFitDef")
        self.verticalLayout.addWidget(self.customFitDef)

        self.retranslateUi(customFitDialog)
        self.customFitButtonBox.accepted.connect(customFitDialog.accept)
        self.customFitButtonBox.rejected.connect(customFitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(customFitDialog)

    def retranslateUi(self, customFitDialog):
        _translate = QtCore.QCoreApplication.translate
        customFitDialog.setWindowTitle(_translate("customFitDialog", "New Fit Definition"))
        self.customFitNameLabel.setText(_translate("customFitDialog", "Function name :"))
        self.customFitDefLabel.setText(_translate("customFitDialog", "<html><head/><body><p>Definition : <span style=\" font-style:italic;\">ex: lambda x, a, b : a*(x-b)**(1/2) ; (1, 0.1)</span></p></body></html>"))

