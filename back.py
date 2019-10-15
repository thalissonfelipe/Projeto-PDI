import imageio
import util
import cv2
import numpy as np
import matplotlib.pyplot as plt
from colors import rgb2gray, rgb2hsv, hsv2rgb, imghsv2rgb, imgrgb2hsv
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
    if len(image.shape) == 2:  # Grayscale Image
        hist = np.zeros(bins, dtype=np.int)
        flat = np.asarray(image)
        flat = flat.flatten()

        for pxl in flat:
            hist[int(round(pxl,5))] += 1

        return hist
    else:  # RGB Image
        r, g, b = np.zeros(bins), np.zeros(bins), np.zeros(bins)
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                r[image[row, col][0]] += 1
                g[image[row, col][1]] += 1
                b[image[row, col][2]] += 1

        return (r, g, b)

def histogram_hsv(image):
    # RGB Image
    v = np.zeros(101)
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            i = image[row,col,2]
            v[i] += 1
    return v

# É pra ficar assim
def equalize_hist2(image):
    img = np.zeros_like(image)
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)

    return img


def equalize_hist(image, hist):
    if len(image.shape) == 2:  # Grayscale Image
        hist = histogram(image)
        cdf = util.cumulative_distribution(hist)
        img = (np.asarray(image)).flatten()
        flat = np.zeros_like(img, dtype=np.uint8)
        for i in range(len(flat)):
            flat[i] = int(round(img[i],5))
        output = cdf[flat]
        output = np.reshape(output, image.shape)
        output[np.where(output > MAX_PIXEL)] = MAX_PIXEL

        return output.astype(np.uint8)
    else:  # RGB Image
        imghsv = image
        print("IMAGEM \n",imghsv)
        #h,s,v = util.split(imghsv)
        v = imghsv[:,:,2]
        print("VALUE \n",v.shape)
        eq_value = util.cumulative_distribution_hsv(hist)
        new_v = eq_value[v]
        print("VALUE \n",v.shape)
        imghsv[:,:,2] = new_v
        print("IMAGEM \n",v)
        rgb_image = imghsv2rgb(imghsv)

        return rgb_image


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


def mean_filter(image, filter_size):
    kernel = np.ones((filter_size, filter_size))*(1.0/(filter_size**2))
    if len(image.shape) == 2:
        return conv(image, kernel)
    else:
        r, g, b = util.split(image)
        R = conv(r, kernel)
        G = conv(g, kernel)
        B = conv(b, kernel)
        output = util.merge(R, G, B)

        return output.astype(np.uint8)


# c = 1: unsharp masking
# c > 1: highboost filtering
# c < 1: attenuates the contribution of the sharpness
def highboost(image, c, filter_size):
    blurred = mean_filter(image, filter_size)
    mask = image - blurred
    output = image + c * mask

    output[np.where(output > MAX_PIXEL)] = MAX_PIXEL
    return output.astype(np.uint8)


def gaussian_kernel(filter_size, sigma):
    x = np.linspace(-(filter_size//2), filter_size//2, filter_size)
    x = x / np.sqrt(2) * sigma
    x = x ** 2
    kernel = np.exp(-x[:,None] - x[None,:])

    return kernel / kernel.sum()


def gaussian_filter(image, filter_size, sigma):
    kernel = gaussian_kernel(filter_size, sigma)
    if len(image.shape) == 2:
        return conv(image, kernel)
    else:
        r, g, b = util.split(image)
        R = conv(r, kernel)
        G = conv(g, kernel)
        B = conv(b, kernel)
        output = util.merge(R, G, B)

        return output.astype(np.uint8)


def laplacian_filter(image, diagonal=True):
    if diagonal:
        kernel = np.array((
                 [-1, -1, -1],
                 [-1, 8, -1],
                 [-1, -1, -1]))
    else:
        kernel = np.array((
                 [0, 1, 0],
                 [1, -4, 1],
                 [0, 1, 0]))

    if len(image.shape) == 2:
        return conv(image, kernel)
    else:
        r, g, b = util.split(image)
        R = conv(r, kernel)
        G = conv(g, kernel)
        B = conv(b, kernel)
        output = util.merge(R, G, B)

        return output.astype(np.uint8)


def sharpen_filter(image):
    lap = laplacian_filter(image)
    output = image + lap
    output[np.where(output > MAX_PIXEL)] = MAX_PIXEL

    return output.astype(np.uint8)


def sobel_filter(image):
    kernelx = np.array(([-1, 0, 1], [-2, 0, 2], [-1, 0, 1]))
    kernely = np.array(([-1, -2, -1], [0, 0, 0], [1, 2, 1]))

    if len(image.shape) == 2:
        gx = conv(image, kernelx)
        gy = conv(image, kernely)

        output = abs(gx) + abs(gy)  # np.sqrt(gx ** 2 + gy ** 2) slower
        output[np.where(output > MAX_PIXEL)] = MAX_PIXEL

        return output.astype(np.uint8)
    else:
        r, g, b = util.split(image)
        rx, ry = conv(r, kernelx), conv(r, kernely)
        gx, gy = conv(g, kernelx), conv(g, kernely)
        bx, by = conv(b, kernelx), conv(b, kernely)

        R = abs(rx) + abs(ry)
        G = abs(gx) + abs(gy)
        B = abs(bx) + abs(by)

        output = util.merge(R, G, B)
        output[np.where(output > MAX_PIXEL)] = MAX_PIXEL

        return output.astype(np.uint8)


def median_filter(image, filter_size):
    height, width = image.shape
    output = np.zeros_like(image)
    pad = (filter_size - 1) // 2
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_DEFAULT)

    for row in np.arange(pad, height + pad):
        for col in np.arange(pad, width + pad):
            roi = image[row-pad:row+pad+1, col-pad:col+pad+1]
            roi = roi.flatten()
            roi.sort()
            output[row-pad, col-pad] = roi[len(roi) // 2]

    return output.astype(np.uint8)


def median_filter_rgb(image, filter_size):
    r, g, b = util.split(image)
    R = median_filter(r, filter_size)
    G = median_filter(g, filter_size)
    B = median_filter(b, filter_size)
    output = util.merge(R, G, B)

    return output.astype(np.uint8)


# Similar to mean filter
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

    output[np.where(output > MAX_PIXEL)] = MAX_PIXEL
    return output.astype(np.uint8)


def geometric_mean_filter_rgb(image, filter_size):
    r, g, b = util.split(image)
    R = geometric_mean_filter(r, filter_size)
    G = geometric_mean_filter(g, filter_size)
    B = geometric_mean_filter(b, filter_size)
    output = util.merge(R, G, B)

    return output.astype(np.uint8)


# Similar to mean filter
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

    output[np.where(output > MAX_PIXEL)] = MAX_PIXEL
    return output.astype(np.uint8)


def harmonic_mean_filter_rgb(image, filter_size):
    r, g, b = util.split(image)
    R = harmonic_mean_filter(r, filter_size)
    G = harmonic_mean_filter(g, filter_size)
    B = harmonic_mean_filter(b, filter_size)
    output = util.merge(R, G, B)

    return output.astype(np.uint8)


# Q > 0:  the filter eliminates pepper noise
# Q < 0:  the filter eliminates salt noise
# Q = 0:  mean filter
# Q = -1: harmonic filter
def contraharmonic_mean_filter(image, filter_size, Q=1):
    height, width = image.shape
    pad = (filter_size - 1) // 2
    output = np.zeros_like(image)
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_DEFAULT)

    for row in np.arange(pad, height + pad):
        for col in np.arange(pad, width + pad):
            kernel = image[row-pad:row+pad+1, col-pad:col+pad+1]
            output[row-pad, col-pad] = \
                util.contraharmonic_mean_aux(kernel, Q)

    output[np.where(output > MAX_PIXEL)] = MAX_PIXEL
    return output.astype(np.uint8)


def contraharmonic_mean_filter_rgb(image, filter_size, Q=1):
    r, g, b = util.split(image)
    R = contraharmonic_mean_filter(r, filter_size, Q)
    G = contraharmonic_mean_filter(g, filter_size, Q)
    B = contraharmonic_mean_filter(b, filter_size, Q)
    output = util.merge(R, G, B)

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


if __name__ == '__main__':
    i = imageio.imread('images/dipxe.jpeg')
    #i = rgb2gray(i)
    #it = equalize_hist(i)
    #it = sharpen_filter(i)]
    it = highboost(i, -3, 5)
    util.subplot_img(i, it)
