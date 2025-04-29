class BaseScope:
    def __init__(self, instrument):
        self.inst = instrument

#Channel commands
    #output [ON|OFF]
    def set_channel_output(self, channel: int, output: str): 
        raise NotImplementedError

    def set_channel_vertical_scale(self, channel: int, volts_per_div: float):
        raise NotImplementedError
    
    def set_channel_units(self, channel: int, units: str):
        raise NotImplementedError
    
    def set_channel_attenuation(self, channel: int, attenuation: int):
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
        raise NotImplementedError
    

#Trigger commands

    def set_trigger_mode(self, mode: str):
        raise NotImplementedError

    def set_trigger_source(self, channel: int):
        raise NotImplementedError

    def set_trigger_level(self, level: float):
        raise NotImplementedError
        

#Measurement commands
    def measure_bode_setup(self, channel1: int, channel2: int):
        raise NotImplementedError

    def measure(self):
        raise NotImplementedError
    
    def measure_rms(self, channel: int):
        raise NotImplementedError
    
    def measure_freq(self, channel: int):
        raise NotImplementedError
    
    def measure_phase(self, channel1: int, channel2: int):
        raise NotImplementedError
    

#Function generator commands
    def set_frequency(self, frequency: float):
        raise NotImplementedError
    def set_amplitude(self, amplitude: float):
        raise NotImplementedError
    def set_offset(self, offset: float):
        raise NotImplementedError
    def set_waveform(self, waveform: str):
        raise NotImplementedError
    def set_output(self, output: str):
        raise NotImplementedError