import fractions
import imp
import marscam
# from ImageConvert import *
# from MVSDK import *
import numpy as np
import cv2
import gc
import time
import os


cam = marscam.marscam()
dir = os.path.dirname(os.path.realpath(__file__))
# os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python')
os.chdir(dir)


mtx = np.array([[1.06552448e+03, 0.00000000e+00, 3.68445322e+02],
                [0.00000000e+00, 1.06982462e+03, 3.36153499e+02],
                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist = np.array([[6.48752208e+00, -1.51685038e+02, -1.65582503e-02, -5.05444850e-02,
                  1.14113631e+03]])


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def demo():
    cam.setCamera(0)
    cam.openCamera()
    cam.setExposureAuto("Auto")

    while 1:
        frame = cam.stream()
        # rescale = rescale_frame(frame, percent=50)
        cv2.imshow('mars-cam', frame)

        # dst = cv2.undistort(frame, mtx, dist, None, None)
        # cv2.imshow("undistort", dst)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite(
                "capture/" + str(round(time.time() * 1000)) + ".jpg", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    cam.closeCamera()
    return 0


if __name__ == "__main__":
    nRet = demo()
    if nRet != 0:
        print("Some Error happend")
    print("--------- Demo end ---------")
