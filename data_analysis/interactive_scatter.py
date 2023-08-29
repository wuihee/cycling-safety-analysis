import os
import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt


def press_callback(event):
    event.canvas.figure.text(event.xdata, event.ydata, "<- clicked here")


def release_callback(event):
    event.canvas.figure.show()


(figure, axes) = plt.subplots()
press_conn_id = figure.canvas.mpl_connect("button_press_event", press_callback)
release_conn_id = figure.canvas.mpl_connect("button_release_event", release_callback)
plt.show()
