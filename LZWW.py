import os
import numpy as np
from PIL import Image


def createCompressionDict():
    dictionary = {}

    for i in range(10):
        dictionary[str(i)] = i
    dictionary[','] = 10

    return (dictionary , 11)


def createDecompressionDict():
    dictionary = {}

    for i in range(10):
        dictionary[i] = str(i)
    dictionary[10] = ','

    return (dictionary , 11)


# Global variables
compressionDictionary, compressionIndex = createCompressionDict()
decompressionDictionary, decompressionIndex = createDecompressionDict()


def compress(path):
    red, green, blue = initCompress(path)
    compressedColors = []

    compressedColors.append(compressColor(red))
    compressedColors.append(compressColor(green))
    compressedColors.append(compressColor(blue))

    filesplit = path.split('.')
    filename = filesplit[0] + '.lzw'

    with open(filename, 'w') as file:
        for color in compressedColors:
            for row in color:
                file.write(row)
                file.write('\n')


def compressColor(colorList):
    compressedColor = []
    i = 0

    for currentRow in colorList:
        currentString = currentRow[0]
        compressedRow = ''
        i += 1

        for charIndex in range(1, len(currentRow)):
            currentChar = currentRow[charIndex]

            global compressionDictionary, compressionIndex

            if currentString + currentChar in compressionDictionary:
                currentString = currentString+currentChar
            else:
                compressedRow = compressedRow + str(compressionDictionary[currentString]) + ','
                compressionDictionary[currentString+currentChar] = compressionIndex
                compressionIndex += 1
                currentString = currentChar

            currentChar = ''
        
        compressedRow = compressedRow + str(compressionDictionary[currentString])
        compressedColor.append(compressedRow)
    
    return compressedColor


def decompress(path):
    image = []

    with open(path, 'r') as file:
        for line in file:
            decodedRow = decompressRow(line)
            image.append(np.array(decodedRow))

    image = np.array(image)
    shapeTup = image.shape
    image = image.reshape((3, shapeTup[0]//3, shapeTup[1]))

    saveImage(image, path)


def decompressRow(line):
    currentRow = line.split(',')
    currentRow[-1] = currentRow[-1][:-1]
    decodedRow = ''
    word, entry = '', ''

    global decompressionDictionary, decompressionIndex

    decodedRow = decodedRow + decompressionDictionary[int(currentRow[0])]
    word = decompressionDictionary[int(currentRow[0])]

    for i in range(1, len(currentRow)):
        new = int(currentRow[i])
        if new in decompressionDictionary:
            entry = decompressionDictionary[new]
            decodedRow += entry
            add = word + entry[0]
            word = entry
        else:
            entry = word + word[0]
            decodedRow += entry
            add = entry
            word = entry

        decompressionDictionary[decompressionIndex] = add
        decompressionIndex += 1

    newRow = decodedRow.split(',')
    decodedRow = [int(x) for x in newRow]

    return decodedRow


def initCompress(path):
    image = Image.open(path)
    height, width = image.size
    red, green, blue = processImage(image, height, width)

    return (red, green, blue)


def processImage(image, height, width):
    image = image.convert('RGB')
    red, green, blue = [], [], []
    pixel_values = list(image.getdata())
    iterator = 0

    for height_index in range(height):
        R, G, B = '', '', ''
        for width_index in range(width):
            RGB = pixel_values[iterator]
            R = R + str(RGB[0]) + ','
            G = G + str(RGB[1]) + ','
            B = B + str(RGB[2]) + ','
            iterator += 1

        red.append(R[:-1])
        green.append(G[:-1])
        blue.append(B[:-1])

    return red, green, blue


def saveImage(image, path):
    filesplit = path.split('.')
    filename = filesplit[0] + '.bmp'
    imagelist, imagesize = makeImageData(image[0], image[1], image[2])
    imagenew = Image.new('RGB', imagesize)
    imagenew.putdata(imagelist)

    imagenew.save(filename)


def makeImageData(r, g, b):
    imagelist = []

    for i in range(len(r)):
        for j in range(len(r[0])):
            imagelist.append((r[i][j], g[i][j], b[i][j]))

    return imagelist, (len(r), len(r[0]))


if __name__ == '__main__':
    compress('images/benchmark.bmp')
    decompress('benchmark.lzw')
