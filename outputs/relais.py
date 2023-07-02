#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

class Relais:
    _bcm_pin = None
    _name = None

    def __init__(self, bcm_pin : int, name : str):
        self._bcm_pin = bcm_pin
        self._name = name

    def setup(self):
        assert GPIO.getmode() == GPIO.BCM, "GPIO mode should be GPIO.BCM"

        GPIO.setup(self._bcm_pin, GPIO.OUT)

        self.off()

    def on(self):
        GPIO.output(self._bcm_pin, GPIO.LOW)

    def off(self):
        GPIO.output(self._bcm_pin, GPIO.HIGH)

    def is_on(self):
        return GPIO.input(self._bcm_pin) == GPIO.LOW

    def toggle(self):
        if self.is_on():
            self.off()
        else:
            self.on()

    def name(self):
        return self._name
