import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor

def plot(results):
    # Optional: Beispiel-Daten für Tests
    # erg = []
    # for i in range(20):
    #     result = [2, pow(3.7, i), 20000 * i, i * 10]
    #     erg.append(result)
    # results = np.array(erg)

    frequencies = results[:, 2]
    rms1 = results[:, 0]
    rms2 = results[:, 1]
    phase = results[:, 3]

    # Erstelle das Plot-Fenster
    fig, ax1 = plt.subplots(figsize=(5, 6), dpi=100)

    # Linke y-Achse: Betrag |H(f)| in dB
    magnitude = 20 * np.log10(rms2 / rms1)
    line1, = ax1.plot(frequencies, magnitude, 'b-', label="|H(f)|")
    ax1.set_xscale('log')
    ax1.set_xlabel("f (Hz)")
    ax1.set_ylabel("|H(f)| / dB", color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True, linestyle='--')

    # Rechte y-Achse: Phase
    ax2 = ax1.twinx()
    line2, = ax2.plot(frequencies, phase, 'r-', label="φ(f)")
    ax2.set_ylim(-180, 180)
    ax2.set_ylabel("φ(f) / deg", color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Cursor-Funktionalität hinzufügen
    cursor = Cursor(ax1, useblit=True, color='green', linewidth=1)

    fig.tight_layout()
    plt.show()