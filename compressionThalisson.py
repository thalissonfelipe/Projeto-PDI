import imageio
import util
import matplotlib.pyplot as plt
import sys
import numpy as np
import colors as cl


def ith_compact(image):
    print(image.shape)
    imagehsv = cl.imgrgb2hsvC(image)
    print("IMAGEM HSV: ",imagehsv)
    comp_image = np.zeros((imagehsv.shape[0], imagehsv.shape[1],2), dtype=np.uint8)

    p = 0
    count = 0
    for row in range(imagehsv.shape[0]):
        for col in range(imagehsv.shape[1]):

            h = imagehsv[row,col,0]
            s = imagehsv[row,col,1]
            i = 0 #0b00000000
            if (h == 0) and (s == 0):
                hs = 0
            elif h == s:
                count += 1
                i = 128 #0xb10000000

            else:
                h = int(round(h/5))
                s = int(round(s/5))
                hs = h
                hs = hs>>1
                hs = hs<<4
                aux = s>>1
                hs = hs + aux
            imagehsv[row,col,2] = imagehsv[row,col,2] + i
            comp_image[row,col,1] = hs

            p += 1
    comp_image[:,:,0] = imagehsv[:,:,2]
    print(comp_image)
    return comp_image

def decompact_ith(comp_image,size):
    #print(imagehsv)
    image = np.zeros((size[0], size[1],3), dtype=np.uint8)
    #comp_image[:,:,0] = imagehsv[:,:,2]   
    row = 0
    col = 0
    print(size[0], size[1])
    #print(ord(comp_image[TAM]))
    p = 0
    print(len(comp_image))
    for k in range(0,len(comp_image)-1,2):
        #print(k)
        #print(k, row, col)
        #if k>20:
        #    break
        v = comp_image[k]
        #print(v)
        #print("V:",v)
        hs = comp_image[k+1]
        #print(hs)
        #print("HS: ",hs)
        if hs == 0:
            h = 0
            s = 0
        elif v >= 128:
            v = v - 128
            h = hs
            s = h
        else:
            h_aux = hs
            s_aux = hs
            h_aux = h_aux>>4
            h = h_aux<<1
            s_aux = s_aux - (h<<3)
            s = s_aux<<1
            h = h*5
            s = s*5

        #print("H:",h)
        #print("S:",s)
        image[row,col,0] = h*3.6
        image[row,col,1] = s
        image[row,col,2] = v
        #print("HSV: ",h,s,v)
        #print(row,col)
        if col < (size[1]-1):
            col += 1
        elif row < (size[0]-1):
            row += 1
            col = 0
        else:
            break
        old_h = h
        old_s = s
        p += 1
    print(image)
    image = cl.imghsv2rgb(image)
    print("SIZE: ",image.shape)
    #image = imgrgb2hsv_boostHSV(image, 0.8, 1, 1)
    #image = imghsv2rgb(image)
    #for row in range(size[0]):
    #    for col in range(size[1]):
    #image = imghsv2rgb(imagehsv)
    return image

def run_length_encode(image):
    img = ith_compact(image)
    x = img[:,:,0]
    y = img[:,:,1]

    f = open('output2.ith', 'w')
    f.write(str(image.shape[0]) + '_' + str(image.shape[1]) + '\n')
    f.close()

    f = open('output2.ith', 'ab')
    count = 1
    countIsBiggerThan255 = False

    for row in range(x.shape[0]):
        for col in range(x.shape[1]):
            if (col + 1) < x.shape[1] and x[row, col] == x[row, col+1] and not countIsBiggerThan255:
                count += 1
                if count == 255:
                    countIsBiggerThan255 = True
            else:
                f.write(int(x[row, col]).to_bytes(1, sys.byteorder))
                f.write(count.to_bytes(1, sys.byteorder))
                count = 1
                countIsBiggerThan255 = False

    count = 1
    countIsBiggerThan255 = False
    
    for row in range(y.shape[0]):
        for col in range(y.shape[1]):
            if (col + 1) < y.shape[1] and y[row, col] == y[row, col+1] and not countIsBiggerThan255:
                count += 1
                if count == 255:
                    countIsBiggerThan255 = True
            else:
                f.write(int(y[row, col]).to_bytes(1, sys.byteorder))
                f.write(count.to_bytes(1, sys.byteorder))
                count = 1
                countIsBiggerThan255 = False
    f.close()


def run_length_decode(filename):
    f = open(filename, 'r')
    shape = f.readline()
    f.close()
    n = len(shape)+1
    shape = [int(x) for x in (shape.replace('\n', '')).split('_')]

    f = open('output2.ith', 'rb')
    content = f.read()
    content = content[n:len(content)]
    f.close()
    print(shape)
    
    data = []
    for byte in content:
        data.append(byte)

    print(data[0:100])

    newData = []
    for i in range(0, len(data)-1, 2):
        for j in range(data[i+1]):
            newData.append(data[i])
    print(newData[0:100])

    print('Size newData:', len(newData))

    image = decompact_ith(newData,shape)
    return image


if __name__ == '__main__':
    img = imageio.imread('images/benchmark.bmp')
    #img_hsv = cl.imgrgb2hsv(img)
    #print('Shape:', img_hsv.shape)
    # print('Size:', img.shape[0]*img.shape[1])
    #h, s, v = util.split(img_hsv)
    
    #run_length_encode(img)
    it = run_length_decode('output.ith')
    #it = util.merge(h, nS, nV)
    # img_rgb = cl.imghsv2rgb(it)
    util.subplot_img(img, it)