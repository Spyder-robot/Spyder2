from S2draw import ST
from spyder2 import s2st, s2bl, WiFiServer, ThreadSerial, I2C, ThreadCamera, ToF
import sys
import time


if __name__ == '__main__':
    disp = s2st()
    drw = ST("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    wf = WiFiServer()
    ser = ThreadSerial("/dev/serial0", 115200)
    ThreadCamera()
    i2c = I2C()
    timer = time.time()

    stateARD = 0
    stateVID = 0
    stateTOF = 0
    menuPressed = False
    tof = 0

    try:
        while True:
            if wf.isUpdated():
                wfmsg = wf.read()
                if menuPressed:
                    if wfmsg[0] < 100:
                        menuPressed = False
                else:
                    if wfmsg[0] > 99:
                        if wfmsg[0] == 100:
                            wfm = 13  # workaround for transmition error causing cmd==0
                        else:
                            wfm = wfmsg[0] - 100
                        i2c.write(0x11, 1, (wfm,))
                        menuPressed = True
                        if wfm == 11:
                            stateTOF = stateTOF ^ 1
                        if wfm == 12:
                            stateVID = stateVID ^ 1

            if time.time() - timer > .2:
                stateARD = i2c.read(0x11, 0, 1)[0]
                if (stateTOF == 1):
                    tof = ToF(i2c)
                else:
                    tof = 0

                if wf.isActive():
                    wf.send("<V=%f> <I=%f> <W=%f> <T=%f>" % ser.read())
                    if stateARD & 3 != 3:
                        wf.send("<S=%f>" % (stateARD + (stateTOF << 8) + (stateVID << 9)))
                    if stateTOF == 1:
                        wf.send("<F=%f>" % tof)
                if stateARD & 3 != 3:
                    img = drw.drawCP(wf.read()[0], wf.read()[1], ser.read()+(wf.isActive(), tof,
                                     stateARD + (stateTOF << 8) + (stateVID << 9)))
                    disp.display(img)

                timer = time.time()

    except KeyboardInterrupt:
        s2bl(disp)
        wf.close()
        sys.exit()
