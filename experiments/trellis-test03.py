import time
import busio
from board import SCL, SDA
from adafruit_trellis import Trellis

i2c = busio.I2C(SCL, SDA)

matrix0 = Trellis(i2c, [0x70])
matrix1 = Trellis(i2c, [0x71])
matrix2 = Trellis(i2c, [0x72])
matrix3 = Trellis(i2c, [0x73])
matrix4 = Trellis(i2c, [0x74])
matrix5 = Trellis(i2c, [0x75])
matrix6 = Trellis(i2c, [0x76])
matrix7 = Trellis(i2c, [0x77])

trellis_set = [matrix0, matrix1, matrix2, matrix3, matrix7, matrix6, matrix5, matrix4]


for _ in range(10):

    for trellis in trellis_set:
        trellis.led.fill(True)
        time.sleep(0.03)

    # time.sleep(1)

    for trellis in trellis_set:
        trellis.led.fill(False)
        time.sleep(0.03)


# matrix0.led.fill(True)
# time.sleep(1)
# matrix1.led.fill(True)
# time.sleep(1)
# matrix0.led.fill(False)
# time.sleep(1)
# matrix1.led.fill(False)

