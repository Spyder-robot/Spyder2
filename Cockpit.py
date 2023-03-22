'''
Backlog
- wifi library (QTimer)
- Arduino датчики
- Передача датчиков по WiFi
'''

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
from S2draw import ST
from PIL.ImageQt import ImageQt

from threading import Thread
import socket

HOST = '10.0.1.20'


class ThreadWiFi(Thread):

    def __init__(self):
        Thread.__init__(self, target=self.wifi)
        self.daemon = True
        self.start()

    def wifi(self):
        cntd = False
        while True:
            while not cntd:
                self.sct = socket.socket()
                cntd = True
                try:
                    self.sct.connect((HOST, 11111))
                except TimeoutError as e:
                    print(e)
                    cntd = False
            print(self.sct.getpeername())
            while True:
                data = self.sct.recv(1024)
                if data is not None:
                    print(data.decode())

    def iswifi(self):
        try:
            self.sct.getpeername()
        except socket.error:
            return False
        return True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 200, 260, 280)

        self.display = QLabel(self)
        self.display.setGeometry(10, 10, 240, 240)

        self.statbar = QLabel(self)
        self.statbar.setGeometry(10, 260, 240, 10)
        self.statbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statbar.setStyleSheet('color: white;')
        self.statbar.setText('Status Bar')

        self.dsp = ST("DejaVuSans-Bold.ttf")
        self.mnit = 6
        self.navi = 0
        self.hlgt = 0
        self.img = self.dsp.drawCP(self.mnit, self.navi, self.hlgt)
        self.keyfl = True

    def paintEvent(self, event):
        self.img = self.dsp.drawCP(self.mnit, self.navi, self.hlgt)
        self.display.setPixmap(QPixmap.fromImage(ImageQt(self.img)))
        if wf.iswifi():
            self.dsp.wifi = 1
        else:
            self.dsp.wifi = 0

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
                self.hlgt = self.hlgt ^ (1 << self.mnit)
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
        if wf.iswifi():
            msg = "<M="+str(self.mnit)+">"
            msg += "<N="+str(self.navi)+">"
            msg += "<H="+str(self.hlgt)+">"
            wf.sct.send(msg.encode())


if __name__ == '__main__':
    wf = ThreadWiFi()
    app = QApplication([])
    window = MainWindow()
    window.setStyleSheet('background-color: grey;')
    window.show()
    app.exec()
