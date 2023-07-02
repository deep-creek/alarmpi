#!/usr/bin/env python3          
                                
import signal                   
import sys
import RPi.GPIO as GPIO

class Door:
    _pin : int = None
    _closed : bool = None 
    _callback_opened = None
    _callback_closed = None

    def __init__(self, bcmPin):
        self._pin = bcmPin

    def read_state(self):
        oldState = self._closed
        self._closed = GPIO.input(self._pin) == 0
        
        if oldState != self._closed:
            return True
        return False

    def button_callback(self, channel):
        if self.read_state() == False:
            return

        if self._closed:
            self._callback_closed() if self._callback_closed != None else None
        else:
            self._callback_opened() if self._callback_opened != None else None

    
    def setup(self, cb_opened, cb_closed):
        self._callback_opened = cb_opened
        self._callback_closed = cb_closed

        assert GPIO.getmode() == GPIO.BCM, "GPIO mode should be GPIO.BCM"

        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.button_callback(self._pin)

        def callback(channel):
            self.button_callback(channel)

        GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=callback, bouncetime=50)

    def is_closed(self):
        return self._closed
