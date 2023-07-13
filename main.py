#!/usr/bin/python3

import time
import threading
import enum
import logging
import sys

# own modules
import inputs.keypad
import outputs.relais
import inputs.door
import outputs.led
import web.webserver as webserver
import settings


#######################################################################################################################
# ALARM SETTINGS
#######################################################################################################################
cfg = settings.get_settings()
TEST_MODE = cfg.test_mode
KEYPAD_PASSWORD = cfg.password
KEYPAD_RESET = '*'
ALARM_DURATION_SECONDS = cfg.alarm_duration 

#######################################################################################################################
# PIN DEFINITIONS (BCM numbering)
#######################################################################################################################
PIN_KEYPAD_ROW  = [26,19,13,6] 
PIN_KEYPAD_COL  = [5,11,9,10] 
PIN_REL_1       = 12
PIN_REL_2       = 16
PIN_REL_3       = 20
PIN_REL_4       = 21
PIN_DOOR        = 18

PIN_LED_RED1    = 17
PIN_LED_RED2    = 27
PIN_LED_RED3    = 22

#######################################################################################################################
# INPUTS
#######################################################################################################################
# door sensor
IN_DOOR = inputs.door.Door(PIN_DOOR)

# keypad
IN_KEYPAD = inputs.keypad.Keypad(PIN_KEYPAD_ROW, PIN_KEYPAD_COL)

#######################################################################################################################
# OUTPUTS
#######################################################################################################################
# relais channels
OUT_REL_BLINDS      = outputs.relais.Relais(PIN_REL_1, "blinds")
OUT_REL_ALARM       = outputs.relais.Relais(PIN_REL_2, "alarm")
OUT_REL_NIGHTLIGHT  = outputs.relais.Relais(PIN_REL_3, "nightlight")
OUT_REL_UNUSED      = outputs.relais.Relais(PIN_REL_4, "unused")
RELAIS              = [OUT_REL_BLINDS, OUT_REL_ALARM, OUT_REL_NIGHTLIGHT, OUT_REL_UNUSED]

# leds
OUT_LED_RED1        = outputs.led.Led(PIN_LED_RED1, "redLight1")
OUT_LED_RED2        = outputs.led.Led(PIN_LED_RED2, "redLight2")
OUT_LED_RED3        = outputs.led.Led(PIN_LED_RED3, "redLight3")
LEDS                = [OUT_LED_RED1, OUT_LED_RED2, OUT_LED_RED3]

OUTPUTS = RELAIS
OUTPUTS.extend(LEDS)

# alarm state
class AlarmStates(enum.Enum):
    ARMED           = enum.auto()
    ALARM           = enum.auto()
    ALARM_TIMED_OUT = enum.auto()
    DISARMED        = enum.auto()
ALARM_STATE = AlarmStates.DISARMED

# Events
class AlarmEvents(enum.Enum):
    DOOR_OPENED     = enum.auto()
    DOOR_CLOSED     = enum.auto()
    CODE_CORRECT    = enum.auto()
    CODE_RESET      = enum.auto()
    TIMEOUT         = enum.auto()
    
def handle_event(evt):
    global ALARM_STATE

    logging.debug("Handle event: " + evt.__str__())

    if AlarmEvents.CODE_CORRECT == evt:
        set_alarm_state(AlarmStates.DISARMED)

    elif AlarmEvents.DOOR_OPENED == evt and ALARM_STATE == AlarmStates.ARMED:
        set_alarm_state(AlarmStates.ALARM)
                
    elif AlarmEvents.DOOR_CLOSED == evt \
            and (ALARM_STATE == AlarmStates.DISARMED or ALARM_STATE == AlarmStates.ALARM_TIMED_OUT):
        set_alarm_state(AlarmStates.ARMED)
        
    elif AlarmEvents.CODE_RESET == evt:
        if ALARM_STATE == AlarmStates.DISARMED:
            set_alarm_state(AlarmStates.ARMED)
        else:
            None # just ignore it, as CODE_RESET resets the input
        
    elif AlarmEvents.TIMEOUT == evt and ALARM_STATE == AlarmStates.ALARM:
        set_alarm_state(AlarmStates.ALARM_TIMED_OUT)

    else:
        logging.warning("************ Unable to handle " + evt.__str__() +
                " while in AlarmState: " + ALARM_STATE.__str__())
            
def set_alarm_state(new_state):
    global ALARM_STATE
    if ALARM_STATE != new_state:
        logging.info("************ AlarmState: " + ALARM_STATE.__str__() + " - > " + new_state.__str__())
        ALARM_STATE = new_state

    if AlarmStates.ARMED == new_state:
        OUT_LED_RED1.on()
        if not TEST_MODE:
            time.sleep(0.2)
            OUT_LED_RED2.on()
        time.sleep(0.2)
        OUT_LED_RED3.on()
    
    elif AlarmStates.ALARM == new_state:
        OUT_REL_BLINDS.on()
        if not TEST_MODE:
            OUT_REL_ALARM.on()

        def callback():
            handle_event(AlarmEvents.TIMEOUT)
        start_time = threading.Timer(ALARM_DURATION_SECONDS, callback)
        start_time.start()
    
    elif AlarmStates.DISARMED == new_state:
        reset_alarm()
        OUT_LED_RED1.off()
        time.sleep(0.2)
        OUT_LED_RED2.off()
        time.sleep(0.2)
        OUT_LED_RED3.off()
    
    elif AlarmStates.ALARM_TIMED_OUT == new_state:
        reset_alarm()
        if IN_DOOR.is_closed():
            handle_event(AlarmEvents.DOOR_CLOSED)

def reset_alarm():
    OUT_REL_BLINDS.off()
    OUT_REL_ALARM.off()

def check_password(input):
    if KEYPAD_PASSWORD == input:
        handle_event(AlarmEvents.CODE_CORRECT)
        IN_KEYPAD.clear_input()
    elif KEYPAD_RESET == input[-1:]:
        handle_event(AlarmEvents.CODE_RESET)
        IN_KEYPAD.clear_input()
    elif len(input) > 0 and not KEYPAD_PASSWORD.startswith(input):
        logging.warning('Wrong code entered "%s"' % (input))

def setup():

    IN_KEYPAD.setup(check_password)

    def door_opened():
        handle_event(AlarmEvents.DOOR_OPENED)
    def door_closed():
        handle_event(AlarmEvents.DOOR_CLOSED)
    IN_DOOR.setup(door_opened, door_closed)
    
    
def cleanup():
    logging.debug("Cleaning up")
    reset_alarm()
    [out.off() for out in OUTPUTS]


if __name__ == "__main__":
    logging.basicConfig(
                level=logging.DEBUG,
                format="[%(asctime)s.%(msecs)03d] %(levelname)-7s %(message)s", # [%(name)s.%(funcName)s:%(lineno)d]",
                datefmt="%d.%m.%Y %H:%M:%S",
                stream=sys.stdout)

    logging.info('Keypad password: "%s"' % (KEYPAD_PASSWORD))
    logging.info('Test Mode is ' + ('enabled' if TEST_MODE else 'disabled'))
    logging.info('Alarm duration: %d seconds' % (ALARM_DURATION_SECONDS))

    try:
        setup()

        httpEndpoint = webserver.Server(OUTPUTS)

        while True:
            time.sleep(1)

    finally:
        cleanup()
