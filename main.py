import argparse

from UI.mainframe import mainframe
from outputs.plot_output import plot
from outputs.export_output import export_csv
from visa_py.inputs_check import check
from visa_py.resources import query


parser = argparse.ArgumentParser(description='Bodeplot-Messprogramm')

parser.add_argument('-c', action='store_true', help='Flag to indicate if the output should be stored in a .csv')
parser.add_argument('-u', action='store_true', help='Flag to indicate if the UI should be used')
parser.add_argument('-startfrequency', type=int, default=10, help='Startfrequency in Hz (Default: 10Hz)')
parser.add_argument('-stopfrequency', type=int, default=100000, help='Stopfrequency in Hz (Default: 100kHz)')
parser.add_argument('-pkpk', type=float, default=2, help='Amplitude in Vpp (Default: 3Vpp)')
parser.add_argument('-sweeptype', type=str, default='lin', help='Type of frequency progression (Default: lin) (Options: lin, exp)')
parser.add_argument('-samples', type=int, default=1000, help='Number of samples (Default: 1000)')
parser.add_argument('-samplerate', type=float, default=0.5, help='Number of measurements per second (Default: 0.5/s)')
parser.add_argument('-scope_manufacturer', type=str, default="Siglent", help='Manufacturere of the Scope (Default: Siglent)')
parser.add_argument('-probe_1', type=int, default=10, help='Attenuation of Channel_1 (Default: 10)')
parser.add_argument('-probe_2', type=int, default=10, help='Attenuation of Channel_2 (Default: 10)')
parser.add_argument('-scope_id', type=str, default="", help='Visa ID of the scope')
parser.add_argument('-functiongenerator_manufacturer', type=str, default="Siglent", help='Manufacturer of the signalgenerator (Default: Siglent)')
parser.add_argument('-functiongenerator_id', type=str, default="", help='Visa ID of the functiongenerator')

args = parser.parse_args()




if args.u:
    if __name__ == "__main__":
        app = mainframe()
        app.mainloop()

else:
    parameters = []
    parameters.append(args.startfrequency)
    parameters.append(args.stopfrequency)
    parameters.append(args.pkpk)
    parameters.append(args.sweeptype)
    parameters.append(args.samples)
    parameters.append(args.samplerate)
    parameters.append(args.scope_id)
    parameters.append(args.scope_manufacturer)
    parameters.append(args.functiongenerator_id)
    parameters.append(args.functiongenerator_manufacturer)
    parameters.append(args.probe_1)
    parameters.append(args.probe_2)

    if(check(parameters)):
        result = query(parameters)
        plot(result)
        if args.c:
            export_csv(result, parameters)
    else: 
        print("Parameter error")