from S2draw import ST
from spyder2 import s2st, s2bl, WiFiServer, ThreadSerial
import sys
import time

if __name__ == '__main__':
    disp = s2st()
    drw = ST("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    wf = WiFiServer()
    ser = ThreadSerial("/dev/serial0", 115200)
    timer1000 = time.time()
    try:
        while True:
            if wf.isUpdated():
                mg = drw.drawCP(wf.read(), ser.read()+(wf.isActive(),))
                disp.display(img)
            if time.time() - timer1000 > 1:
                if wf.isActive():
                    wf.send("<V=%f> <I=%f> %d <T=%f>" % ser.read())
                print("M = %d, N = %d, H = %d" % wf.read())
                img = drw.drawCP(wf.read(), ser.read()+(wf.isActive(),))
                disp.display(img)
                timer1000 = time.time()

    except KeyboardInterrupt:
        s2bl(disp)
        wf.close()
        sys.exit()
