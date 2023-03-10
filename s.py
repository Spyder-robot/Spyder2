import time
import ST7789
from PIL import Image, ImageDraw, ImageFont
from S2draw import ST

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

dsp = ST("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
mnit = 6
navi = 17
img = dsp.drawCP(mnit, navi)

disp.display(img)
