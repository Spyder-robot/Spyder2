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
    timer1000 = time.time()
    flagLED = False
    flagFAN = False

    try:
        while True:
            if wf.isUpdated():
                img = drw.drawCP(wf.read(), ser.read()+(wf.isActive(),))
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

            if time.time() - timer1000 > 3:
                if wf.isActive():
                    wf.send("<V=%f> <I=%f> <W=%f> <T=%f>" % ser.read())
                img = drw.drawCP(wf.read(), ser.read()+(wf.isActive(),))
                disp.display(img)
                timer1000 = time.time()

    except KeyboardInterrupt:
        s2bl(disp)
        wf.close()
        sys.exit()
