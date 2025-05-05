from .base_functiongenerator import BaseFunctionGenerator

class SiglentFunctionGenerator(BaseFunctionGenerator):

   #TODO: to check
    def set_output(self, channel: int, output: str):
        self.inst.write(f":OUTPut{channel}:STATe {output}")
    
    def set_waveform(self, channel: int, waveform: str):
        self.inst.write(f":FUNCtion{channel} {waveform}")
    
    def set_frequency(self, channel: int, frequency: float):
        return
    
    def set_amplitude(self, channel: int, amplitude: float):
        self.inst.write(f":VOLTage{channel} {amplitude}")
