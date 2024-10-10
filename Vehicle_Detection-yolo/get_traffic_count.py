import cv2 as cv
import numpy as np

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Draw the predicted bounding box
def drawPred(image, classId, conf, left, top, right, bottom):
    
    # Get the label for the class name and its confidence for vehicles only
    if classes:
        
        if (classId==1  or classId==2 or classId==3 or classId==5 or classId==7):

            # Draw a bounding box.
            cv.rectangle(image, (left, top), (right, bottom), (0, 0, 255))
            # label = '%.2f' % conf
            label = '%s' % (classes[classId])

            # Display the label at the top of the bounding box
            labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            top = max(top, labelSize[1])
            cv.putText(image, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(image, outs):
    count=0
    imageHeight = image.shape[0]
    imageWidth = image.shape[1]
    
    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * imageWidth)
                center_y = int(detection[1] * imageHeight)
                width = int(detection[2] * imageWidth)
                height = int(detection[3] * imageHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(image, classIds[i], confidences[i], left, top, left + width, top + height)
        if classIds[i] in [1, 2, 3, 5, 7]:  # 0
            count = count + 1
    
    return count

# Load names of classes
classesFile = "inputs/coco.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "inputs/yolov3.cfg"
modelWeights = "inputs/yolov3.weights"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
inpWidth = 416  # Width of network's input image
inpHeight = 416  # Height of network's input image

def get_traffic_count(image):

    # Create a 4D blob from a frame
    blob = cv.dnn.blobFromImage(image, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

    # Set the input to the net
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    count = postprocess(image, outs)
    
    # print("The number of vehicles on road are: " + str(cnt))
    # cv.imshow("output",image)
    # cv.waitKey()
    return count, image