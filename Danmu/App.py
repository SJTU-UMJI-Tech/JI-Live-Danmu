# -*-coding:utf-8 -*-
import os
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget
from PyQt5.QtCore import Qt
from Danmu.config import *


# main window class
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0 if os.name == "nt" else 30
        screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
        self.width = screenRect.width()
        self.height = screenRect.height() - 50 if os.name == "nt" \
            else screenRect.height() - 30
        self.initUi()

    def initUi(self):
        if os.name == 'nt':
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool
                                | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow
                                | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowOpacity(WINDOW_OPACITY)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def getDisplayArea(self):
        return self.width, self.height
