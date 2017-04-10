from __future__ import print_function

import cv2
import numpy as np
from argments    import get_args
from progressbar import ProgressBar
from preprocess  import preprocess
from canny       import canny
from hough       import hough

def postprocess(lines, args):
    """
    Return and write postprocess image

    :param lines: image with extracted edges
    :param args:  for postprocess argments
    """
    mergeLine = 
