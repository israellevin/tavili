#!/usr/bin/python

import matplotlib.image
img = matplotlib.image.imread('map.png')

minlat, maxlat = 32.0517, 32.1042
minlng, maxlng = 34.7573, 34.8199
extent = [minlng, maxlng, minlat, maxlat]

from matplotlib import pyplot as plt
plt.imshow(img, extent=extent)

from random import uniform
def randlatlng():
    return uniform(minlat, maxlat), uniform(minlng, maxlng)

import numpy as np
samples = 50
x = np.linspace(minlng, maxlng, samples)
y = np.linspace(maxlat, minlat, samples)
x, y = np.meshgrid(x, y)
color = np.zeros(x.shape)

# More controlled, smooth heatmap
from matplotlib import mlab
color -= mlab.bivariate_normal(x, y, 0.001, 0.001, minlng, minlat)

color += mlab.bivariate_normal(x, y, 0.001, 0.001, maxlng, maxlat)

color += mlab.bivariate_normal(x, y, 0.001, 0.001, 34.78981, 32.08687)

import matplotlib.colors
cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    name='coldhot',
    colors = [
        (0, 0, 0.7, 1),
        (0, 0, 1, 1),
        (0, 1, 1, 0.5),
        (1, 1, 1, 0.5),
        (1, 1, 0, 0.5),
        (1, 0, 0, 1),
        (0.7, 0, 0, 1)
    ], N=700
)

plt.imshow(color, cmap=cmap, alpha=0.5, extent=extent)

cb = plt.colorbar()
cb.set_alpha(1)
cb.draw_all()

from sys import path
path.append('../')
from router import Router
cnt = 0
while True:
    print(cnt),
    r = Router(randlatlng(), randlatlng())
    p = (r.getPath())
    xs, ys = [x for x, y in p], [y for x, y in p]
    if len(xs) > 1:
        plt.plot(ys, xs, alpha=0.5)
        plt.pause(0.1)
        cnt += 1
        if 50 == cnt: break

plt.show()
