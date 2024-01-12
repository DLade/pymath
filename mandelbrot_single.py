iterations = 100
x, y = -1.414, 0.0


def main():
    c = x + y * 1j
    z = 0j
    for i in range(iterations):
        z = z ** 2 + c

        if abs(z) > 2:
            break


if __name__ == '__main__':
    main()
