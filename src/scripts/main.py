import keyboard
from pynput.keyboard import Key, Listener
from threading import Thread, Lock
from Direction import Direction
from Motor import Motor
from PhonyMotor import PhonyMotor
from Signal import Signal
from PhonySignal import PhonySignal
from Ascent import Ascent

done = False  # for threads
ascent_direction = Direction.NONE
direction_mutex = Lock()
paused_mutex = Lock()
toggle_mutex = Lock()
motors_mutex = Lock()

def update_motors(motors):  # only used for debug
    while not done:
        with motors_mutex:
            for motor in motors:
                motor.update()

def update_direction():
    with direction_mutex:
        global ascent_direction
        if manual_controls:
            ascent_direction = gradient_ascent.determine_direction()


DEBUG = True

manual_controls = True
paused = False
SPIN_SPEED = 1  # TODO: tune speeds
PITCH_SPEED = 1

pitch_motor = Motor()
spin_motor = Motor()
antenna = Signal()

if DEBUG:
    pitch_motor = PhonyMotor()
    spin_motor = PhonyMotor()
    motor_thread = Thread(target=update_motors, args=((spin_motor, pitch_motor),))
    motor_thread.start()
    antenna = PhonySignal(spin_motor)
    SPIN_SPEED = .0001
    PITCH_SPEED = .0001

gradient_ascent = Ascent(antenna=antenna, speed=SPIN_SPEED, motor=spin_motor)

"""
@brief toggles manual controls
"""
def toggle_controls():
    global manual_controls
    with toggle_mutex:
        manual_controls = not manual_controls

"""
@brief stops all motor movement
"""
def toggle_pause():
    global paused
    with paused_mutex:
        paused = not paused

def on_press(key: Key):
    if key == Key.alt_r:
        toggle_pause()
    elif key == Key.ctrl_r:
        toggle_controls()


listener = Listener(on_press=on_press)
listener.start()

try:
    while True:
        # switch between manual controls here

        print(f"Strength: { int(antenna.get_signal_strength()) }")
        with toggle_mutex:
            if manual_controls:
                with paused_mutex:
                    if paused:
                        spin_motor.set_speed(Direction.NONE)
                        pitch_motor.set_speed(Direction.NONE)
                        continue
                left_key = keyboard.is_pressed("left")
                right_key = keyboard.is_pressed("right")
                up_key = keyboard.is_pressed("up")
                down_key = keyboard.is_pressed("down")
                if left_key ^ right_key:
                    if left_key:
                        spin_motor.set_speed(Direction.COUNTER_CLOCKWISE.value * SPIN_SPEED)
                    else:
                        spin_motor.set_speed(Direction.CLOCKWISE.value * SPIN_SPEED)
                else:
                    spin_motor.set_speed(Direction.NONE.value)
                if up_key ^ down_key:
                    if up_key:
                        pitch_motor.set_speed(Direction.CLOCKWISE.value * PITCH_SPEED)
                    else:
                        pitch_motor.set_speed(Direction.CLOCKWISE.value * PITCH_SPEED)
                else:
                    pitch_motor.set_speed(Direction.NONE.value)
            else:  # move based on gradient
                with paused_mutex and motors_mutex:
                    if paused: spin_motor.set_speed(Direction.NONE.value)
                    else:
                        with direction_mutex:
                            spin_motor.set_speed(ascent_direction.value * SPIN_SPEED)
                            print(f"We should point: { ascent_direction }")
except KeyboardInterrupt as e:
    print("Quitting.")
    done = True
    motor_thread.join()
