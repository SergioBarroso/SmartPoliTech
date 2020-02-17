
# For running inference on the TF-Hub module.
import cv2 as cv
import tensorflow as tf
import numpy as np

# For each frame, extract the bounding box and mask for each detected object
def postprocess(boxes, masks):
    # Output size of masks is NxCxHxW where
    # N - number of detected boxes
    # C - number of classes (excluding background)
    # HxW - segmentation shape
    numClasses = masks.shape[1]
    numDetections = boxes.shape[2]
     
    frameH = frame.shape[0]
    frameW = frame.shape[1]
     
    for i in range(numDetections):
        box = boxes[0, 0, i]
        mask = masks[i]
        score = box[2]
        if score > confThreshold:
            classId = int(box[1])
             
            # Extract the bounding box
            left = int(frameW * box[3])
            top = int(frameH * box[4])
            right = int(frameW * box[5])
            bottom = int(frameH * box[6])
             
            left = max(0, min(left, frameW - 1))
            top = max(0, min(top, frameH - 1))
            right = max(0, min(right, frameW - 1))
            bottom = max(0, min(bottom, frameH - 1))
             
            # Extract the mask for the object
            classMask = mask[classId]
             
            # Draw bounding box, colorize and show the mask on the image
            drawBox(frame, classId, score, left, top, right, bottom, classMask)


# Draw the predicted bounding box, colorize and show the mask on the image
def drawBox(frame, classId, conf, left, top, right, bottom, classMask):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
     
    # Print a label of class.
    label = '%.2f' % conf
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)
     
    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)
 
    # Resize the mask, threshold, color and apply it on the image
    classMask = cv.resize(classMask, (right - left + 1, bottom - top + 1))
    mask = (classMask > maskThreshold)
    roi = frame[top:bottom+1, left:right+1][mask]
 
    color = colors[classId%len(colors)]
    # Comment the above line and uncomment the two lines below to generate different instance colors
    #colorIndex = random.randint(0, len(colors)-1)
    #color = colors[colorIndex]
 
    frame[top:bottom+1, left:right+1][mask] = ([0.3*color[0], 0.3*color[1], 0.3*color[2]] + 0.7 * roi).astype(np.uint8)
 
    # Draw the contours on the image
    mask = mask.astype(np.uint8)
    contours, hierarchy = cv.findContours(mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(frame[top:bottom+1, left:right+1], contours, -1, color, 3, cv.LINE_8, hierarchy, 100)
# Print Tensorflow version
# Initialize the parameters
confThreshold = 0.5  #Confidence threshold
maskThreshold = 0.3  # Mask threshold

dir = "/home/juancarlos/Descargas/model/mask_rcnn_inception_v2_coco_2018_01_28/saved_model/"
# Load names of classes
classesFile =  dir +"mscoco_labels.names";
classes = None
with open(classesFile, 'rt') as f:
   classes = f.read().rstrip('\n').split('\n')
 
# Load the colors
colorsFile = "colors.txt";
with open(colorsFile, 'rt') as f:
    colorsStr = f.read().rstrip('\n').split('\n')
colors = []
for i in range(len(colorsStr)):
    rgb = colorsStr[i].split(' ')
    color = np.array([float(rgb[0]), float(rgb[1]), float(rgb[2])])
    colors.append(color)
 
# Give the textGraph and weight files for the model
textGraph = dir + "mask_rcnn_inception_v2_coco_2018_01_28.pbtxt";
modelWeights = "/home/juancarlos/Descargas/model/mask_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb";
 
# Load the network
net = cv.dnn.readNetFromTensorflow(modelWeights, textGraph);
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

backSub =  cv.createBackgroundSubtractorKNN(detectShadows=False) #cv.createBackgroundSubtractorMOG2(detectShadows=False)
#"videos/arriba.mp4"
capture = cv.VideoCapture("norba2.avi")

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    """
    frame = cv.resize(frame, (420,360))

    
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)    
    fgMask = backSub.apply(frame)

    kernel = np.ones((5,5),np.uint8)
    morph = cv.morphologyEx(fgMask,cv.MORPH_CLOSE,kernel, iterations = 3)
    # sure background area
    morph = cv.dilate(morph,kernel,iterations=3)
    morph = cv.morphologyEx(morph,cv.MORPH_OPEN,kernel, iterations = 3)

    morph = cv.cvtColor( morph,cv.COLOR_GRAY2BGR)
    f = cv.min(morph,frame)

    #f = cv.cvtColor(f,cv.COLOR_GRAY2BGR)

    # Create a 4D blob from a frame.
    frame = f
    """

    blob = cv.dnn.blobFromImage(frame, swapRB=True, crop=False)
 
    # Set the input to the network
    net.setInput(blob)
    
    # Run the forward pass to get output from the output layers
    
    boxes, masks = net.forward(['detection_out_final', 'detection_masks'])
 
    # Extract the bounding box and mask for each of the detected objects
    postprocess(boxes, masks)
 
    # Put efficiency information.
    #t, _ = net.getPerfProfile()
    #label = 'Mask-RCNN : Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    #cv.putText(f, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    
    #cv.imshow('Frame', frame)
    #cv.imshow('FG Mask', morph)
    cv.imshow('diff', frame)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
