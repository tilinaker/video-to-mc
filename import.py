import cv2
import pickle
import math
import numpy as np


def load_mix(filename):
    imgrgb = cv2.imread(filename, 1)
    
    
    if type(imgrgb) == type(None):
        return 0

    img = cv2.cvtColor(imgrgb, cv2.COLOR_BGR2HSV)
    result = np.zeros(3)
    for i in range(16):
        for j in range(16):
            result[0], result[1], result[2] = colorMix(result[0], result[0], result[0], img[i][j][0], img[i][j][1], img[i][j][2])

    

    return (result[0], result[1], result[2])

def colorMix(H1, S1, V1, H2, S2, V2):
    return (H1 + H2 / 2, S1 + S2 / 2, V1 + V2 / 2)

def main():
    result = []
    result1 = []
    result2 = []
    
    for i in range(1, 253):
        for j in range(16):
            tmp = load_mix(str(i) + str(hex(j))[-1].upper() + '.png')
            print(str(i) + str(hex(j))[-1].upper() + '.png', end = '')

            if type(tmp) != type(int(1)):
                print(' exists there')
                result.append([(i, j), tmp])
                result1.append(tmp)
                result2.append((i, j))
            else:
                print(" can't find")

            

    file = open("table.txt", "wb")
    pickle.dump([result, result1, result2], file)
    file.close()
    print(len(result))
    print(result)


if __name__ == '__main__':
    main()

    
