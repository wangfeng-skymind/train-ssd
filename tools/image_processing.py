import numpy as np
import cv2

def rescale(im, target_size, max_size):
    """
    only resize input image to target size and return scale

    Parameters:
    ----------
    im : numpy.array
        BGR image input by opencv
    target_size: int
        one dimensional size (the short side)
    max_size: int
        one dimensional max size (the long side)

    Returns:
    ----------
    numpy.array, rescaled image
    """
    im_shape = im.shape
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.min(im_shape[0:2])
    im_scale = float(target_size) / float(im_size_min)
    # prevent bigger axis from being more than max_size:
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)
    im = cv2.resize(im, None, None, fx=im_scale, fy=im_scale, interpolation=cv2.INTER_LINEAR)
    return im, im_scale

def resize(im, target_size, interp_method=cv2.INTER_LINEAR):
    """
    resize image to target size regardless of aspect ratio

    Parameters:
    ----------
    im : numpy.array
        BGR image input by opencv
    target_size : tuple (int, int)
        (h, w) two dimensional size
    Returns:
    ----------
    numpy.array, resized image
    """
    return cv2.resize(im, target_size, interpolation=interp_method)

def transform(im):
    im_tensor = im.transpose(2, 0, 1)
    im_tensor = im_tensor[np.newaxis, :]
    im_tensor = (im_tensor - 127.5)*0.0078125
    return im_tensor


def transform_inverse(im_tensor, pixel_means):
    """
    transform from mxnet im_tensor to ordinary RGB image
    im_tensor is limited to one image

    Parameters:
    ----------
    im_tensor : numpy.array
        in shape [batch, channel, height, width]
    pixel_means: list
        [[[R, G, B pixel means]]]

    Returns:
    ----------
    im [height, width, channel(RGB)]
    """
    assert im_tensor.shape[0] == 1
    im_tensor = im_tensor.copy()
    # put channel back
    channel_swap = (0, 2, 3, 1)
    im_tensor = im_tensor.transpose(channel_swap)
    im = im_tensor[0]
    assert im.shape[2] == 3
    im = im*128+127.5
    im = im.astype(np.uint8)
    return im