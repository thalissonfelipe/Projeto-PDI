import imageio
import util
import matplotlib.pyplot as plt
import sys
import numpy as np
import colors as cl

def compact_vizinhos(image):
    comp_image = cl.imgrgb2hsvC(image)
    imgh = ''
    imgs = ''
    imgv = ''
    for row in range(0,comp_image.shape[0],2):
        for col in range(0,comp_image.shape[1],2):
            imgh = imgh + str(comp_image[row,col,0]) + ","
            imgs = imgs + str(comp_image[row,col,1]) + ","
            imgv = imgv + str(comp_image[row,col,2]) + "," + str(comp_image[row+1,col,2]) + "," + str(comp_image[row,col+1,2]) + "," + str(comp_image[row+1,col+1,2]) + ","
    
    imgv = np.fromstring(imgv, dtype=int, sep=",")
    imgh = np.fromstring(imgh, dtype=int, sep=",")
    imgs = np.fromstring(imgs, dtype=int, sep=",")
    #print(imgv[0:1000])
    #print(imgh[len(imgh)-100:len(imgh)])
    #print(imgs[len(imgs)-100:len(imgs)])
    return (imgv,imgh, imgs)

def decompact_vizinhos(img,size):
    #print(img)
    image = np.zeros((size[0], size[1],3), dtype=np.uint8)
    TAM = len(img)-1 
    row = 0
    col = 0
    #print(size[0], size[1], TAM)
    for k in range(0,TAM-1,6):

        h = img[k]
        s = img[k+1]

        image[row,col,0] = h*3.6
        image[row+1,col,0] = h*3.6
        image[row,col+1,0] = h*3.6
        image[row+1,col+1,0] = h*3.6
        image[row,col,1] = s
        image[row+1,col,1] = s
        image[row,col+1,1] = s
        image[row+1,col+1,1] = s
        image[row,col,2] = img[k+2]
        image[row+1,col,2] = img[k+3]
        image[row,col+1,2] = img[k+4]
        image[row+1,col+1,2] = img[k+5]

        if col < (size[1]-2):
            col += 2
        elif row < (size[0]-2):
            row += 2
            col = 0

    image = cl.imghsv2rgb(image)
    return image


def run_length_encode(image, file):
    (x,y,z) = compact_vizinhos(image)
    file = file + '.ith'
    f = open(file, 'w')
    f.write(str(image.shape[0]) + '_' + str(image.shape[1]) + '\n')
    f.close()

    f = open(file, 'ab')
    count = 1
    countIsBiggerThan255 = False
    for index in range(len(x)):
        if (index + 1) < len(x) and x[index] == x[index+1] and not countIsBiggerThan255:
            count += 1
            if count == 255:
                countIsBiggerThan255 = True
        else:
            f.write(bytes([x[index]]))
            f.write(bytes([count]))
            count = 1
            countIsBiggerThan255 = False

    count = 1
    countIsBiggerThan255 = False
    for index in range(len(y)):
        if (index + 1) < len(y) and y[index] == y[index+1] and not countIsBiggerThan255:
            count += 1
            if count == 255:
                countIsBiggerThan255 = True
        else:
            f.write(bytes([y[index]]))
            f.write(bytes([count]))
            count = 1
            countIsBiggerThan255 = False

    count = 1
    countIsBiggerThan255 = False
    for index in range(len(z)):
        if (index + 1) < len(z) and z[index] == z[index+1] and not countIsBiggerThan255:
            count += 1
            if count == 255:
                countIsBiggerThan255 = True
        else:
            f.write(bytes([z[index]]))
            f.write(bytes([count]))
            count = 1
            countIsBiggerThan255 = False

    f.close()


def run_length_decode(filename):
    f = open(filename, 'r', errors='ignore')
    shape = f.readline()
    f.close()
    n = len(shape)+1
    shape = [int(x) for x in (shape.replace('\n', '')).split('_')]
    #n = 8
    #print(shape)

    f = open(filename, 'rb')
    content = f.read()
    content = content[n:len(content)]

    data = []
    for byte in content:
        data.append(byte)

    #print(data[0:100])
    newData = []
    for i in range(0, len(data)-1, 2):
        for j in range(data[i+1]):
            newData.append(data[i])
    #print(newData[355199])

    #print('Size newData:', len(newData))
    tamX = int(len(newData) * (4/6))
    tamY = int(len(newData) * (1/6))
    #tamZ = tamY
    
    output = []
    f.close()
    k = 0
    for index in range(0,tamX,4):
        #print(index)
        output.append(newData[k+tamX])
        #print(k+tamX+tamY)
        output.append(newData[k+tamX+tamY])
        output.append(newData[index])
        output.append(newData[index+1])
        output.append(newData[index+2])
        output.append(newData[index+3])
        k += 1

    #print(output[0:200])
    imagem = decompact_vizinhos(output,shape)
    return imagem


if __name__ == '__main__':
    img = imageio.imread('images/benchmark.bmp')
    #img_hsv = cl.imgrgb2hsv(img)
    #print('Shape:', img_hsv.shape)
    #h, s, v = util.split(img_hsv)
    #run_length_encode(img,'testefinal')
    it = run_length_decode('testefinal.ith')
    #it = util.merge(h, nS, nV)
    #img_rgb = cl.imghsv2rgb(it)
    util.subplot_img(img, it)