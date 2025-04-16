import pyvisa
import time
import numpy as np
import math

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
        scope = rm.open_resource(scope_id)
        scope_query = scope.query("*IDN?")
        result.append(scope_query)
        scope.close()
        if  not scope_id == functiongenerator_id:
            functiongenerator = rm.open_resource(functiongenerator_id)#TODO: bei zwei gleichech ids nur einmal öffnen
            func_query = functiongenerator.query("*IDN?")
            result.append(func_query)
            functiongenerator.close()
        else:
            print("Scope und Funktionsgenerator haben die gleiche ID. Nur einmal öffnen.")
        print("Verbindung erfolgreich.")
        rm.close()
        return result
    except Exception as e:
        print(f"Fehler bei der Verbindung: {e}")
        return False

def x_axis_scaling(freq):
    """
    Berechnet die X-Achsen-Skalierung basierend auf der Abtastrate und der Anzahl der Samples.
    """
    return (1 / freq) / 3

def y_axis_scaling(amplitude):
    """
    Berechnet die Y-Achsen-Skalierung basierend auf der Amplitude.
    """
    return amplitude / 2 #TODO: Hier die richtige Formel einfügen

def query(parameter):
    startfrequenzy =  parameter[0]
    stopfrequenzy = parameter[1]
    amplitude = parameter[2]
    sweeptype = parameter[3]
    samples = parameter[4]
    samplerate = parameter[5]
    scopeid = parameter[6]
    scope_manufacturer = parameter[7]
    functiongeneratorid = parameter[8]
    functiongenerator_manufacturer = parameter[9]

    rm = pyvisa.ResourceManager('@py')#TODO: bei gleicher id nur einmal öffnen
    try:
        scope = rm.open_resource(scopeid)
        #functiongenerator = rm.open_resource(functiongeneratorid)

        if(scope_manufacturer == "Siglent"):
            scope = SiglentScope(scope)
            print("Using Siglent Instructionset")
        elif(scope_manufacturer == "Rigol"):
            scope = RigolScope(scope)
            print("Using Rigol Instructionset")
        elif(scope_manufacturer == "Keysight" or scope_manufacturer == "Agilent"):
            scope = KeysightScope(scope)
            print("Using Keysight Instructionset")
        
        #recourcesetup
        # functiongenerator.write("FUNCtion SINusoid")
        # functiongenerator.write("VOLTage:UNIT VPP")
        # functiongenerator.write("VOLTage {amplitude}")
        # functiongenerator.write("OUTPut ON")


        scope.set_channel_output(1, "ON")
        scope.set_channel_output(2, "ON")
        scope.set_channel_units(1, "A")
        scope.set_channel_units(2, "A")
        scope.set_channel_vertical_scale(1, 5E+0)

        # scope.write(":CHANnel2:Display ON")
        # # scope.write(":CHANnel1:PROBe 10")#TODO: möglicherweise noch eingabe hinzugfügen
        # # scope.write(":CHANnel2:PROBe 10")
        # scope.write(":CHANnel1:COUPling DC")
        # scope.write(":CHANnel2:COUPling DC")
        # if(stopfrequenzy < 25000000):
        #     scope.write(":CHANnel1:BWLimit ON")
        #     scope.write(":CHANnel2:BWLimit ON")


        # scope.write(":CHANnel1:LABel INPUT")
        # scope.write(":CHANnel2:LABel OUTPUT")


        # scope.write(":CHANnel1:OFFSet 0")
        # scope.write(":CHANnel2:OFFSet 0")
        # scope.write(":CHANnel1:UNITs VOLT")
        # scope.write(":CHANnel2:UNITs VOLT")
        




        # results = []

        # for i in range(samples):
        #     if sweeptype == "lin":
        #         frequency = startfrequenzy + i*((stopfrequenzy - startfrequenzy) / samples)
        #     elif sweeptype == "exp":
        #         frequency = startfrequenzy + math.exp(i*((stopfrequenzy - startfrequenzy) / samples))

            

        #     result = []

        #     # # setze die frequenz des funktionsgenerators
        #     # functiongenerator.write("FREQuency {frequency}")#TODO: frequenz setz befehl richig?
        #     # freq = functiongenerator.query("FREQuency?")
        #     # print("Messe Frequenz:", freq, "...") 

        #     x_axis_scaling = x_axis_scaling(freq)
        #     scope.write("")

        #     y_axis_scaling = y_axis_scaling(amplitude)#TODO: hiern noch anpassen
        #     scope.write(":CHANnel1:SCALe {y_axis_scaling}")

        #     #skaliere beide achsen
        #     #for noch zeit 
        #     #  messe die frequenz 1 und 2
        #     #  amplitude 1 und 2
        #     #  phase zwischen beiden messen
        #     #  speichern in liste
        #     #median oder mittelwert bilden
        #     #result.append(ergebnis)


        #     results.append(result)

        # return results
    except Exception as e:
        print(f"Fehler bei der Abfrage: {e}")