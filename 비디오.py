import cv2
from math import *
import mcpi.block as block
import multiprocessing as mul
import mcpi.minecraft as minecraft
import numpy as np
import os
import pdb
import pickle
import time


mc = minecraft.Minecraft.create()

class imageMc:
    def __init__(self, img_arrary):
        file = pickle.load(open("table.txt","rb"))
        
        self.table, self.block_color, self.block_file = file
        self.img = img_arrary
        self.imgHeight = len(self.img)
        self.imgWidth = len(self.img[0])
        self.counter = 0

    def find_in_table(self, color):
        #find most same block to color
        data_avr = []
    
        for i in range(len(self.table)):
            data_avr.append(abs(self.block_color[i][0] - color[0]) + abs(self.block_color[i][1] - color[1]) + abs(self.block_color[i][2] - color[2]))

        return data_avr.index(min(data_avr))

    def make_img_block(self):
        #img array -> block code array.
        result = []

        for indexY in range(self.imgHeight):
            result.append(self.make_raw(self.img[indexY]))

        self.blockdata = result

    def make_raw(self, raw):
        #one raw of img array -> one raw of block code array.
        result = []
        
        for indexX in range(self.imgWidth):
            result.append(self.block_file[self.find_in_table(raw[indexX])])

        return result

    def render(self, X, Y, Z, processCount):
        #block code array -> mc blocks.
        self.X, self.Y, self.Z = X, Y, Z
        
        blockdata = self.make_img_block()
        self.proc_Num, self.self_proc_Num = divmod(self.imgHeight, processCount)
        print(divmod(self.imgHeight, processCount))

        #make process
        #mapdata = [(blockdata[index], X, Y + index, Z) for index in range(processCount - 1)] + [(blockdata[processCount], X, Y + processCount, Z)]
        pool = mul.Pool(processCount)
        pool.map(self.render_proc, list(range(processCount - 1)) + [-1 * (processCount - 1)])
        pool.close()

        pool.join()

        print('counter ', end = '')
        print(self.counter)

    def render_proc(self, forindex):
        #one raw of block code array -> one raw of mc blocks.
        self.counter = self.counter + 1

        if forindex >= 0:
            for index in range(self.proc_Num):
                for indexX in range(self.imgWidth):
                    mc.setBlock(self.X - indexX, self.Y - forindex - index, self.Z, self.blockdata[forindex + index][indexX][0], self.blockdata[forindex + index][indexX][1])
                    print(self.X - indexX, self.Y - forindex - index, self.Z, self.blockdata[forindex][indexX][0],self.blockdata[forindex][indexX][1])
        else:
            for index in range(self.self_proc_Num):
                for indexX in range(self.imgWidth):
                    mc.setBlock(self.X - indexX, self.Y - abs(forindex) - index, self.Z, self.blockdata[abs(forindex) + index][indexX][0], self.blockdata[abs(forindex) + index][indexX][1])
                    print(self.X - indexX, self.Y - abs(forindex) - index, self.Z,self.blockdata[abs(forindex)][indexX][0], self.blockdata[abs(forindex)][indexX][1])


def import_vid(filename):
    cap = cv2.VideoCapture(filename)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if not frameCount > 536870912 or frameWidth > 536870912 or frameHeight > 536870912:

        buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
        #buf = [i for i in [i for i in [i for i in [i for i in [0] * 3] * frameWidth] * frameHeight] * frameCount]

        fc = 0
        ret = True
    
        while (fc < frameCount  and ret):
            #print('importing frame number ' + str(fc))
            ret, buf[fc] = cap.read()
            buf[fc] = cv2.cvtColor(buf[fc], cv2.COLOR_BGR2HSV)
            fc += 1

        #print('done!')
        return (frameCount, frameWidth, frameHeight, buf)
    else:
        print('''it is too long. the video's frame count should not over 536870912 (4294967295 / 2 / 4)''')

def import_img(filename):
    return cv2.cvtColor(cv2.imread(filename, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2HSV)
            
def main(X, Y, Z, threads):
    os.system('py import.py')
    img = import_img('2380.png')

    mcimg = imageMc(img)
    mcimg.render(X, Y, Z, threads)

if __name__ == '__main__':
    main(249, 96, -1040, 10)
