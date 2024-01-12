from PIL import Image, ImageDraw
from PIL.ImagePalette import ImagePalette
from matplotlib import colormaps as cmaps
from matplotlib import pyplot as plt

iterations = 200
WIDTH, HEIGHT = 800, 800
x_min, x_max, y_min, y_max = -1.5, 1.5, -1.5, 1.5


def get_palette(colormap_name):
    # Create a Pillow palette directly from the flattened list comprehension
    return ImagePalette(mode="RGB", palette=[
        int(c * 255) for i in range(256) for c in cmaps.get_cmap(colormap_name)(i)[:3]
    ])


def main():
    # Erstellen eines Gitters von c-Werten
    source_image = Image.new(mode='P', size=(WIDTH, HEIGHT))  # create the Image of size 1 pixel
    draw_area = ImageDraw.Draw(source_image)

    source_image.putpalette(get_palette('grey'))

    for y in range(HEIGHT):
        scale_y = y_min + y * (y_max - y_min) / HEIGHT
        for x in range(WIDTH):
            scale_x = x_min + x * (x_max - x_min) / WIDTH

            c = scale_x + scale_y * 1j
            z = 0j
            for i in range(iterations):
                z = z ** 2 + c

                abs_z = abs(z)
                if abs_z >= 2:
                    draw_area.point((x, y), int(abs_z * 240 / 6))
                    break

    # Visualisierung
    plt.imshow(source_image.convert('RGB'))
    plt.show()


if __name__ == '__main__':
    main()
