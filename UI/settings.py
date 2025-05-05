import customtkinter
import tkinter as tk
from threading import Thread

from visa_py.resources import check_connection, query
from visa_py.inputs_check import check
from outputs.plot_output import plot



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

        def stop():
            #self.start_button.configure(state="normal")
            self.master.terminalframe.progressbar.stop()
            #TODO: Implement stop functionality here

        self.stop_button = customtkinter.CTkButton(self, text="Stop", command=stop)
        self.stop_button.grid(row=6, column=1, padx=10, pady=5)

        def start():
            def measure():
                self.master.terminalframe.progressbar.start()
                self.master.terminalframe.progressbar.set(0)

                results = query(parameter)  # blockierende Messung

                self.master.after(0, self.master.terminalframe.progressbar.stop)
                self.master.after(0, lambda: plot(results))
                self.master.after(0, lambda: self.start_button.configure(state="normal"))
                self.master.after(0, lambda: self.master.terminalframe.export_csv_button.configure(state="normal"))

            self.start_button.configure(state="disabled")
            self.master.terminalframe.clear_button.invoke()
            Thread(target=measure, daemon=True).start()


        self.start_button = customtkinter.CTkButton(self, text="Start", command=start)
        self.start_button.grid(row=7, column=0, padx=10, pady=5)
        self.start_button.grid(columnspan=2)
        self.start_button.configure(state="disabled")

        def check_params():
            parameter.clear()
            #self.master.terminalframe.clear_button.invoke()
            self.start_button.configure(state="disabled")
            startfrequency = int(self.startfrequency.get())
            stopfrequency = int(self.stopfrequency.get())
            amplitude = float(self.amplitude.get())
            sweeptype = self.sweeptype.get()
            samples = int(self.Samples.get())
            samplerate = float(self.samplerate.get())
            scope = self.master.hardwareframe.scope.get()
            functiongenerator = self.master.hardwareframe.signalgenerator.get()
            scope_manufacturer = self.master.hardwareframe.scope_manufacturer.get()
            functiongenerator_manufacturer = self.master.hardwareframe.signalgenerator_manufacturer.get()
            probe_1 = self.master.hardwareframe.probe_1.get()
            probe_2 = self.master.hardwareframe.probe_2.get()
            
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
            check(parameter)

        self.check_button = customtkinter.CTkButton(self, text="Check", command=check_params)
        self.check_button.grid(row=6, column=0, padx=10, pady=5)



        




