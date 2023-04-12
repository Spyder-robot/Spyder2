from S2draw import ST
from spyder2 import s2st, s2bl, WiFiServer, ThreadSerial, I2C
import sys
import time


if __name__ == '__main__':
    disp = s2st()
    drw = ST("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    wf = WiFiServer()
    ser = ThreadSerial("/dev/serial0", 115200)
    i2c = I2C()
    timerSens = time.time()
    flagRGB = False
    flagLED = False
    flagFAN = False
    flagTOF = False
    tof = 0
    timerTof = time.time()

    try:
        while True:
            if wf.isUpdated():
                img = drw.drawCP(wf.read(), ser.read()+(wf.isActive(), tof))
                disp.display(img)
                # print("M = %d, N = %d, H = %d" % wf.read())
                hl = wf.read()[2]

                if not flagLED and hl >> 8 & 1 == 1:
                    i2c.read(0x11, 10, 1)
                    flagLED = True
                if flagLED and hl >> 8 & 1 == 0:
                    i2c.read(0x11, 11, 1)
                    flagLED = False

                if not flagFAN and hl >> 10 & 1 == 1:
                    i2c.read(0x11, 12, 1)
                    flagFAN = True
                if flagFAN and hl >> 10 & 1 == 0:
                    i2c.read(0x11, 13, 1)
                    flagFAN = False

                if not flagRGB and hl >> 9 & 1 == 1:
                    i2c.read(0x11, 14, 1)
                    flagRGB = True
                if flagRGB and hl >> 9 & 1 == 0:
                    i2c.read(0x11, 15, 1)
                    flagRGB = False

                if not flagTOF and hl >> 11 & 1 == 1:
                    flagTOF = True
                if flagTOF and hl >> 11 & 1 == 0:
                    flagTOF = False

            if time.time() - timerTof > 1 and flagTOF:
                tof = tof + 1
                i2c.write(0x70, 0x51)
                time.sleep(.01)
                rang = i2c.read(0x70, 0x00, 2)
                tof = rang[0]*256 + rang[1]
                if wf.isActive():
                    wf.send("<F=%f>" % tof)
                timerTof = time.time()

            if time.time() - timerSens > 3:
                if wf.isActive():
                    wf.send("<V=%f> <I=%f> <W=%f> <T=%f>" % ser.read())
                img = drw.drawCP(wf.read(), ser.read()+(wf.isActive(), tof))
                disp.display(img)
                timerSens = time.time()

    except KeyboardInterrupt:
        s2bl(disp)
        wf.close()
        sys.exit()
