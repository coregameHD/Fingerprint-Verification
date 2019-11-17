class FpSegmentator:
    def __init__(self, bs = 16, th = 160):
        self.blockSize = bs
        self.threshHold = th

    def segment(self, fpImg):
        segmentedImg = fpImg
        maskImg = fpImg
        #Perform edge detection using Canny technique
        blurImg = cv2.GaussianBlur(fpImg, (7,7), 0) 
        edgeImg = cv2.Canny(blurImg,  20, 70)

        rows, cols, *ch = maskImg.shape
        total = 0
        sd = 0
        size = self.blockSize ** 2

        #Compute statistical features of each block in input fingerprint image
        #And check if SD is less than the threshold value
        for row in range(0,rows, self.blockSize):
            for col in range(0,cols, self.blockSize):
                try:
                  #Calculate total pixels here
                    for r in range(row,row + self.blockSize):
                        for c in range(col,col + self.blockSize):
                            total += edgeImg[r,c]
                  #Calculate total sd of the edgeImg here
                    for r in range(row,row + self.blockSize):
                        for c in range(col,col + self.blockSize):
                            sd += (edgeImg[r,c] - (total // size))**2
                    total_sd = math.sqrt(sd // self.blockSize)
                    #Assign white color to the region with lower threshold 
                    if  total_sd < self.threshHold:
                        for r in range(row,row + self.blockSize):
                            for c in range(col,col + self.blockSize):
                                segmentedImg[r,c] = 255
                    #Reset the sd and total pix for each block
                    total = 0
                    sd = 0
                except IndexError as ie:
                    pass
        return segmentedImg