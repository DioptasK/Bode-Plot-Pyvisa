import customtkinter

from visa_py import resources


class device_input(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=2)
        self.grid_rowconfigure(4, weight=2)
        self.grid_rowconfigure(5, weight=1)


        self.scope = customtkinter.CTkEntry(self, placeholder_text="Scope")
        self.scope.grid(row=1,column=0,padx=10, pady=5)
        self.scope_label = customtkinter.CTkLabel(self, text="Scope-ID", font=("Arial", -16))
        self.scope_label.grid(row=0, column=0, padx=10, pady=5)

        self.signalgenerator = customtkinter.CTkEntry(self, placeholder_text="Signalgenerator")
        self.signalgenerator.grid(row=1,column=1,padx=10, pady=5)
        self.signalgenerator_label = customtkinter.CTkLabel(self, text="Signalgenerator-ID", font=("Arial", -16))
        self.signalgenerator_label.grid(row=0, column=1, padx=10, pady=5)

        self.scope_manufacturer = customtkinter.CTkOptionMenu(self, values=["Siglent", "Rigol","Keysight", "Agilent"])#TODO: Implement not_Visa devices
        self.scope_manufacturer.grid(row=2, column=0, padx=10, pady=5)

        self.signalgenerator_manufacturer = customtkinter.CTkOptionMenu(self, values=["Siglent", "Rigol", "Keysight", "Agilent"])
        self.signalgenerator_manufacturer.grid(row=2, column=1, padx=10, pady=5)
        
        def refresh():
            devices = resources.get_connected_devices()
            if len(devices) == 0:
                self.textbox.insert("end", "No devices found.\n")
            else:
                for device in devices:
                    self.textbox.insert("end", device + "\n")
            self.textbox.see("end")
        
        def check():
            self.textbox.insert("end", "Checking connection...\n")
            scope_id = self.scope.get()
            functiongenerator_id = self.signalgenerator.get()
            if not scope_id:
                self.textbox.insert("end", "No Scope ID given.\n")
                self.textbox.see("end")
                return
            if not functiongenerator_id:
                self.textbox.insert("end", "No Fuctiongenerator ID given\n")
                self.textbox.see("end")
            if not scope_id and not functiongenerator_id:
                self.textbox.insert("end", "No Scope ID and no Functiongenerator ID given\n")
                self.textbox.see("end")
                return
            
            result = resources.check_connection(scope_id, functiongenerator_id)
            self.textbox.insert("end", "Connection check completed.\n")
            if  not result:
                self.textbox.insert("end", "Connection failed.\n")
                self.textbox.see("end")
            else:
                self.textbox.insert("end", "Connected to:\n")
                for item in result:
                    self.textbox.insert("end", f"{item}")
                    
                self.textbox.insert("end", "Connection successful.\n")
                self.textbox.see("end")

        self.refresh_button = customtkinter.CTkButton(self, text="Get Devices", command=refresh)
        self.refresh_button.grid(row=3, column=0,padx=10, pady=5)

        self.check_connection_button = customtkinter.CTkButton(self, text="Check Connection", command=check)
        self.check_connection_button.grid(row=3, column=1,padx=10, pady=5)

        self.probe_1 = customtkinter.CTkOptionMenu(self, values=["10", "1"])
        self.probe_1.grid(row=4, column=0,padx=10,pady=5)

        self.probe_2 = customtkinter.CTkOptionMenu(self, values=["10", "1"])
        self.probe_2.grid(row=4, column=1,padx=10,pady=5)

        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=5, column=0,rowspan=1, columnspan=2, padx=10, pady=5, sticky="nsew")