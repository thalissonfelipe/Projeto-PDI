import os
import numpy as np
from PIL import Image

class LZW:
    def __init__(self, path):
        self.path = path
        self.compressionDictionary, self.compressionIndex = self.createCompressionDict()
        self.decompressionDictionary, self.decompressionIndex = self.createDecompressionDict()

    def compress(self):
        self.initCompress()
        compressedColors = []

        compressedColors.append(self.compressColor(self.red))
        compressedColors.append(self.compressColor(self.green))
        compressedColors.append(self.compressColor(self.blue))

        filesplit = str(os.path.basename(self.path)).split('.')
        filename = filesplit[0] + '.lzw'

        with open(filename, 'w') as file:
            for color in compressedColors:
                for row in color:
                    file.write(row)
                    file.write('\n')
                
    def compressColor(self, colorList):
        compressedColor = []
        i = 0

        for currentRow in colorList:
            currentString = currentRow[0]
            compressedRow = ""
            i += 1

            for charIndex in range(1, len(currentRow)):
                currentChar = currentRow[charIndex]
                if currentString+currentChar in self.compressionDictionary:
                    currentString = currentString+currentChar
                else:
                    compressedRow = compressedRow + str(self.compressionDictionary[currentString]) + ','
                    self.compressionDictionary[currentString+currentChar] = self.compressionIndex
                    self.compressionIndex += 1
                    currentString = currentChar
                currentChar = ''
            
            compressedRow = compressedRow + str(self.compressionDictionary[currentString])
            compressedColor.append(compressedRow)
        
        return compressedColor

    def decompress(self):
        image = []

        with open(self.path, 'r') as file:
            for line in file:
                decodedRow = self.decompressRow(line)
                image.append(np.array(decodedRow))

        image = np.array(image)
        shapeTup = image.shape
        image = image.reshape((3, shapeTup[0]//3, shapeTup[1]))
        self.saveImage(image)

    def decompressRow(self,line):
        currentRow = line.split(',')
        currentRow[-1] = currentRow[-1][:-1]
        decodedRow = ''
        word, entry = '',''
        decodedRow = decodedRow + self.decompressionDictionary[int(currentRow[0])]
        word = self.decompressionDictionary[int(currentRow[0])]

        for i in range(1, len(currentRow)):
            new = int(currentRow[i])
            if new in self.decompressionDictionary:
                entry = self.decompressionDictionary[new]
                decodedRow += entry
                add = word + entry[0]
                word = entry
            else:
                entry = word + word[0]
                decodedRow += entry
                add = entry
                word = entry
            self.decompressionDictionary[self.decompressionIndex] = add
            self.decompressionIndex += 1

        newRow = decodedRow.split(',')
        decodedRow = [int(x) for x in newRow]

        return decodedRow

    def initCompress(self):
        self.image = Image.open(self.path)
        self.height, self.width = self.image.size
        self.red, self.green, self.blue = self.processImage()

    def processImage(self):
        image = self.image.convert('RGB')
        red, green, blue = [], [], []
        pixel_values = list(image.getdata())
        iterator = 0

        for height_index in range(self.height):
            R, G, B = '', '', ''
            for width_index in range(self.width):
                RGB = pixel_values[iterator]
                R = R + str(RGB[0]) + ','
                G = G + str(RGB[1]) + ','
                B = B + str(RGB[2]) + ','
                iterator += 1

            red.append(R[:-1])
            green.append(G[:-1])
            blue.append(B[:-1])

        return red, green, blue

    def saveImage(self, image):
        filesplit = str(os.path.basename(self.path)).split('.')
        filename = filesplit[0] + '.bmp'
        imagelist, imagesize = self.makeImageData(image[0], image[1], image[2])
        imagenew = Image.new('RGB', imagesize)
        imagenew.putdata(imagelist)
        imagenew.save(filename)

    def makeImageData(self, r, g, b):
        imagelist = []

        for i in range(len(r)):
            for j in range(len(r[0])):
                imagelist.append((r[i][j], g[i][j], b[i][j]))

        return imagelist,(len(r),len(r[0]))

    def createCompressionDict(self):
        dictionary = {}

        for i in range(10):
            dictionary[str(i)] = i
        dictionary[','] = 10

        return (dictionary , 11)

    def createDecompressionDict(self):
        dictionary = {}

        for i in range(10):
            dictionary[i] = str(i)
        dictionary[10] = ','

        return (dictionary , 11)

# compressor = LZW('images/benchmark.bmp')
# compressor.compress()

decompressor = LZW('benchmark.lzw')
decompressor.decompress()