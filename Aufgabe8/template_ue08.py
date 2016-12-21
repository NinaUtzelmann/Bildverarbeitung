from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

collissions = list()
labels = list()
mergedLabels = list()
existingRegions = list()

def assignLabels(image_binar):
    labeled_image = np.copy(image_binar)
    label = 2

    for height in range(0, image_binar.shape[0]):               # go through picture
        for width in range(0, image_binar.shape[1]):

            if image_binar[height][width]:                      # when pixel is foreground

                if not(height - 1 < 0 or width - 1 < 0):        # if index is valid

                    if not(labeled_image[height - 1][width]) and not(labeled_image[height][width - 1]):     # when all neighbours are background

                        labeled_image[height][width] = label                                   # pixel is labeled
                        labelset = set()
                        labelset.add(label)
                        labels.append(labelset)
                        label += 1

                    elif (labeled_image[height - 1][width] > 1) != (labeled_image[height][width - 1] > 1):      # logical XOR --> if EXACTLY ONE neighbour is labeled (bei Vierer-Nachbarschaft)
                        if labeled_image[height - 1][width] > 1:
                            labeled_image[height][width] = labeled_image[height - 1][width]
                        else:
                            labeled_image[height][width] = labeled_image[height][width - 1]

                    else:
                        labeled_image[height][width] = labeled_image[height - 1][width]
                        if labeled_image[height - 1][width] != labeled_image[height][width - 1]:
                            collission = set()


                            collission.add(labeled_image[height][width - 1])
                            collission.add(labeled_image[height - 1][width])

                            if not collission in collissions:   #collission nur hinzufügen wenn noch nicht vorhanden
                                collissions.append(collission)

    return labeled_image


def resolveCollisions():
    for col in collissions:
        #tempIndizes = np.array([], dtype=np.int8)
        a = col.pop()
        b = col.pop()

        if a > b:
            x = a
            a = b
            b = x

        for labelA in labels:
            if a in labelA:
                for labelB in labels:
                    if b in labelB and a not in labelB and b not in labelA:
                        for xinlabelB in labelB:
                            labelA.add(xinlabelB)
                        labels.remove(labelB)
                        continue


def relableTheImage(labeledImage):

    for y in range(0, labeledImage.shape[0]):
        for x in range(0, labeledImage.shape[1]):
            if labeledImage.item(y, x) > 1:
                for index in range(len(labels)):
                    if labeledImage.item(y, x) in labels[index]:
                        j = index
                        k = min(labels[index])
                        labeledImage[y][x] = k
                        if k not in existingRegions:
                            existingRegions.append(k)

    return labeledImage

def highlightRegions(relabledImage):

    highLightStartValue = 40
    highlightedRegions = relabledImage
    gray_step = int((255-highLightStartValue)/(len(existingRegions)-1))
    highlightValues = list()
    highlightValues.append(highLightStartValue)

    for region in existingRegions:
        if existingRegions.index(region) is not 0:
            highLightStartValue += gray_step
            highlightValues.append(highLightStartValue)

    for y in range(0, relabledImage.shape[0]):
        for x in range(0, relabledImage.shape[1]):
            if relabledImage.item(y, x) > 1:
                highlightedRegions[y][x] = highlightValues[existingRegions.index(relabledImage.item(y, x))]

    return highlightedRegions


if __name__ == '__main__':
    image = Image.open("regionen1.png").convert("L")
    image = np.array(image)
    image_binar = image.copy()
    image_binar[image == 255] = 0       # white --> background (false)
    image_binar[image == 0] = 1         # black --> foreground (true)

    out_image = np.copy(image)

    labeled_image = assignLabels(image_binar)

    print("Collissions: ")
    print(collissions)
    print("Labels: ")
    print(labels)
    resolveCollisions()
    print("merged Labels: ")
    print(labels)
    
    relabledImage = relableTheImage(labeled_image)
    highlightedRegions = highlightRegions(relabledImage)

    plt.figure(2)
    plt.subplot(211)
    plt.imshow(image, cmap=cm.Greys_r)
    plt.subplot(212)
    plt.imshow(highlightedRegions, cmap=cm.Greys_r)
    plt.show()


