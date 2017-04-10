from __future__ import print_function

import cv2
import numpy as np
from progressbar import ProgressBar
from argments    import get_args
from preprocess  import preprocess
from canny       import canny
from hough       import hough
from sortLines   import sortLines
from mergeLines  import mergeLines

def main(args):
    """
    Excute detect lines process

    :param None: argment is None
    """
    # read img and preprocess
    pre_img, rawImg = preprocess(args)

    # detect edges
    #edges_img = canny(pre_img, args)
    
    # hough trasform
    lines = hough(pre_img, rawImg, args)
    
    # postprocess
    ## sort lines
    if (not args.opt):
        sortedLines = sortLines(lines)

    ## merge lines
    #mergedLines = mergeLines(lines, rawImg, args)

if __name__ == "__main__":
    # get argments
    args = get_args()
    if (args.debug):
        print("---------------------------------------------------------------------------")
        print("=======================")
        print("# run as <DEBUG MODE> #")
        print("=======================")
        print("[argments list]")
        for key, value in vars(args).iteritems():
            print(key,value)
        print("---------------------------------------------------------------------------")
    main(args)
