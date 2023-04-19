import ST7789
from PIL import Image, ImageDraw, ImageFont
import time
from threading import Thread
import socket
import serial
from smbus2 import SMBus

import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
from flask import Flask, Response


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


class WiFiServer(Thread):

    def __init__(self):
        Thread.__init__(self, target=self.mainCycle)
        self.daemon = True

        self.M = 6  # Menu item
        self.N = 0  # Navigation flags
        self.H = 0  # Highlighted flags
        self.updt = True    # Defaults
        self.act = False

        self.clientSock = None
        self.mainSock = socket.socket()
        self.mainSock.bind(('', 11111))
        self.mainSock.listen()
        print("WiFi server started")
        self.start()

    def parse(self, data):
        parsStage = 0
        varNo = 0
        msg = ""
        for c in data.decode():
            if parsStage == 3:
                if c == ">":
                    parsStage = 0
                    if varNo == 1:
                        self.M = int(msg)
                    elif varNo == 2:
                        self.N = int(msg)
                    elif varNo == 3:
                        self.H = int(msg)
                    self.updt = True
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

    def send(self, msg):
        try:
            self.clientSock.send(msg.encode())
        except socket.error as e:
            print(e)
            print("WiFi connection lost")
            self.connect()

    def ping(self):
        self.send("PING")

    def read(self):
        self.updt = False
        return (self.M, self.N, self.H)

    def isActive(self):
        return self.act

    def isUpdated(self):
        return self.updt

    def close(self):
        self.clientSock.close()
        self.mainSock.close()

    def connect(self):
        self.act = False
        print("WiFi waiting for connection...")
        self.clientSock, addr = self.mainSock.accept()
        print("WiFi client connected")
        self.act = True
        print(addr)

    def mainCycle(self):
        while True:
            self.connect()
            while True:
                try:
                    data = self.clientSock.recv(1024)
                except socket.error as e:
                    print(e)
                    print("WiFi connection lost")
                    break
                if (data is not None) and (data.decode() != ""):
                    # print("WiFi recieved "+data.decode())
                    self.parse(data)


class ThreadSerial(Thread):

    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud)
        Thread.__init__(self, target=self.serread, args=(self.ser,))
        self.daemon = True
        self.U = 0
        self.A = 0
        self.T1 = 0
        self.T2 = 0
        self.W = 0
        self.start()

    def read(self):
        return (self.U, self.A, self.W, max(self.T1, self.T2))

    def serread(self, serl):
        while True:
            time.sleep(0.1)
            while serl.in_waiting > 0:
                resp = serl.readline()
                va = resp.decode("utf-8", errors="ignore")[:-2]
                # print(va)
                if va[:3] == "<V=":
                    self.U = float(va[3:va.find(">")])
                elif va[:3] == "<I=":
                    self.A = float(va[3:va.find(">")])
                elif va[:3] == "<W=":
                    self.W = float(va[3:va.find(">")])
                elif va[:4] == "<T1=":
                    self.T1 = int(float(va[4:va.find(">")]))
                elif va[:4] == "<T2=":
                    self.T2 = int(float(va[4:va.find(">")]))
                else:
                    print(va)


class I2C:

    def __init__(self):
        self.bus = SMBus(1)

    def read(self, adr, reg, bts):
        try:
            res = self.bus.read_i2c_block_data(adr, reg, bts)
        except OSError:
            res = [-1]
        # print("I2C: Adr-"+str(adr)+" Reg- "+str(reg)+" Read - "+str(res))
        return res

    def write(self, adr, bts):
        try:
            res = self.bus.write_byte(adr, bts)
        except OSError:
            res = [-1]
        if res is None:
            res = [1]

        # print("I2C: Adr-"+str(adr)+" Write - "+str(bts)+" Result - "+str(res))

        return res


class VideoCamera(object):
    def __init__(self):
        self.vs = PiVideoStream(resolution=(320, 240), framerate=24).start()
        time.sleep(1)

    def __del__(self):
        self.vs.stop()

    def get_frame(self):
        frame = imutils.rotate(self.vs.read(), 180)
        jpeg = cv2.imencode('.jpg', frame)[1]
        return jpeg.tobytes()


class ThreadCamera(Thread):

    def __init__(self):
        Thread.__init__(self, target=self.runcam)
        self.daemon = True
        self.start()

    def runcam(self):
        pi_camera = VideoCamera()

        app = Flask(__name__)

        def gen(camera):
            while True:
                frame = camera.get_frame()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        @app.route('/')
        def video_feed():
            return Response(gen(pi_camera),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        app.run(host='0.0.0.0', debug=False)
