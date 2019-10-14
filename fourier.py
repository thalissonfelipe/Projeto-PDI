import imageio
import numpy as np
import matplotlib.pyplot as plt 
from colors import rgb2gray


# def pad(x):
#     i = 0
#     while 2 ** i < len(x):
#         i += 1
#     x = np.concatenate((x, ([0] * (2 ** i - len(x)))))
#     return x


def dft(x):
    t = []
    n = len(x)
    for i in range(n):
        a = 0
        for m in range(n):
            a += x[m] * np.exp(-2j*np.pi*i*m*(1/n))
        t.append(a)

    return t


# Only works for powers of 2
# def fft(x):
#     n = len(x)
#     if n == 1:
#         return x
#     even, odd = fft(x[0::2]), fft(x[1::2])
#     combined = np.zeros(n, dtype=np.complex)
#     for m in range(n//2):
#         combined[m] = even[m] + np.exp(-2j*np.pi*m/n) * odd[m]
#         combined[m + n//2] = even[m] - np.exp(-2j*np.pi*m/n) * odd[m]
#     return combined


def fft2(image):
    height, width = image.shape
    f1 = np.zeros_like(image, dtype=np.complex)

    for i in range(height):
        f1[i,:] = dft(image[i,:])

    f1 = np.rot90(f1)
    f2 = np.zeros_like(f1, dtype=np.complex)

    for i in range(width):
        f2[i,:] = dft(f1[i,:])

    f3 = np.rot90(f2, 3)
    return f3


def fft2shift(f):
    height, width = f.shape
    sf = np.roll(f, height//2, axis=0)
    sf = np.roll(sf, width//2, axis=1)

    return sf


def ifft2shift(f):
    height, width = f.shape
    sf = np.roll(f, -(width//2), axis=1)
    sf = np.roll(sf, -(height//2), axis=0)

    return sf


def ifft(f):
    f = np.asarray(f, dtype=np.complex)
    conjugate = np.conjugate(f)
    fx = dft(conjugate)
    fx = np.conjugate(fx)
    fx = f / f.shape[0]

    return fx


def ifft2(f):
    height, width = f.shape
    image = fft2(np.conjugate(f))
    image = np.matrix(np.real(np.conjugate(image)))
    image = image / (height * width)

    return image


def create_disk(height, width, center=None, radius=None):
    if center is None:
        center = [width//2, height//2]

    if radius is None:
        radius = min(center[0], center[1], height-center, width-center)

    Y, X = np.ogrid[:h, :w]
    distance = np.sqrt((X - center[0]**2 + (Y-center[1]**2)))

    mask = distance <= radius
    print(mask)
    return mask


def lowPassFilter(image, radius, center=None):
    height, width = image.shape
    mask = create_disk(height, width, radius=radius)
    masked = image.copy()
    masked[~mask] = 0
    return masked


if __name__ == '__main__':
    i = imageio.imread('images/einstein2.jpeg')
    print(i.shape)
    i = rgb2gray(i)
    f = fft2(i)
    f = fft2shift(f)
    plt.imshow(abs(f), cmap='gray')
    plt.show()
    f = ifft2shift(f)
    f = ifft2(f)

    
