import numpy as np
import cv2

def splitImageToColumns(imageNames, inputsDir, columnsDir):
    for image in imageNames:
        print('---------------------',image)
        img = cv2.imread(inputsDir + '/' + image) # Read in the image and convert to grayscale

        h, w = img.shape[:2]
        img = img[:h, 10:w-10] # Crop by hand
        # cv2.imshow("cropped", cv2.resize(img, (int(img.shape[1]/5), int(img.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
        # cv2.imshow("gray", cv2.resize(gray, (int(gray.shape[1]/5), int(gray.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, np.ones((10, 10), dtype=np.uint8)) # Perform noise filtering
        # cv2.imshow("filtered", cv2.resize(gray, (int(gray.shape[1]/5), int(gray.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        coords = cv2.findNonZero(gray) # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box

        cropRight = 0
        if (x + w - img.shape[1]) <= 100 and (x + w - img.shape[1]) >= 0:
            # print('stupid')
            cropRight = 200
        rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
        # cv2.imshow("cropped", cv2.resize(rect, (int(rect.shape[1]/5), int(rect.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite("cropped.jpg", rect)

        # Apply edge detection method on the image 
        edges = cv2.Canny(rect,60,180,apertureSize = 3)

        # This returns an array of r and theta values 
        NUM_POINTS = 200
        lines = cv2.HoughLines(edges,1,np.pi/180, NUM_POINTS)
        try:
            s = lines.shape
        except Exception as e:
            NUM_POINTS = 100
        # if lines == None:ik
        #     NUM_POINTS = 100
        lines = cv2.HoughLines(edges,1,np.pi/180, NUM_POINTS) 

        rect = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY)

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

        angle = 0
        lines = lines.reshape((lines.shape[0], -1))
        for _, theta in lines:
            if abs(theta) >= 70*np.pi/180 and abs(theta) <= 110*np.pi/180:
                if theta < 0:
                    theta = theta*180/np.pi +  90
                else:
                    theta = theta*180/np.pi - 90
                angle = theta
                break

        cy, cx = rect.shape[:2]
        cy /= 2
        cx /= 2
        M = cv2.getRotationMatrix2D((cx,cy), angle, 1.0)
        rect = cv2.warpAffine(rect, M, (rect.shape[1], rect.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        if cropRight != 0:
            rect = rect[:, :-cropRight]

        # cv2.imshow("rotated", cv2.resize(rect, (int(rect.shape[1]/5), int(rect.shape[0]/5))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + '1' + '.jpg', rect[:, :rect.shape[1]//2 - 5])
        cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + '2' + '.jpg', rect[:, rect.shape[1]//2 + 5:])
        # # Apply edge detection method on the image 
        # edges = cv2.Canny(rect,60,180,apertureSize = 3)
        # # This returns an array of r and theta values 
        # lines = cv2.HoughLines(edges,1,np.pi/180, NUM_POINTS) 

        # lines = lines.reshape((lines.shape[0],-1))
        # # The below for loop runs till r and theta values  
        # # are in the range of the 2d array 
        # for r,theta in lines: 
        #     if abs(theta) <= 2*np.pi/180:
        #         # Stores the value of cos(theta) in a 
        #         a = np.cos(theta) 
            
        #         # Stores the value of sin(theta) in b 
        #         b = np.sin(theta) 
                
        #         # x0 stores the value rcos(theta) 
        #         x0 = a*r 
                
        #         # y0 stores the value rsin(theta) 
        #         y0 = b*r 
                
        #         # x1 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
        #         x1 = int(x0 + 1000*(-b)) 
                
        #         # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
        #         y1 = int(y0 + 1000*(a)) 
            
        #         # x2 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
        #         x2 = int(x0 - 1000*(-b)) 
                
        #         # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
        #         y2 = int(y0 - 1000*(a)) 
        #         if abs((x1 + x2)/2 - rect.shape[1]/2) >= rect.shape[1]/20:
        #             continue
        #         # cv2.line draws a line in img from the point(x1,y1) to (x2,y2). 
        #         # (0,0,255) denotes the colour of the line to be  
        #         #drawn. In this case, it is red.
        #         cv2.line(rect,(x1,y1), (x2,y2), (0,0,255),2) 
        #         cv2.imshow("lined", cv2.resize(rect, (int(rect.shape[1]/5), int(rect.shape[0]/5))))
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()
        #         colLeftImg = rect[:, 0:min(x1, x2) - 5]
        #         colRightImg = rect[:, max(x1, x2) + 5:]
        #         # cv2.imshow("left", colLeftImg)
        #         # cv2.waitKey(0)
        #         # cv2.destroyAllWindows()
                
        #         # # colLeftGray = cv2.cvtColor(colLeftImg, cv2.COLOR_BGR2GRAY)
        #         # colLeftInverted = 255*(colLeftImg < 128).astype(np.uint8)
                
        #         # colLeftImg = cv2.morphologyEx(colLeftInverted, cv2.MORPH_CLOSE, np.ones((2, 2), dtype=np.uint8))
        #         # colLeftImg = 255*(colLeftImg < 128).astype(np.uint8)
        #         # cv2.imshow("left", colLeftImg)
        #         # cv2.waitKey(0)
        #         # cv2.destroyAllWindows()

        #         # # colRightGray = cv2.cvtColor(colRightImg, cv2.COLOR_BGR2GRAY)
        #         # colRightInverted = 255*(colRightImg < 128).astype(np.uint8)
                
        #         # colRightImg = cv2.morphologyEx(colRightInverted, cv2.MORPH_CLOSE, np.ones((2, 2), dtype=np.uint8))
        #         # colRightImg = 255*(colRightImg >= 128).astype(np.uint8)

        #         cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + '1' + '.jpg', colLeftImg)
        #         cv2.imwrite(columnsDir + '/' + image[0:-4] + '-' + '2' + '.jpg', colRightImg)
        #         break


if __name__ == "__main__":
    splitImageToColumns( ['image.jpg'], 'inputs', 'splitColumn')