from dip import *
"""
Do not import cv2, numpy and other third party libs
"""

class interpolation:
    def __init__(self):
        pass

    def linear_interpolation(self, x1, y1, x2, y2, x):
        
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    def bilinear_interpolation(self, x1,y1,x2,y2,x,y,q11,q12,q21,q22):
        r1 = self.linear_interpolation(x1, q11, x2, q21, x)
        r2 = self.linear_interpolation(x1, q12, x2, q22, x)
        return linear_interpolation(y1, r1, y2, r2, y)
