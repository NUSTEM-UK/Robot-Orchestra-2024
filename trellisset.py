import numpy as np

class TrellisSet(object):

    def __init__(self, *matrices):
        self._matrices = matrices
        self._button_grid = np.array(
            [[  0,   1,   2,   3,  16,  17,  18,  19,  32,  33,  34,  35,  48,  49,  50,  51],
             [  4,   5,   6,   7,  20,  21,  22,  23,  36,  37,  38,  39,  52,  53,  54,  55],
             [  8,   9,  10,  11,  24,  25,  26,  27,  40,  41,  42,  43,  56,  57,  58,  59],
             [ 12,  13,  14,  15,  28,  29,  30,  31,  44,  45,  46,  47,  60,  61,  62,  63],
             [ 64,  65,  66,  67,  80,  81,  82,  83,  96,  97,  98,  99, 112, 113, 114, 115],
             [ 68,  69,  70,  71,  84,  85,  86,  87, 100, 101, 102, 103, 116, 117, 118, 119],
             [ 72,  73,  74,  75,  88,  89,  90,  91, 104, 105, 106, 107, 120, 121, 122, 123],
             [ 76,  77,  78,  79,  92,  93,  94,  95, 108, 109, 110, 111, 124, 125, 126, 127]]
        )
        # State array for each led/button
        self._led_state = np.zeros_like(self._button_grid, dtype=bool)

    def set_brightness(self, brightness):
        for matrix in self._matrices:
            matrix.set_brightness(brightness)

    def read_buttons(self):
        """Return (16*matrix)+button for each button that was just pressed and released."""
        just_pressed = set()
        released = set()
        for index, matrix in enumerate(self._matrices):
            jp, r = matrix.read_buttons()
            adjusted_jp = {button + (16 * index) for button in jp}
            adjusted_r = {button + (16 * index) for button in r}
            just_pressed.update(adjusted_jp)
            released.update(adjusted_r)
        return just_pressed, released

    def led_from_button(self, button, value:bool) -> None:
        # Find the matrix number from button number, mod 16
        matrix = button // 16
        # Find the button number within the matrix, mod 16
        button = button % 16
        # Set the LED value
        self._matrices[matrix].led[button] = value

    def _get_column_from_button(self, button):
        # Find the column index of the button in the buttonGrid array
        column = np.where(self._button_grid == button)[1][0]
        return column

    def _get_leds_from_column(self, column):
        """Given a column number, return a list of button numbers in that column."""
        leds_in_column = self._button_grid[:, column].tolist()
        return leds_in_column

    def _get_column_leds_from_button(self, button):
        """Given a button number, return a list of button numbers in the same column."""
        column = self._get_column_from_button(button)
        return self._get_leds_from_column(column)

    def led_column_for_button(self, button, value:bool) -> None:
        """Light the entire column of the button."""
        for button in self._get_column_leds_from_button(button):
            self.led_from_button(button, value)

    def led_column(self, column, value:bool) -> None:
        """Light the entire column, indexed by column."""
        for button in self._get_leds_from_column(column):
            self.led_from_button(button, value)

    def _get_row_from_button(self, button):
        # Find the row index of the button in the buttonGrid array
        row = np.where(self._button_grid == button)[0][0]
        return row

    def _get_leds_from_row(self, row):
        """Given a row number, return a list of button numbers in that row."""
        leds_in_row = self._button_grid[row, :].tolist()
        return leds_in_row

    def _get_row_leds_from_button(self, button):
        """Given a button number, return a list of button numbers in the same row."""
        row = self._get_row_from_button(button)
        return self._get_leds_from_row(row)

    def led_row_for_button(self, button, value:bool) -> None:
        """Light the entire row of the button."""
        for button in self._get_row_leds_from_button(button):
            self.led_from_button(button, value)

    def update_led_state(self, led, value:bool) -> None:
        """Update the state of the LED."""
        row, col = np.where(self._button_grid == led)
        self._led_state[row, col] = value

    def get_led_state(self, led) -> bool:
        """Return the state of the LED."""
        row, col = np.where(self._button_grid == led)
        # Return the state of the LED as a boolean
        return bool(self._led_state[row, col])

    def toggle_led_state(self, led) -> None:
        """Toggle the state of the LED."""
        row, col = np.where(self._button_grid == led)
        self._led_state[row, col] = not self._led_state[row, col]

    def update_led(self, button) -> None:
        """Update the LED state."""
        current_state = self.get_led_state(button)
        self.led_from_button(button, current_state)

    def auto_show(self, value:bool) -> None:
        """Control auto_show state so we can update all at once."""
        for matrix in self._matrices:
            matrix.led.auto_show = value

    def flush_row_for_button(self, button) -> None:
        """Flush button row state to the Trellis hardware."""
        row = self._get_row_from_button(button)
        self.auto_show(False)
        for button in self._get_leds_from_row(row):
            value = self.get_led_state(button)
            self.led_from_button(button, value)
        self.auto_show(True)

    def flush_column_for_button(self, button) -> None:
        """Flush button column state to the Trellis hardware."""
        column = self._get_column_from_button(button)
        self.auto_show(False)
        for button in self._get_leds_from_column(column):
            value = self.get_led_state(button)
            self.led_from_button(button, value)
        self.auto_show(True)

    def flush_column(self, column) -> None:
        """Flush button column state for given column."""
        self.auto_show(False)
        for button in self._get_leds_from_column(column):
            value = self.get_led_state(button)
            self.led_from_button(button, value)
        self.auto_show(True)

    def flush_led_state(self) -> None:
        """Flush the LED state to the Trellis hardware."""
        # Disable auto_show
        self.auto_show(False)
        # Update the LED state
        for row in range(self._led_state.shape[0]):
            for col in range(self._led_state.shape[1]):
                button = self._button_grid[row, col]
                value = self._led_state[row, col]
                self.led_from_button(button, value)
        # Enable auto_show
        self.auto_show(True)
