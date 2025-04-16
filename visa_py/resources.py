import pyvisa
import time
import numpy as np
import math

import sys
sys.path.append('/home/user/Documents/Studium/pyvisa')

from UI.device_input import device_input

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
        scope = rm.open_resource(scope_id)
        functiongenerator = rm.open_resource(functiongenerator_id)
        scope_query = scope.query("*IDN?")
        func_query = functiongenerator.query("*IDN?")
        device_input.textbox.insert("end", f"Scope: {scope_query.strip()}\n")
        device_input.textbox.insert("end", f"Function Generator: {func_query.strip()}\n")
        device_input.textbox.insert("end", "Verbindung erfolgreich.\n")
        print("Verbindung erfolgreich.")
        functiongenerator.close()
        scope.close()
        rm.close()
        return True
    except Exception as e:
        print(f"Fehler bei der Verbindung: {e}")
        return False


def query(parameter):
    
    rm = pyvisa.ResourceManager('@py')
    try:
        scope = rm.open_resource(parameter[6])
        functiongenerator = rm.open_resource(parameter[7])
        
        #recourcesetup


        
        frequency = parameter[0]
        amplitude = parameter[2]
        results = []

        for i in range(parameter[4]):
            if parameter[3] == "lin":
                frequency = parameter[0] + i*((parameter[1] - parameter[0]) / parameter[4])
            # elif parameter[3] == "log":
            #     frequency = parameter[0] * (parameter[1] / parameter[0]) ** (i / parameter[4])
            # elif parameter[3] == "exp":
            #     frequency = parameter[0] * (parameter[1] / parameter[0]) ** (i / parameter[4]) 

            print("Messe Frequenz:", frequency, "...")

            result = []

        # setze die frequenz, amplitude des funktionsgenerators
        # mehrmaliges messen von frequenz, amplituden und phase
        # timescale so setzen, dass immer 3-4 periodendauern sichtbar sind
        # amplitude des oszilloskopes einstellen
        #   time_for_measurement = 1 / samplerate
        #   while time < time_for_measurement:
        #      messe die frequenz, amplitude und phase
        #        messe frequenz 1, frequenz 2, amplitude 1, amplitude 2 und phase zwischen beiden
        #      time.sleep(1/samplerate)
        #   median oder mittelwert bilden
        # Ergebnis speichern

            results.append(result)

        return results
    except Exception as e:
        print(f"Fehler bei der Abfrage: {e}")