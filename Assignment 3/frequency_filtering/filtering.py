# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv

import numpy as np
import cv2
import math

class Filtering:

    def __init__(self, image):
        """initializes the variables for frequency filtering on an input image
        takes as input:
        image: the input image
        """
        self.image = image
        rows, cols = self.image.shape
        self.cutoff = min(rows, cols) / 2
        self.order = 0
        self.mask = self.get_mask

    def get_mask(self, shape):
        """Computes a user-defined mask
        takes as input:
        shape: the shape of the mask to be generated
        rtype: a 2d numpy array with size of shape
        """
        return self.get_gaussian_low_pass_filter(shape, self.cutoff)

    def post_process_image(self, image):
        """Post processing to display DFTs and IDFTs
        takes as input:
        image: the image obtained from the inverse fourier transform, forward fourier transform, or filtered fourier transform 
        return an image with full contrast stretch
        -----------------------------------------------------
        You can perform post processing as needed. For example,
        1. You can perfrom log compression
        2. You can perfrom a full contrast stretch (fsimage)
        3. You can take negative (255 - fsimage)
        4. etc.
        """
        a = 0
        b = 255
        c = np.min(image)
        d = np.max(image)
        rows, columns = np.shape(image)
        image1 = np.zeros((rows, columns), dtype=int)
        for i in range(rows):
            for j in range(columns):
                if (d-c) == 0:
                    image1[i, j] = ((b - a) / 0.000001) * (image[i, j] - c) + a
                else:
                    image1[i, j] = ((b - a) / (d - c)) * (image[i, j] - c) + a

        return np.uint8(image1)

    def filter(self):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering
        ----------------------------------------------------------
        You are allowed to use inbuilt functions to compute fft
        There are packages available in numpy as well as in opencv
        Steps:
        1. Compute the fft of the image
        2. shift the fft to center the low frequencies
        3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape)
        4. filter the image frequency based on the mask (Convolution theorem)
        5. compute the inverse shift
        6. compute the inverse fourier transform
        7. compute the magnitude
        8. You will need to do post processing on the magnitude and depending on the algorithm (use post_process_image to write this code)
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        """
        image = self.image
        shape = np.shape(image)

        # Step 1
         # Compute the FFT of the image
        fft_image = np.fft.fft2(image)
        fft_shifted = np.fft.fftshift(fft_image)
        tmp_dft = np.log(np.abs(fft_shifted))

        dft = self.post_process_image(tmp_dft)

        # 3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape, cutoff, order)
        mask = self.mask(shape)

        # 4. filter the image frequency based on the mask (Convolution theorem)
        filtered_image = np.multiply(mask, fft_shifted)
        mag_filtered_dft = np.log(np.abs(filtered_image)+1)
        filtered_dft = self.post_process_image(mag_filtered_dft)

        # 5. compute the inverse shift
        shift_ifft = np.fft.ifftshift(filtered_image)

        # 6. compute the inverse fourier transform
        ifft = np.fft.ifft2(shift_ifft)

        # 7. compute the magnitude
        mag = np.abs(ifft)
        
        #8. Post Processing
        filtered_image = self.post_process_image(mag)

        return [np.uint8(filtered_image), np.uint8(dft), np.uint8(filtered_dft)]


    def get_gaussian_low_pass_filter(self, shape, cutoff):
        """Computes a gaussian low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the gaussian filter (sigma)
        returns a gaussian low pass mask"""
        d0 = cutoff
        rows, columns = shape
        mask = np.zeros((rows, columns))
        mid_R, mid_C = int(rows / 2), int(columns / 2)
        for i in range(rows):
            for j in range(columns):
                d = math.sqrt((i - mid_R) ** 2 + (j - mid_C) ** 2)
                mask[i, j] = np.exp(-(d * d) / (2 * d0 * d0))
        return mask
