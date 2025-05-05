import customtkinter
import sys
from datetime import datetime
import os


class terminal(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=10) 
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)  
        
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=0, column=0, columnspan = 2, padx=10, pady=5, sticky="nsew")

        def clear():
            self.textbox.delete("0.0", "end")


        def export():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bodeplot__{timestamp}.csv"
            filepath = os.path.join(os.getcwd(), filename)
            with open(filepath, "x") as file:
                file.write(self.textbox.get("0.0", "end"))
                file.close()
            self.textbox.insert("end", "Exported CSV to {filename}\n")
            self.textbox.see("end")

        self.clear_button = customtkinter.CTkButton(self, text="Clear", command=clear)
        self.clear_button.grid(row=1, column=0, padx=10, pady=5,sticky="nsew")

        self.export_csv_button = customtkinter.CTkButton(self, text="Export CSV", command=export)
        self.export_csv_button.grid(row=1, column=1, padx=10, pady=5,sticky="nsew")
        self.export_csv_button.configure(state = "disabled")

        self.progressbar = customtkinter.CTkProgressBar(self,orientation="horizontal")
        self.progressbar.grid(row=2, column = 0, columnspan= 2, padx=10,pady=5, sticky = "nsew")
        self.progressbar.configure(mode="indeterminate")
        self.progressbar.set(0)

        sys.stdout = self

    def write(self, message):
        self.textbox.insert("end", message)
        self.textbox.see("end")

    def flush(self):
        self.textbox.update_idletasks()  
        