import pyvisa
import time
from visa_py.instructionsets.scopes.keysight_scope import KeysightScope

rm = pyvisa.ResourceManager('@py')
resources = rm.list_resources()
print("Gefundene VISA-Ressourcen:")
for res in resources:
    print(res)


scope = rm.open_resource(resources[0])
print(scope.query("*IDN?"))

scope = KeysightScope(scope)
try:
    scope.set_channel_output(1, "ON")
    scope.set_channel_output(2, "ON")
    scope.set_channel_units(1, "V")
    scope.set_channel_units(2, "V")
    #scope.set_channel_attenuation(1, 10)
    #scope.set_channel_attenuation(2, 10)
    scope.set_channel_offset(1, 0E0)
    scope.set_channel_offset(2, 0E0)
    scope.set_channel_label(1, "INPUT")
    scope.set_channel_label(2, "OUTPUT")
    scope.set_channel_coupling(1, "AC")
    scope.set_channel_coupling(2, "AC")
    #scope.set_channel_vertical_scale(1, pkpk/9)
    scope.measure_bode_setup(1, 2)

    scope.set_output("ON")
    scope.set_waveform("SINusoid")
    scope.set_frequency(500)
    scope.set_amplitude(3E0)
    scope.set_offset(0)

    time.sleep(5)  # Warten auf Stabilisierung

    scope.measure_bode_setup(1, 2)
    print(scope.measure_rms(1))
    print(scope.measure_rms(2))
    print(scope.measure_freq(1))
    print(scope.measure_phase(1,2))

except Exception as e:
    print(f"Fehler: {e}")