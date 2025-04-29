import customtkinter
import tkinter as tk
from threading import Thread

from visa_py.resources import check_connection, query
from UI import output



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

        self.default_startfrequency = tk.StringVar(value="10")
        self.startfrequency = customtkinter.CTkEntry(self, textvariable=self.default_startfrequency)
        self.startfrequency.grid(row=1,column=0,padx=10, pady=5)
        self.startfrequency_label = customtkinter.CTkLabel(self, text="Startfrequenz [Hz]", font=("Arial", -16))
        self.startfrequency_label.grid(row=0, column=0, padx=10, pady=5)

        self.default_stopfrequency = tk.StringVar(value="1000")
        self.stopfrequency = customtkinter.CTkEntry(self, textvariable=self.default_stopfrequency)
        self.stopfrequency.grid(row=1,column=1,padx=10, pady=5)
        self.stopfrequency_label = customtkinter.CTkLabel(self, text="Stopfrequenz [Hz]", font=("Arial", -16))
        self.stopfrequency_label.grid(row=0, column=1, padx=10, pady=5)

        self.default_amplitude = tk.StringVar(value="3")
        self.amplitude = customtkinter.CTkEntry(self,textvariable=self.default_amplitude)
        self.amplitude.grid(row=3,column=0,padx=10, pady=5)
        self.amplitude_label = customtkinter.CTkLabel(self, text="Amplitude [Vpp]", font=("Arial", -16))
        self.amplitude_label.grid(row=2, column=0, padx=10, pady=5)

        self.sweeptype_label = customtkinter.CTkLabel(self, text="Sweeptyp:", font=("Arial", -16))
        self.sweeptype_label.grid(row=2, column=1, padx=10, pady=5)
        self.sweeptype = customtkinter.CTkOptionMenu(self, values=["lin", "exp"])
        self.sweeptype.grid(row=3, column=1, padx=10, pady=5)

        self.default_samples = tk.StringVar(value="10")
        self.Samples = customtkinter.CTkEntry(self, textvariable=self.default_samples)
        self.Samples.grid(row=5,column=0,padx=10, pady=5)
        self.Samples_label = customtkinter.CTkLabel(self, text="Samples", font=("Arial", -16))
        self.Samples_label.grid(row=4, column=0, padx=10, pady=5)

        self.default_samplerate = tk.StringVar(value="0.5")
        self.samplerate = customtkinter.CTkEntry(self, textvariable=self.default_samplerate)
        self.samplerate.grid(row=5,column=1,padx=10, pady=5)
        self.samplerate_label = customtkinter.CTkLabel(self, text="Samplerate [/s]", font=("Arial", -16))
        self.samplerate_label.grid(row=4, column=1, padx=10, pady=5)

        

        def check():
            parameter.clear()
            self.master.terminalframe.clear_button.invoke()
            self.start_button.configure(state="disabled")

            startfrequency = 0
            stopfrequency = 0
            amplitude = 0
            sweeptype = ""
            samples = 0
            samplerate = 0
            probe_1 = 0
            probe_2 = 0


            startfreqcheck, stopfreqcheck, amplitudecheck, samplescheck, sampleratecheck, scopeidcheck, signalgeneratoridcheck = False, False, False, False, False, False, False

            try:
                startfrequency = int(self.startfrequency.get())
                if startfrequency < 1:
                    print ("Start frequency must be a positive integer.")
                    raise ValueError("Start frequency must be a positive integer.")
                print(f"Startfrequency: {startfrequency} Hz")
                startfreqcheck = True
            except ValueError:
                print("Invalid input for start frequency.")
                

            try:
                stopfrequency = int(self.stopfrequency.get())
                if stopfrequency < 0:
                    raise ValueError("Stop frequency must be a positive integer.")
                if stopfrequency <= startfrequency:
                    startfrequency = 10
                    raise ValueError("Stop frequency must be greater than start frequency.")
                if stopfrequency > 1000000000:
                    raise ValueError("Stop frequency must be less than 1 GHz.")
                print(f"Stopfrequency: {stopfrequency} Hz")
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
                if samplerate > 20 or samplerate < 0.01:
                    print ("Samplerate must be a positive number greater than 0.01 and smaller than 20.")
                    raise ValueError("")
                print(f"Samplerate: {samplerate} /s")
                sampleratecheck = True
            except ValueError:
                print("Invalid input for samplerate.")

            scope = self.master.hardwareframe.scope.get()
            functiongenerator = self.master.hardwareframe.signalgenerator.get()
            scope_manufacturer = self.master.hardwareframe.scope_manufacturer.get()
            functiongenerator_manufacturer = self.master.hardwareframe.signalgenerator_manufacturer.get()
            probe_1 = self.master.hardwareframe.probe_1.get()
            probe_2 = self.master.hardwareframe.probe_2.get()

            if probe_1 == "Probe":
                print("No Attenuation given on Probe_1. Using 1")
                self.master.hardwareframe.probe_1.set("1")
                probe_1 = 1
            if probe_2 == "Probe":
                print("No Attenuation given on Probe_2. Using 1")
                self.master.hardwareframe.probe_2.set("1")
                probe_2 = 1
            
             

            if not scope:
                print("No Scope ID given.")
            if scope and scope == functiongenerator:
                print("Scope and Functiongenerator ID are the same. Only opening Scope")
                
            check = check_connection(scope_id=scope, functiongenerator_id=functiongenerator)
            if check:
                print("Connection check completed.")
                for item in check:
                    print(f"{item}")
                scopeidcheck = True
                signalgeneratoridcheck = True
            else:
                print("Connection failed. Please check device IDs.")

            if (startfreqcheck and stopfreqcheck and amplitudecheck and samplescheck and sampleratecheck and scopeidcheck and signalgeneratoridcheck): 
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
             
            parameter.append(startfrequency)
            parameter.append(stopfrequency)
            parameter.append(amplitude)
            parameter.append(sweeptype)
            parameter.append(samples)
            parameter.append(samplerate)
            parameter.append(scope)
            parameter.append(scope_manufacturer)
            parameter.append(functiongenerator)
            parameter.append(functiongenerator_manufacturer)
            parameter.append(probe_1)
            parameter.append(probe_2)
            print(parameter)



        def stop():
            #self.start_button.configure(state="normal")
            self.master.terminalframe.progressbar.stop()
            #TODO: Implement stop functionality here

        self.check_button = customtkinter.CTkButton(self, text="Check", command=check)
        self.check_button.grid(row=6, column=0, padx=10, pady=5)

        self.stop_button = customtkinter.CTkButton(self, text="Stop", command=stop)
        self.stop_button.grid(row=6, column=1, padx=10, pady=5)

        def start():
            # self.start_button.configure(state="disabled")
            # self.master.terminalframe.clear_button.invoke()
            # print(parameter, flush=True)
            # print("-----------Measuring-----------", flush=True)
            # self.master.terminalframe.progressbar.start()
            # results = query(parameter)
            # self.master.terminalframe.progressbar.stop()
            # self.master.outputframe.plot(results)
            def measure():
                print(parameter, flush=True)
                print("-----------Measuring-----------", flush=True)
                self.master.terminalframe.progressbar.start()
                self.master.terminalframe.progressbar.set(0)

                results = query(parameter)  # blockierende Messung

                self.master.after(0, self.master.terminalframe.progressbar.stop)
                self.master.after(0, lambda: self.master.outputframe.plot(results))
                self.master.after(0, lambda: self.start_button.configure(state="normal"))

            self.start_button.configure(state="disabled")
            self.master.terminalframe.clear_button.invoke()
            Thread(target=measure, daemon=True).start()
            results=[]
            self.master.outputframe.plot(results)


        self.start_button = customtkinter.CTkButton(self, text="Start", command=start)
        self.start_button.grid(row=7, column=0, padx=10, pady=5)
        self.start_button.grid(columnspan=2)
        self.start_button.configure(state="disabled")

        




