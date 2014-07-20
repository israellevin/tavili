#!/usr/bin/python3

import numpy as np

x = y = np.arange(0, 100)
minlng, maxlng = min(x), max(x)
minlat, maxlat = min(y), max(y)
x, y = np.meshgrid(x, y)

color = np.zeros(x.shape)

from matplotlib.mlab import bivariate_normal
def bomb(lat, lng, width=10, height=10):
    return bivariate_normal(x, y, width, height, lat, lng)

color += bomb(45, 50, 12, 7)
color += bomb(55, 60, 15, 5)
color -= bomb(65, 67, 15, 5)
color -= bomb(70, 82, 5, 15)

from matplotlib import pyplot as plt, image

colorful = plt.contourf(x, y, color, 10, alpha=0.3, cmap=plt.cm.spectral)
contours = plt.contour(colorful, levels=colorful.levels[::2], hold='on')

extent = [minlng, maxlng, minlat, maxlat]
plt.imshow(image.imread('map.png'), extent=extent)

cb = plt.colorbar()
cb.set_alpha(1)
cb.draw_all()

plt.show()
