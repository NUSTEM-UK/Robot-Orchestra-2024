from operator import is_
import time
import busio
from board import SCL, SDA
from adafruit_trellis import Trellis
from trellisset import TrellisSet
from repeated_timer import RepeatedTimer
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"MQTT connected with result code {reason_code}")
    # I don't think we need to subscribe to anything, at this point.
    # Certainly not in the orchestra (trellis) controller.

def on_message(client, userdata, message):
    pass

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("localhost", 1883, 60)
mqttc.loop_start() # non-blocking loop

class Orchestra(object):

    def __init__(self):
        self._bpm = 120
        self._current_beat = 0
        self._number_of_beats = 16
        self._running = False

        # Initialize the Untztrument
        i2c = busio.I2C(SCL, SDA)

        matrix0 = Trellis(i2c, [0x70])
        matrix1 = Trellis(i2c, [0x71])
        matrix2 = Trellis(i2c, [0x72])
        matrix3 = Trellis(i2c, [0x73])
        matrix4 = Trellis(i2c, [0x74])
        matrix5 = Trellis(i2c, [0x75])
        matrix6 = Trellis(i2c, [0x76])
        matrix7 = Trellis(i2c, [0x77])

        self.untztrument = TrellisSet(matrix0, matrix1, matrix2, matrix3, matrix4, matrix5, matrix6, matrix7)

        # Ensure all lights are off
        self.clear()
        # Now flush the lights
        self.untztrument.flush_led_state()


    def update(self):
        """Update the orchestra state."""
        # Get the beat state
        playset = self.untztrument.get_column_state_as_string(self._current_beat)
        print(f"BEAT: {self._current_beat:02} PLAYSET: {playset}")

        # Flash the column
        self.flash_column(self._current_beat, 0.05)

        # Network code goes here, I think?
        mqttc.publish("orchestra/playset", playset)

        # Update the current beat
        self._current_beat = (self._current_beat + 1) % self._number_of_beats

    def bpm(self, new_bpm):
        """Set the new beats per minute."""
        self._bpm = new_bpm

    def start(self):
        """Start the orchestra."""
        self._timer = RepeatedTimer((60/self._bpm), self.update)
        self._running = True

    def stop(self):
        """Stop the orchestra."""
        self._timer.stop()
        self._running = False

    def toggle(self):
        """Toggle the orchestra state."""
        if self._running:
            self.stop()
        else:
            self.start()

    def is_running(self):
        """Return the running state of the orchestra."""
        return self._running

    def reset(self):
        """Reset the orchestra."""
        self._current_beat = 0

    def current_beat(self):
        """Return the current beat."""
        return self._current_beat

    def handle_buttons(self, _display:bool = False):
        """Handle button presses and releases, updating Untztrument state."""
        just_pressed, released = self.untztrument.read_buttons()
        for b in just_pressed:
            self.untztrument.toggle_led_state(b)
            self.untztrument.update_led(b)

        # Display button states if any pressed:
        if _display and (just_pressed or released):
            print(f"pressed: {sorted(just_pressed)}, released: {sorted(released)}")

    def handle_buttons_target(self):
        just_pressed, released = self.untztrument.read_buttons()
        for b in just_pressed:
            self.untztrument.led_column_for_button(b, True)
            self.untztrument.led_row_for_button(b, True)
            self.untztrument.toggle_led_state(b)

        for b in released:
            self.untztrument.led_column_for_button(b, False)
            self.untztrument.led_row_for_button(b, False)

    def flash_column(self, column, duration = 0.05):
        """Flash the given column, returning to previous state."""
        self.untztrument.led_column(column, True)
        time.sleep(duration)
        self.untztrument.flush_column(column)

    def clear(self):
        """Clear the untztrument, ensuring nothing's set."""
        for b in range(128):
            self.untztrument.set_led_state(b, False)
