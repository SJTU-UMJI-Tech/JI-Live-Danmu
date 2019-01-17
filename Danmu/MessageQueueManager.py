from urllib.request import urlopen
from urllib.parse import urlencode, urljoin
import time
import socket
from queue import Queue
import threading as td
import ssl
import sys
import re


class MessageQueueManager:
    def __init__(self, url, port):
        self.localmq = Queue()
        self.url = url
        self.port = port
        # try to create a thread to push message to queue
        self.connect()
        td.Thread(
            target=self.getSocketMessage,
            args=(self.localmq, url, port),
            daemon=True).start()

    def connect(self):
        for i in range(65535):
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(10)
                self.sslSock = ssl.wrap_socket(
                    self.s, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
                self.sslSock.connect((self.url, self.port))
                self.sslSock.settimeout(None)
                print('\nConnected' if i > 0 else 'Connected')
                print(self.sslSock.getpeercert())
                break
            except ConnectionRefusedError:
                print(
                    '\rConnectionRefused,' + 'retrying(%d)' % (i + 1), end='')
                time.sleep(5)
            except:
                print("Unexpected error in connect:", str(sys.exc_info()))
                time.sleep(5)

    def getSocketMessage(self, q, url, port):
        emptyMessageCountdown = 0
        while True:
            messages = ''
            try:
                buffer = []
                while True:
                    # receive 1024 byte in maximum
                    d = self.sslSock.recv(1024)
                    if d:
                        buffer.append(d)
                    if len(d) < 1024:
                        break
                messages = b''.join(buffer).decode('utf-8')
                for msg in messages.split('\0'):
                    if len(msg) > 0:
                        q.put(msg)
                        print(msg)
            except socket.timeout:
                print("Socket time out")
                messages = '\0'
            except:
                print("Unexpected error in getSocketMessage:",
                      str(sys.exc_info()))
            if len(messages) == 0:
                emptyMessageCountdown += 1
                print('Empty message %d' % emptyMessageCountdown)
                if emptyMessageCountdown >= 10:
                    self.connect()
                    emptyMessageCountdown = 0
            else:
                emptyMessageCountdown = 0
            time.sleep(0.1)

    def classifyDanmu(self, mainWindow, danmuManager, marquee):
        while not self.localmq.empty():
            newDanmu = self.localmq.get()
            if re.search(r"#system ", newDanmu, re.I):
                if re.search(r"marquee hide", newDanmu, re.I):
                    marquee.hideLabel()
                elif re.search(r"marquee show", newDanmu, re.I):
                    marquee.showLabel()
            else:
                danmuManager.addDanmu(newDanmu)
        danmuManager.showDanmu()
