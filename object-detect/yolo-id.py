import cv2
import argparse
import numpy as np
import os
import time

# Parsing The Arguments For Input, Output, Weight, Class & Config with argparse :
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--inputdir', default="img",
                help = 'path to input images folder')
ap.add_argument('-o', '--imdir', default="opimg",
                help = 'path to save images to folder')
ap.add_argument('-cl', '--cls', default=".\yolo\yolov3.txt",
                help = 'define classes')
ap.add_argument('-cfg', '--config', default=".\yolo\yolov3.cfg",
                help = 'define config')
ap.add_argument('-w', '--weight', default=".\yolo\yolov3.weights",
                help = 'define weight')
args = ap.parse_args()

#Check If Output Directory Exists if Not Create One :
if not os.path.isdir(args.imdir):
        os.mkdir(args.imdir)

print("\n [..Loading images to process with Yolo..] ")
# Loading Classes From Given Class File
classes = None
with open(args.cls, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# For Getting The Output Layers From The Image :
def get_output_layers(net):    
        layer_names = net.getLayerNames()    
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

# Drawing Prediction Box To the Image With Label and Confidence :
def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(" Label : " + classes[class_id] + " | Confidence : 0." + str(int(confidence*100)) )
    print("Object Found with  {} ".format(label))
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#This is Our Main Function Which Will Detect Objects in Images :        
def img_detector(testimg,n):
    start = time.time()
    ob = 0
    # Reading Image and Getting its Properties :
    image = cv2.imread(testimg)
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    # Setting and Passing to net and getting op layer with above Function :
    net = cv2.dnn.readNet(args.weight, args.config)
    #net = cv2.dnn.readNetFromDarknet()
    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    #declaring empty array for storing output results :
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    # Setting Output to empty array with label, Confidence, Detection Co-ordinates :
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.7:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # Setting Co-ordinates for box to Draw :
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
        ob = ob + 1
    #cv2.imshow("object detection", image)
    #cv2.waitKey()
    end = time.time()
    print("{} image Processed in {:.6f} seconds. \nTotal Objects in Image :{} \n".format(n+1, end - start,ob))
    cv2.imwrite(os.path.join(args.imdir, str('test-img' + '{:04}.jpg').format(n+1)), image)

#Getting Images From Directory :
n = 0 
start = time.time()
if os.path.isdir(args.inputdir):
    for file in os.listdir(args.inputdir):
        testimg = os.path.join(args.inputdir,file)
        img_detector(testimg,n)
        n = n + 1
else :
    img_detector(args.inputdir,0)
end = time.time()
print("Total Images Processed {} . \nTotal Time taken {:.6f} seconds. ".format(n+1, end - start))
#cv2.destroyAllWindows()