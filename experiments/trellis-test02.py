import time
import busio
from board import SCL, SDA
from adafruit_trellis import Trellis

i2c = busio.I2C(SCL, SDA)
trellis = Trellis(i2c)

pressed_buttons = set()
while True:
    time.sleep(.1)
    just_pressed, released = trellis.read_buttons()
    for b in just_pressed:
        print('pressed:', b)
        trellis.led[b] = True
    pressed_buttons.update(just_pressed)
    for b in released:
        print('released:', b)
        trellis.led[b] = False
    pressed_buttons.difference_update(released)
    for b in pressed_buttons:
        print('still pressed:', b)
        trellis.led[b] = True

