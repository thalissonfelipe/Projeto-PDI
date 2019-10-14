import imageio
import cv2
import numpy as np
import matplotlib.pyplot as plt
from util import subplot_img, imshow
from colors import rgb2gray
from PIL import Image


# Only Grayscale Image
def nnscale(image, newHeight, newWidth):
    height, width = image.shape
    outputShape = list(map(int, [newHeight, newWidth]))
    output = np.zeros(outputShape[0] * outputShape[1], dtype=np.uint8)
    image = (np.asarray(image)).flatten()
    x_ratio = width / outputShape[1]
    y_ratio = height / outputShape[0]
    for row in range(outputShape[0]):
        for col in range(outputShape[1]):
            px = np.floor(col * x_ratio)
            py = np.floor(row * y_ratio)
            output[(row*outputShape[1])+col] = image[(int)((py*width)+px)]

    output = np.reshape(output, outputShape)
    return output


def getBilinearPixel(imArr, posX, posY):
    out = []

    # Get integer and fractional parts of numbers
    modXi = int(posX)
    modYi = int(posY)
    modXf = posX - modXi
    modYf = posY - modYi
    modXiPlusOneLim = min(modXi+1,imArr.shape[1]-1)
    modYiPlusOneLim = min(modYi+1,imArr.shape[0]-1)

    # Get pixels in four corners
    if len(imArr.shape) == 3:
        for chan in range(imArr.shape[2]):
            bl = imArr[modYi, modXi, chan]
            br = imArr[modYi, modXiPlusOneLim, chan]
            tl = imArr[modYiPlusOneLim, modXi, chan]
            tr = imArr[modYiPlusOneLim, modXiPlusOneLim, chan]

            # Calculate interpolation
            b = modXf * br + (1. - modXf) * bl
            t = modXf * tr + (1. - modXf) * tl
            pxf = modYf * t + (1. - modYf) * b
            out.append(int(pxf + 0.5))
        return out
    else:
        bl = imArr[modYi, modXi]
        br = imArr[modYi, modXiPlusOneLim]
        tl = imArr[modYiPlusOneLim, modXi]
        tr = imArr[modYiPlusOneLim, modXiPlusOneLim]

        # Calculate interpolation
        b = modXf * br + (1. - modXf) * bl
        t = modXf * tr + (1. - modXf) * tl
        pxf = modYf * t + (1. - modYf) * b
        return int(pxf + 0.5)
    

# RGB and Grayscale Image
def bilinearScale(image, newHeight, newWidth):
    height, width = image.shape[:2]
    if len(image.shape) == 3:
        outputShape = list(map(int, [newHeight, newWidth, image.shape[2]]))
        output = np.empty(outputShape, dtype=np.uint8)
    else:
        outputShape = list(map(int, [newHeight, newWidth]))
        output = np.empty(outputShape, dtype=np.uint8)

    rowScale = float(height) / float(output.shape[0])
    colScale = float(width) / float(output.shape[1])
 
    for row in range(output.shape[0]):
        for col in range(output.shape[1]):
            orir = row * rowScale  # Find position in original image
            oric = col * colScale
            output[row, col] = getBilinearPixel(image, oric, orir)
    
    return output


def nnrotate(image, angle):
    height, width = image.shape[:2]
    output = np.zeros_like(image, dtype=np.uint8)
    angle = angle * np.pi / 180

    for x in range(width):
        for y in range(height):
            i = int(x+angle)
            j = int(y+angle)
            print(i,j)
            output[x,y] = image[i,j]

    return output


# RGB and Grayscale Image
def bilinearRotate(image, angle):
    width, height = image.shape[:2]
    output = np.zeros_like(image, dtype=np.uint8)
    angle = angle * np.pi / 180 
    center_x = width / 2
    center_y = height / 2

    for x in range(width):
        for y in range(height):
            xp = int((x - center_x) * np.cos(angle) - (y - center_y) * np.sin(angle) + center_x)
            yp = int((x - center_x) * np.sin(angle) + (y - center_y) * np.cos(angle) + center_y)
            if 0 <= xp < width and 0 <= yp < height:
                output[x, y] = i[xp, yp]

    return output


if __name__ == '__main__':
    filename = 'einstein'
    path = 'images/' + filename + '.jpeg'
    i = imageio.imread(path)
    i = rgb2gray(i)
    print('Shape: ', i.shape)
    #it = bilinearRotate(i, 30)
    #it = nnscale(i, i.shape[0]*1.5, i.shape[1]*1.5)
    it = nnrotate(i, 30)
    print('New shape: ', it.shape)
    #imshow(it)
    #it2 = image.rotate(30)
    #it = resizeBilinearInterpolation(i, i.shape[0]+50, i.shape[1]+50)
    #cv2.imshow('ImageWindow', cv2.cvtColor(it, cv2.COLOR_BGR2RGB))
    #cv2.waitKey()
    #cv2.imshow('ImageWindow', cv2.cvtColor(i, cv2.COLOR_BGR2RGB))
    #cv2.waitKey()
    subplot_img(i, it)