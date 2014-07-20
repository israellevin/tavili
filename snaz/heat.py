#!/usr/bin/python3

import numpy as np

x = y = np.arange(0, 100)
minlng, maxlng = min(x), max(x)
minlat, maxlat = min(y), max(y)
x, y = np.meshgrid(x, y)


from matplotlib.mlab import bivariate_normal
def bomb(lat, lng, width=10, height=10):
    return bivariate_normal(x, y, width, height, lat, lng)

colors = []
for i in range(10):
    color = np.zeros(x.shape)
    color += bomb(i * 10, i * 7, 5, 15)
    color -= bomb(i * 2, 50 - i * 5 , 15, 5)
    colors.append(color)

from matplotlib import pyplot as plt, image
plt.ion()
extent = [minlng, maxlng, minlat, maxlat]

plt.imshow(image.imread('map.png'), extent=extent)
cb = plt.colorbar()
cb.set_alpha(1)
cb.draw_all()

while True:
    for color in colors:
        plt.imshow(image.imread('map.png'), extent=extent)

        colorful = plt.contourf(x, y, color, 10, alpha=0.3, cmap=plt.cm.spectral)
        plt.contour(colorful, levels=colorful.levels[::2], hold='on')

        plt.pause(0.01)
        plt.cla()

plt.ioff()
plt.show()
