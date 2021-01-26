import cv2
import numpy as np
import os

from numpy.core.fromnumeric import take

def splitImageToEntries(imageNames, inputsDir, columnsDir):
    for image in imageNames:
        isRightColumn = False
        flip = -1
        entryCount = 0
        if image[-5] == '1':
            isRightColumn = True
            flip = 1
            entryCount = 100
        
        print('---------------------',image)
        img = cv2.imread(inputsDir + '/' + image) # Read in the image and convert to grayscale
        H, W = img.shape[:2]
        # cv2.imshow("cropped", cv2.resize(img, (int(img.shape[1]/5), int(img.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if isRightColumn:
            gray = cv2.cvtColor(img[:-100, :-200], cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(img[:-100, :], cv2.COLOR_BGR2GRAY)
        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, np.ones((15, 15), dtype=np.uint8)) # Perform noise filtering
        # cv2.imshow("filtered", cv2.resize(gray, (int(gray.shape[1]/7), int(gray.shape[0]/7))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        gray = cv2.bitwise_not(gray)
        coords = cv2.findNonZero(gray) # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
        if W > 2000 and isRightColumn:
            img = img[:, :-200]
            rect = img[:, x - 20 if x - 20 > 0 else x:x+w+50] # Crop the image - note we do this on the original image
        else:
            rect = img[:, x - 20 if x - 20 > 0 else x:]
        img = rect

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = img
        # cv2.imshow("gray", cv2.resize(img, (int(gray.shape[1]/7), int(gray.shape[0]/7))))z
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

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
        
        if isRightColumn and -90 < ang < 90:
            M = cv2.getRotationMatrix2D((cx,cy), 180 - ang, 1)
        elif not isRightColumn and (ang > 90 or ang < -90):
            M = cv2.getRotationMatrix2D((cx,cy), 180 - ang, 1)
        else:
            M = cv2.getRotationMatrix2D((cx,cy), ang, 1)
        rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))
        # Find and draw the upper and lower boundary of each lines
        hist = cv2.reduce(rotated,1,cv2.REDUCE_AVG).reshape(-1)

        # cv2.imshow("rotated", cv2.resize(rotated, (int(rotated.shape[1]/5), int(rotated.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(flip, ang)
        th = 3 # 10: TD001, 5: TD002, 3: TD003
        H,W = rotated.shape[:2]
        uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
        lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]
        if lowers[0] < uppers[0]:
            lowers = lowers[1:]

        rotated = cv2.bitwise_not(rotated)
        # rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
        # for y in uppers:
        #     cv2.line(rotated, (0,y), (W, y), (255,0,0), 1)

        # for y in lowers:
        #     cv2.line(rotated, (0,y), (W, y), (0,255,0), 1)

        # cv2.imshow("drawed", cv2.resize(rotated, (int(rotated.shape[1]/5), int(rotated.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + 'test' + '.jpg', rotated)

        lineMinHeight = 50
        # lineMinLength = 1600 # 1350: TD001, 1800: TD002
        newLineMaxStart = 30
        lastLineMaxLength = 50
        startEntry = 0
        endEntry = 0
        newEntry = False
        # print(len(uppers), len(lowers))
        # cv2.imshow("drawed", cv2.resize(rotated, (int(rotated.shape[1]/7), int(rotated.shape[0]/7))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        for i in range(len(uppers)):
            # print(uppers[i] - lowers[i])
            if (i == len(uppers) - 1): 
                newEntry = True
                if len(uppers) > len(lowers):
                    endEntry = rotated.shape[0] - 1
                else:
                    endEntry = lowers[i]
            else:
                if abs(uppers[i] - lowers[i]) <= lineMinHeight:
                    continue
                line = rotated[uppers[i]:lowers[i], :]
                line = cv2.bitwise_not(line)
                try:
                    line = cv2.morphologyEx(line, cv2.MORPH_OPEN, np.ones((5, 5), dtype=np.uint8)) # Perform noise filtering
                except Exception as _:
                    pass
                coords = cv2.findNonZero(line) # Find all non-zero points (text)
                x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
                # Kết thúc một mục từ:
                # print(x, w)
                # if w <= lineMinLength: # cho từ điển 001 và 002
                    # newEntry = True
                    # endEntry = lowers[i]
                if (x < newLineMaxStart and not isRightColumn) or (x > lastLineMaxLength and isRightColumn):
                    newEntry = True
                    endEntry = uppers[i]
            if newEntry:
                if endEntry == 0:
                    pass
                elif isRightColumn:
                    entry = cv2.rotate(rotated[startEntry-30 if startEntry-30 > 0 else startEntry:endEntry, :], cv2.ROTATE_180)
                    cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + str(entryCount) + '.jpg', entry)
                    entryCount -= 1
                else:
                    entry = rotated[startEntry-30 if startEntry-30 > 0 else startEntry:endEntry, :]
                    cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + str(entryCount) + '.jpg', entry)
                    entryCount += 1
                # if not i + 1 == len(uppers):
                #     startEntry = uppers[i + 1]
                startEntry = uppers[i]
                newEntry = False
        


if __name__ == "__main__":
    inputDir = 'splitColumn/003'
    imageName = list(filter(lambda file: file[-3:] == 'jpg', os.listdir(inputDir)))
    columnDir = 'splitEntry/003'

    splitImageToEntries(imageName[1729:], inputDir, columnDir)
    # splitImageToEntries(['0030867-1.jpg'], inputDir, columnDir)