from visa_py.resources import check_connection

def check(input):#TODO: Funktionalität noch prüfen #TODO: Lade yaml files
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
        return False
        

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
        return False
        

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
        return False

    sweeptype = input[3]
    if sweeptype == "lin" or sweeptype == "exp":
        print(f"Sweeptype: {sweeptype}")
    else:
        print("Wrong frequency progression type given")
        return False
    
    probe_1 = input[10]
    if not probe_1 == "Probe":
        if not isinstance(probe_1, int) and probe_1 >= 0:
            print("Probe_1 must be an unsigned integer.")
            return False
    
    probe_2 = input[11]
    if not probe_2 == "Probe":
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
        return False


    try:
        samplerate = input[5]
        if samplerate > 20 or samplerate < 0.01:
            print ("Samplerate must be a positive number greater than 0.01 and smaller than 20.")
            raise ValueError("")
        print(f"Samplerate: {samplerate} /s")
        sampleratecheck = True
    except ValueError:
        print("Invalid input for samplerate.")
        return False
    
    if not input[6]:
        print("No Scope ID given.")
    if input[6] and input[6] == input[8]:
        print("Scope and Functiongenerator ID are the same. Only opening Scope")
        
    check = check_connection(scope_id=input[6], functiongenerator_id=input[8])

    if check:
        print("Connection check completed.")
        for item in check:
            print(f"{item}")
        scopeidcheck = True
        signalgeneratoridcheck = True
    else:
        print("Connection failed. Please check device IDs.")
        return False

    if not (input[7] == "Agilent" or input[7] == "Siglent" or input[7] == "Rigol" or input[7] == "Agilent"):
        print("Scopemanufacturer not supported")
        return False
    
    if not (input[9] == "Agilent" or input[9] == "Siglent" or input[9] == "Rigol"or input[7] == "Agilent"):
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
        print("Consider adjusting the samplerate or samples.\n")
    elif measurement_time > 1800:
        print("Warning: Measurement time exceeds 30 minutes.")
        print("Consider adjusting the samplerate or samples.\n")
    elif measurement_time > 900:
        print("Warning: Measurement time exceeds 15 minutes.")
        print("Consider adjusting the samplerate or samples.\n")
    elif measurement_time > 600:
        print("Warning: Measurement time exceeds 10 minutes.")
        print("Consider adjusting the samplerate or samples.\n")
    elif measurement_time > 300:
        print("Warning: Measurement time exceeds 5 minutes.")
        print("Consider adjusting the samplerate or samples.\n")

    return True