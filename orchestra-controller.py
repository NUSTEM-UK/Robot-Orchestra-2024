import time
import busio
from board import SCL, SDA
from adafruit_trellis import Trellis
from trellisset import TrellisSet
from repeated_timer import RepeatedTimer

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

def handle_buttons(_display:bool = False):
    """Handle button presses and releases, updating Untztrument state."""
    just_pressed, released = untztrument.read_buttons()
    for b in just_pressed:
        untztrument.toggle_led_state(b)
        untztrument.update_led(b)

    # Display button states if any pressed:
    if _display and (just_pressed or released):
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


class Orchestra(object):
    def __init__(self):
        self._bpm = 120
        self._current_beat = 0
        self._number_of_beats = 16

    def update(self):
        """Update the orchestra state."""
        # Get the beat state
        playset = untztrument.get_column_state_as_string(self._current_beat)
        print(f"BEAT: {self._current_beat:02} PLAYSET: {playset}")

        # Flash the column
        flash_column(self._current_beat, 0.05)

        # Network code goes here, I think?

        # Update the current beat
        self._current_beat = (self._current_beat + 1) % self._number_of_beats

    def bpm(self, new_bpm):
        """Set the new beats per minute."""
        self._bpm = new_bpm

    def start(self):
        """Start the orchestra."""
        self._timer = RepeatedTimer((60/self._bpm), self.update)

    def stop(self):
        """Stop the orchestra."""
        self._timer.stop()

    def reset(self):
        """Reset the orchestra."""
        self._current_beat = 0

    def current_beat(self):
        """Return the current beat."""
        return self._current_beat


orchestra = Orchestra()
orchestra.start()


while True:
    time.sleep(0.1)
    handle_buttons()
    # handle_buttons_target()
    # for i in range(16):
    #     print (i)
    #     # untztrument.led_column(i, True)
    #     flash_column(i, 0.1)
    #     time.sleep(0.01)


