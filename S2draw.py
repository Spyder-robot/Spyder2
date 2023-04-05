from PIL import ImageDraw, Image, ImageFont


class ST:

    vth1 = 11
    vth2 = 10
    cth1 = 40
    cth2 = 60

    mntpl = [[[0, 176, 40, 220], [20, 198], "Sc"],
             [[0, 132, 40, 176], [20, 154], "Pk"],
             [[0, 88, 40, 132], [20, 110], "Rd"],
             [[0, 44, 40, 88], [20, 66], "Al"],
             [[0, 0, 40, 44], [20, 22], "Mn"],
             [[40, 0, 93, 44], [67, 22], "SET"],
             [[93, 0, 147, 44], [120, 22], "SYS"],
             [[147, 0, 200, 44], [173, 22], "TST"],
             [[200, 0, 239, 44], [220, 22], "Ld"],
             [[200, 44, 239, 88], [220, 66], "Rg"],
             [[200, 88, 239, 132], [220, 110], "Fn"],
             [[200, 132, 239, 176], [220, 154], "Tf"],
             [[200, 176, 239, 220], [220, 198], "Vi"]]

    def __init__(self, fstr):
        self.fontstr = fstr

    def drawSBline(self, drw, x):
        drw.line((x, 220, x, 239), (255, 255, 255))

    def drawSBtext(self, drw, x, txt, col=(255, 255, 255)):
        fontmenu = ImageFont.truetype(self.fontstr, 15)
        drw.text((x, 230), txt, font=fontmenu, fill=col, anchor="mm")

    def drawSB(self, drw, tpl):

        vcol = 0
        ccol = 0
        wificol = 0
        v, a, w, c, wifi = tpl

        drw.rectangle((0, 220, 239, 239), outline=(255, 255, 255))

        vcol = 0x00ff00
        if v < self.vth1:
            vcol = 0x00ffff
        if v < self.vth2:
            vcol = 0x0000ff

        ccol = 0x00ff00
        if c > self.cth1:
            ccol = 0x00ffff
        if c > self.cth2:
            ccol = 0x0000ff

        if wifi:
            wificol = 0x00ff00
        else:
            wificol = 0x0000ff

        self.drawSBtext(drw, 28, "{:04.1f}V".format(v), vcol)
        self.drawSBtext(drw, 77, "{:03.1f}A".format(a))
        self.drawSBtext(drw, 129, "{:04.1f}W".format(w))
        self.drawSBtext(drw, 178, "{:02d}C".format(c), ccol)
        self.drawSBtext(drw, 218, "WiFi", wificol)

        self.drawSBline(drw, 55)
        self.drawSBline(drw, 99)
        self.drawSBline(drw, 159)
        self.drawSBline(drw, 196)

    def drawMN(self, drw, actmn, hlg):
        drw.font = ImageFont.truetype(self.fontstr, 20)

        for i in range(13):
            if hlg & (1 << i) == 0:
                drw.rectangle(self.mntpl[i][0])
                drw.text(self.mntpl[i][1], self.mntpl[i][2], anchor="mm")
            else:
                drw.rectangle(self.mntpl[i][0], 0xffffff)
                drw.text(self.mntpl[i][1], self.mntpl[i][2], 0, anchor="mm")

        drw.rectangle(self.mntpl[actmn][0], outline=(255, 255, 0), width=5)

        if hlg & (1 << 11):
            drw.text((125, 60), "{:04.2f}m".format(self.tof), anchor="mm")

    def bitCH(self, kbd, bt):
        if kbd & (1 << bt):
            return 0xff0000
        else:
            return 0xffffff

    def drawSP(self, drw, kbd):
        col = 0xffffff
        drw.regular_polygon((120, 140, 20), 6, 0, col)

        col = self.bitCH(kbd, 0)
        drw.regular_polygon((120, 80, 10), 3, 0, col)
        drw.rectangle((115, 80, 125, 115), col)

        col = self.bitCH(kbd, 1)
        drw.regular_polygon((120, 200, 10), 3, 180, col)
        drw.rectangle((115, 165, 125, 200), col)

        col = self.bitCH(kbd, 2)
        drw.regular_polygon((60, 140, 10), 3, 90, col)
        drw.rectangle((60, 135, 95, 145), col)

        col = self.bitCH(kbd, 3)
        drw.regular_polygon((180, 140, 10), 3, 270, col)
        drw.rectangle((145, 135, 180, 145), col)

        col = self.bitCH(kbd, 4)
        drw.arc((55, 75, 185, 205), 210, 255, col, 10)
        drw.regular_polygon((65.2, 115.5, 10), 3, 30, col)

        col = self.bitCH(kbd, 5)
        drw.arc((55, 75, 185, 205), 285, 330, col, 10)
        drw.regular_polygon((174.8, 115.5, 10), 3, 90, col)

        col = self.bitCH(kbd, 6)
        drw.regular_polygon((160, 175, 10), 3, 0, col)
        drw.polygon((160, 165, 170, 200, 150, 200), col)

        col = self.bitCH(kbd, 7)
        drw.regular_polygon((80, 190, 10), 3, 180, col)
        drw.polygon((70, 165, 90, 165, 80, 200), col)

    def drawCP(self, tpl, sbtpl):
        image = Image.new("RGB", (240, 240), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        self.drawMN(draw, tpl[0], tpl[2])
        self.drawSB(draw, sbtpl)
        self.drawSP(draw, tpl[1])

        return image
