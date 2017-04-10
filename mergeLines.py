from __future__ import print_function

import cv2
import itertools
import numpy as np
from argments    import get_args
from progressbar import ProgressBar
from preprocess  import preprocess
from canny       import canny
from hough       import hough
from copy        import copy

def getManhattanDistance(x1, y1, x2, y2):
    """
    Return manhattan distance

    :param int x1: x1 of point1
    :param int y1: y1 of point1
    :param int x2: x2 of point2
    :param int y2: y2 of point2
    """
    distance = abs(x1-x2)+abs(y1-y2)
    return (distance)

def getLineDirection(line):
    """
    Return line direction
    
    :param int[] line: target line
    """
    x1, y1, x2, y2 = line
    direction = "vertical"
    if (abs(x1-x2)>abs(y1-y2)):
        direction = "holizontal"
    return (direction)

def isSameAreaLine(line, cline):
    """
    Return same area or not between line and cline

    =============================================

           =>
    [line] *-------------*----        endpoint
     startpoint      ----*-------------* [cline]
                 close<=threshold     <=

    =============================================

    :param int[] line:  current line
    :param int[] cline: compare line
    """
    #paramerter
    threshold  = 10
    breakpoint = 1000

    sameAreaLine = False

    lineDirection  = getLineDirection(line)
    clineDirection = getLineDirection(cline)
    #print("lineDirection:  ", lineDirection)
    #print("clineDirection: ", clineDirection)
    if (lineDirection==clineDirection):
        if (lineDirection=="vertical"):
            line_start  = line[1]
            line_end    = line[3]
            line_other  = line[0]  # x point of line
            cline_start = cline[1]
            cline_end   = cline[3]
            cline_other = cline[0] # x point of cline
        else:
            line_start  = line[0]
            line_end    = line[2]
            line_other  = line[1]  # y point of line
            cline_start = cline[0]
            cline_end   = cline[2]
            cline_other = cline[1] # y point of cline

        linePoints   = [i for i in range(line_start+1,   line_end)]
        clinePoints  = [i for i in range(cline_start+1, cline_end)]
        distanceList = []
        for line_point, cline_point in itertools.product(linePoints, clinePoints):
            distanceList.append(getManhattanDistance(line_point,
                                                     line_other,
                                                     cline_end,
                                                     cline_other))
            if (distanceList[-1]> breakpoint):
                break
            if (distanceList[-1]<threshold):
                sameAreaLine = True
                break
        """
        while (((line_start!=line_end) and
                (cline_start!=cline_end))):
            distance = getManhattanDistance(line_start,
                                            line_other,
                                            cline_end,
                                            cline_other)
            if (distance<=threshold):
                sameAreaLine = True
                break
            if (line_start!=line_end):
                line_start += 1
            if (cline_start!=cline_end):
                cline_end  -= 1
        """
    return (sameAreaLine)

def getCloseLines(line, candidateLines):
    """
    Return close lines

    :param line:           current   line
    :param candidateLines: candidate lines
    """
    closeLines = []
    for i, cline in enumerate(candidateLines):
        #print("current line: ", line)
        #print("compare line: ", cline)
        sameAreaLine = isSameAreaLine(line, cline)
        if (sameAreaLine!=False):
            closeLines.append(cline)
            del candidateLines[i]

    return (closeLines, candidateLines)

def mergeLines(lines, rawImg, args):
    """
    Return merged lines(main function)

    Merge same line area in lines

    :param int[][] sortedLines:  sorted hough transform lines
    :param int[][] rawImg:       then preprocess read raw image
    :param dict    args:         for mergeLines argments
    """
    canvasImg      = copy(rawImg)
    candidateLines = list(lines)
    mergedLines    = []
    def merge(line, closeLines):
        """
        Return merged lines
        
        :param int[][] line:       current line
        :param int[]   closeLines: close lines from current line
        """
        lines = np.vstack((line, closeLines))
        #print(lines)
        min_point  = np.min(lines[:,0:2], axis=0)
        max_point  = np.max(lines[:,2:], axis=0)
        mergedLine = [min_point[0],
                      min_point[1],
                      max_point[0],
                      max_point[1]]
        #print(mergedLine)

        return (mergedLine)

    closeLines_cnt = 0 # debug
    while (len(candidateLines)>0): # [!] not yet break conditions
        line = candidateLines.pop(0)
        closeLines, candidateLines = getCloseLines(line, candidateLines)
        closeLines_cnt+=len(closeLines) # debug
        #print(closeLines)
        if (closeLines!=[]):
            mergedLine = merge(line, np.asarray(closeLines)) # merge lines
            candidateLines.append(mergedLine)                # append merged line in candidateLines
        else:
            mergedLines.append(line)
        print("candidateLines: ", len(candidateLines)) # debug
    print("closeLines_cnt: ", closeLines_cnt) # debug
    if (args.debug):
        p = ProgressBar(1, len(mergedLines))
        i = 0
        for x1, y1, x2, y2 in mergedLines:
            cv2.line(canvasImg, (x1, y1), (x2, y2), (0, 255, 0), 2)
            p.update(i+1)
            i += 1
        cv2.imwrite("./results/merged_result.jpg", canvasImg)
    exit()
    return (mergedLines)

if __name__ == "__main__":
    args             = get_args()
    pre_img, rawImg  = preprocess(args)
    #edges_img        = canny(pre_img, args)
    lines            = hough(pre_img, rawImg, args)
    mergedLines      = mergeLines(lines, rawImg, args)
