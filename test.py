import cv2
import imageio
import colors
import util
import back as bk
# from scipy.signal import convolve2d


def negative_filter_test():
    i = imageio.imread('images/breast.jpeg')
    i = colors.rgb2gray(i)
    it1 = cv2.bitwise_not(i)
    it2 = bk.negative_filter(i)
    util.subplot_img(it1, it2)


def logarithm_filter_test():
    i = imageio.imread('images/dft.jpeg')
    i = colors.rgb2gray(i)
    it = bk.logarithm_filter(i, 1)
    util.subplot_img(i, it)


def gamma_filter_test():
    i = imageio.imread('images/aerial.jpeg')
    i = colors.rgb2gray(i)
    it = bk.gamma_filter(i, 1, 5)
    util.subplot_img(i, it)


def mean_filter_test():
    i = imageio.imread('images/blurring.jpeg')
    i = colors.rgb2gray(i)
    it1 = cv2.blur(i, (5, 5))
    it2 = bk.mean_filter(i, 5)
    util.subplot_img(it1, it2)


def median_filter_test():
    i = imageio.imread('images/salt_pepper.jpeg')
    i = colors.rgb2gray(i)
    it1 = cv2.medianBlur(i, 3)
    it2 = bk.median_filter(i, 3)
    util.subplot_img(it1, it2)


def laplacian_filter_test():
    i = imageio.imread('images/moon.jpeg')
    i = colors.rgb2gray(i)
    img = cv2.imread('images/moon.jpeg', 0)
    it1 = cv2.Laplacian(img, cv2.CV_64F)
    it2 = bk.laplacian_filter(i)
    util.subplot_img(it1, it2)


def sobel_filter_test():
    i = imageio.imread('images/lens.jpeg')
    i = colors.rgb2gray(i)
    it = bk.sobel_filter(i)
    util.subplot_img(i, it)


def histogram_test_gray():
    i = imageio.imread('images/hamster.jpeg')
    i = colors.rgb2gray(i)
    img = cv2.imread('images/hamster.jpeg', 0)
    hist1 = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist2 = bk.histogram(i)
    print(hist1.ravel())
    print(hist2)
    util.subplot_hist(hist1.ravel(), hist2)


# def histogram_test_rgb():


if __name__ == '__main__':
    # negative_filter_test()
    # logarithm_filter_test()
    # gamma_filter_test()
    # mean_filter_test()
    # median_filter_test()  # Segmentation fault
    # laplacian_filter_test()
    sobel_filter_test()
    # histogram_test_gray()
