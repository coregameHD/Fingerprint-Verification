class FpEnhancer:
  def __init__(self,bSize = 16):
    self.blockSize = bSize
  # Create the mask to extract only ROI of the fingerprint image
  def createMask(self, segmentedImg, n = 16):
    rows, cols = segmentedImg.shape
    mask = np.zeros(segmentedImg.shape, dtype = np.uint8)
    white = np.ones((n, n), dtype = np.uint8) * 255
    toRemove = []

    for row in range(0, rows, n):
        for col in range(0, cols, n):
            block = segmentedImg[row : row + n, col : col +n]
            if np.array_equal(white, block):
              mask[row : row + n, col : col + n] = 255
            else:
              mask[row : row + n, col : col + n] = 0
      
    for row in range(0, rows, n):
        for col in range(0, cols, n):
            if (row - n < 0 or col - n < 0 or row + n + 1 > rows or col + n + 1 > rows):
                toRemove.append( (row, col) )
            elif (mask[row + 1, col + 1]==0) and (mask[row + n + 1, col + 1]==255 
                                                  or mask[row - n + 1, col + 1]==255 
                                                  or mask[row + 1, col - n + 1]==255 
                                                  or mask[row + 1, col + n + 1]==255):
                toRemove.append((row , col))

    for element in toRemove:
        row, col = element[0], element[1]
        mask[row : row + n, col : col + n] = 255 #Assign white color to the removed region
        
    return mask

  def enhance(self, fpImg, mskImg):
    mskImg2 = self.createMask(fpImg,self.blockSize)
    ofDetector = OfDetector(self.blockSize)
    ofMat, ofImg = ofDetector.detect(fpImg, mskImg)
    gaborFilterBank = GaborFilterbank(10.0, 10, 3.0)
    enhImg = gaborFilterBank.filter(fpImg, ofImg, mskImg2)
    return enhImg
