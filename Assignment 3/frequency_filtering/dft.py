# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries
import math

class Dft:
    def __init__(self):
        pass

    # Function to compute the forward Fourier transform
    def forward_fourier_transform(self, matrix):
        N, M = matrix.shape
        F = [[0j for _ in range(M)] for _ in range(N)]
        for u in range(N):
            for v in range(M):
                sum_real = 0
                sum_imag = 0
                for x in range(N):
                    for y in range(M):
                        angle = 2 * math.pi * ((u * x) / N + (v * y) / M)
                        sum_real += matrix[x][y] * math.cos(angle)
                        sum_imag -= matrix[x][y] * math.sin(angle)
                F[u][v] = complex(sum_real, sum_imag)
        return F

    # Function to compute the inverse Fourier transform
    def inverse_fourier_transform(self, F):
        N, M = len(F), len(F[0])
        f = [[0 for _ in range(M)] for _ in range(N)]
        for x in range(N):
            for y in range(M):
                sum_real = 0
                sum_imag = 0
                for u in range(N):
                    for v in range(M):
                        angle = 2 * math.pi * ((u * x) / N + (v * y) / M)
                        sum_real += F[u][v].real * math.cos(angle) - F[u][v].imag * math.sin(angle)
                        sum_imag += F[u][v].real * math.sin(angle) + F[u][v].imag * math.cos(angle)
                f[x][y] = (sum_real + sum_imag) / (N * M)
        return f

    # Function to compute magnitude of the Fourier transform
    def magnitude_fourier_transform(self, F):
        magnitude = [[abs(F[u][v]) for v in range(len(F[0]))] for u in range(len(F))]
        return magnitude

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""
        # Compute forward Fourier transform
        matrix = self.forward_fourier_transform(matrix)
        return matrix

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse fourier transform"""
        matrix = self.inverse_fourier_transform(matrix)
        return matrix

    def magnitude(self, matrix):
        """Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the complex matrix"""
        matrix = self.magnitude_fourier_transform(matrix)
        return matrix