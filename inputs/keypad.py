from pad4pi import rpi_gpio

import RPi.GPIO as GPIO
from datetime import datetime

class Keypad:
    keypad = {}

    _row_pins = []
    _col_pins = []
    _pass_input_hook = None
    _last_chars = ''
    _last_char_input_time = datetime.now()
    _input_timeout_seconds = 5

    def __init__(self, row_pins, col_pins, input_timeout_seconds = 5):
        self._row_pins = row_pins
        self._col_pins = col_pins
        self._input_timeout_seconds = input_timeout_seconds


    def handle_key_press(self, key):
        now = datetime.now()
        diff = now - self._last_char_input_time
        if diff.total_seconds() > self._input_timeout_seconds:
            self._last_chars = ''
        self._last_char_input_time = now

        self._last_chars += str(key)
        self._pass_input_hook(self._last_chars)

    def clear_input(self):
        self._last_chars = ''

    def setup(self, pass_input_hook): 
        self._pass_input_hook = pass_input_hook

        KEYPAD = [
            [1,2,3,"A"],
            [4,5,6,"B"],
            [7,8,9,"C"],
            ["*",0,"#","D"]
        ]
       
        factory = rpi_gpio.KeypadFactory()

        keypad = factory.create_keypad(keypad=KEYPAD, row_pins=self._row_pins, col_pins=self._col_pins)

        def handler(key):
            self.handle_key_press(key)

        # handleKeyPress will be called each time a keypad button is pressed
        keypad.registerKeyPressHandler(handler)
