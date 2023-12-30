import numpy as np
import matplotlib.pyplot as plt

# Erstellen eines Gitters von c-Werten
breite, höhe = 800, 800
xmin, xmax, ymin, ymax = -2, 2, -2, 2
x = np.linspace(xmin, xmax, breite)
y = np.linspace(ymin, ymax, höhe)
C = x[:, np.newaxis] + 1j * y[np.newaxis, :]

# Initialisierung von z und der Iterationsanzahl
Z = np.zeros_like(C)
iterationen = 50
divergiert = np.zeros(C.shape, dtype=bool)

# Iteration
for i in range(iterationen):
    Z = Z**2 + C
    divergiert |= np.abs(Z) > 2

# Visualisierung
plt.imshow(divergiert, extent=(xmin, xmax, ymin, ymax))
plt.xlabel('Realteil')
plt.ylabel('Imaginärteil')
plt.title('Mandelbrot-Set')
plt.show()
