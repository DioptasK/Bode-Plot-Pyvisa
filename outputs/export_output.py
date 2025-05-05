import os
from datetime import datetime
import numpy as np

def export_csv(input, parameters):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bodeplot_{parameters[0]}Hz_{parameters[1]}Hz_{parameters[2]}Vpp_{parameters[3]}_{parameters[4]}samples_{timestamp}.csv"
    filepath = os.path.join(os.getcwd(), filename)

    try:
        np.savetxt(filepath, input, delimiter=",", header="RMS_1,RMS_2,Frequency,Phase", comments="")
        print(f"Data successfully exported to {filepath}")
    except Exception as e:
        print(f"Failed to export data: {e}")


if __name__ == "__main__":
        # Optional: Beispiel-Daten für Tests
    erg = []
    for i in range(200):
        result = [2, pow(3.7, i), 20000 * i, i * 10]
        erg.append(result)
    results = np.array(erg)
    param=[20,20000,1.4,"lin",200]
    export_csv(results,param)