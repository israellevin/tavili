#!/usr/bin/python3

import numpy as np
from scipy.interpolate import griddata

coords = [
    [0, 0],
    [0, 100],
    [100, 0],
    [100, 100],
    [.5, .1],
    [1, 1],
    [40, 31],
    [1, 1],
]
x, y= [x for x, y in coords], [y for x, y in coords]
minlng, maxlng = min(x), max(x)
minlat, maxlat = min(y), max(y)
extent = [minlng, maxlng, minlat, maxlat]

z = np.random.randn(len(coords)) + 10

xi = np.linspace(minlng, maxlng, 300)
yi = np.linspace(minlat, maxlat, 300)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

from matplotlib import pyplot as plt, image

plt.contourf(xi, yi, zi, 15, extent=extent, cmap=plt.cm.spectral, alpha=0.5)
plt.imshow(image.imread('map.png'), extent=extent)

cb = plt.colorbar()
cb.set_alpha(1)
cb.draw_all()

plt.show()
