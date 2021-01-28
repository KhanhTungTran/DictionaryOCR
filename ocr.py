from functools import reduce
import pytesseract
import os
# from PIL import Image
import numpy as np
import cv2


def entryImageToText(imageNames, inputsDir, outputsDir):
    for imageName in imageNames:
        print('---------------------',imageName)
        try:
            img = cv2.imread(inputsDir + '/' + imageName)
        except Exception as _:
            continue

        # kernel = np.ones((5,5),np.float32)/25
        # # img = 255*(img < 128).astype(np.uint8)
        # kernel = np.ones((5, 5),np.float32)/25
        # img = cv2.dilate(img,kernel,iterations = 1)
        # img = cv2.filter2D(img,-1,kernel)
        # img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)), cv2.INTER_LANCZOS4)
        # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((2, 2), dtype=np.uint8))
        # cv2.imshow("Opening", cv2.resize(img, (int(img.shape[1]), int(img.shape[0]))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # # ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY) 
        
        # kernel = np.ones((2, 2),np.float32)
        # img = cv2.erode(img,kernel,iterations = 1)

        # # img = 255*(img < 128).astype(np.uint8)
        
        custom_oem_psm_config = '--dpi 600'
        try:
            text = pytesseract.image_to_string(img, lang='vie', config=custom_oem_psm_config)
            with open(outputsDir + '/' + imageName[:-3] + 'txt', 'w', encoding='utf8') as f:
                f.write(text)
        except Exception as identifier:
            pass
        # cv2.imshow("filtered", cv2.resize(img, (int(img.shape[1]), int(img.shape[0]))))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

if __name__ == "__main__":
    inputDir = 'splitEntry/003'
    imageName = list(filter(lambda file: file[-3:] == 'jpg', os.listdir(inputDir)))
    outputDir = 'texts/Tu dien 003/results'
    entryImageToText(imageName, inputDir, outputDir)