import math
import numpy as np
from PIL import ImageTk, Image, ImageDraw


def is_grey_scale(image):
        img = image
        w,h = img.size
        for i in range(w):
            for j in range(h):
                r,g,b = img.getpixel((i,j))
                if r != g != b: return False
        return True

def rgb2gray(image):
    if len(image.shape) == 2:  # Check if image is already grayscale
        return image
    else:
        return np.dot(image[..., :3], [0.298936, 0.587043, 0.114021])


# Convert RGB image to grayscale using arithmetic average
def rgb2gray_avg(r, g, b):
    return (r + g + b) / 3


# Convert RGB colors to HSV
def rgb2hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, s, v = 0, 0, 0
    maximo = max(r, g, b)
    minimo = min(r, g, b)
    dif = maximo - minimo

    v = maximo

    if dif == 0:
        h = 0
        s = 0
    else:
        s = dif / maximo

        dr = ((maximo - r)/6 + (dif/2))/dif
        dg = ((maximo - g)/6 + (dif/2))/dif
        db = ((maximo - b)/6 + (dif/2))/dif

        if r == maximo:
            h = db - dg
        elif g == maximo:
            h = (1/3) + dr - db
        elif b == maximo:
            h = (2/3) + dg - dr

        if h < 0:
            h = h + 1
        if h > 1:
            h = h - 1

    return (h*360, s*100, v*100)


# Convert HSV colors to RGB
def hsv2rgb(h, s, v):
    h, s, v = float(h), float(s), float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p, q, t = int(255*v*(1.-s)), int(255*v*(1.-s*f)), int(255*v*(1.-s*(1.-f)))
    v = int(v*255)
    if hi == 0:
        return (v, t, p)
    if hi == 1:
        return (q, v, p)
    if hi == 2:
        return (p, v, t)
    if hi == 3:
        return (p, q, v)
    if hi == 4:
        return (t, p, v)
    if hi == 5:
        return (v, p, q)

def imgrgb2hsv(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            r, g, b = img[i,j,0], img[i,j,1], img[i,j,2]
            h, s, v = rgb2hsv(r,g,b)
            img[i,j,0], img[i,j,1], img[i,j,2] = h, s, v
    return img

def imghsv2rgb(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            h, s, v = img[i,j,0], img[i,j,1], img[i,j,2]
            r, g, b = hsv2rgb(h,s/100,v/100)
            img[i,j,0], img[i,j,1], img[i,j,2] = r, g, b
    return img

def imgrgb2hsv_boost(img, boost):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            r, g, b = img[i,j,0], img[i,j,1], img[i,j,2]
            h, s, v = rgb2hsv(r,g,b)
            img[i,j,0], img[i,j,1], img[i,j,2] = h, s, (v*boost)
            if img[i,j,2] > 100:
                img[i,j,2] = 100
    return img

def dist(x0, y0, x1, y1):
    a = (x1 - x0)**2 + (y1 - y0)**2
    b = math.sqrt(a)
    return b

def chroma_key(img, imgfundo, cr,cg,cb, faixa):
    print("Frente:\n",img.shape)
    print("Trás:\n",imgfundo.shape)
    print("RGB:",cr,cg,cb)
    imgfinal = img
    for i in range(imgfinal.shape[0]):
        for j in range(imgfinal.shape[1]):
            r, g, b = imgfinal[i,j,0], imgfinal[i,j,1], imgfinal[i,j,2]
            distr = dist(0,0,r,cr)
            distg = dist(0,0,r,cr)
            distb = dist(0,0,r,cr)
            if (r == cr and g == cg and b == cb) or (distr < faixa and distg < faixa and distb < faixa):
                #print("ACHOU!")
                imgfinal[i,j,0] = imgfundo[i,j,0] 
                imgfinal[i,j,1] = imgfundo[i,j,1]
                imgfinal[i,j,2] = imgfundo[i,j,2]
    print(imgfinal.shape)    
    return imgfinal

def aumentarbrilho(img, amount):
    boost = amount/100
    print("Imagem RGB:\n",img.shape)
    imghsv = imgrgb2hsv_boost(img, boost)
    imgrgb = imghsv2rgb(imghsv)  
    return imgrgb

if __name__ == '__main__':
    img = Image.open('images/face_rgb.jpeg')
    cor = np.array(img)
    print("imagem frente: ",cor)
    img = Image.open('images/forest.jpeg')
    cornova = np.array(img)
    print("imagem trás: ",cornova)

    i = chroma_key(cor, cornova, 112, 69, 53, 0)
    print("IMAGEM NOVA: ",i)
    #print(rgb2hsv(255, 0, 0))  # red
    #print(rgb2hsv(0, 255, 0))  # green
    #print(hsv2rgb(240, 1, 1))  # blue
    #print(hsv2rgb(300, 1, 1))  # magenta
