from PIL import Image
import numpy as np


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = np.rint(0.2989 * r + 0.5870 * g + 0.1140 * b)
    return gray


def filterImage(in_image, filter, offset, edge=1):
    """Filters an 8-bit grayscale image.
        :param  in_image:   numpy array with grayscale values.
        :param  filter:     two-dimensional numpy arrays of size [(2N+1),(2M+1)]
        :param  offset:     integer value which is added to each filtered value.
        :param  edge:       integer value which specifies how boundary pixels are handled (1=min, 2=max, 3=mirror, 4=continue).
        :return out_image:  numpy array with filtered grayscale values.
    """

    out_image = np.copy(in_image)

    img_width = in_image.shape[1]
    img_height = in_image.shape[0]

    filter_index_start_x = -(int(filter.shape[0] / 2))
    filter_index_stop_x = -(int(filter.shape[0] / 2)) + int(filter.shape[0])
    filter_index_start_y = -int((filter.shape[1] / 2))
    filter_index_stop_y = -(int(filter.shape[1] / 2)) + int(filter.shape[1])


    if edge == 1:
        edge_value = 0
    elif edge == 2:
        edge_value = 255

    scale_factor = 1.0 / filter.sum()

    for img_x in range(0, img_height):

        for img_y in range(0, img_width):
            sum = 0
            for filter_x in range(filter_index_start_x, filter_index_stop_x):

                for filter_y in range(filter_index_start_y, filter_index_stop_y):

                    img_access_index_x = img_x + filter_x
                    img_access_index_y = img_y + filter_y
                    filter_coefficient = filter[filter_x + (filter_index_start_x * (-1)), filter_y + (filter_index_start_y * (-1))]

                    if (0 <= img_access_index_x <= img_height - 1) and (0 <= img_access_index_y <= img_width - 1):
                        sum += (filter_coefficient * in_image[img_access_index_x, img_access_index_y])

                    elif edge == 1 or edge == 2:
                        sum += (filter_coefficient * edge_value)

                    elif edge == 3:
                        # mirroring
                        if img_access_index_x >= img_height and img_access_index_y >= img_width:
                            sum += (filter_coefficient * in_image[img_access_index_x - img_height, img_access_index_y - img_width])
                        elif img_access_index_y >= img_width:
                            sum += (filter_coefficient * in_image[img_access_index_x, (img_access_index_y - img_width)])
                        elif img_access_index_x >= img_height:
                            sum += (filter_coefficient * in_image[(img_access_index_x - img_height), img_access_index_y])
                        else:
                            sum += (filter_coefficient * in_image[img_access_index_x, img_access_index_y])

                    elif edge == 4:
                        # continuing
                        if img_access_index_x < 0 and img_access_index_y < 0:
                            sum += (filter_coefficient * in_image[0,0])
                        elif img_access_index_x > (img_height-1) and img_access_index_y > (img_width - 1):
                            sum += (filter_coefficient * in_image[img_height - 1, img_width - 1])
                        elif img_access_index_x < 0 or img_access_index_x > (img_height-1):
                            if img_access_index_y > (img_width-1):
                                sum += (filter_coefficient * in_image[img_x, img_width-1])
                            elif img_access_index_y < 0:
                                sum += (filter_coefficient * in_image[img_x, 0])
                            else:
                                sum += (filter_coefficient * in_image[img_x, img_access_index_y])
                        elif img_access_index_y < 0 or img_access_index_y > (img_width-1):
                            if img_access_index_x > (img_height-1):
                                sum += (filter_coefficient * in_image[img_height-1, img_y])
                            elif img_access_index_x < 0:
                                sum += (filter_coefficient * in_image[0, img_y])
                            else:
                                sum += (filter_coefficient * in_image[img_access_index_x, img_y])

            filtered_val = int(scale_factor * sum) + offset

            # check clamping
            if filtered_val < 0:
                filtered_val = 0
            elif filtered_val > 255:
                filtered_val = 255

            out_image[img_x, img_y] = filtered_val

    return out_image


if __name__ == '__main__':
    # read img
    img = Image.open("bild02.jpg")

    # convert to numpy array
    img_array = np.array(img)

    # convert to grayscale
    img_gray = rgb2gray(img_array)
    print(img_gray)

    filter = np.array([[1.0,2.0,3.0,2.0,1.0],[2.0,3.0,5.0,3.0,2.0],[3.0,5.0,8.0,5.0,3.0],[2.0,3.0,5.0,3.0,2.0],[1.0,2.0,3.0,2.0,1.0]])

    # apply filter to grayscale
    out_image = filterImage(img_gray, filter, 50, 4)
    print(out_image.shape)

    # save filtered array as image
    filtered_img_array = np.array(img_array)
    filtered_img_array[:, :, 0] = out_image
    filtered_img_array[:, :, 1] = out_image
    filtered_img_array[:, :, 2] = out_image

    filtered_img = Image.fromarray(filtered_img_array, 'RGB')
    filtered_img.save('bild02_filtered_continue.jpg')
