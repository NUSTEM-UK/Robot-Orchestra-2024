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

def handle_buttons():
    """Handle button presses and releases, updating Untztrument state."""
    just_pressed, released = untztrument.read_buttons()
    for b in just_pressed:
        untztrument.toggle_led_state(b)
        untztrument.update_led(b)

    # Display button states if any pressed:
    if (just_pressed or released):
        print(f"pressed: {sorted(just_pressed)}, released: {sorted(released)}")

def handle_buttons_target():
    just_pressed, released = untztrument.read_buttons()
    for b in just_pressed:
        current_state = untztrument.get_led_state(b)
        untztrument.led_column_for_button(b, True)
        untztrument.led_row_for_button(b, True)
        untztrument.toggle_led_state(b)

    for b in released:
        untztrument.led_column_for_button(b, False)
        untztrument.led_row_for_button(b, False)


def flash_column(column, duration = 0.05):
    """Flash the given column, returning to previous state."""
    untztrument.led_column(column, True)
    time.sleep(duration)
    untztrument.flush_column(column)

while True:
    time.sleep(0.1)
    handle_buttons()
    # handle_buttons_target()
    for i in range(16):
        print (i)
        # untztrument.led_column(i, True)
        flash_column(i, 0.1)
        time.sleep(0.01)


