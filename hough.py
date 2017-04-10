from __future__ import print_function

import cv2
import numpy as np
from progressbar import ProgressBar
from argments    import get_args
from preprocess  import preprocess
from canny       import canny
from copy        import copy

def hough(edges, rawImg, args):
    """
    Return detect lines and Write image with detect lines

    :param edges:  image with extraction edges
    :param rawImg: then preprocess read raw image
    :param args:   for hough
    """
    canvasImg = copy(rawImg)
    lines = cv2.HoughLinesP(edges,
                            rho=args.rho,
                            theta=args.theta,
                            threshold=args.threshold,
                            lines=args.lines,
                            minLineLength=args.minLineLength,
                            maxLineGap=args.maxLineGap)
    
    try:
        lines = np.asarray([line for l in lines for line in l])
        if (args.debug or args.opt):
            p = ProgressBar(1, len(lines))
            i = 0
            for x1, y1, x2, y2 in lines:
                cv2.line(canvasImg, (x1, y1), (x2, y2), (0, 255, 0), 2)
                p.update(i+1)
                i += 1
    except TypeError, ZeroDivisionError:
        pass
    cv2.imwrite("./results/result.jpg", canvasImg)

    return (lines)

if __name__ == "__main__":
    args             = get_args()
    pre_img, raw_img = preprocess(args)
    edges_img        = canny(pre_img, args)
    hough_img        = hough(edges_img, raw_img, args)
