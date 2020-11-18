# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'eliteDangerous.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1196, 800)
        font = QFont()
        font.setFamily(u"DejaVu Sans")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lbl_credits = QLabel(self.frame_2)
        self.lbl_credits.setObjectName(u"lbl_credits")

        self.gridLayout_3.addWidget(self.lbl_credits, 0, 4, 1, 1, Qt.AlignRight)

        self.lbl_commander = QLabel(self.frame_2)
        self.lbl_commander.setObjectName(u"lbl_commander")
        self.lbl_commander.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )

        self.gridLayout_3.addWidget(self.lbl_commander, 0, 1, 1, 1)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 3, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 1, 3, 1, 1)

        self.lbl_ship_name = QLabel(self.frame_2)
        self.lbl_ship_name.setObjectName(u"lbl_ship_name")
        self.lbl_ship_name.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )

        self.gridLayout_3.addWidget(self.lbl_ship_name, 1, 1, 1, 1)

        self.lbl_ship_type = QLabel(self.frame_2)
        self.lbl_ship_type.setObjectName(u"lbl_ship_type")

        self.gridLayout_3.addWidget(self.lbl_ship_type, 1, 4, 1, 1, Qt.AlignRight)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)

        self.line = QFrame(self.frame_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setFrameShape(QFrame.VLine)

        self.gridLayout_3.addWidget(self.line, 0, 2, 2, 1)

        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.table_inventory = QTableWidget(self.frame_3)
        self.table_inventory.setObjectName(u"table_inventory")

        self.horizontalLayout.addWidget(self.table_inventory)

        self.tree_loadout = QTreeView(self.frame_3)
        self.tree_loadout.setObjectName(u"tree_loadout")
        self.tree_loadout.setFrameShape(QFrame.StyledPanel)
        self.tree_loadout.setFrameShadow(QFrame.Sunken)
        self.tree_loadout.setLineWidth(1)

        self.horizontalLayout.addWidget(self.tree_loadout)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout_2.addWidget(self.frame_3, 1, 0, 1, 1)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1196, 22))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.action_quit)

        self.retranslateUi(MainWindow)
        self.action_quit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"MainWindow", None)
        )
        self.action_quit.setText(
            QCoreApplication.translate("MainWindow", u"Quit", None)
        )
        # if QT_CONFIG(shortcut)
        self.action_quit.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Q", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.lbl_credits.setText("")
        self.lbl_commander.setText("")
        self.label_9.setText(
            QCoreApplication.translate("MainWindow", u"Commander:", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", u"Credits:", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", u"Ship Type:", None)
        )
        self.lbl_ship_name.setText("")
        self.lbl_ship_type.setText("")
        self.label.setText(
            QCoreApplication.translate("MainWindow", u"Ship Name:", None)
        )
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))

    # retranslateUi
