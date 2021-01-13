import cv2
import numpy as np
import os

# from numpy.core.fromnumeric import take

def splitImageToEntries(imageNames, inputsDir, columnsDir):
    newEntry = False
    beforeTitle = False
    isTitle = True
    for image in imageNames:
        print('---------------------',image)
        img = cv2.imread(inputsDir + '/' + image) # Read in the image and convert to grayscale
        img = img[:-400,400:]
        h, w = img.shape[:2]
        # cv2.imshow("cropped", cv2.resize(gray, (int(img.shape[1]/5), int(img.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # convert the image to grayscale and flip the foreground
        # and background to ensure foreground is now "white" and
        # the background is "black"
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kernel = np.ones((7, 7), np.uint8)
        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

        # cv2.imshow("reduction", cv2.resize(gray, (int(gray.shape[1]/8), int(gray.shape[0]/8))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

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

        cy, cx = img.shape[:2]
        cy /= 2
        cx /= 2
        M = cv2.getRotationMatrix2D((cx,cy), angle, 1.0)
        rotated = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        kernel = np.ones((5, 5), np.uint8)
        rotated = cv2.morphologyEx(rotated, cv2.MORPH_CLOSE, kernel)

        rotated = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        rotated = cv2.bitwise_not(rotated)
        
        # Find and draw the upper and lower boundary of each lines
        hist = cv2.reduce(rotated,1,cv2.REDUCE_AVG).reshape(-1)

        # hist = cv2.reduce(rotated,1,cv2.REDUCE_MIN).reshape(-1)
        # print(hist)

        th = 3 # 10: TD001, 5: TD002, 3: TD003
        H,W = img.shape[:2]
        uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
        lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]
        # print(uppers)
        rotated = cv2.bitwise_not(rotated)
        # rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
        # for y in uppers:
        #     cv2.line(rotated, (0,y), (W, y), (255,0,0), 1)

        # for y in lowers:
        #     cv2.line(rotated, (0,y), (W, y), (0,255,0), 1)

        # cv2.imshow("drawed", cv2.resize(rotated, (int(rotated.shape[1]/10), int(rotated.shape[0]/10))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + 'test' + '.jpg', rotated)

        lineMinHeight = 30

        box = cv2.bitwise_not(rotated)
        box = cv2.morphologyEx(box, cv2.MORPH_OPEN, np.ones((10, 10), dtype=np.uint8)) 
        coords = cv2.findNonZero(box) # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords) 
        lineMinLength = w - 100 # 1350: TD001, 1800: TD002, 3700: TD005
        
        newLineMinStart = x   # 50 cho các từ điển, 600 cho TD005
        entryCount = 0
        startEntry = 0
        endEntry = 0

        firstLine = True
        cont = False
        center = False
        # print(len(uppers), len(lowers))
        for i in range(len(uppers)):
            # print(uppers[i] - lowers[i])
            if (i == len(uppers) - 1): 
                newEntry = True
                if len(uppers) > len(lowers):
                    endEntry = -1
                else:
                    endEntry = lowers[i]
            else:
                if abs(uppers[i] - lowers[i]) <=  lineMinHeight:
                    continue
                line = rotated[uppers[i]:lowers[i], :]
                line = cv2.bitwise_not(line)
                try:
                    box = cv2.morphologyEx(line, cv2.MORPH_OPEN, np.ones((10, 10), dtype=np.uint8)) # Perform noise filtering
                except Exception as _:
                    box = line
                    pass
                coords = cv2.findNonZero(box) # Find all non-zero points (text)
                x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
                # cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + str(entryCount) + '.jpg', line[y:y+h, x:x+w])
                # entryCount += 1
                # Kết thúc một mục từ:
                # print(x, w)
                # if w <= lineMinLength: # cho từ điển 001 và 002
                    # newEntry = True
                    # endEntry = lowers[i]
                # newLineMinStart = min(newLineMinStart, x)
                if x < newLineMinStart + 50 and w <= lineMinLength:
                    newEntry = True
                    endEntry = lowers[i]
                    if beforeTitle:
                        isTitle = True
                    # if x > line.shape[1]/2:
                    #     right = True
                elif x > newLineMinStart + 500:
                    center = True
                    newEntry = True
                    endEntry = lowers[i]
                    # if x > line.shape[1]/2:
                    #     right = True
                
                if firstLine and x < newLineMinStart + 50:
                    cont = True
                firstLine = False

            beforeTitle = False
            if newEntry:
                name = columnsDir + '/' + image[0:-4] + '-' + str(entryCount)
                if isTitle:
                    name += '-title'
                elif cont:
                    name += '-continue'
                elif center:
                    name += '-center'
                name += '.jpg'

                cv2.imwrite(name, rotated[startEntry:endEntry+5, :])
                entryCount += 1
                # if not i + 1 == len(uppers):
                #     startEntry = uppers[i + 1]
                if not i == len(uppers) - 1:
                    startEntry = lowers[i]
                newEntry = False
                beforeTitle = True
                isTitle = False
                center = False
                cont = False


if __name__ == "__main__":
    inputDir = 'images/005'
    imageName = list(filter(lambda file: file[-3:] == 'png', os.listdir(inputDir)))
    columnDir = 'splitEntry/005'

    splitImageToEntries(imageName, inputDir, columnDir)
    # splitImageToEntries(['Ke_chuyen_thanh_ngu_tuc_ngu_1997_056.png'], inputDir, columnDir)