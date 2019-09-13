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
			igray[v][w] = int(gray[v][w])
	return igray

def imshow(img):
	plt.imshow(img, cmap=plt.get_cmap(name='gray'))
	plt.show()

def negative_transform(img):
	return 255 - img

def log_transform(img, c):
	return c * np.log(1 + img)

def gamma_transform(img, c, gama):
	return c * np.power(img, gama)

#TODO: implementar transformaçao linear
#def linear_transform(i):

def histogram(img):
	hist = [0]*256 
	for v in range(img.shape[0]): 	#height
		for w in range(img.shape[1]):	#width
			pxl = img[v][w]
			hist[pxl] += 1
	return hist

#TODO: implementar transformada de Fourier
#def ft(img):
#	fn = np.zeros(img.shape)
#	for v in range(img.shape[0]):
#		for w in range(img.shape[1]):
			
if __name__ == '__main__':
	i = imageio.imread('images/einstein.jpeg')
	i = rgb2gray(i)
	#it = log_transform(i, 1)
	#it = negative_transform(i)
	#it = gamma_transform(i, 1, 3)
	hist = histogram(i)
	plt.hist(i.ravel(),256,[0,256]); plt.show()
	plt.hist(hist); plt.show()
	#imshow(i)
	