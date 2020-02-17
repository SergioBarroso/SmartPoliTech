
# For running inference on the TF-Hub module.
import cv2 as cv
import numpy as np
import PIL
import torch

from openpifpaf.network import nets
from openpifpaf import decoder, show, transforms
import openpifpaf
#

backSub =  cv.createBackgroundSubtractorKNN(detectShadows=False) #cv.createBackgroundSubtractorMOG2(detectShadows=False)
#"videos/arriba.mp4"
capture = cv.VideoCapture("norba2.avi")
net, _ = openpifpaf.network.factory()
decode = decoder.factory_decode(net, seed_threshold=0.5)
processor = decoder.Processor(net, decode, 
                              instance_threshold=0.2,
                              keypoint_threshold=0.3)
device = torch.device('cpu')

#if torch.cuda.is_available():
#    device = torch.device('cuda')


while True:
    ret, frame = capture.read()
    if frame is None:
        break
    #frame = cv.resize(frame, (420,360))
    
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)    
    fgMask = backSub.apply(frame)

    kernel = np.ones((5,5),np.uint8)
    morph = cv.morphologyEx(fgMask,cv.MORPH_CLOSE,kernel, iterations = 3)
    # sure background area
    morph = cv.dilate(morph,kernel,iterations=3)
    morph = cv.morphologyEx(morph,cv.MORPH_OPEN,kernel, iterations = 3)

    morph = cv.cvtColor( morph,cv.COLOR_GRAY2BGR)
    
    f = cv.min(morph,frame)
    #cv.imshow("img", f)
    
    image_pil = PIL.Image.fromarray(f)

    processed_image_cpu, _, __ = transforms.EVAL_TRANSFORM(image_pil, [], None)
    processed_image = processed_image_cpu.contiguous().to(
        device, non_blocking=True)
    fields = processor.fields(torch.unsqueeze(processed_image, 0))[0]

    annotations = processor.annotations(fields)
    skeleton_painter = openpifpaf.show.KeypointPainter(
        show_box=False, color_connections=True, markersize=1, linewidth=6)
    im = np.asarray(image_pil)        
    #viz.annotations(ax, annotations = annotations)
    #print(list(map(lambda x: x.data, annotations)))
    #list(map(lambda x: x.skeleton, annotations)) ,
    if len(annotations) > 0:
        print('Personas detectadas', len(annotations), list(map(lambda x: len([i for i in x.data if  np.any(i)]), annotations)))

    #with openpifpaf.show.canvas() as ax:
    #    ax.imshow(im)
    #    skeleton_painter.annotations(ax, annotations)
        
    """
        
        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', morph)
        cv.imshow('diff', f)

        keyboard = cv.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break
    """
    