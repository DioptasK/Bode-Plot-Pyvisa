class BaseFunctionGenerator:
    def __init__(self, instrument):
        self.inst = instrument

    def set_output(self, channel: int, output: str):
        raise NotImplementedError
    
    def set_waveform(self, channel: int, waveform: str):
        raise NotImplementedError
    
    def set_frequency(self, channel: int, frequency: float):
        raise NotImplementedError
    
    def set_amplitude(self, channel: int, pkpk: float):
        raise NotImplementedError
    
    def apply_settings(self, channel: int, frequency: float, amplitude: float, waveform: str):
        raise NotImplementedError
        