import math
import numpy as np

## Convert RGB image to grayscale using weighted average
def rgb2gray(r, g, b):
	return (r * 0.298936) + (g * 0.587043) + (b * 0.114021)

## Convert RGB image to grayscale using arithmetic average
def rgb2gray_avg(r, g, b):
	return (r + g + b) / 3

## Convert RGB colors to HSV
def rgb2hsv(r, g, b):
	r, g, b = r / 255.0, g / 255.0, b / 255.0
	h, s, v = 0, 0, 0
	maximo = max(r, g, b)
	minimo = min(r, g, b)
	dif = maximo - minimo

	if maximo == minimo:
		h = 0
	elif maximo == r:
		h = (60 * ((g - b) / dif) + 360) % 360
	elif maximo == g:
		h = (60 * ((b - r) / dif) + 120) % 360
	elif maximo == b:
		s = 0
	else:
		s = (dif / maximo) * 100
	v = maximo * 100

	return (h, s, v)

## Convert HSV colors to RGB
def hsv2rgb(h, s, v):
	h, s, v = float(h), float(s), float(v)
	h60 = h / 60.0
	h60f = math.floor(h60)
	hi = int(h60f) % 6
	f = h60 - h60f
	p,q,t = int(255*v*(1.-s)), int(255*v*(1.-s*f)), int(255*v*(1.-s*(1.-f))) 
	v = int(255*v)
	if hi == 0: return (v, t, p)
	if hi == 1: return (q, v, p)
	if hi == 2: return (p, v, t)
	if hi == 3: return (p, q, v)
	if hi == 4: return (t, p, v)
	if hi == 5: return (v, p, q)


if __name__ == '__main__':
	print(rgb2hsv(255, 0, 0)) #red
	print(rgb2hsv(0, 255, 0)) #green
	print(hsv2rgb(240, 1, 1)) #blue
	print(hsv2rgb(300, 1, 1)) #magenta