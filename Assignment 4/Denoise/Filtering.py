import math
import dip

class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        # global_var: noise variance to be used in the Local noise reduction filter        
        self.global_var = var
        # S_max: Maximum allowed size of the window that is used in the adaptive median filter
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input ROI
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        return sum(i for i in roi) / len(roi)

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        return roi.prod()**(1.0/len(roi))

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        pixel = roi[1]
        roi = roi[0]
        n = len(roi)                  
        localMean = (float)(math.fsum(i for i in roi) / n)         
        localVar = (float)((math.fsum(i**2 for i in roi) / n) - localMean**2)                  
        result = (float)((float)(pixel)  - (self.global_var/localVar)*((float)(pixel) -localMean))                  
        return (float)(result)

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi
        Do not use any in-built median function from numpy or other libraries.
        """
        sorted_roi = sorted(roi)
        length = len(sorted_roi)

        # Check if the length of the ROI is odd or even
        if length % 2 == 0:
            # If the length is even, average the two middle values
            median = (sorted_roi[length // 2 - 1] + sorted_roi[length // 2]) / 2
        else:
            # If the length is odd, pick the middle value
            median = sorted_roi[length // 2]
        return median

    def second_step(self, matrix, min_z, med_z, max_z):   
        """
        matrix: matrix passed from get_adaptive_median          
        returns the median value of the roi
        """      
        x,y = matrix.shape                  
        z_value = matrix[x//2, y//2]         
        B1 = z_value - min_z         
        B2 = z_value - max_z              
        if B1 > 0 and B2 < 0 :             
            return z_value         
        else:             
            return med_z
  
    def get_adaptive_median(self, img, x, y, size, max_s):
        """
        Use this function to implement the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """
        #reshapes window for every pixel         
        matrix = size//2
        roi_window = img[x - matrix: x + matrix + 1, y - matrix: y + matrix + 1]
        
        #gets window intensity values
        tmp_flattened = [element for sublist in roi_window for element in sublist]
        min_z = dip.min(roi_window)         
        med_z = self.get_median(tmp_flattened)         
        max_z = dip.max(roi_window)
        
        tmp1 = med_z - min_z         
        tmp2 = med_z - max_z              
        if tmp1 > 0 and tmp2 < 0:             
            return Filtering.second_step(self, roi_window, min_z, med_z, max_z)         
        else:             
            size += 2              
            if size <= max_s:                 
                return Filtering.get_adaptive_median(self, img, x, y, size, max_s)             
            else:                 
                return med_z


    def filtering(self):
        """performs filtering on an image containing Gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernel and apply a mathematical
        operation for all the elements within the kernel. For example, mean, median, etc.

        Steps:
        1. add the necessary zero padding to the noisy image, that way we have sufficient values to perform the operations on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and for every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the output image.
        5. return the output image

        Note: You can create extra functions as needed. For example, if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        

        #1. 1. add the necesssary zero padding to the noisy image, 
        # that way we have sufficient values to perform the operations on the pixels at the image corners. 
        # The number of rows and columns of zero padding is defined by the kernel size         
        noised_image = self.image
        if isinstance(self.filter, type(self.get_adaptive_median)):           
            padded_value = self.S_max//2   
            padded_rows = noised_image.shape[0] + 2 * padded_value
            padded_cols = noised_image.shape[1] + 2 * padded_value
                    
            paddedImage = dip.zeros((padded_rows, padded_cols)) 
            paddedImage[padded_value:-padded_value,padded_value:-padded_value] = noised_image
        else:             
            padded_value = self.filter_size//2    
            padded_rows = noised_image.shape[0] + 2 * padded_value
            padded_cols = noised_image.shape[1] + 2 * padded_value

            paddedImage = dip.zeros((padded_rows, padded_cols))             
            paddedImage[padded_value:-padded_value,padded_value:-padded_value] = noised_image          
        
        # 2. Iterate through the image and for every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        # 3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        # 4. Save the results at (i,j) in the output image.
        # 5. return the output image

        outputImage = dip.zeros(paddedImage.shape)
        if isinstance(self.filter, type(self.get_adaptive_median)):                
            for i in range(padded_value, noised_image.shape[0]+padded_value+1):                 
                for j in range(padded_value, noised_image.shape[1]+padded_value+1):                     
                    denoisedValue = Filtering.get_adaptive_median(self, paddedImage, i, j, self.filter_size, self.S_max)                     
                    outputImage[i,j] = denoisedValue                              
        elif isinstance(self.filter, type(self.get_local_noise)):           
            for i in range(padded_value, noised_image.shape[0]+padded_value+1):                 
                for j in range(padded_value, noised_image.shape[1]+padded_value+1):                     
                    windowFilter = paddedImage[i-padded_value:i+padded_value+1, j-padded_value:j+padded_value+1]                 
                    roiFilter = windowFilter.flatten() 
                    #flattens 2d image array to 1d array                     
                    denoisedValue = Filtering.get_local_noise(self, (roiFilter, paddedImage[i,j]))                     
                    outputImage[i,j] = denoisedValue   
                    
        elif isinstance(self.filter, type(self.get_arithmetic_mean)):             
            for i in range(padded_value, noised_image.shape[0]+padded_value+1):                 
                for j in range(padded_value, noised_image.shape[1]+padded_value+1):                     
                    windowFilter = paddedImage[i-padded_value:i+padded_value+1, j-padded_value:j+padded_value+1]                     
                    roiFilter = windowFilter.flatten()                     
                    denoisedValue = Filtering.get_arithmetic_mean(self, roiFilter)                     
                    outputImage[i,j] = denoisedValue          
        elif isinstance(self.filter, type(self.get_geometric_mean)):             
            for i in range(padded_value, noised_image.shape[0]+padded_value+1):                 
                for j in range(padded_value, noised_image.shape[1]+padded_value+1):                     
                    windowFilter = paddedImage[i-padded_value:i+padded_value+1, j-padded_value:j+padded_value+1]                     
                    roiFilter = windowFilter.flatten()                     
                    denoisedValue = Filtering.get_geometric_mean(self, roiFilter)                     
                    outputImage[i,j] = denoisedValue                  
        elif isinstance(self.filter, type(self.get_median)):           
            for i in range(padded_value, noised_image.shape[0]+padded_value+1):                 
                for j in range(padded_value, noised_image.shape[1]+padded_value+1):                     
                    windowFilter = paddedImage[i-padded_value:i+padded_value+1, j-padded_value:j+padded_value+1]                     
                    roiFilter = windowFilter.flatten()                     
                    denoisedValue = Filtering.get_median(self, roiFilter)                     
                    outputImage[i,j] = denoisedValue
        
        # Crops image to remove padding
        return outputImage[padded_value:-padded_value, padded_value:-padded_value] 
