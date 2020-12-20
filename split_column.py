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

        bordersize = 10
        rect = cv2.copyMakeBorder(
            rect,
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )

        # convert the image to grayscale and flip the foreground
        # and background to ensure foreground is now "white" and
        # the background is "black"
        gray = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        # threshold the image, setting all foreground pixels to
        # 255 and all background pixels to 0
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # grab the (x, y) coordinates of all pixel values that
        # are greater than zero, then use these coordinates to
        # compute a rotated bounding box that contains all
        # coordinates
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]
        # the `cv2.minAreaRect` function returns values in the
        # range [-90, 0); as the rectangle rotates clockwise the
        # returned angle trends to 0 -- in this special case we
        # need to add 90 degrees to the angle
        if angle < -45:
            angle = -(90 + angle)
        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = -angle

        cy, cx = rect.shape[:2]
        cy /= 2
        cx /= 2
        M = cv2.getRotationMatrix2D((cx,cy), angle, 1.0)
        rect = cv2.warpAffine(rect, M, (rect.shape[1], rect.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        # if cropRight != 0:
        #     rect = rect[:, :-cropRight]

        # cv2.imshow("rotated", cv2.resize(rect, (int(rect.shape[1]/5), int(rect.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        gray = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY)
        # Create some large dark area with the text, 10 is quite big!
        eroded = skimage.morphology.erosion(gray, skimage.morphology.square(5))

        # Compute mean values along axis 0 or 1
        hist = np.mean(eroded, axis=0)

        # Search large (here 2% of dimension size) and distant (here 15% of dimension size) peaks
        peaks, _ = sp.signal.find_peaks(hist, width=len(hist)*2//100, distance=len(hist)*15//100)
        # print(peaks)
        try:
            center = min(peaks, key=lambda x : abs(x - 1900))
        except Exception as e:
            center = int(rect.shape[1]/2)
            print("Error, please check your image named", image)
        print(peaks, center)
        colLeftImg = rect[:, 0:center]
        colRightImg = rect[:, center:]
        cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + '0' + '.jpg', colLeftImg)
        cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + '1' + '.jpg', colRightImg)

if __name__ == "__main__":
    inputDir = 'images/003'
    imageName = list(filter(lambda file: file[-3:] == 'png', os.listdir(inputDir)))
    columnDir = 'splitColumn/003'

    splitImageToColumns(imageName, inputDir, columnDir)
    # splitImageToColumns(['Tu dien tieng viet Ng Kim Than p1 (1)_019.jpg'], inputDir, columnDir)