# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_WPS.ui'
#
# Created: Wed Aug 27 16:45:44 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WPS(object):
    def setupUi(self, WPS):
        WPS.setObjectName(_fromUtf8("WPS"))
        WPS.resize(490, 306)
        self.verticalLayout = QtGui.QVBoxLayout(WPS)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addressLabel = QtGui.QLabel(WPS)
        self.addressLabel.setObjectName(_fromUtf8("addressLabel"))
        self.horizontalLayout.addWidget(self.addressLabel)
        self.mimeComboBox = QtGui.QComboBox(WPS)
        self.mimeComboBox.setObjectName(_fromUtf8("mimeComboBox"))
        self.horizontalLayout.addWidget(self.mimeComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.code = QtGui.QPlainTextEdit(WPS)
        self.code.setObjectName(_fromUtf8("code"))
        self.verticalLayout.addWidget(self.code)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.clearButton = QtGui.QPushButton(WPS)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout_2.addWidget(self.clearButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(WPS)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(WPS)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), WPS.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), WPS.reject)
        QtCore.QMetaObject.connectSlotsByName(WPS)

    def retranslateUi(self, WPS):
        WPS.setWindowTitle(_translate("WPS", "WPS", None))
        self.addressLabel.setText(_translate("WPS", "Choose mime type:", None))
        self.code.setPlainText(_translate("WPS", "# Type your python code here", None))
        self.clearButton.setText(_translate("WPS", "Clear", None))

