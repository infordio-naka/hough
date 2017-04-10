from __future__ import print_function

import cv2
import numpy      as     np
from   preprocess import preprocess
from   argments   import get_args

def canny(pre_img, args):
    """
    Return detect edges image

    :param pre_img: image
    :param dict args:    for canny argments
    """
    edges = cv2.Canny(pre_img,
                      threshold1=args.threshold1,
                      threshold2=args.threshold2,
                      apertureSize=args.apertureSize,
                      L2gradient=args.l2gradient)
    if (args.debug):
        cv2.imwrite("./results/canny.jpg", edges)
    return (edges)

if __name__ == "__main__":
    args       = get_args()
    pre_img, _ = preprocess(args)
    canny(pre_img, args)
