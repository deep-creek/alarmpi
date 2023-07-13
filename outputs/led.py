#!/usr/bin/python3

import gpiozero

class Led(gpiozero.LED):
    _name = None

    def __init__(self, bcm_pin : int, name : str):
        super().__init__(bcm_pin)
        self._name = name
        self.off()

    def is_on(self) -> bool:
        return self.is_lit

    def name(self):
        return self._name
