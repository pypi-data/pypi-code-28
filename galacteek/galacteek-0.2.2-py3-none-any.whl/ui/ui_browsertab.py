# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/browsertab.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BrowserTabForm(object):
    def setupUi(self, BrowserTabForm):
        BrowserTabForm.setObjectName("BrowserTabForm")
        BrowserTabForm.resize(811, 444)
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(BrowserTabForm)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setContentsMargins(-1, -1, -1, 10)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadIpfsButton = QtWidgets.QToolButton(BrowserTabForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/share/icons/ipfs-logo-128-ice.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadIpfsButton.setIcon(icon)
        self.loadIpfsButton.setObjectName("loadIpfsButton")
        self.horizontalLayout.addWidget(self.loadIpfsButton)
        self.loadFromClipboardButton = QtWidgets.QPushButton(BrowserTabForm)
        self.loadFromClipboardButton.setMaximumSize(QtCore.QSize(40, 24))
        self.loadFromClipboardButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/share/icons/clipboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadFromClipboardButton.setIcon(icon1)
        self.loadFromClipboardButton.setObjectName("loadFromClipboardButton")
        self.horizontalLayout.addWidget(self.loadFromClipboardButton)
        self.urlZone = QtWidgets.QLineEdit(BrowserTabForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.urlZone.sizePolicy().hasHeightForWidth())
        self.urlZone.setSizePolicy(sizePolicy)
        self.urlZone.setMinimumSize(QtCore.QSize(400, 0))
        self.urlZone.setMaximumSize(QtCore.QSize(1000, 26))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setItalic(False)
        self.urlZone.setFont(font)
        self.urlZone.setStyleSheet("background-color: rgb(189, 236, 255);")
        self.urlZone.setMaxLength(2048)
        self.urlZone.setObjectName("urlZone")
        self.horizontalLayout.addWidget(self.urlZone)
        self.backButton = QtWidgets.QToolButton(BrowserTabForm)
        self.backButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/share/icons/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon2)
        self.backButton.setObjectName("backButton")
        self.horizontalLayout.addWidget(self.backButton)
        self.forwardButton = QtWidgets.QToolButton(BrowserTabForm)
        self.forwardButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/share/icons/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.forwardButton.setIcon(icon3)
        self.forwardButton.setObjectName("forwardButton")
        self.horizontalLayout.addWidget(self.forwardButton)
        self.stopButton = QtWidgets.QPushButton(BrowserTabForm)
        self.stopButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/share/icons/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon4)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.refreshButton = QtWidgets.QPushButton(BrowserTabForm)
        self.refreshButton.setMaximumSize(QtCore.QSize(50, 24))
        self.refreshButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/share/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon5)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout.addWidget(self.refreshButton)
        self.pinAllButton = QtWidgets.QToolButton(BrowserTabForm)
        self.pinAllButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/share/icons/pin-black.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pinAllButton.setIcon(icon6)
        self.pinAllButton.setObjectName("pinAllButton")
        self.horizontalLayout.addWidget(self.pinAllButton)
        self.actionComboBox = QtWidgets.QComboBox(BrowserTabForm)
        self.actionComboBox.setObjectName("actionComboBox")
        self.horizontalLayout.addWidget(self.actionComboBox)
        self.hashmarkPageButton = QtWidgets.QPushButton(BrowserTabForm)
        self.hashmarkPageButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/share/icons/hashmarks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hashmarkPageButton.setIcon(icon7)
        self.hashmarkPageButton.setObjectName("hashmarkPageButton")
        self.horizontalLayout.addWidget(self.hashmarkPageButton)
        self.progressBar = QtWidgets.QProgressBar(BrowserTabForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(40, 0))
        self.progressBar.setMaximumSize(QtCore.QSize(30, 16777215))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.horizontalLayout_7.addLayout(self.horizontalLayout)
        self.verticalLayout_17.addLayout(self.horizontalLayout_7)
        self.vLayoutBrowser = QtWidgets.QVBoxLayout()
        self.vLayoutBrowser.setObjectName("vLayoutBrowser")
        self.verticalLayout_17.addLayout(self.vLayoutBrowser)
        self.verticalLayout_18.addLayout(self.verticalLayout_17)

        self.retranslateUi(BrowserTabForm)
        QtCore.QMetaObject.connectSlotsByName(BrowserTabForm)

    def retranslateUi(self, BrowserTabForm):
        _translate = QtCore.QCoreApplication.translate
        BrowserTabForm.setWindowTitle(_translate("BrowserTabForm", "Form"))
        self.loadIpfsButton.setToolTip(_translate("BrowserTabForm", "<html><head/><body><p>Browse IPFS</p></body></html>"))
        self.loadIpfsButton.setText(_translate("BrowserTabForm", "..."))
        self.loadFromClipboardButton.setToolTip(_translate("BrowserTabForm", "<html><head/><body><p>Load IPFS CID from clipboard</p></body></html>"))
        self.backButton.setToolTip(_translate("BrowserTabForm", "<html><head/><body><p>Previous</p></body></html>"))
        self.forwardButton.setToolTip(_translate("BrowserTabForm", "<html><head/><body><p>Next</p></body></html>"))
        self.refreshButton.setToolTip(_translate("BrowserTabForm", "<html><head/><body><p>Reload page</p></body></html>"))
        self.pinAllButton.setToolTip(_translate("BrowserTabForm", "<html><head/><body><p>Automatically pins visited pages</p></body></html>"))
        self.actionComboBox.setToolTip(_translate("BrowserTabForm", "<html><head/><body><p>Pin</p></body></html>"))
        self.hashmarkPageButton.setToolTip(_translate("BrowserTabForm", "<html><head/><body><p>Hashmark this page</p></body></html>"))

from . import galacteek_rc
