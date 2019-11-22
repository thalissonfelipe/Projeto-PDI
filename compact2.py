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
    for row in range(imagehsv.shape[0]):
        for col in range(imagehsv.shape[1]):
            #print(p)
            h = imagehsv[row,col,0]
            s = imagehsv[row,col,1]
            i = 0 #0b00000000
            if (h == 0) and (s == 0):
                hs = 0
            elif h == s:
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
        f = open(file, 'w+')
        f.write("%d_%d\n"% (int(comp_image.shape[0]),int(comp_image.shape[1])))
        f.close()
        f = open(file, 'ab+')
        #f.write("%d_%d|"% (int(comp_image.shape[0]),int(comp_image.shape[1])))
        for row in range(comp_image.shape[0]):
            for col in range(comp_image.shape[1]):
                f.write(bytes([comp_image[row,col,0]]))
                f.write(bytes([comp_image[row,col,1]]))
                #f.write("%c%c" % (chr(comp_image[row,col,0]),chr(comp_image[row,col,1])))
    finally:
        f.close()

def compact_vizinhos(image):
    comp_image = imgrgb2hsvC(image)
    img = ''
    for row in range(0,comp_image.shape[0],2):
        for col in range(0,comp_image.shape[1],2):
            #print(row, col)
            img = img+str(comp_image[row,col,0])+","+str(comp_image[row,col,1])+","+str(comp_image[row,col,2])+","+ str(comp_image[row+1,col,2])+","+str(comp_image[row,col+1,2])+","+str(comp_image[row+1,col+1,2])+","
    
    print(img)
    img = np.fromstring(img, dtype=int, sep=",")
    print(img)
    return img

def filecompact_vizinhos(image, file):
    comp_image = imgrgb2hsvC(image)
    file = file + ".ith"
    try:
        f = open(file, 'w+')
        f.write("%d_%d\n"% (int(comp_image.shape[0]),int(comp_image.shape[1])))
        f.close()
        f = open(file, 'ab+')
        img = ''
        for row in range(0,comp_image.shape[0],2):
            for col in range(0,comp_image.shape[1],2):
                img = img+","+str(comp_image[row,col,0])+","+str(comp_image[row,col,1])+","+str(comp_image[row,col,2])+","+ str(comp_image[row+1,col,2])+","+str(comp_image[row,col+1,2])+","+str(comp_image[row+1,col+1,2])+","
                f.write(bytes([comp_image[row,col,0]]))
                f.write(bytes([comp_image[row,col,1]]))
                f.write(bytes([comp_image[row,col,2]]))
                f.write(bytes([comp_image[row+1,col,2]]))
                f.write(bytes([comp_image[row,col+1,2]]))
                f.write(bytes([comp_image[row+1,col+1,2]]))
        image = np.fromstring(img, dtype=int, sep=",")
        return image
    finally:
        f.close()

def runlength_encode(image,file):
    comp_image = compact_vizinhos(image)
    print(comp_image)
    file = file + ".ith"
    try:
        f = open(file, 'w+')
        f.write("%d_%d\n"% (int(image.shape[0]),int(image.shape[1])))
        f.close()
        f = open(file, 'ab+')
        count = 1
        s = ''
        #print(comp_image[0])
        for index in range(comp_image.shape[0]):
            if (index+1) < comp_image.shape[0] and comp_image[index] == comp_image[index+1] and count < 255:
                count += 1
            else:
                f.write(bytes([comp_image[index]]))
                f.write(bytes([count]))
                count = 1
        f.close()
    finally:
        f.close()

def runlength_encode2(image,file):
    comp_image = ith_compact(image)
    print(comp_image)
    file = file + ".ith"
    try:
        f = open(file, 'w+')
        f.write("%d_%d\n"% (int(comp_image.shape[0]),int(comp_image.shape[1])))
        f.close()
        f = open(file, 'ab+')
        count = 1
        s = ''
        print(comp_image[0,0,0])
        for row in range(comp_image.shape[0]):
            for col in range(comp_image.shape[1]):
                if (col+1) < comp_image.shape[1] and comp_image[row,col,0] == comp_image[row,col+1,0] and count < 255:
                    count += 1
                else:
                    f.write(bytes([comp_image[row,col,0]]))
                    f.write(bytes([count]))
                    count = 1
        f.close()
        f = open(file, 'a+')
        f.write("\n")
        f.close()
        f = open(file, 'ab+')
        #print(len(s))
        #imgrec = np.fromstring(s, dtype=int, sep=",")
        #return imgrec
        #f.write("|")
        #count = 1
        c = 0 
        for r in range(comp_image.shape[0]-1):
            for c in range(comp_image.shape[1]-1):
                print(r,c)
                if (col+1) < comp_image.shape[1] and comp_image[r,c,1] == comp_image[r,c+1,1] and count < 255:
                    #print("elemento: ", comp_image[row,col,1], " contador: ",count)
                    count += 1
                else:
                    c += c
                    #print("valor %d: %d" % (int(comp_image[row,col,1]),int(count)))
                    f.write(bytes([comp_image[r,c,1]]))
                    f.write(bytes([count]))
                    count = 1
        print("Nº bytes: ",c*2)
    finally:
        f.close()

#DECOMPACTAÇÃO
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
        print(v)
        #print("V:",v)
        hs = comp_image[k+1]
        print(hs)
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
        f = open(image, 'r')
        content = f.readline()
        print(content)
        dim = np.fromstring(content, dtype=int, sep="_")
        print("DIMENSÕES",dim)
        f.close()
        f = open(image, 'rb')
        content = f.read()
        content = content[9:len(content)]
        #print(content)
        s = ''
        for c in range(len(content)):
            s = s + str(content[c]) + ","
        #while True:
        #    c = f.read(1)
        #    if not c:
        #        print("End of file")
        #        break      
            #print("Read a character:",int.from_bytes(c, byteorder='big'))
        #    s = s + str(int.from_bytes(c, byteorder='big')) + ","
        f.close()
        img = np.fromstring(s, dtype=int, sep=",")
        print("Shape do vetor string : ",img.shape)
        print(img)
        image = decompact_ith(img,dim)
        return image
    finally:
        f.close()

def filedecompact_vizinhos(file):
    try:
        f = open(file, 'r')
        content = f.readline()
        print(content)
        dim = np.fromstring(content, dtype=int, sep="_")
        print("DIMENSÕES",dim)
        size = dim
        f.close()
        f = open(file, 'rb')
        content = f.readline()
        content = f.read()
        #content = content[9:len(content)]
        s = ''
        for c in range(len(content)):
            s = s + str(content[c]) + ","
        f.close()


        img = np.fromstring(s, dtype=int, sep=",")
        print("Shape do vetor string : ",img.shape)
        print("Imagem: ",img)

        image = np.zeros((size[0], size[1],3), dtype=np.uint8)
        #comp_image[:,:,0] = imagehsv[:,:,2]
        TAM = len(img)-1 
        row = 0
        col = 0
        print(size[0], size[1], TAM)
        for k in range(0,TAM,6):
            #print(ord(comp_image[int(TAM/2)+1]))
            #print(k, row, col)
            #print("K: ",k)
            h = img[k]
            #print("H: ",h)
            #print("V:",v)
            s = img[k+1]
            #print("S: ",s)

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
            #print("Vs: ",img[k+2],img[k+3],img[k+4],img[k+5])
            #print(row,col)
            if col < (size[1]-2):
                col += 2
            elif row < (size[0]-2):
                row += 2
                col = 0
            #print(row,col)
        image = imghsv2rgb(image)
        return image
    finally:
        f.close()

def decompact_vizinhos(img,size):
    #img = np.fromstring(s, dtype=int, sep=",")
    #print("Shape do vetor string : ",img.shape)
    #print("Imagem: ",img)
    image = np.zeros((size[0], size[1],3), dtype=np.uint8)
    #comp_image[:,:,0] = imagehsv[:,:,2]
    TAM = len(img)-1 
    row = 0
    col = 0
    print(size[0], size[1], TAM)
    for k in range(0,TAM-1,6):
        #print(ord(comp_image[int(TAM/2)+1]))
        #print(k, row, col)
        #print("K: ",k)
        h = img[k]
        #print("H: ",h)
        #print("V:",v)
        s = img[k+1]
        #print("S: ",s)

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
        #print("Vs: ",img[k+2],img[k+3],img[k+4],img[k+5])
        #print(row,col)
        if col < (size[1]-2):
            col += 2
        elif row < (size[0]-2):
            row += 2
            col = 0
        #print(row,col)
    image = imghsv2rgb(image)
    return image

def filedecompact_runlength2(file):
    try:
        #f = open(file, 'r')
        #content = f.readline()
        #print(content)
        #dim = np.fromstring(content, dtype=int, sep="_")
        #print("DIMENSÕES",dim)
        size = [444,640]
        #f.close()
        f = open(file, 'rb')
        content = f.read()
        hs = f.read()
        #content = content[9:len(content)]
        s = ''
        hs = ''
        for c in range(len(content)):
            s = s + str(content[c]) + ","

        for c in range(len(hs)):
            hs = hs + str(hs[c]) + ","
        f.close()


        img = np.fromstring(s, dtype=int, sep=",")
        print("Shape do vetor string : ",img.shape)
        print("Imagem: ",img)

        imghs = np.fromstring(hs, dtype=int, sep=",")
        print("Shape do vetor string : ",imghs.shape)
        print("Imagem: ",imghs)

        image = np.zeros((size[0], size[1],3), dtype=np.uint8)

        TAM = len(img)
        #comp_image = comp_image[init:TAM]
        #print(comp_image)
        #comp_image = np.fromstring(comp_image, dtype=int, sep=",")
        #print(comp_image)
        pxl = 0
        count = 0
        #print(init)
        #print(len(comp_image), TAM)
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
        print(TAM, size[0], size[1])
        #imgrec = np.fromstring(s, dtype=int, sep=",")
        #imgrec = comp_image
        row = 0
        col = 0
        for pixel in range(0,len(img)-1,2):
            #print("POSIÇÃO: ", row,col)         
            valor = img[pixel]
            #print(valor)
            contador = img[pixel+1]
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

def filedecompact_runlength(file):
    try:
        f = open(file, 'r')
        content = f.readline()
        print(content)
        dim = np.fromstring(content, dtype=int, sep="_")
        print("DIMENSÕES",dim)
        size = dim
        f.close()
        f = open(file, 'rb')
        content = f.readline()
        content = f.read()
        #content = content[9:len(content)]
        s = ''
        for c in range(len(content)):
            s = s + str(content[c]) + ","

        img = np.fromstring(s, dtype=int, sep=",")
        print("Shape do vetor string : ",img.shape)
        print("Imagem: ",img)

        

        TAM = len(img)
        image = np.zeros(TAM, dtype=np.uint8)
        #comp_image = comp_image[init:TAM]
        #print(comp_image)
        #comp_image = np.fromstring(comp_image, dtype=int, sep=",")
        #print(comp_image)
        pxl = 0
        count = 0
        #print(init)
        #print(len(comp_image), TAM)
        x = 0
        p = 0
        s = ''

        print(TAM, size[0], size[1])
        #imgrec = np.fromstring(s, dtype=int, sep=",")
        #imgrec = comp_image
        index = 0
        for pixel in range(0,TAM-1,2):
            #print("POSIÇÃO: ", row,col)         
            valor = img[pixel]
            #print(valor)
            contador = img[pixel+1]
            #print(contador)
            for c in range(contador):
                #print(row,col)             
                image[index] = valor
                #print(image[row,col], contador)
                if index < (TAM-1):
                    index += 1
        #print(image.shape, x, p)
        print("Imagem descompactada : ",image)
        image = decompact_vizinhos(image,size)
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
    print(i)
    
    # h = 0
    # s = 66
    # h = int(round(h/5))
    # s = int(round(s/5))
    # hs = h
    # hs = hs>>1
    # hs = hs<<4
    # aux = s>>1
    # hs = hs + aux
    # print("HS: ",hs)

    # h_aux = hs
    # s_aux = hs
    # h_aux = h_aux>>4
    # h = h_aux<<1
    # s_aux = s_aux - (h<<3)
    # s = s_aux<<1
    # h = h*5
    # s = s*5
    # print("H: ",h, " S: ",s)
    

    #it = filedecompact_vizinhos('testevizinhos.ith')
    #it = runlength_encode(i, 'teste')
    it = filedecompact_runlength('teste.ith')
    print(it)
    #it = filedecompact_runlength('testetop.ith')
    #ih = imgrgb2hsv(i)
    
    #for row in range(it.shape[0]):
    #    for col in range(it.shape[1]):
    #        if it[row,col] >= 128:
    #            it[row,col] = it[row,col] - 128
    #ih[:,:,2] = it
    #i = imghsv2rgb(ih)
    #plt.imshow(it)
    #plt.show()
