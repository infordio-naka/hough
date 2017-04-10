from __future__ import print_function

import cv2
import numpy as np
import argparse
from   argments import get_args

def denoise(img, args):
    """
    Return denoised image

    :param int[] img: grayscaled image
    """
    denoised = img
    kernel   = np.ones((2, 2), np.uint8)
    #denoised = cv2.morphologyEx(denoised, cv2.MORPH_OPEN, kernel, iterations=2)
    #denoised = cv2.morphologyEx(denoised, cv2.MORPH_, kernel, iterations=2)
    #denoised = cv2.morphologyEx(denoised, cv2.MORPH_DILATE, kernel, iterations=2)
    #denoised = cv2.morphologyEx(denoised, cv2.MORPH_ERODE, kernel, iterations=2)
    denoised = cv2.GaussianBlur(denoised, ksize=(args.ksize, args.ksize), sigmaX=args.sigmax)
    if (args.debug):
        cv2.imwrite("./results/denoised.jpg",   denoised)

    return (denoised)

def preprocess(args):
    """
    Retrun binary image and raw image
    
    :param dict args: for preprocess argments
    """
    rawImg   = cv2.imread(args.in_image)
    gray     = cv2.cvtColor(rawImg, args.code)
    denoised = denoise(gray, args)
    ret, binImg  = cv2.threshold(denoised, args.pthreshold, args.maxval, args.ttype)
    if (args.debug):
        cv2.imwrite("./results/raw_img.jpg",   rawImg)
        cv2.imwrite("./results/gray.jpg",      gray)
        cv2.imwrite("./results/binImg.jpg",    binImg)
    return (binImg, rawImg)
    #return (binImg, rawImg)

if __name__ == "__main__":
    args       = get_args()
    gauss, _ = preprocess(args)
