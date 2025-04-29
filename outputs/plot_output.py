import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor, MultiCursor

def plot(results):
    frequencies = results[:, 2]
    rms1 = results[:, 0]
    rms2 = results[:, 1]
    phase = results[:, 3]

    magnitude = 20 * np.log10(rms2 / rms1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8), dpi=100, sharex=True)

    ax1.plot(frequencies, magnitude, 'b-', label="|H(f)|")
    ax1.set_xscale('log')
    ax1.set_xlabel("f (Hz)")
    ax1.set_ylabel("|H(f)| / dB", color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True, linestyle='--')
    ax1.set_title("Magnitude")

    ax2.plot(frequencies, phase, 'r-', label="φ(f)")
    ax2.set_xscale('log')
    ax2.set_xlabel("f (Hz)")
    ax2.set_ylabel("φ(f) / deg", color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.set_ylim(-180, 180)
    ax2.grid(True, linestyle='--')
    ax2.set_title("Phase")

    multi = MultiCursor(fig.canvas, (ax1, ax2), color='black', lw=1, 
                    horizOn=False, vertOn=True) 

    # Layout anpassen und anzeigen
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
        # Optional: Beispiel-Daten für Tests
    erg = []
    for i in range(20):
        result = [2, pow(3.7, i), 20000 * i, i * 10]
        erg.append(result)
    results = np.array(erg)
    plot(results)