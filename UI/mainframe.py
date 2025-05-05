import customtkinter
import threading

import numpy as np

from UI import terminal
from UI import device_input
from UI import settings

customtkinter.set_appearance_mode("light")  # Set dark mode
customtkinter.set_default_color_theme("green")  # Set color theme

class mainframe(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bode-Plot")
        self.geometry("1200x800")  # Set initial window size
        self.resizable(True, True)  # Allow resizing

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)

        self.results_for_export = np.array([])
        self.parameters = []
 
        self.terminalframe = terminal.terminal(self)
        self.terminalframe.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.terminalframe.grid(rowspan=2)

        self.hardwareframe = device_input.device_input(self)
        self.hardwareframe.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.settingframe = settings.settings(self)
        self.settingframe.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Handler für das Schließen des Fensters."""
        print("Programm wird beendet...")

        # Threads stoppen (falls vorhanden)
        for thread in threading.enumerate():
            if thread is not threading.main_thread():
                print(f"Beende Thread: {thread.name}")
                thread.join(timeout=1)

        self.destroy()  # Beendet das Fenster
        exit(0)  # Beendet den Python-Prozess


# if __name__ == "__main__":
#     app = mainframe()
#     app.mainloop()