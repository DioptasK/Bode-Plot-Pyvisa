import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import MultiCursor, Cursor
from matplotlib.backend_bases import MouseEvent

class SnappingCursor:
    """
    A cross-hair cursor that snaps to the data point of a line, which is
    closest to the *x* position of the cursor.

    For simplicity, this assumes that *x* values of the data are sorted.
    """
    def __init__(self, ax, line):
        self.ax = ax
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        self.x, self.y = line.get_data()
        self._last_index = None
        # text location in axes coords
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            index = min(np.searchsorted(self.x, x), len(self.x) - 1)
            if index == self._last_index:
                return  # still on the same data point. Nothing to do.
            self._last_index = index
            x = self.x[index]
            y = self.y[index]
            # update the line positions
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([x])
            self.text.set_text(f'x={x:1.2f}, y={y:1.2f}')
            self.ax.figure.canvas.draw()

def plot(results):

    rms1 = results[:, 0]
    rms1 = np.array(rms1, dtype=float)
    rms2 = results[:, 1]
    rms2 = np.array(rms2, dtype=float)
    frequencies = results[:, 2]
    phase = results[:, 3]

    magnitude = 20 * np.log10((rms2) / (rms1))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8), dpi=100, sharex=True)

    line1, = ax1.plot(frequencies, magnitude, 'b-', label="|H(f)|")
    ax1.set_xscale('log')
    ax1.set_xlabel("f (Hz)")
    ax1.set_ylabel("|H(f)| / dB", color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True, linestyle='--')
    ax1.set_title("Magnitude")

    line2, = ax2.plot(frequencies, phase, 'r-', label="φ(f)")
    ax2.set_xscale('log')
    ax2.set_xlabel("f (Hz)")
    ax2.set_ylabel("φ(f) / deg", color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.set_ylim(-180, 180)
    ax2.grid(True, linestyle='--')
    ax2.set_title("Phase")

    snap_cursor1 = SnappingCursor(ax1, line1)
    fig.canvas.mpl_connect('motion_notify_event', snap_cursor1.on_mouse_move)

    snap_cursor2 = SnappingCursor(ax2, line2)
    fig.canvas.mpl_connect('motion_notify_event', snap_cursor2.on_mouse_move)

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    erg = []
    for i in range(2200):
        result = [2, i*i+1, 200 * i, i/10 ]
        erg.append(result)
    results = np.array(erg)
    plot(results)