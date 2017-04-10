from __future__ import print_function

import numpy as np
import cv2
import argparse

def get_args():
    """
    Return argments for each process

    :param None: argment is None
    """
    # for optimizer_pram
    parser = argparse.ArgumentParser()
    parser.add_argument("-datapath", "--dpath",       type=str,   default="./dataset/binary.txt", help="[optimizer]dataset path")
    parser.add_argument("-ind",      "--individuals", type=int,   default=100,                    help="[optimizer]Number of individuals")
    parser.add_argument("-gene",     "--gene",        type=int,   default=68,                     help="[optimizer]Length of gene")
    parser.add_argument("-revo" ,    "--revolution",  type=int,   default=100,                    help="[optimizer]Number of revolution")
    parser.add_argument("-elite",    "--elite",                   default=False,                  help="[optimizer]Use elite selection", action="store_true")
    parser.add_argument("-esize",    "--esize",       type=int,   default=2,                      help="[optimizer]Size of elite")
    parser.add_argument("-tornsize", "--tornsize",    type=int,   default=3,                      help="[optimizer]Size of tournament")
    parser.add_argument("-mode",     "--mode",        type=str,   default="min",                  help="[optimizer]Max or min")
    parser.add_argument("-crate",    "--crossrate",   type=float, default=0.7,                    help="[optimizer]probability of crossover")
    parser.add_argument("-cmode",    "--crossmode",   type=str,   default="one",                  help="[optimizer]one or two or random")
    parser.add_argument("-mrate",    "--mutaterate",  type=float, default=0.05,                   help="[optimizer]probability of mutation")
    parser.add_argument("-teach",    "--teach_image", type=str,   default="images/sample_rakuju1_teach.jpg", help="[optimizer]teach image")
    parser.add_argument("--opt",     "--optimize",                default=False,                  help="optimize", action="store_true")

    # for preprocess
    parser.add_argument("--in_image",  "-in",   type=str,   default="./images/sample2.jpg", help="[preprocess]input image file path")
    parser.add_argument("--code",      "-c",    type=int,   default=cv2.COLOR_BGR2GRAY,     help="[preprocess]color space conversion code")
    parser.add_argument("--ksize",     "-k",    type=int,   default=5,                      help="[preprocess]Gaussian kernel size. ksize.width and ksize.height can differ but they both must be positive and odd. Or, they can be zero's  and then they are computed from sigma ")
    parser.add_argument("--sigmax",    "-sigx", type=int,   default=0,                      help="[preprocess]Gaussian kernel standard deviation in X direction.")
    parser.add_argument("--pthreshold","-ptr",  type=float, default=100,                    help="[preprocess]threshold value.")
    parser.add_argument("--maxval",    "-mval", type=int,   default=255,                    help="[preprocess]maximum value to use with the THRESH_BINARY and THRESH_BINARY_INV thresholding types.")
    parser.add_argument("--ttype",     "-tt",    type=int,   default=cv2.THRESH_BINARY_INV,  help="[preprocess]thresholding type")

    # for canny
    parser.add_argument("--threshold1",    "-tr1",  type=float, default=50,    help="[canny]first threshold for the hysteresis procedure.")
    parser.add_argument("--threshold2",    "-tr2",  type=float, default=150,   help="[canny]second threshold for the hysteresis procedure.")
    parser.add_argument("--apertureSize",  "-as",   type=int,   default=3,     help="[canny]aperture size for the Sobel() operator.")
    parser.add_argument("--l2gradient",    "-l2g",              default=False, help="[canny]a flag, indicating whether a more accurate  L_2 norm =\sqrt{(dI/dx)^2 + (dI/dy)^2} should be used to calculate the image gradient magnitude ( L2gradient=true ), or whether the default  L_1 norm  =|dI/dx|+|dI/dy| is enough ( L2gradient=false ).", action='store_true')

    # for hough
    parser.add_argument("--rho",           "-rho", type=int,   default=1,         help="[hough]Distance resolution of the accumulator in pixels.")
    parser.add_argument("--theta",         "-th",  type=float, default=np.pi/180, help="[hough]Angle resolution of the accumulator in radians.")
    parser.add_argument("--threshold",     "-tr",  type=int,   default=100,       help="[hough]Accumulator threshold parameter. Only those lines are returned that get enough votes ( >\texttt{threshold} ).")
    parser.add_argument("--lines",         "-l",   type=int,   default=100,       help="[hough]Minimum line length. Line segments shorter than that are rejected.")
    parser.add_argument("--minLineLength", "-len", type=float, default=150,       help="[hough]Minimum line length. Line segments shorter than that are rejected.")
    parser.add_argument("--maxLineGap",    "-gap", type=float, default=50,        help="[hough]Maximum allowed gap between points on the same line to link them.")

    # for mergeLine
    parser.add_argument("--wSize",         "-ws",  type=int,   default=3,         help="[mergeLine]detection window width size")
    parser.add_argument("--hSize",         "-hs",  type=int,   default=3,         help="[mergeLine]detection window height size")

    # othrer
    parser.add_argument("--debug",         "-d",               default=False,     help="debug", action="store_true")
    args = parser.parse_args()

    return (args)

if __name__ == "__main__":
    print(get_args())
