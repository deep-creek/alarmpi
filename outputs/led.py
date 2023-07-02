#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

class Led:
    bcm_pin = None
    name = None

    def __init__(self, bcm_pin : int, name : str):
        self.bcm_pin = bcm_pin
        self.name = name

    def setup(self):
        assert GPIO.getmode() == GPIO.BCM, "GPIO mode should be GPIO.BCM"

        GPIO.setup(self.bcm_pin, GPIO.OUT)

        self.off()

    def on(self):
        GPIO.output(self.bcm_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.bcm_pin, GPIO.LOW)

    def isOn(self):
        return GPIO.input(self.bcm_pin) == GPIO.HIGH

    def toggle(self):
        if self.isOn():
            self.off()
        else:
            self.on()

    def name(self):
        return self._name
