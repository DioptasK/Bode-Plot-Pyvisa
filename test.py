import pyvisa

rm = pyvisa.ResourceManager('@py')
resources = rm.list_resources()
print("Gefundene VISA-Ressourcen:")
for res in resources:
    print(res)


scope = rm.open_resource('USB0::62700::4119::SDS08A0X802632::0::INSTR')
print(scope.query("*IDN?"))