import cv2
import multiprocessing as mul
import pdb
import time
import pickle
import numpy as np
import mcpi.minecraft as minecraft
import mcpi.block as block
from math import *

mc = minecraft.Minecraft.create()

class image_mc:
    def __init__(img_arrary):
        file = pickle.load(open("table.txt","rb"))
        
        self.table, self.block_color, self.block_file = file
        self.img = img_arrary
        self.imgHeight = len(img_arrary)
        self.imgWidth = len(img_array[0])

    def find_in_table(color):
        '''find most same block to color'''
        data_avr = []
    
        for i in range(len(table)):
            data_avr.append(abs(self.block_color[i][0] - color[0]) + abs(self.block_color[i][1] - rgb[1]) + abs(self.block_color[i][2] - rgb[2]))

        return data_avr.index(min(data_avr))

    def make_img_block():
        '''img array -> block code array.'''
        result = []
        
        pool = mul.Pool
        
        result.append(self.make_one_raw(self.img[index_Y]))

        return result

    def make_raw(raw):
        '''one raw of img array -> one raw of block code array.'''
        result = []
        
        for index in range(self.Width):
            result.append(self.block_file[find_in_table(raw[index])])

        return result

    def render(X, Y, Z, processCount):
        '''block code array -> mc blocks.'''
        blockdata = self.making_img_block()
        proc_Num, self_proc_Num = divmod(self.Height, processCount)

        #make process
        pool = mul.Pool(processes = processCount - 1)
        pool.map(render_raw,[(blockdata[index], X, Y + index, Z) for index in range(processCount - 1)])
        pool.close()
        
        for index in range(self_proc_Num):
            self.render_raw(blockdata[index], X, Y + index, Z)

        pool.join()

    def render_raw(raw, X, Y, Z):
        '''one raw of block code array -> one raw of mc blocks.'''
        for index in range(self.Width):
            mc.setBlock(X + index, Y, Z, raw[index][0], raw[index][1])


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
    img = import_img('2527.png')

    mcimg = image_mc(img)
    mcimg.render(X, Y, Z, threads)

if __name__ == '__main__':
    main(0, 0, 0, 10)
