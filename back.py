import imageio
import cv2 #comparar histograma
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15, 15)

def rgb2gray(img):
	if len(img.shape) == 2:
		return img
	else:
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

def histogram(img, bins=256):
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

		
def conv(image, kernel):
	"""kernel = np.flipud(np.fliplr(kernel))
	output = np.zeros_like(image)
	pad = (size) // 2
	image_padded = np.zeros((image.shape[0] + pad, image.shape[1] + pad))
	image_padded[1:-1, 1:-1] = image
	for v in np.arange(pad, image.shape[1]+pad):
		for w in np.arange(pad, image.shape[0]+pad):
			roi = image_padded[v-pad:v+1, w-pad:w+1]
			k = (roi * kernel).sum()
			output[v-pad, w-pad] = k
	return output

	#for v in range(image.shape[1]):
	#	for w in range(image.shape[0]):
	#		output[w,v] = (kernel*image_padded[w:w+k, v:v+k]).sum()
	#return output"""

	(height, width) = image.shape
	(heightK, widthK) = kernel.shape
	output = np.zeros_like(image)
	kernel = np.flipud(np.fliplr(kernel))
	pad = (widthK - 1) // 2
	image = cv2.copyMakeBorder(image, pad, pad, pad, pad, 0)

	for v in np.arange(pad, height + pad):
		for w in np.arange(pad, width + pad):
			roi = image[v-pad:v+pad+1, w-pad:w+pad+1]
			#if (roi.shape[0] != kernel.shape[0] or 
			#	roi.shape[1] != kernel.shape[1]):
			#	pass
			#else:
			k = (roi * kernel).sum()
			output[v-pad, w-pad] = k

	output = (output * 255.0) / output.max()
	return output.astype('uint8')

def kernel_transform(kernel):
	k = np.zeros_like(kernel)
	for i in range(kernel.shape[0]):
		for j in range(kernel.shape[1]):
			k[i][j] = kernel[kernel.shape[0]-i-1][kernel.shape[1]-j-1]
	return k

def conv2(image, kernel):
	(height, width) = image.shape
	(heightK, widthK) = kernel.shape
	output = np.zeros_like(image)

	pad_h = heightK // 2
	pad_w = widthK // 2

	for v in range(pad_h, height-pad_h):
		for w in range(pad_w, width-pad_w):
			s = 0
			for i in range(heightK):
				for j in range(widthK):
					s += kernel[i][j] * image[v-pad_h+i][w-pad_h+j]

			output[v][w] = s

	output = (output * 255.0) / output.max()
	return output.astype('uint8')

def mean_filter(image, size):
	f = np.ones((size, size))*(1.0/(size*size))
	return conv(image, f) 

## AJEITAR
def laplacian_filter(image):
	f = np.array((
		[0, 1, 0],
		[1, -4, 1],
		[0, 1, 0]))
	f = np.array((
		[-1, -1, -1],
		[-1, 8, -1],
		[-1, -1, -1]))
	return conv(image, f)

def sobel_filter(image):
	fh = np.array((
		[1, 2, 1],
		[0, 0, 0],
		[-1, -2, -1]))

	fv = np.array((
		[-1, 0, 1],
		[-2, 0, 2],
		[-1, 0, 1]))

	horizontal = conv(image, fh)
	vertical = conv(image, fv)

	#G = sqrt(horizonal² + vertical²)
	output = np.sqrt(np.square(horizontal) + np.square(vertical))
	output = (output * 255.0) / output.max()
	return output.astype('uint8')

def median_filter(image, filter_size):
	(height, width) = image.shape
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

			neighbors.sort()
			output[v,w] = neighbors[len(neighbors) // 2]

	return output.astype('uint8')


def sepia_filter(image):
	img = np.asarray(image)

	lmap = np.matrix([[ 0.393, 0.769, 0.189 ],
					  [ 0.349, 0.686, 0.168 ],
					  [ 0.272, 0.534, 0.131 ]])
	
	output = np.array([x * lmap.T for x in img])
	output[np.where(output > 255)] = 255
	output = np.reshape(output, image.shape)

	return output.astype('uint8')

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

			if tr > 255: tr = 255
			if tg > 255: tg = 255
			if tb > 255: tb = 255

			output[v,w] = tr, tg, tb

	return output.astype('uint8')"""

if __name__ == '__main__':
	i = imageio.imread('images/hamster.jpeg')
	#i = rgb2gray(i)
	#i = np.ones((10,10))
	#hist = histogram(i, 256)
	#it = equalize_hist(i, hist)
	#histeq = histogram(it, 256)
	#subplot_hist(hist, histeq)
	#subplot_img(i, it)
	#subplot(histogram(i, 256), histogram(it, 256))
	#it = mean_filter(i, 35)
	it = sepia_filter(i)
	#it = laplacian_filter(i)
	#hist = histogram(it)
	#it = equalize_hist(it, hist)
	#it = median_filter(i, 3)
	#it = sobel_filter(i)
	subplot_img(i, it)
