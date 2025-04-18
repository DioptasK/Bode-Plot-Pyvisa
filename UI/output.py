import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class output(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        

    def plot(self, results):

        #print(results)
        
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
            del self.canvas

        # Create a combined plot with two y-axes
        fig, ax1 = plt.subplots(figsize=(5, 6), dpi=100)

        frequencies = results[:, 2]
        rms1 = results[:, 0]
        rms2 = results[:, 1]
        phase = results[:, 3]

        # First plot (left y-axis)
        magnitude = 20 * np.log10(rms2 / rms1)  # Calculate |H(f)| in dB
        ax1.plot(frequencies, magnitude, 'b-', label="H(f)")
        ax1.set_xscale('log')
        ax1.set_xlabel("f (Hz)")
        ax1.set_ylabel("|H(f)|/dB", color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.grid(True, linestyle='--')

        # Second plot (right y-axis)
        ax2 = ax1.twinx()
        ax2.plot(frequencies, phase, 'r-', label="phi(f)")
        ax2.set_ylim(-180, 180)
        ax2.set_ylabel("phi(f)/deg", color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        fig.tight_layout()


        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
