import cv2 as cv
import numpy as np

run = False

def draw(event, x, y, flag, param):
    global run
    
    if event == cv.EVENT_LBUTTONDOWN:
        run = True
        cv.circle(image, (x,y), 15 , (0,0,0), -1)

    if event == cv.EVENT_LBUTTONUP:
        run = False

    if event == cv.EVENT_MOUSEMOVE:
        if run == True:
            cv.circle(image, (x,y), 15 , (0,0,0), -1)

def draw_1(event, x, y, flag, param):
    global run
    
    if event == cv.EVENT_LBUTTONDOWN:
        run = True
        cv.circle(image, (x,y), 15 , (255,255,255), -1)

    if event == cv.EVENT_LBUTTONUP:
        run = False

    if event == cv.EVENT_MOUSEMOVE:
        if run == True:
            cv.circle(image, (x,y), 15 , (255,255,255), -1)

def specify_roi(frame,name=None):
    
    global image
    image = frame
    if(name==None):
        out = "mask_image.png"
    else:
        out = name
    
    cv.namedWindow('Specify your Region of Interest')
    cv.setMouseCallback('Specify your Region of Interest',draw)

    while(1):
        cv.imshow('Specify your Region of Interest',image)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            cv.destroyAllWindows()
            break

    image[image != 0] = 255 # change everything to white where pixel is not black

    cv.namedWindow('Make whole background white if there are any unnecessary pixels')
    cv.setMouseCallback('Make whole background white if there are any unnecessary pixels',draw_1)

    while(1):
        cv.imshow('Make whole background white if there are any unnecessary pixels',image)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            cv.destroyAllWindows()
            break

    cv.imwrite(out, image)

    return image
    