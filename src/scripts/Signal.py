import os

class Signal:
    def __init__(self):
        super().__init__()

    def get_signal_strength(self):
        strength = float(os.popen('iw wlan0 station dump | grep -E "signal:\s*" | tr -d -c "\- 0-9"').read())
        return (10 ** (strength / 10.0)) * 10 ** 7