from .interpolation import interpolation
from dip import *
import math

class Geometric:
    def __init__(self):
        self.interpolator = interpolation()

    def forward_rotate(self, image, theta):
        height, width = len(image), len(image[0])
        rotated_image = [[0] * width for _ in range(height)]

        for y in range(height):
            for x in range(width):
                new_x = int((x - width / 2) * math.cos(theta) - (y - height / 2) * math.sin(theta) + width / 2)
                new_y = int((x - width / 2) * math.sin(theta) + (y - height / 2) * math.cos(theta) + height / 2)

                if 0 <= new_x < width and 0 <= new_y < height:
                    rotated_image[new_y][new_x] = image[y][x]

        return rotated_image

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        height, width = len(rotated_image), len(rotated_image[0])
        original_image = [[0] * width for _ in range(height)]

        for y in range(height):
            for x in range(width):
                new_x = int((x - width / 2) * math.cos(theta) + (y - height / 2) * math.sin(theta) + origin[0])
                new_y = int(-(x - width / 2) * math.sin(theta) + (y - height / 2) * math.cos(theta) + origin[1])

                if 0 <= new_x < width and 0 <= new_y < height:
                    original_image[new_y][new_x] = rotated_image[y][x]

        return original_image

    def rotate(self, image, theta, interpolation_type):
        height, width = len(image), len(image[0])
        rotated_image = [[0] * width for _ in range(height)]

        for y in range(height):
            for x in range(width):
                new_x = int((x - width / 2) * math.cos(theta) - (y - height / 2) * math.sin(theta) + width / 2)
                new_y = int((x - width / 2) * math.sin(theta) + (y - height / 2) * math.cos(theta) + height / 2)

                x1, y1 = int(new_x), int(new_y)
                x2, y2 = x1 + 1, y1 + 1

                if 0 <= x1 < width - 1 and 0 <= y1 < height - 1 and 0 <= x2 < width - 1 and 0 <= y2 < height - 1:
                    dx = new_x - x1
                    dy = new_y - y1

                    q11 = image[y1][x1]
                    q12 = image[y2][x1]
                    q21 = image[y1][x2]
                    q22 = image[y2][x2]

                    if interpolation_type == "nearest_neighbor":
                        rotated_image[y][x] = q11
                    elif interpolation_type == "bilinear":
                        rotated_image[y][x] = self.interpolator.bilinear_interpolation(x1, y1, x2, y2, new_x, new_y,
                                                                                        q11, q12, q21, q22)

        return rotated_image
