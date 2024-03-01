from dip import *

class Rle:
    def __init__(self):
        pass

    def encode_image(self, binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        rle_code = []
        height, width = binary_image.shape

        current_run = 0
        current_value = binary_image[0, 0]

        for y in range(height):
            for x in range(width):
                pixel = binary_image[y, x]

                if pixel == current_value:
                    current_run += 1
                else:
                    rle_code.append(current_value)
                    rle_code.append(current_run)
                    current_value = pixel
                    current_run = 1

        rle_code.append(current_value)
        rle_code.append(current_run)

        return array(rle_code)

    def decode_image(self, rle_code, height, width):
        """
        Get the original image from the rle_code
        takes as input:
        rle_code: the run-length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        decoded_image = zeros((height, width), uint8)
        y, x = 0, 0
        rle_index = 0

        while rle_index < len(rle_code):
            value = rle_code[rle_index]
            run_length = rle_code[rle_index + 1]

            for _ in range(run_length):
                decoded_image[y, x] = value
                x += 1
                if x == width:
                    x = 0
                    y += 1

            rle_index += 2

        return decoded_image
