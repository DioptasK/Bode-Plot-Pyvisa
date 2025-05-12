import os
from datetime import datetime
import numpy as np
from tkinter import filedialog

def choose_location():
    filepath = filedialog.askdirectory(
        title="Choose directory to save the file"
    )
    if filepath:
        print(f"Chosen filepath: {filepath}")
        return filepath


def export_csv(input, parameters):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bodeplot_{parameters[0]}Hz_{parameters[1]}Hz_{parameters[2]}Vpp_{parameters[3]}_{parameters[4]}samples_{timestamp}.csv"
    path = choose_location()
    if path:
        filepath = os.path.join(path, filename)
    else:
        filepath = os.path.join(os.getcwd(), filename)
        print("Using working directory as location to save")

    try:
        np.savetxt(filepath, input, delimiter=",", header="RMS_1,RMS_2,Frequency,Phase", comments="")
        print(f"Data successfully exported to {filepath}")
        return True
    except Exception as e:
        print(f"Failed to export data: {e}")
        return False


if __name__ == "__main__":
    erg = []
    for i in range(200):
        result = [2, pow(3.7, i), 20000 * i, i * 10]
        erg.append(result)
    results = np.array(erg)
    param=[20,20000,1.4,"lin",200]
    export_csv(results,param)
