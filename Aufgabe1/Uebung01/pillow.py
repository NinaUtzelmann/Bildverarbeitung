from datetime import datetime

import numpy as np
from PIL import Image


def readPic(path):
    img = Image.open(path)
    return img


def showPic(img):
    img.show()


def printPicDetails(array, name):
    print("Das Bild '" + name + "' hat insgesamt " + str(array.size/3) + " Bildpunkte (" + str(array.shape[0]) + " Pixel hoch, " + str(array.shape[1]) + " Pixel breit).")
    print("Durchschnittliche Staerken der RGB-Kaenale (auf einer Skala von 0 - 255):")
    print("     Rot --> " + str(np.mean(array[:,:,0])))
    print("     Gruen --> " + str(np.mean(array[:,:,1])))
    print("     Blau --> " + str(np.mean(array[:,:,2])))
    print("Hoechstwerte der RGB-Kaenale (auf einer Skala von 0 - 255):")
    print("     Rot --> " + str(np.max(array[:,:,0])))
    print("     Gruen --> " + str(np.max(array[:,:,1])))
    print("     Blau --> " + str(np.max(array[:,:,2])))


def splitPicToRGB(array, name):
    # Arbeitskopien d. Original-Arrays fuer jeden Channel
    red_array = np.copy(array)
    green_array = np.copy(array)
    blue_array = np.copy(array)
    # In jedem Array jeweils die Werte fuer R, G oder B nullen
    red_array[:, :, 1] = 0 #hier werden die Werte fuer x + y in der Dimension 1 (blau) genullt
    red_array[:, :, 2] = 0 #hier werden die Werte fuer x + y in der Dimension 2 (gruen) genullt
    green_array[:, :, 0] = 0
    green_array[:, :, 2] = 0
    blue_array[:, :, 0] = 0
    blue_array[:, :, 1] = 0
    # Image-Objekt aus NP-Arrays erzeugen
    img_red_channel = Image.fromarray(red_array, 'RGB')
    img_green_channel = Image.fromarray(green_array, 'RGB')
    img_blue_channel = Image.fromarray(blue_array, 'RGB')
    # Image-Objekte als Bilder speichern
    img_red_channel.save(name + '_red.png')
    img_green_channel.save(name + '_green.png')
    img_blue_channel.save(name + '_blue.png')


def mirrorPicHorizontal(array, name):
    mirrored_array = np.copy(array)
    mirrored_array_1 = np.copy(array)

    #Spiegelung ganzer Zeilen
    start_time_method_1 = datetime.now()
    for index, val in np.ndenumerate(array):
        mirrored_array[index[0]] = array[-1 -index[0]]
    duration_method_1 = datetime.now() - start_time_method_1

    #Spiegelung einzelner Bildpunkte
    start_time_method_2 = datetime.now()
    for index, val in np.ndenumerate(array):
        mirrored_array_1[int(array.shape[0])-(index[0]+1), index[1], index[2]] = val
    duration_method_2 = datetime.now() - start_time_method_2

    print('######runtime info#######')
    print('Horizontale Spiegelung ganzer Zeilen dauerte: ' + str(duration_method_1))
    print('Horizontale Spiegelung einzelner Bildpunkte dauerte: ' + str(duration_method_2))

    img_mirrored = Image.fromarray(mirrored_array_1, 'RGB')
    img_mirrored.save(name + '_horizontal.png')


def mirrorPicVertical(array, name):
    mirrored_array = np.copy(array)
    mirrored_array_1 = np.copy(array)

    #Spiegelung ganzer Spalten
    start_time_method_1 = datetime.now()
    for index, val in np.ndenumerate(array):
        mirrored_array[index[0], index[1]] = array[index[0], -1 - index[1]]
    duration_method_1 = datetime.now() - start_time_method_1

    #Spiegelung einzelner Bildpunkte
    start_time_method_2 = datetime.now()
    for index, val in np.ndenumerate(array):
        mirrored_array_1[index[0], int(array.shape[1])-(index[1]+1), index[2]] = val
    duration_method_2 = datetime.now() - start_time_method_2

    print('######runtime info#######')
    print('Vertikale Spiegelung ganzer Spalten dauerte: ' + str(duration_method_1))
    print('Vertikale Spiegelung einzelner Bildpunkte dauerte: ' + str(duration_method_2))

    img_mirrored = Image.fromarray(mirrored_array_1, 'RGB')
    img_mirrored.save(name + '_vertical.png')


def processPic(path):
    name, extension = path.split('.')
    img = readPic(path)
    img_np_array = np.array(img)
    printPicDetails(img_np_array, name)
    showPic(img)
    splitPicToRGB(img_np_array, name)
    img_red = readPic(name + '_red.png')
    showPic(img_red)
    img_green = readPic(name + '_green.png')
    showPic(img_green)
    img_blue = readPic(name + '_blue.png')
    showPic(img_blue)
    mirrorPicHorizontal(img_np_array, name)
    img_mirrored_horizontal = readPic(name + '_horizontal.png')
    showPic(img_mirrored_horizontal)
    mirrorPicVertical(img_np_array, name)
    img_mirrored_vertical = readPic(name + '_vertical.png')
    showPic(img_mirrored_vertical)


if __name__ == "__main__":
    processPic('monkey.jpg')
    #processPic('hidden.png')
    #processPic('wood.jpg')
    #processPic('sea_wall.jpg')
