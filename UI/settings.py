import customtkinter
import tkinter as tk

import sys
sys.path.append('/home/user/Documents/Studium/pyvisa')

from visa_py.resources import check_connection, query
import output



class settings(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        parameter = []

        self.grid_columnconfigure(0, weight=1)  # Textbox-Spalte
        self.grid_columnconfigure(1, weight=1)  # Button-Spalte (fix)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.default_startfrequenzy = tk.StringVar(value="10")
        self.startfrequenzy = customtkinter.CTkEntry(self, textvariable=self.default_startfrequenzy)
        self.startfrequenzy.grid(row=1,column=0,padx=10, pady=5)
        self.startfrequenzy_label = customtkinter.CTkLabel(self, text="Startfrequenz [Hz]", font=("Arial", -16))
        self.startfrequenzy_label.grid(row=0, column=0, padx=10, pady=5)

        self.default_stopfrequenzy = tk.StringVar(value="1000000")
        self.stopfrequenzy = customtkinter.CTkEntry(self, textvariable=self.default_stopfrequenzy)
        self.stopfrequenzy.grid(row=1,column=1,padx=10, pady=5)
        self.stopfrequenzy_label = customtkinter.CTkLabel(self, text="Stopfrequenz [Hz]", font=("Arial", -16))
        self.stopfrequenzy_label.grid(row=0, column=1, padx=10, pady=5)

        self.default_amplitude = tk.StringVar(value="2")
        self.amplitude = customtkinter.CTkEntry(self,textvariable=self.default_amplitude)
        self.amplitude.grid(row=3,column=0,padx=10, pady=5)
        self.amplitude_label = customtkinter.CTkLabel(self, text="Amplitude [Vpp]", font=("Arial", -16))
        self.amplitude_label.grid(row=2, column=0, padx=10, pady=5)

        self.sweeptype_label = customtkinter.CTkLabel(self, text="Sweeptyp:", font=("Arial", -16))
        self.sweeptype_label.grid(row=2, column=1, padx=10, pady=5)
        self.sweeptype = customtkinter.CTkOptionMenu(self, values=["log", "lin", "exp"])
        self.sweeptype.grid(row=3, column=1, padx=10, pady=5)

        self.default_samples = tk.StringVar(value="1000")
        self.Samples = customtkinter.CTkEntry(self, textvariable=self.default_samples)
        self.Samples.grid(row=5,column=0,padx=10, pady=5)
        self.Samples_label = customtkinter.CTkLabel(self, text="Samples", font=("Arial", -16))
        self.Samples_label.grid(row=4, column=0, padx=10, pady=5)

        self.default_samplerate = tk.StringVar(value="2")
        self.samplerate = customtkinter.CTkEntry(self, textvariable=self.default_samplerate)
        self.samplerate.grid(row=5,column=1,padx=10, pady=5)
        self.samplerate_label = customtkinter.CTkLabel(self, text="Samplerate [/s]", font=("Arial", -16))
        self.samplerate_label.grid(row=4, column=1, padx=10, pady=5)

        self.waveform_label = customtkinter.CTkLabel(self, text="Waveform:", font=("Arial", -16))
        self.waveform_label.grid(row=2, column=1, padx=10, pady=5)
        self.waveform = customtkinter.CTkOptionMenu(self, values=["sin", "ramp", "sqr", "saw", "pulse", "noise"])
        self.waveform.grid(row=6, column=0, padx=10, pady=5)

        def check():
            parameter.clear()
            self.master.terminalframe.clear_button.invoke()
            self.start_button.configure(state="disabled")

            startfrequenzy = 0
            stopfrequenzy = 0
            amplitude = 0
            sweeptype = ""
            samples = 0
            samplerate = 0
            waveform = ""

            startfreqcheck, stopfreqcheck, amplitudecheck, samplescheck, sampleratecheck, scopeidcheck, signalgeneratoridcheck = False, False, False, False, False, False, False

            try:
                startfrequenzy = int(self.startfrequenzy.get())
                if startfrequenzy < 0:
                    print ("Start frequency must be a positive integer.")
                    raise ValueError("Start frequency must be a positive integer.")
                print(f"Startfrequenzy: {startfrequenzy} Hz")
                startfreqcheck = True
            except ValueError:
                print("Invalid input for start frequency.")
                

            try:
                stopfrequenzy = int(self.stopfrequenzy.get())
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
                amplitude = float(self.amplitude.get())
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

            sweeptype = self.sweeptype.get()
            print(f"Sweeptype: {sweeptype}")
            waveform = self.waveform.get()
            print(f"Waveform: {waveform}")

            try:
                samples = int(self.Samples.get())
                if samples < 1:
                    print ("Samples must be a positive integer.")
                    raise ValueError("")
                print(f"Samples: {samples}")
                samplescheck = True
            except ValueError:
                print("Invalid input for samples.")


            try:
                samplerate = float(self.samplerate.get())
                if samplerate > 1000 or samplerate < 0.1:
                    print ("Samplerate must be a positive number greater than 0.1 and smaller than 1000.")
                    raise ValueError("")
                print(f"Samplerate: {samplerate} /s")
                sampleratecheck = True
            except ValueError:
                print("Invalid input for samplerate.")

            scope = self.master.hardwareframe.scope.get()
            functiongenerator = self.master.hardwareframe.signalgenerator.get()
            #TODO: Auskommentieren
            # if check_connection(scope, functiongenerator):
            #     print("Connection check completed.")
            #     print(f"Scope: {scope}\nFunction Generator: {functiongenerator}")
            # else:
            #     print("Connection failed. Please check device IDs.")

            if (startfreqcheck and stopfreqcheck and amplitudecheck and samplescheck and sampleratecheck):# and scopeidcheck and signalgeneratoridcheck): 
                print("All checks passed.")
                self.start_button.configure(state="normal")
            else:
                print("Some checks failed. Please correct the input values.")
                return
            
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
            print("Drücke Start um Messung zu starten...")
             
            parameter[0] = startfrequenzy
            parameter[1] = stopfrequenzy
            parameter[2] = amplitude
            parameter[3] = sweeptype
            parameter[4] = waveform
            parameter[5] = samples
            parameter[6] = samplerate
            parameter[7] = scope
            parameter[8] = functiongenerator
            print(parameter)



        def stop():
            self.start_button.configure(state="normal")
            print("Stop button pressed")
            #TODO: Implement stop functionality here

        self.check_button = customtkinter.CTkButton(self, text="Check", command=check)
        self.check_button.grid(row=6, column=0, padx=10, pady=5)

        self.stop_button = customtkinter.CTkButton(self, text="Stop", command=stop)
        self.stop_button.grid(row=6, column=1, padx=10, pady=5)

        def start():
            self.start_button.configure(state="disabled")
            results = query(parameter)
            self.master.outputframe.plot(results)


        self.start_button = customtkinter.CTkButton(self, text="Start", command=start)
        self.start_button.grid(row=7, column=0, padx=10, pady=5)
        self.start_button.grid(columnspan=2)
        self.start_button.configure(state="disabled")

        