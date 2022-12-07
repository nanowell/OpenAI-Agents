Optimize this code:
# Check if used with Python 3
import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


import os
import time
import datetime
import argparse
import logging
import logging.handlers
import signal


# Import the library
from pyA20.gpio import gpio


# Define the constants
# GPIO pin used to switch the relay
RELAY_PIN = "PA7"
# GPIO pin used to read the status of the switch
SWITCH_PIN = "PA8"
# GPIO pin used to read the status of the motion sensor
MOTION_PIN = "PA9"
# GPIO pin used to read the status of the door sensor
DOOR_PIN = "PA10"


# Define the global variables
# The current state of the system
state = "unknown"
# The last state of the system
last_state = "unknown"
# The time when the system was armed
armed_time = None
# The time when the system was disarmed
disarmed_time = None


# Setup logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


# Define the functions
def setup_gpio():
    """Setup the GPIO pins"""
    log.debug("Setting up the GPIO pins")
    gpio.init()
    gpio.setcfg(RELAY_PIN, gpio.OUTPUT)
    gpio.setcfg(SWITCH_PIN, gpio.INPUT)
    gpio.setcfg(MOTION_PIN, gpio.INPUT)
    gpio.setcfg(DOOR_PIN, gpio.INPUT)
    gpio.pullup(SWITCH_PIN, gpio.PULLDOWN)
    gpio.pullup(MOTION_PIN, gpio.PULLDOWN)
    gpio.pullup(DOOR_PIN, gpio.PULLDOWN)


def cleanup_gpio():
    """Cleanup the GPIO pins"""
    log.debug("Cleaning up the GPIO pins")
    gpio.output(RELAY_PIN, 0)
    gpio.cleanup()


def read_switch():
    """Read the state of the switch"""
    return gpio.input(SWITCH_PIN)


def arm_system():
    """Arm the system"""
    global armed_time
    log.debug("Arming the system")
    gpio.output(RELAY_PIN, 1)
    armed_time = datetime.datetime.now()


def disarm_system():
    """Disarm the system"""
    global disarmed_time
    log.debug("Disarming the system")
    gpio.output(RELAY_PIN, 0)
    disarmed_time = datetime.datetime.now()


def read_motion():
    """Read the state of the motion sensor"""
    return gpio.input(MOTION_PIN)


def get_state():
    """Get the current state of the system"""
    if read_switch() == 1:
        return "armed"
    else:
        return "disarmed"


def main():
    """Main function"""
    global state
    global last_state
    global armed_time
    global disarmed_time

    # Setup the GPIO pins
    setup_gpio()

    # Setup the signal handler
    signal.signal(signal.SIGTERM, signal_handler)

    # Loop forever
    while True:
        # Get the current state of the system
        state = get_state()

        # Check if the state has changed
        if state != last_state:
            log.info("State changed from %s to %s", last_state, state)

            # Check if the system was armed
            if state == "armed":
                arm_system()
            # Check if the system was disarmed
            elif state == "disarmed":
                disarm_system()

            # Update the last state
            last_state = state

        # Check if the system is armed
        if state == "armed":
            # Check if the motion sensor is triggered
            if read_motion() == 1:
                log.info("Motion sensor triggered")
                # TODO: Send an email

        # Sleep for a while
        time.sleep(0.1)


def signal_handler(signum, frame):
    """Signal handler"""
    log.debug("Signal handler called with signal %d", signum)
    cleanup_gpio()
    sys.exit(0)


# Run the main function
if __name__ == "__main__":
    main()
