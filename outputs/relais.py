#!/usr/bin/python3

import gpiozero

class Relais(gpiozero.OutputDevice):
    _name = None

    def __init__(self, bcm_pin : int, name : str):
        super().__init__(bcm_pin, active_high=False)

        self._name = name

        self.off()
        
    def is_on(self):
        return self.value == 1

    def name(self):
        return self._name
