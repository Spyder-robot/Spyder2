'''
Backlog
- Step size normalizing
- Speed calculated based on path length
- Dualshock 3
- Control send/recieve (main - joistick)
- Menu control (button press - highlight menu, joystick - select, button release - confirm)
- Free gait (walking)
- Free move (without walking)
- Avoid pause between stages
- switch-case for poses
- Temperature measurement delay
- I2C stuck
- Add cycle leverage and fixing avg min max cycle time
- Unactive (grey) unaccessible modes (e.g. Rad from Park)
- Display sensors on Spyder w/o wifi connection
- Processing model adaptation
- Radar scan and draw
- Data collecting W(V) - calculate % of remaining power
- Flickering during video playback
- Smooth moving through stage (not a max speed by cycles)
- Display for joistick (ESP32)
'''

from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, pyqtSlot
from S2draw import ST
from PIL.ImageQt import ImageQt
import cv2
from threading import Thread
import socket
import time

HOST = '192.168.0.102'


class WiFiClient(Thread):

    def __init__(self):
        Thread.__init__(self, target=self.mainCycle)
        self.daemon = True
        self.updt = True
        print("WiFi client started")
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
                        self.U = float(msg)
                    elif varNo == 2:
                        self.A = float(msg)
                    elif varNo == 3:
                        self.W = float(msg)
                    elif varNo == 4:
                        self.T = float(msg)
                    elif varNo == 5:
                        self.F = int(float(msg))
                    elif varNo == 6:
                        self.S = int(float(msg))
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
                if c == "V":
                    varNo = 1
                    parsStage = 2
                elif c == "I":
                    varNo = 2
                    parsStage = 2
                elif c == "W":
                    varNo = 3
                    parsStage = 2
                elif c == "T":
                    varNo = 4
                    parsStage = 2
                elif c == "F":
                    varNo = 5
                    parsStage = 2
                elif c == "S":
                    varNo = 6
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
        return (self.U, self.A, self.W, int(self.T), self.act, self.F, self.S)

    def isActive(self):
        return self.act

    def isUpdated(self):
        return self.updt

    def connect(self):
        self.act = False
        self.U = 0
        self.A = 0
        self.W = 0
        self.T = 0  # Temperature
        self.F = 0  # ToF
        self.S = 0  # State
        print("WiFi trying to connect...")
        cntd = False
        while not cntd:
            cntd = True
            try:
                self.clientSock = socket.socket()
                self.clientSock.connect((HOST, 11111))
            except Exception as e:
                print(e)
                cntd = False
                time.sleep(3)
                self.clientSock.close()
        print("WiFi connected to server")
        self.act = True
        print(self.clientSock.getsockname())
        print(self.clientSock.getpeername())

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
                    self.parse(data)


class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)
    killed = False

    def run(self):
        cap = cv2.VideoCapture('http://'+HOST+':5000')
        while True:
            if self.killed:
                break
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.changePixmap.emit(p)

    def kill(self):
        self.killed = True


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 200, 260, 260)

        self.vid = QLabel(self)
        self.vid.setGeometry(1, 1, 1, 1)

        self.display = QLabel(self)
        self.display.setGeometry(10, 10, 240, 240)

        self.dsp = ST("DejaVuSans-Bold.ttf")
        self.mnit = 6
        self.navi = 0
        self.img = self.dsp.drawCP(self.mnit, self.navi, wf.read())
        self.keyfl = True
        self.videoState = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video)
        self.timer.start(100)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ping)
        self.timer.start(1000)

    def video(self):
        if wf.isActive():
            if not self.videoState and (wf.read()[6] >> 9) & 1 == 1:
                self.setGeometry(400, 10, 660, 750)
                self.vid.setGeometry(10, 10, 640, 480)
                self.display.setGeometry(210, 500, 240, 240)
                self.th = VideoThread(self)
                self.th.changePixmap.connect(self.setImage)
                self.th.start()
                self.videoState = True

            if self.videoState and (wf.read()[6] >> 9) & 1 == 0:
                self.th.kill()
                self.setGeometry(600, 200, 260, 260)
                self.vid.setGeometry(1, 1, 1, 1)
                self.display.setGeometry(10, 10, 240, 240)
                self.videoState = False

    def ping(self):
        if wf.isActive():
            wf.ping()
            self.dsp.wifi = 1
        else:
            self.dsp.wifi = 0

    def paintEvent(self, event):
        self.img = self.dsp.drawCP(self.mnit, self.navi, wf.read())
        self.display.setPixmap(QPixmap.fromImage(ImageQt(self.img)))

    def keyPressEvent(self, event):
        if self.keyfl:
            if event.key() == Qt.Key.Key_N:
                self.mnit += 1
                if self.mnit == 13:
                    self.mnit = 0
                self.keyfl = False
            if event.key() == Qt.Key.Key_V:
                self.mnit -= 1
                if self.mnit == -1:
                    self.mnit = 12
                self.keyfl = False
            if event.key() == Qt.Key.Key_B:
                self.mnit = self.mnit + 100
                self.keyfl = False

        if event.key() == Qt.Key.Key_E:
            self.navi = self.navi | (1 << 6)
        if event.key() == Qt.Key.Key_D:
            self.navi = self.navi | (1 << 7)
        if event.key() == Qt.Key.Key_S:
            self.navi = self.navi | (1 << 4)
        if event.key() == Qt.Key.Key_F:
            self.navi = self.navi | (1 << 5)
        if event.key() == Qt.Key.Key_J:
            self.navi = self.navi | (1 << 2)
        if event.key() == Qt.Key.Key_L:
            self.navi = self.navi | (1 << 3)
        if event.key() == Qt.Key.Key_I:
            self.navi = self.navi | (1 << 0)
        if event.key() == Qt.Key.Key_K:
            self.navi = self.navi | (1 << 1)
        self.sendCntrl()

    def keyReleaseEvent(self, event):
        if not self.keyfl:
            if event.key() == Qt.Key.Key_N or event.key() == Qt.Key.Key_V or event.key() == Qt.Key.Key_B:
                if self.mnit > 99:
                    self.mnit = self.mnit - 100
                self.keyfl = True
        if event.key() == Qt.Key.Key_E:
            self.navi = self.navi ^ (1 << 6)
        if event.key() == Qt.Key.Key_D:
            self.navi = self.navi ^ (1 << 7)
        if event.key() == Qt.Key.Key_S:
            self.navi = self.navi ^ (1 << 4)
        if event.key() == Qt.Key.Key_F:
            self.navi = self.navi ^ (1 << 5)
        if event.key() == Qt.Key.Key_J:
            self.navi = self.navi ^ (1 << 2)
        if event.key() == Qt.Key.Key_L:
            self.navi = self.navi ^ (1 << 3)
        if event.key() == Qt.Key.Key_I:
            self.navi = self.navi ^ (1 << 0)
        if event.key() == Qt.Key.Key_K:
            self.navi = self.navi ^ (1 << 1)
        self.sendCntrl()

    def sendCntrl(self):
        if wf.isActive():
            msg = "<M="+str(self.mnit)+">"
            msg += "<N="+str(self.navi)+">"
            wf.send(msg)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.vid.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    wf = WiFiClient()
    app = QApplication([])
    window = MainWindow()
    window.setStyleSheet('background-color: grey;')
    window.show()
    app.exec()
