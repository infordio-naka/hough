from __future__ import print_function

import cv2
import numpy as np
from progressbar import ProgressBar
from argments    import get_args
from preprocess  import preprocess
from canny       import canny
from hough       import hough

def sortLines(lines):
    """
    Return sorted lines

    line(x1, y1, x2, y2) in lines,
    defined to:
    start_p = (x1, y1)
    end_p   = (x2, y2)

    to sort as start_p < end_p at all line for merge line

    :param lines: hough transform lines
    """
    for i in range(len(lines)):
        start_p = np.copy(lines[i][:2])
        end_p   = np.copy(lines[i][2:])
        if (sum(start_p) > sum(end_p)):
            lines[i][:2] = end_p
            lines[i][2:] = start_p
