from .base_scope import BaseScope

class RigolScope(BaseScope):
    def set_channel_on(self, channel: int):
        self.inst.write(f":CHAN{channel}:DISP ON")

    def set_channel_off(self, channel: int):
        self.inst.write(f":CHAN{channel}:DISP OFF")

    def set_timebase(self, seconds_per_div: float):
        self.inst.write(f":TIM:SCAL {seconds_per_div}")
