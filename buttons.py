
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

import pickle
import glob
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

fig = plt.figure(figsize=(18, 6))
ICON_PLAY =  plt.imread("./image/1.png")
ICON_PAUSE = plt.imread("./image/2.png")

def play(event):
    image_axes.imshow(ICON_PLAY)
    fig.canvas.draw_idle()

image_axes = plt.axes([0.0, 0.0, 1.0, 1.0])
image_axes.imshow(ICON_PAUSE)
button_axes = plt.axes([0.5,0.05,0.08,0.05])
start_button = Button(button_axes, "hhh")
start_button.on_clicked(play)
plt.show()