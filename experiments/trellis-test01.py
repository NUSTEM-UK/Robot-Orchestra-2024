import time
import busio
from board import SCL, SDA
from adafruit_trellis import Trellis

i2c = busio.I2C(SCL, SDA)
trellis = Trellis(i2c)

trellis.led.fill(True)
time.sleep(1)
trellis.led.fill(False)
