from Motor import Motor
from Direction import Direction

class PhonyMotor(Motor):
    def __init__(self):
        super().__init__()
        self.position = 0.0

    def update(self):
        self.position += self.speed

    def set_speed(self, speed: float):
        self.speed = speed
    
    def get_direction(self) -> Direction:
        if self.speed > 0:
            return Direction.CLOCKWISE
        if self.speed < 0:
            return Direction.COUNTER_CLOCKWISE
        return Direction.NONE
