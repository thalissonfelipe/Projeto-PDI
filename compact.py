import imageio
import util
from PIL import ImageTk, Image, ImageDraw
import cv2
import numpy as np
import matplotlib.pyplot as plt
from colors import rgb2gray, rgb2hsv, rgb2hsvC, hsv2rgb, imghsv2rgb, imgrgb2hsv, imgrgb2hsvC,imgrgb2hsv_boostHSV
plt.rcParams['figure.figsize'] = (15, 15)


MAX_PIXEL = 255
DADOS = ''

#COMPACTAÇÃO
def ith_compact(image):
    print(image.shape)
    imagehsv = imgrgb2hsvC(image)
    print("IMAGEM HSV: ",imagehsv)
    comp_image = np.zeros((imagehsv.shape[0], imagehsv.shape[1],2), dtype=np.uint8)
    #comp_image[:,:,0] = imagehsv[:,:,2]
    p = 0
    count = 0
    for row in range(imagehsv.shape[0]):
        for col in range(imagehsv.shape[1]):
            #print(p)
            h = imagehsv[row,col,0]
            s = imagehsv[row,col,1]
            i = 0 #0b00000000
            if (h == 0) and (s == 0):
                hs = 0
            elif h == s:
                count += 1
                i = 128 #0xb10000000
            #print(p % 2)
            else:
                h = int(round(h/5))
                s = int(round(s/5))
                hs = h
                hs = hs>>1
                hs = hs<<4
                aux = s>>1
                hs = hs + aux
            imagehsv[row,col,2] = imagehsv[row,col,2] + i
            #hs = bin(hs)5
            #print("INT: ",h>>7, s)
            #print("Bin: ",bin(hs))
            comp_image[row,col,1] = hs
            #print("HSV: ",h,s,imagehsv[row,col,2])
            #print("HS : ",hs)
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",comp_image[row,col,1])
            #comp_image[row,col,1] = image[row,col,1]
            p += 1
    comp_image[:,:,0] = imagehsv[:,:,2]
    print(comp_image)
    return comp_image

def filecompact_ith(image, file):
    comp_image = ith_compact(image)
    file = file + ".ith"
    try:
        f = open(file, 'w+', encoding="utf-8")
        f.write("%d_%d|"% (int(comp_image.shape[0]),int(comp_image.shape[1])))
        for row in range(comp_image.shape[0]):
            for col in range(comp_image.shape[1]):
                f.write("%c%c" % (chr(comp_image[row,col,0]),chr(comp_image[row,col,1])))
    finally:
        f.close()

def filecompact_vizinhos(image, file):
    comp_image = imgrgb2hsvC(image)
    file = file + ".ith"
    try:
        f = open(file, 'w+', encoding="utf-8")
        f.write("%d_%d|"% (int(comp_image.shape[0]),int(comp_image.shape[1])))
        for row in range(0,comp_image.shape[0],2):
            for col in range(0,comp_image.shape[1],2):
                f.write("%c%c" % (chr(comp_image[row,col,0]),chr(comp_image[row,col,1])))
                f.write("%c%c%c%c" % (chr(comp_image[row,col,2]),chr(comp_image[row+1,col,2]),chr(comp_image[row,col+1,2]),chr(comp_image[row+1,col+1,2])))
    finally:
        f.close()

def runlength_encode(image,file):
    comp_image = ith_compact(image)
    print(comp_image)
    file = file + ".ith"
    try:
        f = open(file, 'w+', encoding="utf-8")
        f.write("%d_%d|"% (int(comp_image.shape[0]),int(comp_image.shape[1])))
        count = 1
        p = 0
        c = 0
        s = ''
        print(comp_image[0,0,0])
        for row in range(comp_image.shape[0]):
            for col in range(comp_image.shape[1]):
                p += 1
                #print("POSIÇÃO: ", row,col)
                if (col+1) < comp_image.shape[1] and comp_image[row,col,0] == comp_image[row,col+1,0]:
                    count += 1
                    #print("elemento: ", comp_image[row,col,0], " contador: ",count)
                else:
                    #print(comp_image[row,col,0], count)
                    c += count
                    s = s + str(comp_image[row,col,0]) + "," + str(count) + ","
                    #print("valor %d: %d" % (int(comp_image[row,col,0]),int(count)))
                    f.write("%d,%d," % (comp_image[row,col,0],count))
                    count = 1
            #f.write("%d"%0)
        print(p,c)
        print(len(s))
        #imgrec = np.fromstring(s, dtype=int, sep=",")
        #return imgrec
        #f.write("|")
        #count = 1
        #for row in range(comp_image.shape[0]):
        #    for col in range(comp_image.shape[1]-1):
        #        print("POSIÇÃO: ", row,col)
        #        if comp_image[row,col,1] == comp_image[row,col+1,1]:
        #            print("elemento: ", comp_image[row,col,1], " contador: ",count)
        #            count += 1
        #        else:
        #            print("valor %d: %d" % (int(comp_image[row,col,1]),int(count)))
        #            f.write("%c%c" % (chr(comp_image[row,col,1]),chr(count)))
        #            count = 1
    finally:
        f.close()

#DECOMPACTAÇÃO
def decompact_ith(comp_image,size):
    #print(imagehsv)
    image = np.zeros((size[0], size[1],3), dtype=np.uint8)
    #comp_image[:,:,0] = imagehsv[:,:,2]   
    init = 0
    for i in range(len(comp_image)):
        if comp_image[i] == '|':
            init = i+1
            break
    TAM = (size[0]*size[1])*2 + init-1
    row = 0
    col = 0
    old_s = ord(comp_image[init+3])
    old_h = ord(comp_image[init+1])
    print(size[0], size[1])
    #print(ord(comp_image[TAM]))
    p = 0
    for k in range(init,TAM,2):
        #print(k)
        #print(k, row, col)
        v = ord(comp_image[k])
        #print("V:",v)
        hs = ord(comp_image[k+1])
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
        if col < (size[1]-1):
            col += 1
        elif row < (size[0]-1):
            row += 1
            col = 0
        old_h = h
        old_s = s
        p += 1
    print(image)
    image = imghsv2rgb(image)
    print("SIZE: ",image.shape)
    #image = imgrgb2hsv_boostHSV(image, 0.8, 1, 1)
    #image = imghsv2rgb(image)
    #for row in range(size[0]):
    #    for col in range(size[1]):
    #image = imghsv2rgb(imagehsv)
    return image

def filedecompact_ith(image):
    try:
        f = open(image, 'r', encoding="utf-8")
        content = f.read()
        #print(content)
        dim = np.fromstring(content, dtype=int, sep="_")
        print(dim)
        image = decompact_ith(content,dim)
        return image
    finally:
        f.close()

def filedecompact_vizinhos(file):
    try:
        f = open(file, 'r', encoding="utf-8")
        content = f.read()
        #print(content)
        dim = np.fromstring(content, dtype=int, sep="_")
        print(dim)
        size = dim
        comp_image = content
        image = np.zeros((size[0], size[1],3), dtype=np.uint8)
        #comp_image[:,:,0] = imagehsv[:,:,2]   
        init = 0
        for i in range(len(comp_image)):
            if comp_image[i] == '|':
                init = i+1
                break
        TAM = (size[0]*size[1])*3 + init-1
        row = 0
        col = 0
        old_s = ord(comp_image[init+3])
        old_h = ord(comp_image[init+1])
        print(size[0], size[1], TAM)
        for k in range(init,TAM,6):
            #print(ord(comp_image[int(TAM/2)+1]))
            #print(k, row, col)
            h = ord(comp_image[k])
            #print("V:",v)
            s = ord(comp_image[k+1])

            image[row,col,0] = h*3.6
            image[row+1,col,0] = h*3.6
            image[row,col+1,0] = h*3.6
            image[row+1,col+1,0] = h*3.6
            image[row,col,1] = s
            image[row+1,col,1] = s
            image[row,col+1,1] = s
            image[row+1,col+1,1] = s
            image[row,col,2] = ord(comp_image[k+2])
            image[row+1,col,2] = ord(comp_image[k+3])
            image[row,col+1,2] = ord(comp_image[k+4])
            image[row+1,col+1,2] = ord(comp_image[k+5])
            if col < (size[1]-2):
                col += 2
            elif row < (size[0]-2):
                row += 2
                col = 0
            else:
                break
            print(row,col)
        image = imghsv2rgb(image)
        return image
    finally:
        f.close()

def filedecompact_runlength(image):
    try:
        f = open(image, 'r', encoding="utf-8")
        content = f.read()
        #print(content)
        dim = np.fromstring(content, dtype=int, sep="_")
        print(dim)
        size = dim
        comp_image = content
        image = np.zeros((size[0], size[1]), dtype=np.uint8)   
        init = 0
        for i in range(len(comp_image)):
            if comp_image[i] == '|':
                init = i+1
                break
        TAM = len(comp_image)
        comp_image = comp_image[init:TAM]
        print(comp_image)
        comp_image = np.fromstring(comp_image, dtype=int, sep=",")
        print(comp_image)
        pxl = 0
        count = 0
        print(init)
        print(len(comp_image), TAM)
        x = 0
        p = 0
        s = ''
        #print(decode)
        #print(decode)
        #for k in range(len(comp_image)):
        #    x += 1
        #    if k%2 == 0:
        #        pxl = ord(comp_image[k])
        #        s = s + str(pxl) + ","
        #    else:
        #        count = ord(comp_image[k])
        #        p += count
        #        s = s + str(count) + ","
        print(len(s), size[0], size[1])
        #imgrec = np.fromstring(s, dtype=int, sep=",")
        imgrec = comp_image
        row = 0
        col = 0
        for pixel in range(0,len(imgrec)-1,2):
            #print("POSIÇÃO: ", row,col)         
            valor = imgrec[pixel]
            #print(valor)
            contador = imgrec[pixel+1]
            #print(contador)
            for c in range(contador):
                #print(row,col)             
                image[row,col] = valor
                #print(image[row,col], contador)
                if col < (size[1]-1):
                    col += 1
                elif row < (size[0]-1):
                    row += 1
                    col = 0
        #print(image.shape, x, p)
        print(image)
        return image
    finally:
        f.close()

if __name__ == '__main__':
    i = imageio.imread('images/benchmark.bmp')
    url = 'imgcomp.ith'
    print("original: ",i)
    #i = rgb2gray(i)
    #it = equalize_hist(i)
    #it = sharpen_filter(i)]
    i = np.array(i)

    print(i.shape[0])
    print(i.shape[1])
    print(ord(chr(440)))
    #h = 0
    #s = 66
    #hs = int(round(h/5))
    #hs = hs>>1
    #print("H>>1: ",hs)
    #hs = hs<<4
    #print("H<<4: ",hs)
    #aux = int(round(s/5))
    #aux = aux>>1
    #print("S>>1: ",aux)
    #hs = hs + aux
    #print("HS: ",hs)
    ####################
    #hs = 44
    #h_aux = hs
    #s_aux = hs
    #h_aux = h_aux>>4
    #print("HS>>4", h_aux)
    #h = h_aux<<1
    #print("H : ", h*5)
    #s_aux = s_aux - (h<<3)
    #print(s_aux)
    #s = s_aux<<1
    #print("S : ", s*5)
    #print("NP: ",i)
    #print(ord(chr(13)))
    #print(ord(chr(1000)))
    #dadosencode = runlength_encode(i,'testetop')
    it = filedecompact_runlength('testetop.ith')
    ih = imgrgb2hsv(i)
    
    for row in range(it.shape[0]):
        for col in range(it.shape[1]):
            if it[row,col] >= 128:
                it[row,col] = it[row,col] - 128
    ih[:,:,2] = it
    i = imghsv2rgb(ih)
    #dadosdecode = it
    #c = 0
    #for k in range(len(dadosencode)):
    #    if dadosencode[k] != dadosdecode[k] and k%2 == 0:
    #        print(k)
            #print(k)
    #        print("VALOR DIV: ", dadosencode[k],"/",dadosdecode[k])   
    #    elif dadosencode[k] != dadosdecode[k] and k%2 != 0:
    #        c += dadosencode[k] - dadosdecode[k]
            #print(k)
            #print("COUNT DIV: ", dadosencode[k],"/",dadosdecode[k])
    #print(c)
    #print("ENCODE: ",dadosencode[5142:5460])
    #print("DECODE: ",dadosdecode[5142:5460])
    plt.imshow(i)
    plt.show()
    #img = imgrgb2hsv(i)
    #img[:,:,2] = it
    #it = imghsv2rgb(img)

        #else:
            #print("DADOS IGUAIS")
    
    
    #print(it)
    #print("COMPACTADA: ",it)
    #it = Image.fromarray(it)
    #it.save("images/teste.bmp")
