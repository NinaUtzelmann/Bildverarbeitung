from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def dilate(in_image, filter, iternum):
    out_image = np.copy(in_image)

    filter_index_start_x = -(int(filter.shape[0] / 2))
    filter_index_stop_x = -(int(filter.shape[0] / 2)) + int(filter.shape[0])
    filter_index_start_y = -int((filter.shape[1] / 2))
    filter_index_stop_y = -(int(filter.shape[1] / 2)) + int(filter.shape[1])

    for i in range(iternum):
        for img_x in range(0, in_image.shape[0]):

            for img_y in range(0, in_image.shape[1]):
                maxList = np.array([])
                for filter_x in range(filter_index_start_x, filter_index_stop_x):

                    for filter_y in range(filter_index_start_y, filter_index_stop_y):
                        img_access_index_x = img_x + filter_x
                        img_access_index_y = img_y + filter_y

                        if (0 <= img_access_index_x <= in_image.shape[0] - 1) and (0 <= img_access_index_y <= in_image.shape[1] - 1):
                            maxList = np.append(maxList, in_image[img_access_index_x, img_access_index_y] + filter[filter_x, filter_y])

                maxValue = maxList.max()
                if maxValue > 255:
                    maxValue = 255
                if maxValue < 0:
                    maxValue = 0
                out_image[img_x, img_y] = maxValue

    return out_image

def erode(in_image, filter, iternum):
    inverted_image = invert(in_image)
    dilated_image = dilate(inverted_image, filter, iternum)
    inverted_image = invert(dilated_image)

    return inverted_image

def invert(in_image):
    inverted_image = np.copy(in_image)

    for index, val in np.ndenumerate(in_image):
        inverted_image[index] = 255 - val

    return inverted_image


if __name__ == '__main__':
    image = Image.open("fhorn.jpg").convert("L")
    image = np.array(image)

    filter = np.array([[0,0,5,0,0],[0,5,5,5,0],[5,5,5,5,5],[0,5,5,5,0],[0,0,5,0,0]])
    iternum = 1
    out_image = dilate(image, filter, iternum)
    new_image = Image.fromarray(out_image, 'L')
    new_image.save('fhorn_dilated_raute.jpg')