import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

os.chdir(os.path.dirname(os.path.realpath(__file__)))


def on_pick(event):
    print("hi")
    img = np.asarray(Image.open(pathlib.Path("./data/screenshots/Taxi_14-55-22.jpg")))
    axes[1].imshow(img)
    plt.draw()


x = [1, 2, 3]
y = [3, 1, 2]

fig, axes = plt.subplots(2, 1)
axes[0].scatter(x, y, picker=True)
axes[1].axis("off")

fig.canvas.mpl_connect("pick_event", on_pick)
plt.show()
