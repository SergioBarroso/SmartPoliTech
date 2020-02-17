import PIL
import torch
import numpy as np

import cv2  # pylint: disable=import-error
from openpifpaf.network import nets
from openpifpaf import decoder, show, transforms
import openpifpaf

# cap = cv2.VideoCapture('http://admin:xtrem$@10.253.246.38/snapshot.cgi')
# http://158.49.247.18/zm/cgi-bin/nph-zms?mode=jpeg&monitor=7&user=guest&pass=smpt00
# cap = cv2.VideoCapture('http://158.49.247.18/zm/cgi-bin/nph-zms?mode=jpeg&monitor=7&user=guest&pass=smpt00')
cap = cv2.VideoCapture(
    'http://10.253.247.34:88/cgi-bin/CGIStream.cgi?cmd=GetMJStream&usr=guest&pwd=smpt00')

"""
http://10.253.247.34:88/cgi-bin/CGIStream.cgi?cmd=GetMJStream&usr=guest&pwd=smpt00

http://10.253.247.35:88/cgi-bin/CGIStream.cgi?cmd=GetMJStream&usr=guest&pwd=smpt00

http://user:cotilla$@10.253.247.22:5900/mjpg/video.mjpg

"""


# net, _ = openpifpaf.network.factory(checkpoint='resnet101')
net, _ = openpifpaf.network.factory()
decode = decoder.factory_decode(net, seed_threshold=0.5)
processor = decoder.Processor(net, decode,
                              instance_threshold=0.2,
                              keypoint_threshold=0.3)

device = torch.device('cpu')

# if torch.cuda.is_available():
#    device = torch.device('cuda')

scale = 1.0
videoInput = False

while(cap.isOpened()):


    frame = None
    processImage = False

    if not videoInput:
        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')  # JPEG start
        b = bytes.find('\xff\xd9')  # JPEG end
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]  # actual image
            bytes = bytes[b + 2:]  # other informations

            # decode to colored image ( another option is cv2.IMREAD_GRAYSCALE )
            if len(jpg) == 0:
                continue

            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            processImage = True

    else:
        frame = cap.read()


        processImage = True

    if processImage:

        if frame is None:
            continue

        ret, frame = cap.read()

        image = cv2.resize(frame, None, fx=scale, fy=scale)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = PIL.Image.fromarray(image)
        processed_image_cpu, _, __ = transforms.EVAL_TRANSFORM(
            image_pil, [], None)
        processed_image = processed_image_cpu.contiguous().to(
            device, non_blocking=True)
        fields = processor.fields(torch.unsqueeze(processed_image, 0))[0]

        annotations = processor.annotations(fields)
        skeleton_painter = openpifpaf.show.KeypointPainter(
            show_box=False, color_connections=True, markersize=1, linewidth=6)
        im = np.asarray(image_pil)
        # viz.annotations(ax, annotations = annotations)
        # print(list(map(lambda x: x.data, annotations)))
        # list(map(lambda x: x.skeleton, annotations)) ,
        #if len(annotations) > 0:
        print('Personas detectadas', len(annotations), list(
            map(lambda x: len([i for i in x.data if np.any(i)]), annotations)))

        with openpifpaf.show.canvas() as ax:
            ax.imshow(im)
            skeleton_painter.annotations(ax, annotations)


cap.release()
cv2.destroyAllWindows()
