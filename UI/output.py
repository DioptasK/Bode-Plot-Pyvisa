import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class output(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        

    def plot(self, results):
        # Create a combined plot with two y-axes
        fig, ax1 = plt.subplots(figsize=(5, 6), dpi=100)

        # First plot (left y-axis)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        ax1.plot(x, y1, 'b-', label="H(f)")
        ax1.set_xscale('log')
        ax1.set_xlabel("f")
        ax1.set_yscale('log')
        ax1.set_ylabel("|H(f)|/dB", color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.grid(True, linestyle='--')

        # Second plot (right y-axis)
        ax2 = ax1.twinx()
        y2 = np.cos(x)
        ax2.plot(x, y2, 'r-', label="phi(f)")
        ax2.set_ylim(-90, 90)
        ax2.set_ylabel("phi(f)/deg", color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        fig.tight_layout()  # Adjust spacing to prevent overlap

        # Matplotlib-Canvas erzeugen und ins Frame einbetten
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
