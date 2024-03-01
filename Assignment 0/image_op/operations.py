import math
from dip import *

"""
Do not import cv2, numpy and other third party libs
"""

class Operation:

    def __init__(self):
        pass

    def flip(self, image, direction="horizontal"):
        """
          Perform image flipping along horizontal or vertical direction

          image: the input image to flip
          direction: direction along which to flip

          return: output_image
          """

        output_image = []

        if direction == "horizontal":
            for row in image:
                flipped_row = row[::-1] 
                output_image.append(flipped_row)

        elif direction == "vertical":
            for i in range(len(image) - 1, -1, -1):
                output_image.append(image[i])

        return array(output_image)

    def chroma_keying(self, foreground, background, target_color, threshold):
        """
        Perform chroma keying to create an image where the targeted green pixels is replaced with
        background

        foreground_img: the input image with green background
        background_img: the input image with normal background
        target_color: the target color to be extracted (green)
        threshold: value to threshold the pixel proximity to the target color

        return: output_image
        """
    
        for i in range(0,len(foreground)):
            for j in range(0, len(foreground[i])):
                distance = sqrt(((foreground[i][j][0]-target_color[0])**2)+((foreground[i][j][1]-target_color[1])**2)+((foreground[i][j][2]-target_color[2])**2))
                if distance <= threshold:
                    foreground[i][j] = background[i][j]

        return  foreground 

   