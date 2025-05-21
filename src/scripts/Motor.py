from Direction import Direction

"""
@brief class that represents a motor
"""
class Motor:
    def __init__(self):
        self.speed = 0.0

    def set_speed(self, speed: float):
        self.speed = speed
        # send speed via UART here

    def get_speed(self) -> float:
        return self.speed
    
    def get_direction(self) -> Direction:
        if self.speed > 0:
            return Direction.CLOCKWISE
        if self.speed < 0:
            return Direction.COUNTER_CLOCKWISE
        return Direction.NONE
