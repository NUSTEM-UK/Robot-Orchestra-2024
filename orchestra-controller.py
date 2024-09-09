import time
import busio
from board import SCL, SDA
from adafruit_trellis import Trellis
from trellisset import TrellisSet

i2c = busio.I2C(SCL, SDA)

matrix0 = Trellis(i2c, [0x70])
matrix1 = Trellis(i2c, [0x71])
matrix2 = Trellis(i2c, [0x72])
matrix3 = Trellis(i2c, [0x73])
matrix4 = Trellis(i2c, [0x74])
matrix5 = Trellis(i2c, [0x75])
matrix6 = Trellis(i2c, [0x76])
matrix7 = Trellis(i2c, [0x77])

untztrument = TrellisSet(matrix0, matrix1, matrix2, matrix3, matrix4, matrix5, matrix6, matrix7)

while True:
    time.sleep(0.1)

    just_pressed, released = untztrument.read_buttons()
    # for b in just_pressed:
    #     print("pressed:", b)
    #     untztrument.led(b, True)
    #     untztrument.led_column(b, True)
    #     untztrument.led_row(b, True)

    # for b in released:
    #     print("released:", b)
    #     untztrument.led(b, False)
    #     untztrument.led_column(b, False)
    #     untztrument.led_row(b, False)

    # for b in just_pressed:
    #     print("pressed:", b)
    #     untztrument.led(b, True)
    #     # untztrument.led_column(b, True)
    #     # untztrument.led_row(b, True)
    #     current_state = untztrument.get_led_state(b)
    #     untztrument.update_led_state(b, not current_state)

    # for b in released:
    #     print("released:", b)
    #     # untztrument.led_column(b, False)
    #     # untztrument.led_row(b, False)
    #     untztrument.flush_led_state()

    for b in just_pressed:
        print("pressed:", b)
        current_state = untztrument.get_led_state(b)
        untztrument.update_led_state(b, not current_state)
        untztrument.led(b, not current_state)

    for b in released:
        print("released:", b)


