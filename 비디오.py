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

def load_table():
    file = pickle.load(open("table.txt","rb"))
    #print(file)
    return file

def findtable(rgb):
    tmp1 = []
    
    for i in range(len(table)):
        tmp1.append(abs(table[i][0] - rgb[0]) + abs(table[i][1] - rgb[1]) + abs(table[i][2] - rgb[2]))

    return tmp1.index(min(tmp1))

def make_imgmc(array):
    result = []
    for i in range(width):
        result.append([])
        for j in range(height):
            result[i].append(table2[findtable(table1, array[i][j])])
            

    return result

def proc_int(integer):
    if type(integer[-5]) in ['A', 'B', 'C', 'D', 'E', 'F']:
        return (int(integer[0:-6]), int('0x' + integer[-5]))
    elif len(integer) == 6:
        return (int(integer[-6]), int(integer[-5]))
    else:
        return (int(integer[0:-6]), int(integer[-5]))
        
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
    print('process reading.')
    thr1, thr2 = divmod(frame, threads)
    temp = []
    img = list(range(frame))

    print('processing.')
    pool = mul.Pool(processes = threads)
    pool.map(threadfunc, [(thr1 * i, thr1) for i in range(threads - 1)] + [(thr1 * threads - 1, thr2)])
    pool.close()

    print('processes ready.')
    print('start. wait a min.')

    pool.join()

    print(len(img))

    input('done! press enter!')

    print('drawing video')
    for i in range(frame):
        print('drawing frame num ' + str(i))
        draw_frame(vid, i, width, height, table1, table2, X, Y, Z, img[i])
    print('done!')

X = int(input('X:'))
Y = int(input('Y:'))
Z = int(input('Z:'))
processes = int(input('process count:'))
filename = input('video file name:')

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
