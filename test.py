# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode
import time
import random

# pressure test
if __name__ == "__main__":
    while True:
        content = ''
        if random.random() < 0.4:
            content += '#'
            for i in range(3):
                tmp = hex(random.randint(0, 255))[2:]
                if len(tmp) == 1:
                    tmp = '0' + tmp
                content += tmp
        if random.random() < 0.1:
            content += '#btm '
        elif random.random() < 0.11:
            content += '#top '
        if random.random() < 0.2:
            content += '#time' + str(random.randint(2, 20)) + ' '
        WORDS = ("python", "jumble", "easy", "difficult", "answer",
                 "xylophone")
        for i in range(random.randint(1, 3)):
            content += ' ' + random.choice(WORDS)
        try:
            urlopen('http://127.0.0.1:5000/push?' +
                    urlencode({
                        'message': content
                    }))
        except:
            pass
        time.sleep(0.1)
