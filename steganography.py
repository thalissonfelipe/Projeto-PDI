import os
from PIL import Image


# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def str2bin(data):
    binary = []
    for i in data:
        binary.append(format(ord(i), '08b'))

    return binary


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    binary = str2bin(data)
    lendata = len(binary)
    imdata = iter(pix)

    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                  imdata.__next__()[:3] +
                                  imdata.__next__()[:3]]

        for j in range(0, 8):
            if (binary[i][j] == '0') and (pix[j] % 2 != 0):
                if (pix[j] % 2 != 0):
                    pix[j] -= 1
            elif (binary[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


# Encode data into image
def encode(image, message, new_img_name):
    if (len(message) == 0):
        raise ValueError('Message is empty.')

    newimg = image.copy()
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), message):
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

    directory = 'output/'
    new_img_name = new_img_name.split('.')[0] + '.bmp'
    if not os.path.exists(directory):
        os.makedirs(directory)
    newimg.save(directory + new_img_name, 'bmp')


# Decode the data in the image
def decode(image):
    data = ''
    imgdata = iter(image.getdata())

    while(True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                     imgdata.__next__()[:3] +
                                     imgdata.__next__()[:3]]
        # string of binary data
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data


if __name__ == '__main__':
    i = Image.open('images/hamster.jpeg')
    encode(i, 'Hello World!', 'hamster')
    it = Image.open('output/hamster.bmp')
    print(decode(it))
