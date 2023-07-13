#!/usr/bin/env python3          

import gpiozero

class Door(gpiozero.Button):

    def __init__(self, bcmPin):
        super().__init__(bcmPin)
    
    def setup(self, cb_opened, cb_closed):

        self.when_pressed = cb_closed
        self.when_released = cb_opened

        if self.is_closed():
            cb_closed()
        else:
            cb_opened()

    def is_closed(self) -> bool:
        return self.is_pressed
