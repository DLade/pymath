import matplotlib.pyplot as plt
from math import sqrt

# Erstellen eines Gitters von c-Werten
iterations = 1000
width, height = 800, 800
xmin, xmax, ymin, ymax = -2.0, 1.0, -sqrt(2.0), sqrt(2.0)

converged = [[0 for _ in range(width)] for _ in range(height)]
for y in range(height):
    scale_y = ymin + y * (ymax - ymin) / height
    for x in range(width):
        scale_x = xmin + x * (xmax - xmin) / width

        c = scale_x + scale_y * 1j
        z, sum_z = c, 0j
        for i in range(iterations):
            z = z**2 + c

            abs_z = abs(z)
            if abs_z >= 2:
                converged[y][x] = 50 if abs_z > 50 else abs_z
                break

            sum_z += z
            if i >= 10:
                mean_z = abs(sum_z / (i + 1))
                if mean_z < 1.0:
                    converged[y][x] = 0
                    break


# Visualisierung
plt.imshow(converged, extent=(xmin, xmax, ymin, ymax), cmap='grey')
plt.xlabel('Realteil')
plt.ylabel('Imaginärteil')
plt.title('Mandelbrot-Set')
plt.show()
