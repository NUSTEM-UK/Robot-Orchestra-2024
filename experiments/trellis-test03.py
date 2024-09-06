import time
import busio
from board import SCL, SDA
from adafruit_trellis import Trellis

i2c = busio.I2C(SCL, SDA)

matrix0 = Trellis(i2c, [0x70])
matrix1 = Trellis(i2c, [0x71])

matrix0.led.fill(True)
time.sleep(1)
matrix1.led.fill(True)
time.sleep(1)
matrix0.led.fill(False)
time.sleep(1)
matrix1.led.fill(False)

