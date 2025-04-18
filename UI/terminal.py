import customtkinter
import sys



class terminal(customtkinter.CTkFrame):
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

        #TODO: implement export to png anstatt csv
        def export_csv():
            with open("output.csv", "w") as file:
                file.write(self.textbox.get("0.0", "end"))
                file.close()
            self.textbox.insert("end", "Data exported to output.csv\n")
            self.textbox.see("end")

        self.clear_button = customtkinter.CTkButton(self, text="Clear", command=clear)
        self.clear_button.grid(row=0, column=1, padx=10, pady=5,sticky="nsew")

        self.export_csv_button = customtkinter.CTkButton(self, text="Export CSV", command=export_csv)
        self.export_csv_button.grid(row=1, column=1, padx=10, pady=5,sticky="nsew")

        sys.stdout = self

    def write(self, message):
        self.textbox.insert("end", message)
        self.textbox.see("end")

    def flush(self):
        self.textbox.update_idletasks()  
        