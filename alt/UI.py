import customtkinter
import sys
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from Visa.resources import get_connected_devices, check_connection, query

customtkinter.set_appearance_mode("dark")  # Set dark mode
customtkinter.set_default_color_theme("dark-blue")  # Set color theme


def measure(parameter):
    result = query(parameter)
    if result is not None:
        # Process the result and update the UI
        app.settingframe.start_button.configure(state="normal")
        print("Measurement completed.")
       #TODO: create_Output() aufrufen
        
class hardwareframe(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)


        self.scope = customtkinter.CTkEntry(self, placeholder_text="Scope")
        self.scope.grid(row=1,column=0,padx=10, pady=5)
        self.scope_label = customtkinter.CTkLabel(self, text="Scope-ID", font=("Arial", -16))
        self.scope_label.grid(row=0, column=0, padx=10, pady=5)

        self.signalgenerator = customtkinter.CTkEntry(self, placeholder_text="Signalgenerator")
        self.signalgenerator.grid(row=1,column=1,padx=10, pady=5)
        self.signalgenerator_label = customtkinter.CTkLabel(self, text="Signalgenerator-ID", font=("Arial", -16))
        self.signalgenerator_label.grid(row=0, column=1, padx=10, pady=5)

        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=3, column=0,rowspan=1, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        def refresh():
            devices = get_connected_devices()
            if len(devices) == 0:
                self.textbox.insert("end", "No devices found.\n")
            else:
                self.textbox.delete("0.0", "end")
                for device in devices:
                    self.textbox.insert("end", device + "\n")
        
        def check():
            scope_id = self.scope.get()
            functiongenerator_id = self.signalgenerator.get()
            if not scope_id or not functiongenerator_id:
                self.textbox.insert("end", "Please enter both device IDs.\n")
                return
            result = check_connection(scope_id, functiongenerator_id)
            self.textbox.insert("end", "Connection check completed.\n")
            if result:
                self.textbox.insert("end", f"Scope: {result[0]}\n")
                self.textbox.insert("end", f"Function Generator: {result[1]}\n")
            else:
                self.textbox.insert("end", "Connection failed.\n")

        self.refresh_button = customtkinter.CTkButton(self, text="Get Devices", command=refresh)
        self.refresh_button.grid(row=2, column=0,padx=10, pady=5)

        self.check_connection_button = customtkinter.CTkButton(self, text="Check Connection", command=check)
        self.check_connection_button.grid(row=2, column=1,padx=10, pady=5)


class settingframe(customtkinter.CTkFrame):
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

        def check():#TODO: checke ob die geräte auch wirklich verbunden sind
            parameter.clear()
            self.master.termianlframe.clear_button.invoke()

            startfrequenzy = 0
            stopfrequenzy = 0
            amplitude = 0
            sweeptype = ""
            samples = 0
            samplerate = 0

            try:
                startfrequenzy = int(self.startfrequenzy.get())
                if startfrequenzy < 0:
                    print ("Start frequency must be a positive integer.")
                    raise ValueError("Start frequency must be a positive integer.")
                print(f"Startfrequenzy: {startfrequenzy} Hz")
            except ValueError:
                print("Invalid input for start frequency. Using default value: 10 Hz")
                startfrequenzy = 10

            try:
                stopfrequenzy = int(self.stopfrequenzy.get())
                if stopfrequenzy < 0:
                    raise ValueError("Stop frequency must be a positive integer. Using default value: 1000000 Hz")
                if stopfrequenzy <= startfrequenzy:
                    startfrequenzy = 10
                    raise ValueError("Stop frequency must be greater than start frequency. Using default values 10 Hz and 1000000 Hz.")
                if stopfrequenzy > 1000000000:
                    raise ValueError("Stop frequency must be less than 1 GHz. Using default value: 1000000 Hz")
                print(f"Stopfrequenzy: {stopfrequenzy} Hz")
            except ValueError as e:
                print(e)
                stopfrequenzy = 1000000

            try:
                amplitude = float(self.amplitude.get())
                if amplitude < 0.02:
                    print ("Amplitude must be a positive number greater than 20mVpp.")
                    raise ValueError("Amplitude must be a positive number.")
                if amplitude > 20:
                    print ("Amplitude must be less than 20 Vpp.")
                    raise ValueError("Amplitude must be less than 20 Vpp.")
                print(f"Amplitude: {amplitude} Vpp")
            except ValueError:
                print("Invalid input for amplitude. Using default value: 2 Vpp")
                amplitude = 2

            sweeptype = self.sweeptype.get()
            print(f"Sweeptype: {sweeptype}")

            try:
                samples = int(self.Samples.get())
                if samples < 1:
                    print ("Samples must be a positive integer.")
                    raise ValueError("")
                print(f"Samples: {samples}")
            except ValueError:
                print("Invalid input for samples. Using default value: 1000")
                samples = 1000

            try:
                samplerate = float(self.samplerate.get())
                if samplerate > 1000 or samplerate < 0.1:
                    print ("samplerate must be a positive number greater than 0.1 and smaller than 1000.")
                    raise ValueError("")
                print(f"samplerate: {samplerate} /s")
            except ValueError:
                print("Invalid input for samplerate time. Using default value: 2 /s")
                samplerate = 2

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

            parameter.append(startfrequenzy)
            parameter.append(stopfrequenzy)
            parameter.append(amplitude)
            parameter.append(sweeptype)
            parameter.append(samples)
            parameter.append(samplerate)
            parameter.append(self.master.hardwareframe.scope.get())
            parameter.append(self.master.hardwareframe.signalgenerator.get())
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
            measure(parameter)


        self.start_button = customtkinter.CTkButton(self, text="Start", command=start)
        self.start_button.grid(row=7, column=0, padx=10, pady=5)
        self.start_button.grid(columnspan=2)

class termianlframe(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=0) 
        
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.textbox.grid(rowspan=2)

        def clear():
            self.textbox.delete("0.0", "end")

        self.clear_button = customtkinter.CTkButton(self, text="Clear", command=clear)
        self.clear_button.grid(row=0, column=1, padx=10, pady=5,sticky="nsew")

        self.export_csv_button = customtkinter.CTkButton(self, text="Export CSV", command=clear)
        self.export_csv_button.grid(row=1, column=1, padx=10, pady=5,sticky="nsew")

        sys.stdout = self

    def write(self, message):
        self.textbox.insert("end", message)
        self.textbox.see("end")

    def flush(self):
        pass  
        



class outputframe(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create a combined plot with two y-axes
        fig, ax1 = plt.subplots(figsize=(5, 6), dpi=100)

        # First plot (left y-axis)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        ax1.plot(x, y1, 'b-', label="H(f)")
        ax1.set_xscale('log')
        ax1.set_xlabel("f")
        ax1.set_yscale('log')
        ax1.set_ylabel("|H(f)|/dB", color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.grid(True, linestyle='--')

        # Second plot (right y-axis)
        ax2 = ax1.twinx()
        y2 = np.cos(x)
        ax2.plot(x, y2, 'r-', label="phi(f)")
        ax2.set_ylim(-90, 90)
        ax2.set_ylabel("phi(f)/deg", color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        fig.tight_layout()  # Adjust spacing to prevent overlap

        # Matplotlib-Canvas erzeugen und ins Frame einbetten
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bode-Plot")
        self.geometry("1200x800")  # Set initial window size
        self.resizable(True, True)  # Allow resizing

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
 
        self.hardwareframe = hardwareframe(self)
        self.hardwareframe.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.settingframe = settingframe(self)
        self.settingframe.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        def create_Output():
            self.outputframe = outputframe(self)
            self.outputframe.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
            self.outputframe.grid(rowspan=2)
  
        self.termianlframe = termianlframe(self)
        self.termianlframe.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.termianlframe.grid(columnspan=2)


if __name__ == "__main__":
    app = App()
    app.mainloop()
