import matplotlib.pyplot as plt

# Erstellen eines Gitters von c-Werten
epsilon = 1e-1
iterations = 10
width, height = 800, 800
xmin, xmax, ymin, ymax = -2, 2, -2, 2

scale_factor_x = ((xmax - xmin) / width)
scale_factor_y = ((ymax - ymin) / height)

converged = [[0 for _ in range(width)] for _ in range(height)]
for y in range(height):
    scale_y = ymin + y * scale_factor_y
    for x in range(width):
        scale_x = xmin + x * scale_factor_x

        c = scale_x + scale_y * 1j
        z = c
        for i in range(1, iterations):
            z = z**2 + c
            if abs(z) > 2:
                break

            if abs(z - c) < epsilon:
                converged[y][x] = i
                break

#            converged[y][x] = i

print(0, max(max(converged)))

# Visualisierung
plt.imshow(converged, extent=(xmin, xmax, ymin, ymax))
plt.xlabel('Realteil')
plt.ylabel('Imaginärteil')
plt.title('Mandelbrot-Set')
plt.show()
