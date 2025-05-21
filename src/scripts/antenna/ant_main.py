
from enum import Enum
import keyboard
import os
import threading
import math

class Direction(Enum):
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = -1
    NONE = 0

spin_direction = Direction.CLOCKWISE
manual_controls = False
SPIN_SPEED = 1
DEBUG = True

if DEBUG:
    _DEBUG_direction = 0
    SPIN_SPEED = .0001

def set_pitch_speed(speed):
    print(f"Sending pitch speed {speed}")
    # send speed via UART

def set_spin_speed(speed):
    global spin_direction
    if speed == 0: spin_direction = Direction.NONE
    elif speed > 0: spin_direction = Direction.CLOCKWISE
    else: spin_direction = Direction.COUNTER_CLOCKWISE
    print(f"Sending spin speed {speed}")
    # send speed via UART

def get_signal_strength():
    if DEBUG:
        return abs(math.sin(_DEBUG_direction)) * 1000

    strength = float(os.popen('iw wlan0 station dump | grep -E "signal:\s*" | tr -d -c "\- 0-9"').read())
    return (10 ** (strength / 10.0)) * 10 ** 7
    

"""
@brief determines the direction where the signal strength gradient is positive
@return the direction we should spin
"""
def determine_direction():  # use threading
    # figure out gradient
    s_0 = get_signal_strength()

    # force clockwise movement to determine gradeint at current position
    if (spin_direction == Direction.NONE):
        set_spin_speed(Direction.CLOCKWISE * SPIN_SPEED)
    time.sleep(.1)
    s_1 = get_signal_strength()
    if (spin_direction == Direction.NONE):
        set_spin_speed(0)

    if spin_direction == Direction.CLOCKWISE: gradient = s_1 - s_0
    else: gradient = s_0 - s_1

    # positive gradient means signal strength is increasing in the clockwise direction
    # might want to remove this to make sure it stays accurate
    if abs(gradient) < 5:
        return Direction.NONE

    if gradient > 0:
        return Direction.CLOCKWISE
    
    return Direction.COUNTER_CLOCKWISE

while True:
    if DEBUG:
        _DEBUG_direction += spin_direction.value * SPIN_SPEED
    if manual_controls:
        print(f"Strength: { int(get_signal_strength()) }")
        left_key = keyboard.is_pressed("left")
        right_key = keyboard.is_pressed("right")
        up_key = keyboard.is_pressed("up")
        down_key = keyboard.is_pressed("down")
        if left_key ^ right_key:
            if left_key:  # counter
                set_spin_speed(Direction.COUNTER_CLOCKWISE.value * SPIN_SPEED)
            else:  # regular
                set_spin_speed(Direction.CLOCKWISE.value * SPIN_SPEED)
        else:
            set_spin_speed(0)
        if up_key ^ down_key:
            if up_key:
                print("pitch up")
            else:
                print("pitch down")
        else:
            set_pitch_speed(0)
    else:  # gradient ascent
        print(f"Direction: { determine_direction() }")
        print(f"Strength: { int(get_signal_strength()) }")

