from .base_functiongenerator import BaseFunctionGenerator

class KeysightFunctionGenerator(BaseFunctionGenerator):

    def set_output(self, channel: int, output: str):
        raise NotImplementedError
    
    def set_waveform(self, channel: int, waveform: str):
        self.inst.write(f"FUNCtion {waveform}") #SINusoid, SQUare, RAMP, PULSe, NOISe, DC, USER
    
    def set_frequency(self, channel: int, frequency: float):
        self.inst.write(f"FREQuency {frequency}")
    
    def set_amplitude(self, channel: int, amplitude: float):
        self.inst.write(f"VOLTage:UNIT VPP")
        self.inst.write(f"VOLTage {amplitude}")

    def apply_settings(self, channel, frequency, amplitude, waveform):
        self.inst.write(f"APPLy:{waveform}, {frequency}, {amplitude}")#SINusoid
