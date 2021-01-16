import cv2

# This example requires the use of TWO cameras
# this is a work in progress and doesn't work perfectly, I didn't have steroscopic
# cameras, had to use the laptop camera and a usb camera, so it was bad output

capA = cv2.VideoCapture(0) # 0 for first device (webcam by default)
# pos 1 is laptop IR sensor
capB = cv2.VideoCapture(4) # 2 for second device (attached camera)


frameSize = (640, 480)

capA.set(cv2.CAP_PROP_FRAME_WIDTH, frameSize[0])
capA.set(cv2.CAP_PROP_FRAME_HEIGHT, frameSize[1])

capB.set(cv2.CAP_PROP_FRAME_WIDTH, frameSize[0])
capB.set(cv2.CAP_PROP_FRAME_HEIGHT, frameSize[1])

zoom = 1.0
capA.set(cv2.CAP_PROP_ZOOM, zoom)
capB.set(cv2.CAP_PROP_ZOOM, zoom)

while(True):
    # capture frame by frame (save last to lastFrame)
    retA, frameA = capA.read()
    retB, frameB = capB.read()

    # make gray scale
    frameA = cv2.cvtColor(frameA, cv2.COLOR_BGR2GRAY)
    frameB = cv2.cvtColor(frameB, cv2.COLOR_BGR2GRAY)

    stero = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stero.compute(frameA, frameB)

    cv2.imshow('frameA', frameA)
    cv2.imshow('frameB', frameB)

    # display the resulting frame
    # normalize for available values
    disparity = cv2.normalize(disparity, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    cv2.imshow('depth disparity', disparity)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when everything done, release capture
capA.release()
capB.release()
cv2.destroyAllWindows()
