from .base_scope import BaseScope

class SiglentScope(BaseScope):


#Channel commands

    def set_channel_output(self, channel: int, output: str):
        self.inst.write(f":CHAN{channel}:SWITch {output}")

    def set_channel_vertical_scale(self, channel: int, volts_per_div: float):
        self.inst.write(f":CHANnel{channel}:SCALe {volts_per_div}")
    
    def set_channel_units(self, channel: int, units: str):
        self.inst.write(f":CHANnel{channel}:UNIT {units}")
    
    def set_channel_attentuation(self, channel: int, attentuation: int):
        raise NotImplementedError
    
    def set_channel_coupling(self, channel: int, coupling: str):
        raise NotImplementedError
    
    def set_channel_bwlimit(self, channel: int, limit: str):
        raise NotImplementedError
    
    def set_channel_label(self, channel: int, label: str):
        raise NotImplementedError
    
    def set_channel_offset(self, channel:int ,offset: float):
        raise NotImplementedError

#Timebase commands

    def set_timebase(self, seconds_per_div: float):
        self.inst.write(f":TIMebase:SCALe {seconds_per_div}")

#Trigger commands

    def set_trigger_mode(self, mode: str):
        self.inst.write(f":TRIGger:MODE {mode}")

    def set_trigger_source(self, channel: int):
        self.inst.write(f":TRIGger:EDGE:SOURce CHANnel{channel}")

    def set_trigger_level(self, level: float):
        self.inst.write(f":TRIGger:LEVel {level}")
        