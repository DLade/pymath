from PIL import Image, ImageDraw
from PIL.ImagePalette import ImagePalette
from matplotlib import colormaps as cmaps
from matplotlib import pyplot as plt


def get_palette(colormap_name: str) -> ImagePalette:
    """
    Converts a colormap to a palette.

    :param colormap_name: https://matplotlib.org/stable/gallery/color/colormap_reference.html
    :return: palette
    """
    # Create a Pillow palette directly from the flattened list comprehension
    return ImagePalette(mode="RGB", palette=[
        int(c * 255) for i in range(256) for c in cmaps.get_cmap(colormap_name)(i)[:3]
    ])


def mandelbrot(draw_area, x_min, x_max, y_min, y_max, num_iterations, z0 = 0j):
    width, height = draw_area.im.size

    for y in range(height):
        scale_y = y_min + y * (y_max - y_min) / height
        for x in range(width):
            scale_x = x_min + x * (x_max - x_min) / width

            c = scale_x + scale_y * 1j
            z = z0
            for i in range(num_iterations):
                z = z ** 2 + c

                abs_z = abs(z)
                if abs_z >= 2:
                    draw_area.point((x, y), int(abs_z * 240 / 6))
                    break


def julia(draw_area, x_min, x_max, y_min, y_max, num_iterations, c0 = 0j):
    width, height = draw_area.im.size

    for y in range(height):
        scale_y = y_min + y * (y_max - y_min) / height
        for x in range(width):
            scale_x = x_min + x * (x_max - x_min) / width

            c = c0
            z = scale_x + scale_y * 1j
            for i in range(num_iterations):
                z = z ** 2 + c

                abs_z = abs(z)
                if abs_z >= 2:
                    draw_area.point((x, y), int(abs_z * 240 / 6))
                    break


if __name__ == '__main__':
    source_image = Image.new(mode='P', size=(1000, 800))  # create the Image of size 1 pixel
    source_image.putpalette(get_palette('Blues_r'))

    # mandelbrot(ImageDraw.Draw(source_image), -2.0, 1.0, -1.5, 1.5, 200)
    julia(ImageDraw.Draw(source_image), -1.6, 1.6, -1.0, 1.0, 400, -0.7 + 0.27015j)

    # Visualisierung
    rgb_image = source_image.convert('RGB')
    rgb_image.save('fractal.png')

    plt.imshow(rgb_image)
    plt.show()
