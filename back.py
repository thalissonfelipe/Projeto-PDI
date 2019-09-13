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

def equalizeHist(hist):
	n = len(hist)
	prob = [0]*n
	proba = [0]*n
	hist_equalizado = [0]*n
	total_pxl = 0

	for h in hist:
		total_pxl += h 

	prob[0] = hist[0]/total_pxl
	proba[0] = prob[0]
	for i in range(1, n):
		prob[i] = hist[i]/total_pxl
		proba[i] = prob[i] + proba[i-1]

	hist_equalizado = [int(i*255) for i in proba]
	return hist_equalizado

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
	hist_equalizado = equalizeHist(hist)
	#plt.hist(i.ravel(),256,[0,256]); plt.show()
	plt.hist(hist_equalizado); plt.show()
	#imshow(i)
	