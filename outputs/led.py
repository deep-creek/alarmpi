#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

class Led:
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
        GPIO.output(self._bcm_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self._bcm_pin, GPIO.LOW)

    def isOn(self):
        return GPIO.input(self._bcm_pin) == GPIO.HIGH

    def toggle(self):
        if self.isOn():
            self.off()
        else:
            self.on()

    def name(self):
        return self._name
