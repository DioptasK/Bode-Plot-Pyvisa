import customtkinter

import sys
sys.path.append('/home/user/Documents/Studium/pyvisa')

from visa_py import resources


class device_input(customtkinter.CTkFrame):
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
            devices = resources.get_connected_devices()
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
            result = resources.check_connection(scope_id, functiongenerator_id)
            self.textbox.insert("end", "Connection check completed.\n")
            if  not result:
                self.textbox.insert("end", "Connection failed.\n")

        self.refresh_button = customtkinter.CTkButton(self, text="Get Devices", command=refresh)
        self.refresh_button.grid(row=2, column=0,padx=10, pady=5)

        self.check_connection_button = customtkinter.CTkButton(self, text="Check Connection", command=check)
        self.check_connection_button.grid(row=2, column=1,padx=10, pady=5)
