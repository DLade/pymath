import matplotlib.pyplot as plt

# Erstellen eines Gitters von c-Werten
width, height = 800, 800
xmin, xmax, ymin, ymax = -2, 2, -2, 2


def scale_x(x):
    return xmin + ((xmax - xmin) * x / width)


def scale_y(y):
    return ymin + ((ymax - ymin) * y / width)


iterations = 10
divergiert = [[False for _ in range(width)] for _ in range(height)]
for y in range(height):
    for x in range(width):
        c = scale_x(x) + scale_y(y) * 1j
        z = c
        for i in range(iterations):
            z = z**2 + c
            if abs(z) > 2:
                divergiert[y][x] = True
                break

# Visualisierung
plt.imshow(divergiert, extent=(xmin, xmax, ymin, ymax))
plt.xlabel('Realteil')
plt.ylabel('Imaginärteil')
plt.title('Mandelbrot-Set')
plt.show()
