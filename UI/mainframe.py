import customtkinter

import terminal
import output
import device_input
import settings

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
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
 
        self.hardwareframe = device_input.device_input(self)
        self.hardwareframe.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        
        
        self.outputframe = output.output(self)
        self.outputframe.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.outputframe.grid(rowspan=2)

        self.settingframe = settings.settings(self)
        self.settingframe.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
  
        self.terminalframe = terminal.terminal(self)
        self.terminalframe.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.terminalframe.grid(columnspan=2)


if __name__ == "__main__":
    app = mainframe()
    app.mainloop()