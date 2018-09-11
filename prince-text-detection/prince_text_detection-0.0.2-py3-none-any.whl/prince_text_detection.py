from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
import tkinter
from tkinter import *
from tkinter import messagebox
import glob

width = 320
height = 320
root = tkinter.Tk()
root.withdraw()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
	help="path to input image")
ap.add_argument("-east", "--east", type=str,
	help="path to input EAST text detector")
ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
	help="minimum probability required to inspect a region")
ap.add_argument("-w", "--width", type=int, default=320,
	help="resized image width (should be multiple of 32)")
ap.add_argument("-e", "--height", type=int, default=320,
	help="resized image height (should be multiple of 32)")
args = vars(ap.parse_args())

class TextImages:
    def __init__(self):
        pass
    
    @staticmethod
    def SingleImageTest(image, path_of_memory_file):
        """This Method is for using Single Images"""
        image = cv2.imread(image)
        orig = image.copy()
        (H, W) = image.shape[:2]

        (newW, newH) = width, height
        rW = W / float(newW)
        rH = H / float(newH)

        image = cv2.resize(image, (newW, newH))
        (H, W) = image.shape[:2]


        layerNames = [
                "feature_fusion/Conv_7/Sigmoid",
                "feature_fusion/concat_3"]

        print("[INFO] loading Prince text detector...")
        net = cv2.dnn.readNet(path_of_memory_file)

        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                (123.68, 116.78, 103.94), swapRB=True, crop=False)
        start = time.time()
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)
        end = time.time()
        major = end-start
        

        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []


        for y in range(0, numRows):
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

	# loop over the number of columns
            for x in range(0, numCols):
		# if our score does not have sufficient probability, ignore it
                if scoresData[x] < args["min_confidence"]:
                    continue

		# compute the offset factor as our resulting feature maps will
		# be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

		# extract the rotation angle for the prediction and then
		# compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

		# use the geometry volume to derive the width and height of
		# the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

		# compute both the starting and ending (x, y)-coordinates for
		# the text prediction bounding box
                offsetX = offsetX + cos * xData1[x] + sin * xData2[x] 
                offsetY = offsetY - sin * xData1[x] + cos * xData2[x]                
        
# calculate the UL and LR corners of the bounding rectangle
                p1x = -cos * w + offsetX
                p1y = -cos * h + offsetY
                p3x = -sin * h + offsetX
                p3y = sin * w + offsetY
                           
# add the bounding box coordinates
                rects.append((p1x, p1y, p3x, p3y))
                confidences.append(scoresData[x])
        #print(confidences)
        if len(confidences)==0:
            messagebox.showinfo("Info",f"probability of text on this image is 0 percent")
        else:
            print(confidences[-1])
            messagebox.showinfo("Info",f"probability of text on this image is {confidences[-1]} percent")

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
        boxes = non_max_suppression(np.array(rects), probs=confidences)

# loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
	# scale the bounding box coordinates based on the respective
	# ratios
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)

	# draw the bounding box on the image
            cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

# show the output image
        cv2.imshow("Text Detection", orig)
        cv2.waitKey(0)
        cv.destroyallwindows()

    @staticmethod
    def MultipleImageTest(image_path, path_of_memory_file):
        database = glob.glob(image_path)
        for images in database:
            image = cv2.imread(images)
            orig = image.copy()
            (H, W) = image.shape[:2]

            (newW, newH) = width, height
            rW = W / float(newW)
            rH = H / float(newH)

            image = cv2.resize(image, (newW, newH))
            (H, W) = image.shape[:2]


            layerNames = [
                    "feature_fusion/Conv_7/Sigmoid",
                    "feature_fusion/concat_3"]

            print("[INFO] loading Prince text detector...")
            net = cv2.dnn.readNet(path_of_memory_file)

            blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                    (123.68, 116.78, 103.94), swapRB=True, crop=False)
            start = time.time()
            net.setInput(blob)
            (scores, geometry) = net.forward(layerNames)
            end = time.time()
            major = end-start
        

            (numRows, numCols) = scores.shape[2:4]
            rects = []
            confidences = []


            for y in range(0, numRows):
                scoresData = scores[0, 0, y]
                xData0 = geometry[0, 0, y]
                xData1 = geometry[0, 1, y]
                xData2 = geometry[0, 2, y]
                xData3 = geometry[0, 3, y]
                anglesData = geometry[0, 4, y]

	# loop over the number of columns
                for x in range(0, numCols):
                    # if our score does not have sufficient probability, ignore it
                    if scoresData[x] < args["min_confidence"]:
                        continue

		# compute the offset factor as our resulting feature maps will
		# be 4x smaller than the input image
                    (offsetX, offsetY) = (x * 4.0, y * 4.0)

		# extract the rotation angle for the prediction and then
		# compute the sin and cosine
                    angle = anglesData[x]
                    cos = np.cos(angle)
                    sin = np.sin(angle)

		# use the geometry volume to derive the width and height of
		# the bounding box
                    h = xData0[x] + xData2[x]
                    w = xData1[x] + xData3[x]

		# compute both the starting and ending (x, y)-coordinates for
		# the text prediction bounding box
                    offsetX = offsetX + cos * xData1[x] + sin * xData2[x] 
                    offsetY = offsetY - sin * xData1[x] + cos * xData2[x]                
        
# calculate the UL and LR corners of the bounding rectangle
                    p1x = -cos * w + offsetX
                    p1y = -cos * h + offsetY
                    p3x = -sin * h + offsetX
                    p3y = sin * w + offsetY
                           
# add the bounding box coordinates
                    rects.append((p1x, p1y, p3x, p3y))
                    confidences.append(scoresData[x])
        #print(confidences)
            if len(confidences)==0:
                messagebox.showinfo("Info",f"probability of text on this image is 0 percent")
            else:
                print(confidences[-1])
                messagebox.showinfo("Info",f"probability of text on this image is {confidences[-1]} percent")

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
            boxes = non_max_suppression(np.array(rects), probs=confidences)

# loop over the bounding boxes
            for (startX, startY, endX, endY) in boxes:
	# scale the bounding box coordinates based on the respective
	# ratios
                startX = int(startX * rW)
                startY = int(startY * rH)
                endX = int(endX * rW)
                endY = int(endY * rH)

	# draw the bounding box on the image
                cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

# show the output image
            cv2.imshow("Text Detection", orig)
            cv2.waitKey(0)
            cv.destroyallwindows()
