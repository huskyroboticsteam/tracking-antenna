import math

from Signal import Signal
from PhonyMotor import PhonyMotor

class PhonySignal(Signal):
    def __init__(self, motor: PhonyMotor):
        super().__init__()
        self.motor = motor
        self.position = 0.0

    def get_signal_strength(self):
        return abs(math.sin(self.motor.position)) * 1000
