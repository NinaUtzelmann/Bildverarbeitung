from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#load Image and convert to array
image = Image.open("bild03.png").convert("L")
image = np.array(image)
image_binar = image.copy()

# make image binar
image_binar[image == 255] = False
image_binar[image == 0] = True

nAng = 400
nRad = 400

dAng = math.pi / nAng
xCtr = int(image.shape[1] / 2)
yCtr = int(image.shape[0] / 2)
rMax = math.sqrt(xCtr * xCtr + yCtr * yCtr)
dRad = (2 * rMax)/nRad

# make houghArray with zeros
houghArray = np.zeros([nAng, nRad], dtype=np.int)
treshold = 0

def doPixel(v, u):
    x = u - xCtr
    y = v - yCtr

    for a in range(nAng):
        theta = dAng * a
        r = int(round((x * math.cos(theta) + y * math.sin(theta)) / dRad) + nRad / 2)
        if r >= 0 and r < nRad:
            houghArray[a, r] += 1


def LinearHoughTransformation():
    for v in range(image_binar.shape[0]):
        for u in range(image_binar.shape[1]):
            if image_binar[v, u]:
                doPixel(v, u)


def Treshold():
    houghArray[houghArray < treshold] = 0



if __name__ == '__main__':
    LinearHoughTransformation()
    Treshold()
    # plot image_binar
    plt.figure(1)
    plt.subplot(211)
    plt.imshow(image_binar, cmap=cm.Greys_r)

    # plot houghArray
    plt.figure(1)
    plt.subplot(212)
    plt.imshow(houghArray, cmap=cm.Greys_r)
    plt.show()
