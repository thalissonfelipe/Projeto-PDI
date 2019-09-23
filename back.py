import imageio
import cv2 #comparar histograma
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15, 15)

def rgb2gray(img):
	gray = np.dot(img[...,:3], [0.298936, 0.587043, 0.114021])
	igray = np.zeros(gray.shape, dtype=int)
	for v in range(igray.shape[0]):
		for w in range(igray.shape[1]):
			igray[v][w] = int(round(gray[v][w],5))
	return igray

def imshow(img):
	plt.imshow(img, cmap=plt.get_cmap(name='gray'))
	plt.axis('off')
	plt.show()

def plot_hist(hist):
	x = [i for i in range(len(hist))]
	plt.bar(x, height=hist, width=1.0)
	plt.show()

def subplot_hist(hist, histeq):
	fig, axes = plt.subplots(1, 2)
	x = [i for i in range(len(hist))]

	axes[0].bar(x, height=hist, width=1.0)
	axes[1].bar(x, height=histeq, width=1.0)
	plt.show()

def subplot_img(img, it):
	fig, axes = plt.subplots(1, 2)

	axes[0].imshow(img, cmap=plt.get_cmap(name='gray'))
	axes[0].axis('off')
	axes[1].imshow(it, cmap=plt.get_cmap(name='gray'))
	axes[1].axis('off')
	plt.show()

def negative_transform(img):
	return 255 - img

def log_transform(img, c):
	return c * np.log(1 + img)

def gamma_transform(img, c, gama):
	return c * np.power(img, gama)

#TODO: implementar transformaçao linear
#def linear_transform(i):

def histogram(img, bins):
	hist = np.zeros(bins)
	flat = np.asarray(img)
	flat = flat.flatten()

	for pxl in flat:
		hist[pxl] += 1

	return hist

def cumulative_distribution(hist):
	x = iter(hist)
	y = [next(x)]

	for i in x:
		y.append(y[-1] + i)

	y = np.array(y)
	numerator = (y - y.min()) * 255
	denominator = y.max() - y.min()
	y = numerator / denominator 
	y = y.astype('uint8')

	return y

def equalize_hist(img, hist):
	y = cumulative_distribution(hist)
	flat = (np.asarray(img)).flatten()

	new_img = y[flat]
	new_img = np.reshape(new_img, img.shape)

	return new_img 

"""
def equalizeHist(hist):
	n = len(hist) #256
	prob = [0]*n  
	proba = []
	total_pxl = 0

	for h in hist:
		total_pxl += h 
	prob[0] = hist[0]/total_pxl
	proba.append(prob[0])
	for i in range(1, n):
		prob[i] = hist[i]/total_pxl
		if prob[i] != 0:
			proba.append(prob[i] + proba[-1])

	hist_equalizado = [int(round(i*255,5)) for i in proba]
	return hist_equalizado

def applyHistEqualization(i, hist_equalizado):
	n = len(hist_equalizado)
	img = i
	for i in range(n):
		for v in range(img.shape[0]):
			for w in range(img.shape[1]):
				if img[v][w] == i:
					img[v][w] = hist_equalizado[i]

	return img
"""

#TODO: implementar transformada discreta de Fourier
#def dft(img):

		
def conv(image, kernel, k):
	kernel = np.flipud(np.fliplr(kernel))
	output = np.zeros_like(image)
	image_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))
	image_padded[1:-1, 1:-1] = image
	for v in range(image.shape[1]):
		for w in range(image.shape[0]):
			output[w,v] = (kernel*image_padded[w:w+k, v:v+k]).sum()
	return output

def mean_filter(image, size):
	f = np.ones((size, size))
	f /= size

	image_mean = conv(image, f, size)

	return image_mean 

if __name__ == '__main__':
	i = imageio.imread('images/a.jpeg')
	i = rgb2gray(i)
	#hist = histogram(i, 256)
	#it = equalize_hist(i, hist)
	#histeq = histogram(it, 256)
	#subplot_hist(hist, histeq)
	#subplot_img(i, it)
	#subplot(histogram(i, 256), histogram(it, 256))
	it = mean_filter(i, 3)
	subplot_img(i, it)
