import cv2
import pickle
import numpy as np


def load_mix(filename):
    img = cv2.imread(filename, 1)
    
    if type(img) == type(None):
        return 0

    result = np.zeros(3)
    for i in range(16):
        for j in range(16):
            result = result + img[i][j]

    if result[0] > 255:
        result[0] = 255
    if result[1] > 255:
        result[1] = 255
    if result[2] > 255:
        result[2] = 255

    return (result[2], result[1], result[0])

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
                result.append([str(i) + str(hex(j))[-1].upper() + '.png', tmp])
                result1.append(tmp)
                result2.append(str(i) + str(hex(j))[-1].upper() + '.png')
            else:
                print(" can't find")

            

    file = open("table.txt", "wb")
    pickle.dump([result, result1, result2], file)
    file.close()
    print(len(result))
    print(result)

main()

    
