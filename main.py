import argparse

from UI.mainframe import mainframe
from UI.plot_only import plot
from visa_py import resources

parser = argparse.ArgumentParser(description='Bodeplot-Messprogramm')

parser.add_argument('-c', action='store_true', help='Flag to indicate if the output should be stored in a .csv')
parser.add_argument('-u', action='store_true', help='Flag to indicate if the UI should be used')
parser.add_argument('-startfrequency', type=int, default=10, help='Startfrequency in Hz (Default: 10Hz)')
parser.add_argument('-stopfrequency', type=int, default=100000, help='Stopfrequency in Hz (Default: 100kHz)')
parser.add_argument('-amplitude', type=float, default=2, help='Amplitude in Vpp (Default: 3Vpp)')
parser.add_argument('-sweeptype', type=str, default='log', help='Type of frequency progression (Default: lin) (Options: lin, exp)')
parser.add_argument('-samples', type=int, default=1000, help='Number of samples (Default: 1000)')
parser.add_argument('-samplerate', type=float, default=0.5, help='Number of measurements per second (Default: 0.5/s)')
parser.add_argument('-scope_manufacturer', type=str, default="Siglent", help='Manufacturere of the Scope (Default: Siglent)')
parser.add_argument('-probe_1', type=int, default=0.5, help='Attenuation of Channel_1 (Default: 10)')
parser.add_argument('-probe_2', type=int, default=0.5, help='Attenuation of Channel_2 (Default: 10)')
parser.add_argument('-scope_id', type=str, default="", help='Visa ID of the scope')
parser.add_argument('-functiongenerator_manufacturer', type=str, default="Siglent", help='Manufacturer of the signalgenerator (Default: Siglent)')
parser.add_argument('-functiongenerator_id', type=str, default="", help='Visa ID of the functiongenerator')

args = parser.parse_args()

def export_csv(input):
    print("Test")

def check(input):#TODO: Funktionalität noch anpassen
    startfrequenzy = 0
    stopfrequenzy = 0
    amplitude = 0
    sweeptype = ""
    samples = 0
    samplerate = 0
    probe_1 = 0
    probe_2 = 0


    startfreqcheck, stopfreqcheck, amplitudecheck, samplescheck, sampleratecheck, scopeidcheck, signalgeneratoridcheck = False, False, False, False, False, False, False

    try:
        startfrequenzy = input[0]
        if startfrequenzy < 1:
            print ("Start frequency must be a positive integer.")
            raise ValueError("Start frequency must be a positive integer.")
        print(f"Startfrequenzy: {startfrequenzy} Hz")
        startfreqcheck = True
    except ValueError:
        print("Invalid input for start frequency.")
        

    try:
        stopfrequenzy = input[1]
        if stopfrequenzy < 0:
            raise ValueError("Stop frequency must be a positive integer.")
        if stopfrequenzy <= startfrequenzy:
            startfrequenzy = 10
            raise ValueError("Stop frequency must be greater than start frequency.")
        if stopfrequenzy > 1000000000:
            raise ValueError("Stop frequency must be less than 1 GHz.")
        print(f"Stopfrequenzy: {stopfrequenzy} Hz")
        stopfreqcheck = True
    except ValueError as e:
        print(e)
        print("Invalid input for stop frequency.")
        

    try:
        amplitude = input[2]
        if amplitude < 0.02:
            print ("Amplitude must be a positive number greater than 20mVpp.")
            raise ValueError("")
        if amplitude > 20:
            print ("Amplitude must be less than 20 Vpp.")
            raise ValueError("")
        print(f"Amplitude: {amplitude} Vpp")
        amplitudecheck = True
    except ValueError:
        print("Invalid input for amplitude.")

    sweeptype = input[3]
    if sweeptype == "lin" or sweeptype == "exp":
        print(f"Sweeptype: {sweeptype}")
    else:
        print("Wrong frequency progression type given")
        return False
    
    probe_1 = input[10]
    if not isinstance(probe_1, int) and probe_1 >= 0:
        print("Probe_1 must be an unsigned integer.")
        return False
    
    probe_2 = input[11]
    if not isinstance(probe_2, int) and probe_2 >= 0:
        print("Probe_2 must be an unsigned integer.")
        return False

    try:
        samples = input[4]
        if samples < 1:
            print ("Samples must be a positive integer.")
            raise ValueError("")
        print(f"Samples: {samples}")
        samplescheck = True
    except ValueError:
        print("Invalid input for samples.")


    try:
        samplerate = input[5]
        if samplerate > 20 or samplerate < 0.01:
            print ("Samplerate must be a positive number greater than 0.01 and smaller than 20.")
            raise ValueError("")
        print(f"Samplerate: {samplerate} /s")
        sampleratecheck = True
    except ValueError:
        print("Invalid input for samplerate.")
    
    if not input[6]:
        print("No Scope ID given.")
    if input[6] and input[6] == input[8]:
        print("Scope and Functiongenerator ID are the same. Only opening Scope")
        
    check = resources.check_connection(scope_id=input[6], functiongenerator_id=input[8])

    if check:
        print("Connection check completed.")
        for item in check:
            print(f"{item}")
        scopeidcheck = True
        signalgeneratoridcheck = True
    else:
        print("Connection failed. Please check device IDs.")

    if not (input[7] == "Agilent" or input[7] == "Siglent" or input[7] == "Rigol"):
        print("Scopemanufacturer not supported")
        return False
    
    if not (input[9] == "Agilent" or input[9] == "Siglent" or input[9] == "Rigol"):
        print("Signalgeneratormanufacturer not supported")
        return False

    if (startfreqcheck and stopfreqcheck and amplitudecheck and samplescheck and sampleratecheck and scopeidcheck and signalgeneratoridcheck): 
        print("All checks passed.")
    else:
        print("Some checks failed. Please correct the input values.")
        return False
    
    measurement_time = (1/samplerate) * samples
    print(f"Measurement time: {measurement_time} seconds")
    if measurement_time > 3600:
        print("Warning: Measurement time exceeds 1 hour.")
        print("Eventuel Samplerate oder Samples anpassen\n")
    elif measurement_time > 1800:
        print("Warning: Measurement time exceeds 30 minutes.")
        print("Eventuel Samplerate oder Samples anpassen\n")
    elif measurement_time > 900:
        print("Warning: Measurement time exceeds 15 minutes.")
        print("Eventuel Samplerate oder Samples anpassen\n")
    elif measurement_time > 600:
        print("Warning: Measurement time exceeds 10 minutes.")
        print("Eventuel Samplerate oder Samples anpassen\n")
    elif measurement_time > 300:
        print("Warning: Measurement time exceeds 5 minutes.")
        print("Eventuel Samplerate oder Samples anpassen\n")

    return True


if args.u:
    if __name__ == "__main__":
        app = mainframe()
        app.mainloop()

else:
    parameters = []
    parameters.append(args.startfrequency)
    parameters.append(args.stopfrequency)
    parameters.append(args.amplitude)
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
        result = resources.query(parameters)
        plot(result)
        if args.c:
            export_csv(result)