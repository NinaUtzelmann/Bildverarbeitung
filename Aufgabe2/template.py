# coding=utf-8
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def computeHisto(img):

    gray = rgb2gray(img);
    histo = np.zeros(256,dtype=int)

    for index, val in np.ndenumerate(gray):
        # Der Zaehler für den jeweiligen Intensitaetswert im Histogramm wird hochgesetzt
        histo[int(val)] += 1

    return histo


def bin_Histo(img, bin=1):

    K = 256 #Anzahl von Intensitaetswerten
    grauwertklassen = int(np.ceil(K / bin)) #Anzahl von Grauwertklassen auf Basis der angegebenen Bin-Groesse

    gray = rgb2gray(img)
    bin_histo = np.zeros(grauwertklassen, dtype=int)

    for index, val in np.ndenumerate(gray):
        # Um das Histogrammelement zu finden, kann der Pixelwert durch die Intervalllaenge dividiert
        # bzw. mit dem Kehrwert multipliziert werden
        i = int(val * grauwertklassen/K)
        # Der Zaehler fuer das Histogrammelement wird erhoeht
        bin_histo[i] += 1

    return bin_histo


def brighten(img, offset):

    img_brightened_arr = np.copy(img)

    for index, val in np.ndenumerate(img):
        # check clamping
        if (val + offset) < 255:
            # add offset to img
            img_brightened_arr[index] = val + offset
        else:
            img_brightened_arr[index] = 255

    return img_brightened_arr


def get_lut(k=256):

    # create lut-table
    # which only brightens the darker pixel values (e.g. < 200)
    # bright pixel values should not change that much

    # Dynamische Festlegung von Schwellwerten und Erhellungsfaktoren zur Nutzung von anderen Bittiefen
    lut = np.zeros(k, dtype=int)
    upper_threshold = int(round(k/5*4))
    brighten_factor = int(round(k*0.04))
    lower_brighten_factor = int(round(brighten_factor/2))
    #print('Obere Grenze: ' + str(upper_threshold))
    #print('Helligkeitsfaktor: ' + str(brighten_factor))
    #print('kleinerer Faktor: ' + str(lower_brighten_factor))

    for index,val in np.ndenumerate(lut):
        if index[0] < upper_threshold:
            lut[index[0]] = index[0]+brighten_factor
        elif (index[0]+lower_brighten_factor) > (k-1):
            lut[index[0]] = (k-1)
        else:
            lut[index[0]] = index[0]+lower_brighten_factor

    return lut


def brighten_with_lut(img, lut):

    img_arr_brightened = np.copy(img)

    # check clamping --> clamping already checked when generating lookup table

    # brighten image using the lookup-table
    for index, val in np.ndenumerate(img):
        img_arr_brightened[index] = lut[val]

    return img_arr_brightened


def rgb2gray(img):

    new = np.array(img)

    # convert to grayscale image (only one channel)
    # Aufteilung in separate Channel
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    # Multiplikation mit "allgemein bekannten" Gewichtungsfaktoren (siehe z.B. hier https://en.wikipedia.org/wiki/Grayscale)
    gray = np.rint(0.2989 * r + 0.5870 * g + 0.1140 * b)
    new[:, :, 0] = gray
    new[:, :, 1] = gray
    new[:, :, 2] = gray

    new_image = Image.fromarray(new, 'RGB')
    new_image.save('bild01_gray.jpg')

    return gray


if __name__ == '__main__':
    # read img
    im = Image.open("bild01.jpg")

    # convert to numpy array
    im_array = np.array(im)

    # convert to grayscale
    im_gray = rgb2gray(im_array)

    # brighten image
    im_brightened = brighten(im_array, 20)

    # brighten image with lut-table
    lut = get_lut(256)
    im_brightened_with_lut = brighten_with_lut(im_array, lut)

    histo = computeHisto(im_array)

    # compute histogram (with bin-size)
    histo = bin_Histo(im_array, 5)

    # plot histogram
    N = histo.size
    x = range(N)
    width = 1

    plt.figure(1)
    plt.subplot(211)
    plt.bar(x, histo, width, color="blue")
    plt.xlim([0,N-1])

    # plot processed img
    plt.subplot(212)
    plt.imshow(im, cmap = cm.Greys_r)

    plt.show()