import pyvisa
import time
import numpy as np

from visa_py.instructionsets.functiongenerators.siglent_functiongenerator import SiglentFunctionGenerator
from visa_py.instructionsets.functiongenerators.rigol_functiongenerator import RigolFunctionGenerator
from visa_py.instructionsets.functiongenerators.keysight_functiongenerator import KeysightFunctionGenerator
from visa_py.instructionsets.scopes.siglent_scope import SiglentScope
from visa_py.instructionsets.scopes.rigol_scope import RigolScope
from visa_py.instructionsets.scopes.keysight_scope import KeysightScope


def get_connected_devices():
    """
    Listet alle verfügbaren Geräte auf und gibt sie zurück.
    """
    rm = pyvisa.ResourceManager('@py')
    connected_devices = rm.list_resources()
    rm.close()
    return connected_devices


def check_connection(scope_id, functiongenerator_id):
    rm = pyvisa.ResourceManager('@py')
    try:
        result = []
        if not scope_id:
            return
        if (scope_id):        
            scope = rm.open_resource(scope_id)
            scope_query = scope.query("*IDN?")
            result.append(scope_query)
            scope.close()
        if(functiongenerator_id):
            if(functiongenerator_id != scope_id):
                functiongenerator = rm.open_resource(functiongenerator_id)
                func_query = functiongenerator.query("*IDN?")
                result.append(func_query)
                functiongenerator.close()
        
        rm.close()
        return result
    except Exception as e:
        print(f"Fehler bei der Verbindung: {e}")
        return False

def x_axis_scaling(scope, freq):
    timebase = (1 / freq) / 3
    scope.set_timebase(timebase)
    

def y_axis_scaling(scope, pkpk):
    #scope.set_channel_vertical_scale(2, pkpk)#TODO: Hier die richtige vorgehensweise implementieren
    print("y_axis_scaling not implemented yet")

def functiongenerator_setup(functiongenerator, frequency, pkpk):
    print("Functiongenerator setup")
    freq = f"{frequency:.2E}"
    functiongenerator.apply_settings(1, freq, pkpk, "SINusoid")

def scope_setup(scope, use_as_functiongenerator, pkpk, frequency, probe_1, probe_2):
    print("Scope setup")

    scope.set_channel_output(1, "ON")
    scope.set_channel_output(2, "ON")
    scope.set_channel_units(1, "V")
    scope.set_channel_units(2, "V")
    scope.set_channel_attenuation(1, int(probe_1))
    scope.set_channel_attenuation(2, int(probe_2))
    scope.set_channel_offset(1, 0E0)
    scope.set_channel_offset(2, 0E0)
    scope.set_channel_label(1, "INPUT")
    scope.set_channel_label(2, "OUTPUT")
    scope.set_channel_coupling(1, "AC")
    scope.set_channel_coupling(2, "AC")
    #scope.set_channel_vertical_scale(1, pkpk/9)
    scope.measure_bode_setup(1, 2)


    if use_as_functiongenerator:
        scope.set_output("ON")
        scope.set_waveform("SINusoid")
        scope.set_frequency(frequency)
        scope.set_amplitude(pkpk)
        scope.set_offset(0)
    



def query(parameter):


    scope_is_functiongenerator = False
    startfrequency =  parameter[0]
    stopfrequency = parameter[1]
    pkpk = parameter[2]
    sweeptype = parameter[3]
    samples = parameter[4]
    samplerate = parameter[5]
    scopeid = parameter[6]
    scope_manufacturer = parameter[7]
    functiongeneratorid = parameter[8]
    functiongenerator_manufacturer = parameter[9]
    probe_1 = parameter[10]
    probe_2 =parameter[11]

    rm = pyvisa.ResourceManager('@py')
    try:

        scope = rm.open_resource(scopeid)

        if(scope_manufacturer == "Siglent"):
            scope = SiglentScope(scope)
            print("Using Siglent Instructionset")
        elif(scope_manufacturer == "Rigol"):
            scope = RigolScope(scope)
            print("Using Rigol Instructionset")
        elif(scope_manufacturer == "Keysight" or scope_manufacturer == "Agilent"):
            scope = KeysightScope(scope)
            print("Using Keysight Instructionset")

        if(scopeid == functiongeneratorid or not functiongeneratorid):
            print("Using Scope as functiongenerator")
            scope_setup(scope, True, pkpk,startfrequency,probe_1,probe_2)
            scope_is_functiongenerator = True
        else:
            functiongenerator = rm.open_resource(functiongeneratorid)
            if(functiongenerator_manufacturer =="Siglent"):
                functiongenerator = SiglentFunctionGenerator(functiongenerator)
            elif(functiongenerator_manufacturer == "Keysight" or functiongenerator_manufacturer == "Agilent"):
                functiongenerator = KeysightFunctionGenerator(functiongenerator)
            elif(functiongenerator_manufacturer == "Rigol"):
                functiongenerator = RigolFunctionGenerator(functiongenerator)
            scope_setup(scope, False, pkpk, startfrequency,probe_1,probe_2)
            functiongenerator_setup(functiongenerator, startfrequency, pkpk)   

        print(parameter, flush=True)
        print("-----------Measuring-----------", flush=True)         

        print("Samples        RMS 1      RMS 2       Frequency       Phase")
        print("-------------------------------------------------------------------------------")
        results = []
        samples_to_do = samples

        x_points = np.logspace(np.log10(startfrequency),np.log10(stopfrequency),samples)

        for i in range(samples):
            if sweeptype == "lin":
                frequency = startfrequency + i*((stopfrequency - startfrequency) / samples)
            elif sweeptype == "exp":
                frequency = x_points[i]

            if frequency < 20000000:
                scope.set_channel_bwlimit(1, "ON")
                scope.set_channel_bwlimit(2, "ON")
            else:
                scope.set_channel_bwlimit(1, "OFF")
                scope.set_channel_bwlimit(2, "OFF")

            if scope_is_functiongenerator: 
                scope.set_frequency(frequency)
            else:
                functiongenerator.set_frequency(frequency)
            x_axis_scaling(scope, frequency)
            #y_axis_scaling(scope, pkpk)
            time.sleep((1 / samplerate))
            result = [0,0,0,0]
            rms1 = scope.measure_rms(1)
            result[0] = rms1
            rms2 = scope.measure_rms(2)
            result[1] = rms2
            freq = scope.measure_freq(1)
            result[2] = freq
            phase = scope.measure_phase(1,2)
            result[3] = phase
            print(samples_to_do,",",rms1, ",", rms2, ",", freq, ",", phase, flush=True)
            results.append(result)
            samples_to_do -= 1

        results_array = np.array(results)
        return results_array
    except Exception as e:
        print(f"Fehler bei der Abfrage: {e}")