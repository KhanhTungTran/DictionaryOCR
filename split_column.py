import numpy as np
import cv2
import os
import skimage.morphology
import scipy as sp

def splitImageToColumns(imageNames, inputsDir, columnsDir):
    for image in imageNames:
        print('---------------------',image)
        img = cv2.imread(inputsDir + '/' + image) # Read in the image and convert to grayscale

        img = img[...,::-1]
        h, w = img.shape[:2]
        # cv2.imshow("cropped", cv2.resize(img, (int(img.shape[1]/5), int(img.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        # cv2.imshow("gray", cv2.resize(gray, (int(gray.shape[1]/5), int(gray.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, np.ones((10, 10), dtype=np.uint8)) # Perform noise filtering
        # cv2.imshow("filtered", cv2.resize(gray, (int(gray.shape[1]/5), int(gray.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        coords = cv2.findNonZero(gray) # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box

        rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
        # rect = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("cropped", cv2.resize(rect, (int(rect.shape[1]/5), int(rect.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        orig = rect
        bordersize = 10
        rect = cv2.copyMakeBorder(
            rect,
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 0]
        )

        
        gray = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY)
        # threshold:
        th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
        
        # minAreaRect on the nozeros:
        pts = cv2.findNonZero(threshed)
        ret = cv2.minAreaRect(pts)

        (cx,cy), (w,h), ang = ret
        if w>h:
            w,h = h,w
            ang += 90


        # Find rotated matrix, do rotation:
        if ang > 90 or ang < -90:
            M = cv2.getRotationMatrix2D((cx,cy), 180 - ang, 1)
        else:
            M = cv2.getRotationMatrix2D((cx,cy), ang, 1)

        rect = cv2.warpAffine(orig, M, (rect.shape[1], rect.shape[0]))
        # if cropRight != 0:
        #     rect = rect[:, :-cropRight]

        # cv2.imshow("rotated", cv2.resize(rect, (int(rect.shape[1]/5), int(rect.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        rect = rect[:, :-11]

        gray = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY)
        # Create some large dark area with the text, 10 is quite big!
        eroded = skimage.morphology.erosion(gray, skimage.morphology.square(5))

        # Compute mean values along axis 0 or 1
        hist = np.mean(eroded, axis=0)

        # Search large (here 2% of dimension size) and distant (here 15% of dimension size) peaks
        peaks, _ = sp.signal.find_peaks(hist, width=len(hist)*2//100, distance=len(hist)*15//100)
        # print(peaks)
        try:
            center = min(peaks, key=lambda x : abs(x - 2300))
            right = min(peaks, key=lambda x : abs(x - 4000))
        except Exception as e:
            center = int(rect.shape[1]/2)
            right = -11
            print("Error, please check your image named", image)
        print(peaks, center)
        colLeftImg = rect[:, 0:center]
        if abs(right - 4000) > 1000:
            right = -11
        colRightImg = rect[:, center:right]
        cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + '0' + '.png', colLeftImg)
        cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + '1' + '.png', colRightImg)

if __name__ == "__main__":
    inputDir = 'images/033'
    imageName = list(filter(lambda file: file[-3:] == 'png', os.listdir(inputDir)))
    columnDir = 'splitColumn/033'

    splitImageToColumns(imageName, inputDir, columnDir)
    # splitImageToColumns(['Tu dien tieng viet Ng Kim Than p1 (1)_019.jpg'], inputDir, columnDir)