import time
import re
import sip
from PyQt5.QtGui import QColor
from Danmu.Danmu import Danmu
from Danmu.config import *


# manage all Danmus
class DanmuManager:
    def __init__(self, window, displayArea=0.9):
        self.window = window
        self.width, self.height = window.getDisplayArea()
        self.flyTracks = []
        self.topTracks = []
        self.btmTracks = []
        for _ in range(int(self.height * displayArea / (FONT_SIZE + 20))):
            self.flyTracks.append([])
            self.topTracks.append([])
            self.btmTracks.append([])
        self.flyDanmuQueue = []
        self.topDanmuQueue = []
        self.btmDanmuQueue = []

    def cleanDanmu(self):
        timeNow = time.time()
        invlTime = DISPLAY_TIME / 1000 + 0.5
        for track in self.flyTracks:
            if track and timeNow - track[0][1] > invlTime:
                sip.delete(track[0][0])
                track.pop(0)
        for track in self.topTracks:
            if track and timeNow - track[0][1] > invlTime:
                sip.delete(track[0][0])
                track.pop(0)
        for track in self.btmTracks:
            if track and timeNow - track[0][1] > invlTime:
                sip.delete(track[0][0])
                track.pop(0)

    # put Danmu in queue on track
    def showDanmu(self):
        isAdded = True
        while self.flyDanmuQueue and isAdded:
            isAdded = False
            text, color = self.flyDanmuQueue[0]
            danmu = Danmu(text, color, 0, self.window)
            v2 = danmu.getSpeed()
            for idx, track in enumerate(self.flyTracks):
                if not track:
                    track.append((danmu, time.time()))
                    track[-1][0].showFlyDanmu((FONT_SIZE + 20) * idx)
                    isAdded = True
                    break
                else:
                    v1 = track[-1][0].getSpeed()
                    minIntervalTime = (self.width + track[-1][0].width() -
                                       self.width * v1 / v2) / v1
                    minIntervalTime = max(minIntervalTime,
                                          track[-1][0].width() / v1)
                    if time.time() - track[-1][1] > minIntervalTime / 1000:
                        track.append((danmu, time.time()))
                        track[-1][0].showFlyDanmu((FONT_SIZE + 20) * idx)
                        isAdded = True
                        break
            if isAdded:
                self.flyDanmuQueue.pop(0)
            else:
                sip.delete(danmu)

        isAdded = True
        while self.topDanmuQueue and isAdded:
            isAdded = False
            text, color = self.topDanmuQueue[0]
            for idx, track in enumerate(self.topTracks):
                if not track or time.time(
                ) - track[-1][1] > DISPLAY_TIME / 1000 + 1:
                    track.append((Danmu(text, color, (FONT_SIZE + 20) * idx,
                                        self.window), time.time()))
                    track[-1][0].showFixedDanmu()
                    isAdded = True
                    break
            if isAdded:
                self.topDanmuQueue.pop(0)

        isAdded = True
        while self.btmDanmuQueue and isAdded:
            isAdded = False
            text, color = self.btmDanmuQueue[0]
            for idx, track in enumerate(self.btmTracks):
                if not track or time.time(
                ) - track[-1][1] > DISPLAY_TIME / 1000 + 1:
                    track.append((Danmu(
                        text, color,
                        self.height - (FONT_SIZE + 20) * (1 + idx),
                        self.window), time.time()))
                    track[-1][0].showFixedDanmu()
                    isAdded = True
                    break
            if isAdded:
                self.btmDanmuQueue.pop(0)

    # add Danmu to queue
    def addDanmu(self, text):
        repeat = re.search(r'\#time(\d+)', text)
        if repeat:
            repeatCount = max(min(MAX_REPEAT_COUNT, int(repeat.group(1))), 1)
            message = re.sub(r'\#time\d+', '', text)
            # rainbow Danmu for multiple times
            if not re.search(r'\#[0-9a-fA-F]{6}', message):
                rainbowRgbIndex = 0
                for _ in range(repeatCount):
                    self.addDanmu(RAINBOW_RGB_LIST[rainbowRgbIndex] + message)
                    rainbowRgbIndex = 0 if rainbowRgbIndex == 6 \
                        else rainbowRgbIndex + 1
            else:
                for _ in range(repeatCount):
                    self.addDanmu(message)
        else:
            # classify Danmu
            text, color, style = self.parseText(text)
            if len(text.strip()) == 0:
                return
            if style == 'fly':
                self.flyDanmuQueue.append((text, color))
            elif style == 'top':
                self.topDanmuQueue.append((text, color))
            elif style == 'btm':
                self.btmDanmuQueue.append((text, color))

    # analyze special commands in text
    def parseText(self, text):
        text = re.sub(r'/Emoji\d+|/表情|^ | $', '',
                      text.replace('\n', ' '))[0:MAX_STR_LEN]
        textColor = QColor(240, 240, 240)
        style = 'fly'
        if re.search(r'请使用手机QQ进行查看', text):
            return '', textColor, style
        matchObject = re.search(
            r'\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', text)
        if matchObject:
            textColor = QColor(
                int(matchObject.group(1), 16), int(matchObject.group(2), 16),
                int(matchObject.group(3), 16))
            text = re.sub(r'\#[0-9a-fA-F]{6}', '', text)
        if re.search(r'\#top', text, re.I):
            style = 'top'
            text = re.sub(r'\#top', '', text, re.I)
        elif re.search(r'\#btm', text, re.I):
            style = 'btm'
            text = re.sub(r'\#btm', '', text, re.I)
        return text.strip(), textColor, style
