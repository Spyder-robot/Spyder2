'''
Backlog
- WiFi связь
- Передача управления по WiFi
- Arduino датчики
- Передача датчиков по WiFi
'''


from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
from S2draw import ST
from PIL.ImageQt import ImageQt


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
        self.img = self.dsp.drawCP(self.mnit, self.navi)
        self.keyfl = True

    def paintEvent(self, event):
        self.img = self.dsp.drawCP(self.mnit, self.navi)
        self.display.setPixmap(QPixmap.fromImage(ImageQt(self.img)))

    def keyPressEvent(self, event):
        if self.keyfl:
            if event.key() == Qt.Key.Key_Right:
                self.mnit += 1
                if self.mnit == 13:
                    self.mnit = 0
                self.keyfl = False
            if event.key() == Qt.Key.Key_Left:
                self.mnit -= 1
                if self.mnit == -1:
                    self.mnit = 12
                self.keyfl = False
            if event.key() == 16777220:
                self.dsp.mntpl[self.mnit][0] = abs(self.dsp.mntpl[self.mnit][0] - 1)
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
        self.update()

    def keyReleaseEvent(self, event):
        if not self.keyfl:
            if event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_Left or event.key() == 16777220:
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


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.setStyleSheet('background-color: grey;')
    window.show()
    app.exec()
