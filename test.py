import pyvisa
from visa_py.instructionsets.scopes.siglent_scope import SiglentScope

rm = pyvisa.ResourceManager('@py')
resources = rm.list_resources()
print("Gefundene VISA-Ressourcen:")
for res in resources:
    print(res)


scope = rm.open_resource('USB0::62700::4119::SDS08A0X802632::0::INSTR')
print(scope.query("*IDN?"))

scope = SiglentScope(scope)
try:
    scope.set_channel_output(1, "ON")
    scope.set_channel_output(2, "ON")
    scope.set_channel_units(1, "V")
    scope.set_channel_units(2, "V")
    scope.set_channel_attentuation(1, 10)
    scope.set_channel_attentuation(2, 10)
    scope.set_channel_offset(1, 5E-1)

    scope.measure_bode_setup(1, 2)
    result = scope.measure()
    print(result)
except Exception as e:
    print(f"Fehler: {e}")