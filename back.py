import imageio
import util
import cv2
import numpy as np
import matplotlib.pyplot as plt
from colors import rgb2gray
plt.rcParams['figure.figsize'] = (15, 15)


MAX_PIXEL = 255


def negative_filter(image):
    return (MAX_PIXEL - image).astype(np.uint8)


def logarithm_filter(image, c=1):
    log = c * (np.log(image + 1) / (np.log(1 + np.max(image)))) * MAX_PIXEL
    return log.astype(np.uint8)


def gamma_filter(image, gamma, c=1):
    gamma = c * np.array(MAX_PIXEL * (image / MAX_PIXEL) ** gamma)
    return gamma.astype(np.uint8)


# TODO: implementar transformaçao linear
# def linear_transform(i):


def histogram(image, bins=256):
    if len(image.shape) == 2:  # 2D Grayscale Image
        hist = np.zeros(bins, dtype=np.int)
        flat = np.asarray(image)
        flat = flat.flatten()

        for pxl in flat:
            hist[pxl] += 1

        return hist
    else:  # RGB Image
        r, g, b = np.zeros(bins), np.zeros(bins), np.zeros(bins)
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                r[image[row, col][0]] += 1
                g[image[row, col][1]] += 1
                b[image[row, col][2]] += 1

        return (r, g, b)


def equalize_hist(image, hist):
    if len(image.shape) == 2:  # 2D Grayscale Image
        y = util.cumulative_distribution(hist)
        flat = (np.asarray(image)).flatten()

        new_img = y[flat]
        new_img = np.reshape(new_img, image.shape)

        return new_img
    # TODO
    # else:  # RGB Image
    #     cr, cg, cb = cumulative_distribution(hist)
    #     flatr = (np.asarray(image[:,:,0])).flatten()
    #     flatg = (np.asarray(image[:,:,1])).flatten()
    #     flatb = (np.asarray(image[:,:,2])).flatten()

    #     new_img = np.zeros_like(image)
    #     print(len(new_img[:,:,0]), len(cr[flatr]))
    #     new_img[:,:,0] = cr[flatr]
    #     new_img[:,:,1] = cg[flatg]
    #     new_img[:,:,2] = cb[flatb]
    #     new_img = np.reshape(new_img, image.shape)

    #     return new_img


def conv(image, kernel):
    height, width = image.shape
    output = np.zeros_like(image)
    kernel = np.flipud(np.fliplr(kernel))
    pad = (kernel.shape[0] - 1) // 2
    # image_padded = np.zeros((height + pad, width + pad))
    # print(image_padded.shape)
    # image_padded[pad:-pad, pad:-pad] = image
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_DEFAULT)

    for row in np.arange(pad, height + pad):
        for col in np.arange(pad, width + pad):
            roi = image[row-pad:row+pad+1, col-pad:col+pad+1]
            k = (roi * kernel)
            output[row-pad, col-pad] = min(MAX_PIXEL, max(0, k.sum()))

    return output.astype(np.uint8)


def fft(x):
    N = len(x)
    if N <= 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [np.exp(-2j*np.pi*k/N)*odd[k] for k in range(N//2)]
    return [even[k] + T[k] for k in range(N//2)] + \
           [even[k] - T[k] for k in range(N//2)]


"""def conv(image, kernel):
    height, width = image.shape
    pad = (kernel.shape[0] - 1)
    output = np.zeros_like(image)

    for row in range(1, height - 1):
        for col in range(1, width - 1):
            k = kernel * image[(row-1):(row+2), (col-1):(col+2)]
            output[row-1, col-1] = min(MAX_PIXEL, max(0, k.sum()))

    return output.astype(np.uint8)"""


def mean_filter(image, filter_size):
    f = np.ones((filter_size, filter_size))*(1.0/(filter_size**2))
    return conv(image, f)


def laplacian_filter(image, diagonal=True):
    if diagonal:
        f = np.array((
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]))
    else:
        f = np.array((
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]))

    return conv(image, f)


def sharpen_filter(image):
    lap = laplacian_filter(image)
    output = image + lap
    output[np.where(output > MAX_PIXEL)] = MAX_PIXEL
    # output = (output * MAX_PIXEL) / output.max()
    return output.astype(np.uint8)


def sobel_filter(image):
    fx = np.array(([-1, 0, 1], [-2, 0, 2], [-1, 0, 1]))
    fy = np.array(([-1, -2, -1], [0, 0, 0], [1, 2, 1]))

    gx = conv(image, fx)
    gy = conv(image, fy)

    output = abs(gx) + abs(gy)  # np.sqrt(gx ** 2 + gy ** 2) slower
    # output[np.where(output > MAX_PIXEL)] = MAX_PIXEL
    output = (output * MAX_PIXEL) / output.max()
    return output.astype(np.uint8)


def median_filter(image, filter_size):
    height, width = image.shape
    mid = (filter_size - 1) // 2
    output = np.zeros_like(image)

    for row in range(height):
        for col in range(width):
            neighbors = []
            for x in range(filter_size):
                if row + x - mid < 0 or row + x - mid > height - 1:
                    for i in range(filter_size):
                        neighbors.append(0)
                else:
                    if col + x - mid < 0 or col + mid > width - 1:
                        neighbors.append(0)
                    else:
                        for i in range(filter_size):
                            neighbors.append(image[row+x-mid, col+i-mid])

            neighbors.sort()
            output[row, col] = neighbors[len(neighbors) // 2]

    output = (output * MAX_PIXEL) / output.max()
    return output.astype(np.uint8)


"""def multiply(neighbors):
    neighbors = np.array(neighbors, dtype=np.float64)
    result = 1
    for x in neighbors:
        result *= x
    return result


## Bordas pretas
def geometric_mean_filter(image, filter_size):
    height, width = image.shape
    mid = filter_size // 2
    output = np.zeros_like(image)

    for v in range(height):
        for w in range(width):
            neighbors = []
            for x in range(filter_size):
                if v + x - mid < 0 or v + x - mid > height - 1:
                    for i in range(filter_size):
                        neighbors.append(0)
                else:
                    if w + x - mid < 0 or w + mid > width - 1:
                        neighbors.append(0)
                    else:
                        for i in range(filter_size):
                            neighbors.append(image[v+x-mid,w+i-mid])

            output[v,w] = np.power(multiply(neighbors), 1.0/(filter_size**2))

    return output.astype(np.uint8)"""


def geometric_mean_filter(image, filter_size):
    height, width = image.shape
    pad = (filter_size - 1) // 2
    output = np.zeros_like(image)
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_DEFAULT)

    for row in np.arange(pad, height + pad):
        for col in np.arange(pad, width + pad):
            kernel = image[row-pad:row+pad+1, col-pad:col+pad+1]
            output[row-pad, col-pad] = (util.geometric_mean_aux(kernel)) ** \
                                       (1./(filter_size**2))

    output = (output * MAX_PIXEL) / output.max()
    return output.astype(np.uint8)


def harmonic_mean_filter(image, filter_size):
    height, width = image.shape
    pad = (filter_size - 1) // 2
    output = np.zeros_like(image)
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_DEFAULT)

    for row in np.arange(pad, height + pad):
        for col in np.arange(pad, width + pad):
            kernel = image[row-pad:row+pad+1, col-pad:col+pad+1]
            s = util.harmonic_mean_aux(kernel)
            if s == 0:  # Check division by 0
                output[row-pad, col-pad] = 0
                continue
            output[row-pad, col-pad] = (filter_size**2) / s

    output = (output * MAX_PIXEL) / output.max()
    return output.astype(np.uint8)


def contraharmonic_mean_filter(image, filter_size):
    height, width = image.shape
    pad = (filter_size - 1) // 2
    output = np.zeros_like(image)
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_DEFAULT)

    for row in np.arange(pad, height + pad):
        for col in np.arange(pad, width + pad):
            kernel = image[row-pad:row+pad+1, col-pad:col+pad+1]
            output[row-pad, col-pad] = util.contraharmonic_mean_aux(kernel)

    output = (output * MAX_PIXEL) / output.max()
    return output.astype(np.uint8)


def sepia_filter(image):
    img = np.asarray(image)

    lmap = np.matrix([[0.393, 0.769, 0.189],
                      [0.349, 0.686, 0.168],
                      [0.272, 0.534, 0.131]])

    output = np.array([x * lmap.T for x in img])
    output[np.where(output > MAX_PIXEL)] = MAX_PIXEL
    output = np.reshape(output, image.shape)

    return output.astype(np.uint8)


""" Demora uns 20 segundos
def sepia_filter2(image):
    height, width, _ = image.shape
    output = np.zeros_like(image)

    for v in range(height):
        for w in range(width):
            r, g, b = image[v,w]
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > MAX_PIXEL: tr = MAX_PIXEL
            if tg > MAX_PIXEL: tg = MAX_PIXEL
            if tb > MAX_PIXEL: tb = MAX_PIXEL

            output[v,w] = tr, tg, tb

    return output.astype(np.uint8)"""


if __name__ == '__main__':
    i = imageio.imread('images/einstein.jpeg')
    i = rgb2gray(i)
    # it = logarithm_filter(i, 1)
    # hist = histogram(i)
    # it = equalize_hist(i, hist)
    # r, g, b = histogram(i, 256)
    # cr, cg, cb = cumulative_distribution((r, g, b))
    # it = equalize_hist(i, (r, g, b))
    # plt.plot(cr, color='r')
    # plt.plot(cg, color='g')
    # plt.plot(cb, color='b')
    # plt.show()
    # it = equalize_hist(i, hist)
    # histeq = histogram(it, 256)
    # subplot_hist(hist, histeq)
    # subplot_img(i, it)
    # subplot(histogram(i, 256), histogram(it, 256))
    # it = mean_filter(i, 35)
    # it = sepia_filter(i)
    # it = laplacian_filter(i)
    # it = gamma_filter(i, 0.4)
    # it = sharpen_filter(i)
    # it = negative_filter(i)
    # hist = histogram(it)
    # it = equalize_hist(it, hist)
    # it = sobel_filter(i)
    # it = geometric_mean_filter(i, 3)
    # it = harmonic_mean_filter(i, 3)
    # it = contraharmonic_mean_filter(i, 3)
    # util.subplot_img(i, it)
