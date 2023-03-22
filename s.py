from S2draw import ST
from spyder2 import s2st, s2bl, ThreadWiFi
import sys
import time

import socket


if __name__ == '__main__':
    disp = s2st()
    drw = ST("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    wf = ThreadWiFi()
    print("Ready")
    try:
        while True:
            if wf.updt:
                wf.updt = False
                print("M = %d, N = %d, H = %d" % (wf.mnit, wf.navi, wf.hlgt))
                img = drw.drawCP(wf.mnit, wf.navi, wf.hlgt)
                disp.display(img)
            try:
                print(wf.wificonn.send("PING".encode()))
            except AttributeError as e:
                print(e)
            except socket.error as e:
                print(e)
            time.sleep(1)
            # if wf.wificonn:
            #     try:
            #         wf.wificonn.send("123".encode())
            #     except socket.error as e:
            #         wf.wificonn = None
            #         print(e)
    except KeyboardInterrupt:
        s2bl(disp)
        sys.exit()
