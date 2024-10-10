import get_traffic_count as gtc
import get_traffic_slots as gts
import specify_roi as roi
import cv2 as cv
import os
import multiprocessing
import time
import matplotlib.pyplot as plt

def show_bar_plots(time, baseTimer, list):
    
    nlanes = len(list)

    l=[]
    l.append('g')
    for i in range(nlanes -1):
        l.append('r')
    if nlanes == 3:
        lanes = ['lane1','lane2','lane3']
    elif nlanes == 4:
        lanes = ['lane1','lane2','lane3','lane4']
    tlzero = []
    tlzero.append(list[0])
    tlzero.append(list[0])
    tlzero.append(list[0] + list[1])
    if nlanes == 4:
        tlzero.append(list[0] + list[1] + list[2])
    plt.xlabel("Lanes")
    plt.ylabel("Light Color")
    plt.title("Traffic Signals after " + str(time) + " seconds: ")
    plt.bar(lanes, tlzero, color=l)
    plt.show()

    #plotted next signal timers
    lone=[]
    lone.append('r')
    lone.append('g')
    for i in range(nlanes -2):
        lone.append('r')   
    count = list[0]
    tlone=[]
    tlone.append(baseTimer - count)
    tlone.append(list[1])
    tlone.append(list[1])
    if nlanes == 4:
        tlone.append(list[2] + list[1])
    # print("After ", count, " seconds: ")
    plt.xlabel("Lanes")
    plt.ylabel("Light Color")
    plt.title("Traffic Signals after "+ str(time+count)+ " seconds:")
    plt.bar(lanes, tlone, color=lone)
    plt.show()

    #plotted next signal timers
    ltwo=[]
    ltwo.append('r')
    ltwo.append('r')
    ltwo.append('g')
    if nlanes == 4:
        ltwo.append('r')    
    count = list[0] + list[1]
    ttwo=[]
    ttwo.append(baseTimer - count)
    ttwo.append(baseTimer - list[1])
    ttwo.append(list[2])
    if nlanes == 4:
        ttwo.append(list[2])
    # print("After ", count, " seconds: ")
    plt.xlabel("Lanes")
    plt.ylabel("Light Color")
    plt.title("Traffic Signals after "+ str(time+count)+ " seconds:")
    plt.bar(lanes, ttwo, color=ltwo)
    plt.show()

    #plotted next signal timers
    if nlanes == 4:
        lth=[]
        lth.append('r')
        lth.append('r')
        lth.append('r')
        lth.append('g')
        count = list[0] + list[1] + list[2]
        tth=[]
        tth.append(baseTimer - count)
        tth.append(baseTimer - list[1] - list[2])
        tth.append(baseTimer - list[2])
        tth.append(list[3])
        # print("After ", count, " seconds: ")
        plt.xlabel("Lanes")
        plt.ylabel("Light Color")
        plt.title("Traffic Signals after "+ str(time+count)+ " seconds:")
        plt.bar(lanes, tth, color=lth)
        plt.show()


# class traffic_light(enum.Enum):
#     red = 1
#     orange = 2
#     green = 3

def initialize_camera(cap):
    _, frame = cap.read()
    return frame 

lanes = ["lane videos/lane_1.mp4", "lane videos/lane_2.mp4", "lane videos/lane_3.mp4"]

caps = [None]*len(lanes)
fpss = []
durations = []
masks = []
lane_names = []
for i in range(len(lanes)):
    
    caps[i] = cv.VideoCapture(lanes[i])
    name = os.path.basename(lanes[i])
    name = os.path.splitext(name)[0]
    lane_names.append(name)
    mask_image = "mask images/mask_"+name+".png"

    fps = caps[i].get(cv.CAP_PROP_FPS)
    #print("frame rate = " + str(fps))
    frame_count =   int(caps[i].get(cv.CAP_PROP_FRAME_COUNT))
    #print("frame count = " + str(frame_count))
    duration = frame_count/fps
    #print("duration = "+str(int(duration/60))+ ":"+ str(duration-int(duration/60)*60))
    
    fpss.append(fps)
    durations.append(duration)

    if not os.path.exists(mask_image):
        image = initialize_camera(caps[i])
        mask = roi.specify_roi(image, "mask images/"+"mask_"+name)
        masks.append(mask)
        cv.imshow(mask_image,mask)
        cv.waitKey()
    else:
        mask = cv.imread(mask_image)
        masks.append(mask)
        cv.imshow(mask_image,mask)
        cv.waitKey()

cv.destroyAllWindows()

print(durations)
t = 0
pool = multiprocessing.Pool(processes=len(lanes))

while (all(x > t for x in durations)):
    inputs = []
    start = time.time()
    for i in range(len(lanes)):
        frame_no = t * fpss[i]
        caps[i].set(cv.CAP_PROP_POS_FRAMES,frame_no)
        ret, frame = caps[i].read()
        frame = cv.bitwise_or(frame, masks[i])
        inputs.append([frame])

    outputs = pool.starmap(gtc.get_traffic_count, inputs)
    counts, images = zip(*outputs)
    end = time.time()
    print("Time taken is", float(end-start))
    print(counts)
    a,time_slots = gts.get_traffic_slots(counts)
    print("Time Slots:" ,time_slots)
    show_bar_plots(t, a, time_slots)
#     for i in range(len(lanes)):
#         cv.imshow("output_"+str(i+1),images[i])
#         cv.waitKey()
#     cv.destroyAllWindows()
    t+=a
