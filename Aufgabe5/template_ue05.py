from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def medianFilter(in_image, filter, offset=0):
    out_image = np.copy(in_image)

    img_width = in_image.shape[1]
    img_height = in_image.shape[0]

    filter_index_start_x = -(int(filter.shape[0] / 2))
    filter_index_stop_x = -(int(filter.shape[0] / 2)) + int(filter.shape[0])
    filter_index_start_y = -int((filter.shape[1] / 2))
    filter_index_stop_y = -(int(filter.shape[1] / 2)) + int(filter.shape[1])

    scale_factor = 1.0 / filter.sum()

    for img_x in range(0, img_height):

        for img_y in range(0, img_width):
            sum = 0
            medianArray = np.array([])

            for filter_x in range(filter_index_start_x, filter_index_stop_x):

                for filter_y in range(filter_index_start_y, filter_index_stop_y):

                    img_access_index_x = img_x + filter_x
                    img_access_index_y = img_y + filter_y
                    filter_coefficient = filter[
                        filter_x + (filter_index_start_x * (-1)), filter_y + (filter_index_start_y * (-1))]

                    if (0 <= img_access_index_x <= img_height - 1) and (0 <= img_access_index_y <= img_width - 1):
                        sum += (filter_coefficient * in_image[img_access_index_x, img_access_index_y])
                        medianArray = np.append(medianArray, in_image[img_access_index_x, img_access_index_y])

                    else:
                        pass

            medianArray = np.sort(medianArray, axis=None, kind="heapsort")
            if medianArray.size % 2 is 0:
                median = round((medianArray[medianArray.size/2 + 1] + medianArray[medianArray.size/2]) / 2)
            else:
                median = medianArray[medianArray.size/2]

            # check clamping
            newPixel = median + offset
            if newPixel < 0:
                newPixel = 0
            elif newPixel > 255:
                newPixel = 255

            out_image[img_x, img_y] = newPixel

    return out_image


if __name__ == '__main__':
    in_image = Image.open("lena.jpg").convert("L")
    in_image = np.array(in_image)

    out_image = medianFilter(in_image, np.array([[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]), 0)

    new_img = Image.fromarray(out_image, 'L')
    new_img.save('lena_bigFilter.jpg')