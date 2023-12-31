# Erstellen eines Gitters von c-Werten
epsilon = 1e-4
iterations = 100
x, y = -1.414, 0.0

c = x + y * 1j
z, sum_z = c, 0j
all_z = [0j for _ in range(iterations)]
for i in range(iterations):
    z = z ** 2 + c
    sum_z += z
    print("mean '{}'".format(abs(sum_z / (i + 1))))
    if abs(z) > 2:
        break

