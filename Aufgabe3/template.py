from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def compute_cumHisto(img, binSize=1):

    K = 256  # Anzahl von Intensitaetswerten
    grauwertklassen = int(np.ceil(K / binSize))  # Anzahl von Grauwertklassen auf Basis der angegebenen Bin-Groesse

    #gray = rgb2gray(img)
    bin_histo = np.zeros(grauwertklassen, dtype=int)
    cum_histo = np.zeros(grauwertklassen, dtype=int)

    for index, val in np.ndenumerate(img):
        # Um das Histogrammelement zu finden, kann der Pixelwert durch die Intervalllaenge dividiert
        # bzw. mit dem Kehrwert multipliziert werden
        i = int(val * grauwertklassen / K)
        # Der Zaehler fuer das Histogrammelement wird erhoeht
        bin_histo[i] += 1

    toAdd = 0
    for index, val in np.ndenumerate(bin_histo):
        cum_histo[index] += (val + toAdd)
        toAdd += val;

    cum_histo = cum_histo / cum_histo[len(cum_histo)-1]

    return cum_histo



def match_Histo(img_histo, ref_histo):
    #img_histo . . . original histogram
    #ref_histo . . . reference histogram
    lenHisto = len(img_histo)
    LUT = np.zeros(256, dtype=int)
    #returns the mapping function LUT to be applied to the image
    for i in range(lenHisto):
        j = lenHisto - 1
        LUT[i] = j
        j = j - 1
        while j >= 0 and img_histo[i] <= ref_histo[j]:
            LUT[i] = j
            j = j - 1

    return LUT

def apply_LUT(img, lut):
    img_arr = np.copy(img)

    # check clamping --> clamping already checked when generating lookup table

    for index, val in np.ndenumerate(img):
        img_arr[index] = lut[int(val)]

    return img_arr



def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = np.rint(0.2989 * r + 0.5870 * g + 0.1140 * b)
    return gray


if __name__ == "__main__":

    # read img
    img = Image.open("bild01.jpg")
    ref = Image.open("bild02.jpg")


    # convert to numpy array
    img_array = np.array(img)
    ref_array = np.array(ref)

    img_array = rgb2gray(img_array)
    ref_array = rgb2gray(ref_array)

    # compute histograms
    img_histo = compute_cumHisto(img_array, binSize=1)
    # histo_ref
    ref_histo = compute_cumHisto(ref_array, binSize=1)

    # compute mapping function (LUT) for matching histograms
    LUT = match_Histo(img_histo, ref_histo)
    # compute new image with lut
    # im_new

    # compute new histogram of new image
    img_new = apply_LUT(img_array, LUT)
    #img_new_gray =
    histo_new = compute_cumHisto(img_new, binSize=1)
    # plot information
    N = histo_new.size
    x = range(N)
    width = 1

    # plot histogram of new image
    plt.figure(1)
    plt.subplot(211)
    plt.bar(x, histo_new, width, color="blue")
    plt.xlim([0,N-1])
    # plot new img
    plt.figure(1)
    plt.subplot(212)
    plt.imshow(img_new, cmap = cm.Greys_r)

    # plot reference histogram
    plt.figure(2)
    plt.subplot(211)
    plt.bar(x, ref_histo, width, color="blue")
    plt.xlim([0,N-1])
    # plot reference image
    plt.figure(2)
    plt.subplot(212)
    plt.imshow(ref_array, cmap = cm.Greys_r)

    plt.show()

