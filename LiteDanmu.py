# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEventLoop, QTimer
import os
import time
import re
from urllib.request import urlopen
import threading
from queue import Queue


FONT_SIZE = 24
DISPLAY_AREA = 0.9
DISPLAY_TIME = 8000
INVL_TIME = 2000
WINDOW_OPACITY = 0.8
MAX_STR_LEN = 30
RAINBOW_RGB_LIST = ['#FF0000','#FFA500','#FFFF00','#00FF00','#007FFF','#0000FF','#8B00FF']
screenRect = None
screenWidth = None
screenHeight = None


class Danmu(QLabel):
    def __init__(self, text, color, y, parent=None):
        super(Danmu, self).__init__(parent)
        self.yPos = y
        text = re.sub(r'/Emoji\d+|/表情|^ | $', '',
                      text.replace('\n', ' '))[0:MAX_STR_LEN]
        self.setText(text)
        self.setFont(QFont('SimHei', FONT_SIZE, 100))
        pa = QPalette()
        pa.setColor(QPalette.Foreground, color)
        self.setPalette(pa)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowOpacity(WINDOW_OPACITY)
        if os.name == 'nt':
            self.setWindowFlags(Qt.FramelessWindowHint |
                                Qt.Tool | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint |
                                Qt.SubWindow | Qt.WindowStaysOnTopHint)

        self.eff = QGraphicsDropShadowEffect()
        self.eff.setBlurRadius(5)
        self.eff.setColor(QColor('#060606'))
        self.eff.setOffset(1.5, 1.5)
        self.setGraphicsEffect(self.eff)

        self.anim = QPropertyAnimation(self, b'geometry')
        self.setFixedSize(self.fontMetrics().boundingRect(self.text()).width(
        ) + 10, self.fontMetrics().boundingRect(self.text()).height())

    def showFlyDM(self):
        self.anim.setDuration(DISPLAY_TIME)
        self.anim.setStartValue(
            QRect(screenWidth - 1, self.yPos, self.width(), self.height()))
        self.anim.setEndValue(
            QRect(-self.width(), self.yPos, self.width(), self.height()))

        self.show()
        self.anim.start()

    def showFixedDM(self):
        self.anim.setDuration(DISPLAY_TIME)
        self.anim.setStartValue(
            QRect(int((screenWidth - self.width()) / 2), self.yPos, self.width(), self.height()))
        self.anim.setEndValue(
            QRect(int((screenWidth - self.width()) / 2), self.yPos, self.width(), self.height()))

        self.show()
        self.anim.start()


class DanmuManager:
    def __init__(self, display_area=0.8):
        self.flyDandaos = []
        self.topDandaos = []
        self.btmDandaos = []
        for _ in range(int(screenHeight * display_area / (FONT_SIZE + 20))):
            self.flyDandaos.append([])
            self.topDandaos.append([])
            self.btmDandaos.append([])

    def destroyDM(self):
        for dandao in self.flyDandaos:
            while dandao:
                if dandao[0][0] is not None and time.time() - dandao[0][1] > DISPLAY_TIME / 1000 + 2:
                    dandao[0][0].destroy()
                    dandao.pop(0)
                else:
                    break
        for dandao in self.topDandaos:
            while dandao:
                if dandao[0][0] is not None and time.time() - dandao[0][1] > DISPLAY_TIME / 1000 + 2:
                    dandao[0][0].destroy()
                    dandao.pop(0)
                else:
                    break
        for dandao in self.btmDandaos:
            while dandao:
                if dandao[0][0] is not None and time.time() - dandao[0][1] > DISPLAY_TIME / 1000 + 2:
                    dandao[0][0].destroy()
                    dandao.pop(0)
                else:
                    break

    def add(self, text):
        text, color, style = self.parse(text)
        flag = True if text else False
        while flag:
            if style == 'fly':
                myDandaos = self.flyDandaos
            elif style == 'top':
                myDandaos = self.topDandaos
            elif style == 'btm':
                myDandaos = self.btmDandaos
            for idx, dandao in enumerate(myDandaos):
                if style == 'fly' and flag and (not dandao or time.time() - dandao[-1][1] > INVL_TIME / 1000):
                    dandao.append(
                        (Danmu(text, color, (FONT_SIZE + 20)*idx), time.time())
                    )
                    dandao[-1][0].showFlyDM()
                    flag = False
                elif style == 'top' and flag and (not dandao or time.time() - dandao[-1][1] > DISPLAY_TIME / 1000):
                    dandao.append(
                        (Danmu(text, color, (FONT_SIZE + 20)*idx), time.time())
                    )
                    dandao[-1][0].showFixedDM()
                    flag = False
                elif style == 'btm' and flag and (not dandao or time.time() - dandao[-1][1] > DISPLAY_TIME / 1000):
                    dandao.append(
                        (Danmu(text, color, screenHeight -
                               (FONT_SIZE+20)*(2+idx)), time.time())
                    )
                    dandao[-1][0].showFixedDM()
                    flag = False
                if not flag:
                    break
            if flag:
                loop = QEventLoop()
                QTimer.singleShot(400, loop.quit)
                loop.exec()

    def parse(self, text):
        txtColor = QColor(240, 240, 240)
        style = 'fly'
        matchObj = re.search(
            r'\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', text)
        if matchObj:
            txtColor = QColor(int(matchObj.group(1), 16), int(
                matchObj.group(2), 16), int(matchObj.group(3), 16))
            text = re.sub(r'\#[0-9a-fA-F]{6}', '', text)
        if re.search(r'\#top', text, re.I):
            style = 'top'
            text = re.sub(r'\#top', '', text, re.I)
        elif re.search(r'\#btm', text, re.I):
            style = 'btm'
            text = re.sub(r'\#btm', '', text, re.I)
        return text, txtColor, style


if __name__ == '__main__':
    print("Started")
    app = QApplication(sys.argv)
    screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
    screenWidth = screenRect.width()
    screenHeight = screenRect.height()

    danmu_manager = DanmuManager(DISPLAY_AREA)
    danmu_manager.add('Hello, world!')

    while True:
        loop = QEventLoop()
        QTimer.singleShot(50, loop.quit)
        loop.exec()
        danmu_manager.destroyDM()
        message = urlopen('http://127.0.0.1:5000/get').read().decode('utf-8')
        if message != 'Error:Empty':
            loopTime = 1
            matchObj = re.search(
                r'\#time(\d+)', message)
            if matchObj:
                rbClrIdx = 0
                loopTime = max(min(20, int(matchObj.group(1))), 1)
                message = re.sub('\#time\d+', '', message)
                if not re.search(r'\#[0-9a-fA-F]{6}', message):
                    for _ in range(loopTime):
                        danmu_manager.add(RAINBOW_RGB_LIST[rbClrIdx] + message)
                        rbClrIdx = 0 if rbClrIdx == 6 else rbClrIdx + 1
                else:
                    for _ in range(loopTime):
                        danmu_manager.add(message)
                        rbClrIdx = 0 if rbClrIdx == 6 else rbClrIdx + 1
            else:
                danmu_manager.add(message)
        else:
            loop = QEventLoop()
            QTimer.singleShot(200, loop.quit)
            loop.exec()
