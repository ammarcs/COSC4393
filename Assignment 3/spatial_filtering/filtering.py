class Filtering:

    def __init__(self, image):
        self.image = image

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""
        gaussian_filter = [
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1]
        ]

        # Perform division by 256.0 manually
        for i in range(len(gaussian_filter)):
            for j in range(len(gaussian_filter[i])):
                gaussian_filter[i][j] /= 256.0
        
        return gaussian_filter

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""
        laplacian_filter = [[0, 1, 0],
                            [1, -4, 1],
                            [0, 1, 0]]
        return laplacian_filter

    def convolution(self, img, kernel):
        kernel_length = len(kernel)
        imx, imy = img.shape[0:2]
        new_image = img[::, ::]
        for i in range(kernel_length, imx - kernel_length):
            for j in range(kernel_length, imy - kernel_length):
                acc = 0
                for ki in range(kernel_length):
                    for kj in range(kernel_length):
                        acc += img[i+ki-2][j+kj-2] * kernel[ki][kj]
                new_image[i][j] = acc
        return new_image

    def gaussian_blur(self, image):
        kernel = self.get_gaussian_filter()
        return self.convolution(image, kernel)
    
    def convolution_laplacian(self, image, filter, thresh=20):
        
        height, width = len(image), len(image[0])
        filtered = image.copy()
        filtered[:, :] = 0
        
        for i in range(1, height-1):
            for j in range(1, width-1):
                temp_arr = []
                left, right = j - 1, j + 2
                upper, lower = i - 1, i + 2
                for r in range(upper, lower):
                    temp_arr.extend(image[r][left:right])
                
                temp_arr = [temp_arr[k:k+3] for k in range(0, len(temp_arr), 3)]
                grad = sum(filter[row][col] * temp_arr[row][col] for row in range(3) for col in range(3))
                if grad > thresh:
                    filtered[i-1][j-1] = 255
                else:
                    filtered[i-1][j-1] = 0        
        return filtered    
    
    def laplacian_filter(self, image):
        kernel = self.get_laplacian_filter()
        return self.convolution_laplacian(image, kernel)

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
                """
        if filter_name == "gaussian":
            self.image = self.gaussian_blur(self.image)
        elif filter_name == "laplacian":
            self.image = self.laplacian_filter(self.image)
        else:
            raise ValueError("Filter not supported")

        return self.image

