from Signal import Signal
from Motor import Motor
from Direction import Direction

import time

class Ascent:
    def __init__(self, antenna: Signal, speed: float, motor: Motor):
        assert(speed >= 0)  # speed should not be negative
        self.last_direction = Direction.NONE
        self.motor = motor
        self.antenna = antenna
        self.speed = speed
    
    """
    @brief determines the direction where the signal strength gradient is positive
    @param antenna the antenna used to calculate strength gradient
    @param motor the motor to use
    @param speed the speed to move if not in manual controls
    @param manual_controls whether or not there are manual controls, false by default
    @return the direction we should spin
    """
    def determine_direction(self, manual_controls=False) -> Direction:
        if manual_controls:
            if self.motor.get_speed() == Direction.NONE.value:
                return self.last_direction

        # figure out gradient start
        s_0 = self.antenna.get_signal_strength()

        # force movement to determine gradeint at current position if not manually controlling
        if not manual_controls:
            self.motor.set_speed(Direction.CLOCKWISE.value * self.speed)
        time.sleep(.1)
        s_1 = self.antenna.get_signal_strength()  # gradient end
        if not manual_controls:
            self.motor.set_speed(Direction.COUNTER_CLOCKWISE.value * self.speed)
            time.sleep(.1)
            self.motor.set_speed(Direction.NONE.value)

        if self.motor.get_direction() == Direction.CLOCKWISE or manual_controls: gradient = s_1 - s_0
        else: gradient = s_0 - s_1

        # positive gradient means signal strength is increasing in the clockwise direction
        # might want to remove this to make sure it stays accurate
        self.last_direction = Direction.COUNTER_CLOCKWISE
        if abs(gradient) < .01:
            self.last_direction = Direction.NONE
        elif gradient > 0:
            self.last_direction = Direction.CLOCKWISE
        
        return self.last_direction