import ST7789
from PIL import Image, ImageDraw, ImageFont
import time
from threading import Thread
import socket


def s2st():
    disp = ST7789.ST7789(port=0, cs=0, rst=23, dc=24, backlight=25, rotation=0, spi_speed_hz=80 * 1000 * 1000)
    disp._spi.mode = 3
    disp.reset()
    disp._init()
    img = Image.new('RGB', (240, 240), color=(0, 0, 0))
    disp.display(img)
    draw = ImageDraw.Draw(img)
    fontmenu = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    draw.text((120, 120), "SPYDER 2.0", font=fontmenu, fill=(255, 255, 255), anchor="mm")
    disp.display(img)
    time.sleep(3)
    return disp


def s2bl(disp):
    img = Image.new('RGB', (240, 240), color=(0, 0, 0))
    disp.display(img)


class ThreadWiFi(Thread):

    def __init__(self):
        Thread.__init__(self, target=self.wifi)
        self.daemon = True
        self.wificonn = None
        self.start()
        self.mnit = 6
        self.navi = 0
        self.hlgt = 0
        self.updt = True

    def wifi(self):
        s = socket.socket()
        s.bind(('', 11111))

        while True:
            s.listen()
            self.wificonn, addr = s.accept()
            print(addr)
            while self.wificonn:
                data = self.wificonn.recv(1024)
                if data is not None:
                    if data.decode() == "":
                        break
                    print(data)
                    parsStage = 0
                    varNo = 0
                    msg = ""
                    for c in data.decode():
                        if parsStage == 3:
                            if c == ">":
                                parsStage = 0
                                self.updt = True
                                if varNo == 1:
                                    self.mnit = int(msg)
                                elif varNo == 2:
                                    self.navi = int(msg)
                                elif varNo == 3:
                                    self.hlgt = int(msg)
                            else:
                                msg = msg + c
                        if parsStage == 2:
                            if c == "=":
                                parsStage = 3
                                msg = ""
                            else:
                                parsStage = 0
                        if parsStage == 1:
                            if c == "M":
                                varNo = 1
                                parsStage = 2
                            elif c == "N":
                                varNo = 2
                                parsStage = 2
                            elif c == "H":
                                varNo = 3
                                parsStage = 2
                            else:
                                parsStage = 0
                        if parsStage == 0 and c == "<":
                            parsStage = 1
