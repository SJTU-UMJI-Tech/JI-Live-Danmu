# -*-coding:utf-8 -*-
import math

from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt


# marquee label
class Marquee(QFrame):
    CHANGE_TIMES = 10
    RAINBOW_RGB_LIST = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0),
                        (0, 127, 255), (0, 0, 255), (139, 0, 255)]
    FIXED_WIDTH = 500
    ANIM_TIME = 8000

    def __init__(self, window, text, color):
        super().__init__(window)
        self.screenWidth, self.screenHeight = window.getDisplayArea()
        self.changeColorIdx = 0
        self.clrIdx = 0
        self.changeRGB = [0, 0, 0]
        self.label = QLabel(self)
        self.initUi(text, color, self.screenWidth, self.screenHeight)

    def initUi(self, text, color, screenWidth, screenHeight):
        # self.setStyleSheet("border:1px solid blue;")
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # self.doubleText = text + " " + text
        self.doubleText = text
        self.setFont(QFont('SimHei', 24, 100))
        self.myRect = self.fontMetrics().boundingRect(text)
        self.setGeometry(screenWidth - self.FIXED_WIDTH - 40,
                         screenHeight - self.myRect.height() - 10,
                         self.FIXED_WIDTH + 20,
                         self.myRect.height() + 10)
        self.initLabel(self.label, self.doubleText)
        self.label.anim = QPropertyAnimation(self.label, b'geometry')
        self.label.anim.setDuration(self.ANIM_TIME)
        self.label.anim.setStartValue(
            QRect(
                self.fontMetrics().boundingRect(self.doubleText).width() + 10, 0,
                self.fontMetrics().boundingRect(self.doubleText).width() + 20,
                self.myRect.height() + 10))
        self.label.anim.setEndValue(
            QRect(
                -(self.fontMetrics().boundingRect(self.doubleText).width() + 10), 0,
                self.fontMetrics().boundingRect(self.doubleText).width() + 20,
                self.myRect.height() + 10))
        self.label.anim.setLoopCount(-1)
        self.label.anim.start()
        # self.label.setStyleSheet("border:1px solid red;")
        self.setChangeRGB(self.RAINBOW_RGB_LIST[self.clrIdx],
                          self.RAINBOW_RGB_LIST[(self.clrIdx + 1) % 7])
        self.label.show()

    def initLabel(self, label, text):
        label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        label.setText(text)
        label.setFont(QFont('SimHei', 24, 100))
        eff = QGraphicsDropShadowEffect()
        eff.setColor(QColor(6, 6, 6))
        eff.setBlurRadius(5)
        eff.setOffset(1.5, 1.5)
        label.setGraphicsEffect(eff)
        label.setGeometry(0, 0,
                          self.fontMetrics().boundingRect(text).width() + 20,
                          self.fontMetrics().boundingRect(text).height() + 10)

    def changeColor(self):
        if self.changeColorIdx < self.CHANGE_TIMES:
            pa = QPalette()
            pa.setColor(
                QPalette.Foreground,
                QColor(
                    self.RAINBOW_RGB_LIST[self.clrIdx][0] + self.changeRGB[0] /
                    self.CHANGE_TIMES * self.changeColorIdx,
                    self.RAINBOW_RGB_LIST[self.clrIdx][1] + self.changeRGB[1] /
                    self.CHANGE_TIMES * self.changeColorIdx,
                    self.RAINBOW_RGB_LIST[self.clrIdx][2] + self.changeRGB[2] /
                    self.CHANGE_TIMES * self.changeColorIdx))
            self.label.setPalette(pa)
            self.changeColorIdx += 1
            self.show()
        else:
            self.changeColorIdx = 0
            self.clrIdx = 0 if self.clrIdx == 6 else self.clrIdx + 1
            self.setChangeRGB(self.RAINBOW_RGB_LIST[self.clrIdx],
                              self.RAINBOW_RGB_LIST[(self.clrIdx + 1) % 7])

    def setShadow(self, color, blurRadius, offset):
        self.eff = QGraphicsDropShadowEffect()
        self.eff.setColor(color)
        self.eff.setBlurRadius(blurRadius)
        self.eff.setOffset(offset, offset)
        self.setGraphicsEffect(self.eff)

    def setChangeRGB(self, clr1, clr2):
        self.changeRGB = [
            clr2[0] - clr1[0], clr2[1] - clr1[1], clr2[2] - clr1[2]
        ]

    def hideLabel(self):
        self.label.hide()

    def showLabel(self):
        self.label.show()
