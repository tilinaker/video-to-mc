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
        
        for index_Y in range(self.Height):
            result.append(make_one_raw(self.img[index_Y]))

        return result

    def make_raw(raw):
        '''one raw of img array -> one raw of block code array.'''
        result = []
        
        for index in range(self.Width):
            result.append(self.block_file[find_in_table(raw[index])])

        return result

class render:
    def __init__():
        pass

    def renderframe(frameindex):
        pass


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
            fc += 1

        #print('done!')
        return (frameCount, frameWidth, frameHeight, buf)
    else:
        print('''it is too long. the video's frame count should not over 536870912 (4294967295 / 2 / 4)''')
            

def draw_frame(frame, X, Y, Z, img1):
    for i in range(width):
        for j in range(height):
            mc.setBlock(X - i, Y - j, Z, img1[i][j][0], img1[i][j][0])

def threadfunc(tup):
    stframe, count = tup
    for i in range(stframe, stframe + count):
        img[i] = make_imgmc(vid[i])
def main(X, Y, Z, threads):
    global img
    thr1, thr2 = divmod(frame, threads)
    temp = []
    img = list(range(frame))

    print('making process.')
    pool = mul.Pool(processes = threads)
    pool.map(threadfunc, [(thr1 * i, thr1) for i in range(threads - 1)] + [(thr1 * threads - 1, thr2)])
    pool.close()

    print('processes ready.')
    print('process start. wait a min.')

    pool.join()

    print(len(img))

    input('done! press enter!')

    print('drawing video')
    for i in range(frame):
        print('drawing frame num ' + str(i))
        draw_frame(vid, i, width, height, table1, table2, X, Y, Z, img[i])
    print('done!')

ans = input('do you want to use normal setting(y, n)')
if ans == 'n':
    X = int(input('X:'))
    Y = int(input('Y:'))
    Z = int(input('Z:'))
    processes = int(input('process count:'))
    filename = input('video file name:')
elif ans == 'y':
    X = 0
    Y = 0
    Z = 0
    processes = 5
    filename = 'Untitled.avi'

frame, width, height, vid = import_vid(filename)
print('frame count', end='')
print(frame)
print('width', end='')
print(width)
print('height', end='')
print(height)
#input()
table, table1, table2 = load_table()

main(X, Y, Z, processes)
