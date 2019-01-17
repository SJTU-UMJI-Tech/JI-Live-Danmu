# -*-coding:utf-8 -*-
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import re
from Danmu.config import *


# Danmu class
class Danmu(QLabel):
    def __init__(self, text, color, top, window):
        super(Danmu, self).__init__(window)
        self.top = top
        self.setTextFormat(Qt.PlainText)
        self.setText(text)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setFont(QFont('SimHei', FONT_SIZE, 100))
        # set size of label
        myRect = self.fontMetrics().boundingRect(text)
        self.setFixedSize(myRect.width() + 20, myRect.height() + 10)
        self.setColor(color)
        self.setShadow(QColor('#060606'), 5, 1.5)
        # self.setStyleSheet("border:1px solid red;")

    def setColor(self, color):
        pa = QPalette()
        pa.setColor(QPalette.Foreground, color)
        self.setPalette(pa)

    def setShadow(self, color, blurRadius, offset):
        self.eff = QGraphicsDropShadowEffect()
        self.eff.setColor(color)
        self.eff.setBlurRadius(blurRadius)
        self.eff.setOffset(offset, offset)
        self.setGraphicsEffect(self.eff)

    def setFlyAnim(self, top, displayTime):
        self.anim = QPropertyAnimation(self, b'geometry')
        self.anim.setDuration(displayTime)
        self.anim.setStartValue(
            QRect(self.window().width - 1, top, self.width(), self.height()))
        self.anim.setEndValue(
            QRect(-self.width(), top, self.width(), self.height()))

    def showFlyDanmu(self, top=None):
        if top:
            self.top = top
        self.setFlyAnim(self.top, DISPLAY_TIME)
        self.show()
        self.anim.start()

    def setFixedAnim(self, top, displayTime):
        self.anim = QPropertyAnimation(self, b'geometry')
        self.anim.setDuration(displayTime)
        self.anim.setStartValue(
            QRect(
                int((self.window().width - self.width()) / 2), top,
                self.width(), self.height()))
        self.anim.setEndValue(
            QRect(
                int((self.window().width - self.width()) / 2), top,
                self.width(), self.height()))

    def showFixedDanmu(self):
        self.setFixedAnim(self.top, DISPLAY_TIME)
        self.show()
        self.anim.start()

    def getSpeed(self):
        return (self.width() + self.window().width) / DISPLAY_TIME
