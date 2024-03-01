from dip import *

class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        hist = [0] * 256
        height, width = image.shape
        for y in range(height):
            for x in range(width):
                pixel_value = image[y, x]
                hist[pixel_value] += 1
        return hist

    def find_otsu_threshold(self, hist):
        total_pixels = sum(hist)
        max_threshold = 0
        max_variance = 0

        for threshold in range(256):
            w0 = sum(hist[:threshold]) / total_pixels
            w1 = sum(hist[threshold:]) / total_pixels
            mu0 = sum(i * hist[i] for i in range(threshold)) / (sum(hist[:threshold]) + 1)
            mu1 = sum(i * hist[i] for i in range(threshold, 256)) / (sum(hist[threshold:]) + 1)
            variance = w0 * w1 * (mu0 - mu1) ** 2

            if variance > max_variance:
                max_variance = variance
                max_threshold = threshold

        return max_threshold

    def binarize(self, image):
        bin_img = image.copy()
        threshold = self.find_otsu_threshold(self.compute_histogram(image))
        height, width = image.shape
        for y in range(height):
            for x in range(width):
                if bin_img[y, x] > threshold:
                    bin_img[y, x] = 0  # Background
                else:
                    bin_img[y, x] = 255  # Foreground
        return bin_img
