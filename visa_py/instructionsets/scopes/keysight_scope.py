from .base_scope import BaseScope
import re


class KeysightScope(BaseScope):

#Channel commands

    def set_channel_output(self, channel: int, output: str):
        self.inst.write(f":CHANnel{channel}:DISPlay {output}")

    def set_channel_vertical_scale(self, channel: int, volts_per_div: float):
        volts_per_div = "{:.2E}".format(volts_per_div)
        self.inst.write(f":CHANnel{channel}:SCALe {volts_per_div} V")
    
    def set_channel_units(self, channel: int, units: str):
        if units == "V":
            units = "VOLT"
        elif units == "A":
            units = "AMPere"
        self.inst.write(f":CHANnel{channel}:UNITs {units}")
    
    def set_channel_attenuation(self, channel: int, attenuation: int):
        attenuation = "{:.2E}".format(attenuation)
        self.inst.write(f":CHANnel{channel}:PROBe {attenuation}")
    
    def set_channel_coupling(self, channel: int, coupling: str):
        self.inst.write(f":CHANnel{channel}:COUPling {coupling}")

    def set_channel_bwlimit(self, channel: int, limit: str):
        self.inst.write(f":CHANnel{channel}:BWLimit {limit}")
    
    def set_channel_label(self, channel: int, label: str):
        self.inst.write(f"CHANnel{channel}:LABel \"{label}\"")
    
    def set_channel_offset(self, channel:int ,offset: float):
        self.inst.write(f":CHANnel{channel}:OFFSet {offset} V")

#Timebase commands

    def set_timebase(self, seconds_per_div):
        seconds_per_div = "{:.2E}".format(seconds_per_div)
        self.inst.write(f":TIMebase:MODE MAIN")
        self.inst.write(f":TIMebase:SCALe {seconds_per_div}")
        #raise NotImplementedError

#Trigger commands

    def set_trigger_mode(self, mode: str):
        raise NotImplementedError

    def set_trigger_source(self, channel: int):
        raise NotImplementedError

    def set_trigger_level(self, level: float):
        raise NotImplementedError

#Function generator commands    
#Befehle auf seite 743 im agilent pdf
    def set_frequency(self, frequency: float):
        frequency = "{:.2E}".format(frequency)
        self.inst.write(f":WGEN:FREQuency {frequency}")
    
    def set_amplitude(self, pkpk: float):
        self.inst.write(f":WGEN:VOLTage {pkpk}")
    
    def set_offset(self, offset: float):
        self.inst.write(f":WGEN:VOLTage:OFFSet {offset}")
    
    def set_waveform(self, waveform: str):
        self.inst.write(f":WGEN:FUNCtion {waveform}")#SINusoid, SQUare, RAMP, PULSe, NOISe, DC, USER
    
    def set_output(self, output: str):
        self.inst.write(f":WGEN:OUTPut {output}")#ON or OFF

#Measurement commands

    def measure_bode_setup(self, channel1: int, channel2: int):
        self.inst.write(f":MEASure:CLEar")
        self.inst.write(f":MEASure:STATistics MEAN")
        self.inst.write(f":MEASure:VRMS AC,CHANnel{channel1}")
        self.inst.write(f":MEASure:VRMS AC,CHANnel{channel2}")
        self.inst.write(f":MEASure:FREQuency CHANnel{channel1}")
        #Phasenmeasurement überprüfen



    def measure(self):
        # rms1 = float(self.inst.query(f":MEASure:VRMS? CHANnel1"))
        # rms2 = float(self.inst.query(f":MEASure:VRMS? CHANnel1"))
        # freq = float(self.inst.query(f":MEASure:FREQuency? CHANnel1"))
        phase = float(self.inst.query(f":MEASure:PHASe? CHANnel1,CHANnel2"))
        self.inst.write(f":MEASure:STATistics:RESet")
        result = self.inst.query(f":MEASure:RESults?")
        result.append(phase)
        #return rms1, rms2, freq, phase
        res = [re.split(r'\s+', sub) for sub in result] # auf funktionalität prüfen!
        return res


    def measure_rms(self, channel: int):
        return float(self.inst.query(f":MEASure:VRMS? CHANnel{channel}"))
    
    def measure_freq(self, channel: int):
        return float(self.inst.query(f":MEASure:FREQuency? CHANnel{channel}"))
    
    def measure_phase(self, channel1: int, channel2: int):
        return float(self.inst.query(f":MEASure:PHASe? CHANnel{channel1},CHANnel{channel2}"))
        