import random
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from PIL.ImagePalette import ImagePalette
from matplotlib import colormaps as cmaps

WIDTH = 2 ** 10
HEIGHT = 2 ** 10

BOTTOM_LEVEL = 0.15
TOP_LEVEL = 1

RND = random.Random(6)  # 2, 6, 389457


# see: https://janert.org/blog/2022/the-diamond-square-algorithm-for-terrain-generation/
# Thx ;-)


def clamp(value, min_value, max_value):
    return min_value if value < min_value else max_value if value > max_value else value


def average(data, x, y, center_x, center_y, offsets):
    data_width = data.shape[1] - 1
    data_height = data.shape[0] - 1

    res = 0
    for offset_y, offset_x in offsets:
        res += data[clamp(y + offset_y * center_y, 0, data_height), clamp(x + offset_x * center_x, 0, data_width)]
    return res / 4.0


def single_diamond_square_step(data, cell_width, cell_height, roughness):
    # w is the dist from one "new" cell to the next
    # v is the dist from a "new" cell to the nbs to average over

    data_width = data.shape[1]
    data_height = data.shape[0]
    center_x = cell_width // 2
    center_y = cell_height // 2

    # offsets:
    diamond = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    square = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    def update_cell(idx_x, idx_y, shape):
        a = average(data, idx_x, idx_y, center_x, center_y, shape)
        r = RND.uniform(-roughness, roughness)

        return clamp(a + r, 0.0, 1.0)

    for y in range(center_y, data_height, cell_height):
        for x in range(center_x, data_width, cell_width):
            data[y, x] = update_cell(x, y, diamond)
            data[y, x - center_x] = update_cell(x - center_x, y, square)
            data[y - center_y, x] = update_cell(x, y - center_y, square)


def make_terrain(width, height, roughness_factor):
    # Returns an n-by-n landscape using the Diamond-Square algorithm, using
    # roughness delta ds (0..1). bdry is an averaging fct, including the
    # bdry conditions: fixed() or periodic(). n must be 2**k, k integer.
    data = np.zeros(width * height).reshape(height, width)

    roughness = 1.0
    while width > 1 or height > 1:
        single_diamond_square_step(data, width, height, roughness)

        width //= 2 if width > 1 else 1
        height //= 2 if height > 1 else 1
        roughness *= roughness_factor

    return data


def get_palette(colormap_name):
    # Create a Pillow palette directly from the flattened list comprehension
    return ImagePalette(mode="RGB", palette=[
        int(c * 255) for i in range(256) for c in cmaps.get_cmap(colormap_name)(i)[:3]
    ])


def main():
    source_image = Image.new(mode='P', size=(WIDTH, HEIGHT))  # create the Image of size 1 pixel
    draw_area = ImageDraw.Draw(source_image)

    source_image.putpalette(get_palette('gist_earth'))

    factor = 2 ** 1
    roughness = 0.7  # Roughness delta, 0 < ds <= 1 : smaller ds => smoother results

    time_av1, time_av2 = (0, 0)
    # loop
    time0 = time.thread_time_ns()
    terrain = make_terrain(WIDTH // factor, HEIGHT // factor, roughness)

    time1 = time.thread_time_ns()
    for y in range(0, HEIGHT // factor):
        for x in range(0, WIDTH // factor):
            level = clamp(terrain[y, x], BOTTOM_LEVEL, TOP_LEVEL)
            draw_area.rectangle(xy=(x * factor, y * factor, (x + 1) * factor, (y + 1) * factor), fill=int(level * 255))

    time2 = time.thread_time_ns()

    time_av1 = (time_av1 + (time1 - time0)) / 2
    time_av2 = (time_av2 + (time2 - time1)) / 2
    # loop end

    print(f"{int(time_av1 / 1000000)} + {int(time_av2 / 1000000)} = {int((time_av1 + time_av2) / 1000000)}")

    image_rgb = source_image.convert('RGB')
    image_rgb.save('terrain_1.png')
    image_rgb.filter(ImageFilter.GaussianBlur(2)).save('terrain_1_blurred.png')


if __name__ == '__main__':
    main()
