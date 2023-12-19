import marscam
from ImageConvert import *
from MVSDK import *
import numpy
import cv2
import gc
import datetime


cam = marscam.marscam()


def demo():
    # enumerate camera
    cameraCnt, cameraList = cam.enumCameras()
    if cameraCnt is None:
        return -1

    # print camera info
    for index in range(0, cameraCnt):
        camera = cameraList[index]
        print("\nCamera Id = " + str(index))
        print("Key           = " + str(camera.getKey(camera)))
        print("vendor name   = " + str(camera.getVendorName(camera)))
        print("Model  name   = " + str(camera.getModelName(camera)))
        print("Serial number = " + str(camera.getSerialNumber(camera)))

    camera = cameraList[0]

    # open camera
    nRet = cam.openCamera(camera)
    if (nRet != 0):
        print("openCamera fail.")
        return -1

    # create stream source object
    streamSourceInfo = GENICAM_StreamSourceInfo()
    streamSourceInfo.channelId = 0
    streamSourceInfo.pCamera = pointer(camera)

    streamSource = pointer(GENICAM_StreamSource())
    nRet = GENICAM_createStreamSource(
        pointer(streamSourceInfo), byref(streamSource))
    if (nRet != 0):
        print("create StreamSource fail!")
        return -1

    # create corresponding property node according to the value type of property, here is enumNode
    # set trigger mode to Off for continuously grabbing
    trigModeEnumNode = pointer(GENICAM_EnumNode())
    trigModeEnumNodeInfo = GENICAM_EnumNodeInfo()
    trigModeEnumNodeInfo.pCamera = pointer(camera)
    trigModeEnumNodeInfo.attrName = b"TriggerMode"
    nRet = GENICAM_createEnumNode(
        byref(trigModeEnumNodeInfo), byref(trigModeEnumNode))
    if (nRet != 0):
        print("create TriggerMode Node fail!")
        # release node resource before return
        streamSource.contents.release(streamSource)
        return -1

    nRet = trigModeEnumNode.contents.setValueBySymbol(trigModeEnumNode, b"Off")
    if (nRet != 0):
        print("set TriggerMode value [Off] fail!")
        # release node resource before return
        trigModeEnumNode.contents.release(trigModeEnumNode)
        streamSource.contents.release(streamSource)
        return -1

    # release node resource at the end of use
    trigModeEnumNode.contents.release(trigModeEnumNode)

    # start grabbing
    nRet = streamSource.contents.startGrabbing(streamSource, c_ulonglong(0),
                                               c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
    if (nRet != 0):
        print("startGrabbing fail!")
        # release stream source object before return
        streamSource.contents.release(streamSource)
        return -1

    isGrab = True

    while isGrab:
        # get one frame
        frame = pointer(GENICAM_Frame())
        nRet = streamSource.contents.getFrame(
            streamSource, byref(frame), c_uint(1000))
        if (nRet != 0):
            print("getFrame fail! Timeout:[1000]ms")
            # release stream source object before return
            streamSource.contents.release(streamSource)
            return -1
        else:
            print("getFrame success BlockId = [" + str(frame.contents.getBlockId(
                frame)) + "], get frame time: " + str(datetime.datetime.now()))

        nRet = frame.contents.valid(frame)
        if (nRet != 0):
            print("frame is invalid!")
            # release frame resource before return
            frame.contents.release(frame)
            # release stream source object before return
            streamSource.contents.release(streamSource)
            return -1

        # fill conversion parameter
        imageParams = IMGCNV_SOpenParam()
        imageParams.dataSize = frame.contents.getImageSize(frame)
        imageParams.height = frame.contents.getImageHeight(frame)
        imageParams.width = frame.contents.getImageWidth(frame)
        imageParams.paddingX = frame.contents.getImagePaddingX(frame)
        imageParams.paddingY = frame.contents.getImagePaddingY(frame)
        imageParams.pixelForamt = frame.contents.getImagePixelFormat(frame)

        # copy image data out from frame
        imageBuff = frame.contents.getImage(frame)
        userBuff = c_buffer(b'\0', imageParams.dataSize)
        memmove(userBuff, c_char_p(imageBuff), imageParams.dataSize)

        # release frame resource at the end of use
        frame.contents.release(frame)

        # no format conversion required for Mono8
        if imageParams.pixelForamt == EPixelType.gvspPixelMono8:
            grayByteArray = bytearray(userBuff)
            cvImage = numpy.array(grayByteArray).reshape(
                imageParams.height, imageParams.width)
        else:
            # convert to BGR24
            rgbSize = c_int()
            rgbBuff = c_buffer(b'\0', imageParams.height *
                               imageParams.width * 3)

            nRet = IMGCNV_ConvertToBGR24(cast(userBuff, c_void_p),
                                         byref(imageParams),
                                         cast(rgbBuff, c_void_p),
                                         byref(rgbSize))

            colorByteArray = bytearray(rgbBuff)
            cvImage = numpy.array(colorByteArray).reshape(
                imageParams.height, imageParams.width, 3)
    # --- end if ---

        cv2.imshow('myWindow', cvImage)
        gc.collect()

        if (cv2.waitKey(1) >= 0):
            isGrab = False
            break
    # --- end while ---

    cv2.destroyAllWindows()

    # stop grabbing
    nRet = streamSource.contents.stopGrabbing(streamSource)
    if (nRet != 0):
        print("stopGrabbing fail!")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # close camera
    nRet = cam.closeCamera(camera)
    if (nRet != 0):
        print("closeCamera fail")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # release stream source object at the end of use
    streamSource.contents.release(streamSource)

    return 0


if __name__ == "__main__":

    nRet = demo()
    if nRet != 0:
        print("Some Error happend")
    print("--------- Demo end ---------")
