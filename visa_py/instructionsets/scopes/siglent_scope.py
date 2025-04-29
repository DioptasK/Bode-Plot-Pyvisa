from .base_scope import BaseScope

class SiglentScope(BaseScope):


#Channel commands

    def set_channel_output(self, channel: int, output: str):
        self.inst.write(f":CHAN{channel}:SWITch {output}")

    def set_channel_vertical_scale(self, channel: int, volts_per_div: float):
        self.inst.write(f":CHANnel{channel}:SCALe {volts_per_div}")
    
    def set_channel_units(self, channel: int, units: str):
        self.inst.write(f":CHANnel{channel}:UNIT {units}")
    
    def set_channel_attenutaion(self, channel: int, attenuation: int):
        self.inst.write(f":CHANnel{channel}:PROBe VALue,{attenuation}")
    
    def set_channel_coupling(self, channel: int, coupling: str):
        self.inst.write(f":CHANnel{channel}:COUPling {coupling}")
    
    def set_channel_bwlimit(self, channel: int, limit: str):
        if limit == "ON":
            self.inst.write(f":CHANnel{channel}:BWLimit 20M") #FULL, 20M oder 200M
        elif limit == "OFF":
            self.inst.write(f":CHANnel{channel}:BWLimit FULL")
        else:
            raise ValueError("Invalid bandwidth limit. Use 'ON' or 'OFF'.")
    
    def set_channel_label(self, channel: int, label: str):
        self.inst.write(f":CHANnel{channel}:LABel ON")
        self.inst.write(f":CHANnel{channel}:LABel:TEXT {label}")
    
    def set_channel_offset(self, channel:int ,offset: float):
        self.inst.write(f":CHANnel{channel}:OFFSet {offset}")

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

#Function generator commands    

    def set_frequency(self, frequency: float):
        raise RuntimeError("The device does not contain a function generator")
    
    def set_amplitude(self, amplitude: float):
        raise RuntimeError("The device does not contain a function generator")
    
    def set_offset(self, offset: float):
        raise RuntimeError("The device does not contain a function generator")
    
    def set_waveform(self, waveform: str):
        raise RuntimeError("The device does not contain a function generator")
    
    def set_output(self, output: str):
        raise RuntimeError("The device does not contain a function generator")

#Measurement commands

    def measure_bode_setup(self, channel1: int, channel2: int):
        self.inst.write(f":MEASure ON")
        self.inst.write(f":MEASure:ADVanced:CLEar")
        self.inst.write(f":MEASure:ADVanced:LINenumber 4")
        self.inst.write(f":MEASure:ADVanced:P1 ON")
        self.inst.write(f":MEASure:ADVanced:P2 ON")
        self.inst.write(f":MEASure:ADVanced:P3 ON")
        self.inst.write(f":MEASure:ADVanced:P4 ON")
        self.inst.write(f".MEASure:ADVanced:P1:SOURce1 C{channel1}")
        self.inst.write(f".MEASure:ADVanced:P2:SOURce1 C{channel2}")
        self.inst.write(f".MEASure:ADVanced:P3:SOURce1 C{channel1}")
        self.inst.write(f".MEASure:ADVanced:P4:SOURce1 C{channel1}")
        self.inst.write(f".MEASure:ADVanced:P4:SOURce2 C{channel2}")
        self.inst.write(f":MEASure:ADVanced:P1:TYPE RMS")
        self.inst.write(f":MEASure:ADVanced:P2:TYPE RMS")
        self.inst.write(f":MEASure:ADVanced:P3:TYPE FREQ")
        self.inst.write(f":MEASure:ADVanced:P4:TYPE PHA")
        self.inst.write(f":MEASure:MODE ADVanced")
        self.inst.write(f":MEASure:ADVanced:STATistics ON")
        self.inst.write(f":MEASure:ADVanced:STATistics: AIMLimit 30")

    def measure(self):
        rms1 = float(self.inst.query(f":MEASure:ADVanced:P1:STATistics? MEAN"))
        rms2 = float(self.inst.query(f":MEASure:ADVanced:P2:STATistics? MEAN"))
        freq = float(self.inst.query(f":MEASure:ADVanced:P3:STATistics? MEAN"))
        phase = float(self.inst.query(f":MEASure:ADVanced:P4:STATistics? MEAN"))
        return rms1, rms2, freq, phase
    

    def measure_rms(self, channel: int):
        if channel == 1:
            return float(self.inst.query(f":MEASure:ADVanced:P1:STATistics? MEAN"))
        elif channel == 2: 
            return float(self.inst.query(f":MEASure:ADVanced:P2:STATistics? MEAN"))
        else: raise RuntimeError("Only Channel 1 and 2 can be used for measurement")
    
    def measure_freq(self, channel: int):
        float(self.inst.query(f":MEASure:ADVanced:P3:STATistics? MEAN"))
    
    def measure_phase(self, channel1: int, channel2: int):
        phase = float(self.inst.query(f":MEASure:ADVanced:P4:STATistics? MEAN"))