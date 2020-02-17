from torchvision import models
import PIL 
import matplotlib.pyplot as plt
import torch
import numpy as np
import cv2 as cv

# Apply the transformations needed
import torchvision.transforms as T

# Define the helper function
def decode_segmap(image, source, nc=21):
  
  label_colors = np.array([(0, 0, 0),  # 0=background
               # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
               (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
               # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
               (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
               # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
               (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
               # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
               (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])

  r = np.zeros_like(image).astype(np.uint8)
  g = np.zeros_like(image).astype(np.uint8)
  b = np.zeros_like(image).astype(np.uint8)
   

  for l in range(0, nc):
    idx = image == l
    r[idx] = label_colors[l, 0]
    g[idx] = label_colors[l, 1]
    b[idx] = label_colors[l, 2]
  
  rgb = np.stack([r, g, b], axis=2)

  foreground = source
  # Change the color of foreground image to RGB 
  # and resize image to match shape of R-band in RGB output map
  #foreground = cv.cvtColor(foreground, cv.COLOR_BGR2RGB)
  foreground = cv.resize(foreground,(r.shape[1],r.shape[0]))

  # Create a background array to hold white pixels
  # with the same size as RGB output map
  background = 255 * np.ones_like(rgb).astype(np.uint8)

  # Convert uint8 to float
  foreground = foreground.astype(float)
  background = background.astype(float)

  # Create a binary mask of the RGB output map using the threshold value 0
  th, alpha = cv.threshold(np.array(rgb),0,255, cv.THRESH_BINARY)

  # Apply a slight blur to the mask to soften edges
  alpha = cv.GaussianBlur(alpha, (7,7),0)

  # Normalize the alpha mask to keep intensity between 0 and 1
  alpha = alpha.astype(float)/255

  # Multiply the foreground with the alpha matte
  foreground = cv.multiply(alpha, foreground)  
  
  # Multiply the background with ( 1 - alpha )
  background = cv.multiply(1.0 - alpha, background)  
  
  # Add the masked foreground and background
  outImage = cv.add(foreground, background)

  # Return a normalized output image for display
  return outImage/255

def segment(net, frame, show_orig=True, dev='cpu'):
  img =  PIL.Image.fromarray(frame)
  #if show_orig: plt.imshow(img); plt.axis('off'); plt.show()
  # Comment the Resize and CenterCrop for better inference results
  trf = T.Compose([T.Resize(450), 
                   #T.CenterCrop(224), 
                   T.ToTensor(), 
                   T.Normalize(mean = [0.485, 0.456, 0.406], 
                               std = [0.229, 0.224, 0.225])])
  inp = trf(img).unsqueeze(0).to(dev)
  out = net.to(dev)(inp)['out']
  om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
  f = frame
  rgb = decode_segmap(om, f)
    
  return rgb
  
dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()

backSub =  cv.createBackgroundSubtractorMOG2(detectShadows=False)


#"videos/arriba.mp4"
capture = cv.VideoCapture("norba2.avi")

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    frame = cv.resize(frame, (420,360))

    """
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)    
    fgMask = backSub.apply(frame)

    kernel = np.ones((5,5),np.uint8)
    morph = cv.morphologyEx(fgMask,cv.MORPH_CLOSE,kernel, iterations = 3)
    # sure background area
    morph = cv.dilate(morph,kernel,iterations=3)
    morph = cv.morphologyEx(morph,cv.MORPH_OPEN,kernel, iterations = 3)

    morph = cv.cvtColor( morph,cv.COLOR_GRAY2BGR)
    f = cv.min(morph,frame)
    """
    rgb = segment(dlab, frame, show_orig=False)
    cv.imshow('f', rgb)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break