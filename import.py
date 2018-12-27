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
            result = result + hsv(img[i][j])

    

    return (rgb(result[2], result[1], result[0]))

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

def hsv(B, G, R):
    r, g, b = R/255, G/255, B/255
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

main()

    
