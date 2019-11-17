class OfDetector:
  def __init__(self, bSize = 16):
    self.blockSize = bSize

  def computeOrientation(self, block):
      #Using Sobel technique to find gradient magnitude in X, Y axis of the block
      blockGx = cv2.Sobel(block, cv2.CV_32F, 1, 0)
      blockGy = cv2.Sobel(block, cv2.CV_32F, 0, 1)
      numerator = 0
      denominator = 0
      rows, cols = blockGx.shape
      #Estimate local ridge orientation based on specified formula
      for row in range(rows):
          for col in range(cols):
              numerator += 2 * blockGx[row, col] * blockGy[row, col]
              denominator += (blockGx[row, col]) ** 2 - (blockGy[row, col])**2
      theta = (np.arctan2(numerator, denominator)) / 2

      # Rotate the orientations so that they point along the ridges, and wrap
      # them into only half of the circle (all should be less than 180 degrees).
      theta = (theta + np.pi * 0.5) % np.pi
      return math.degrees(theta)

  def quantizeOrientation(self, orientation):
      #This function used to estimate the local ridge orientation
      orientations = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5]
      #In case that the orientation is less negative
      if orientation < 0 :
          orientation += 360
      #In case that the orientation exceeds 180 degree
      if orientation > 180:
          orientation /= 2
      max_angle = 999
      currentOrientation = 0
      for angle in orientations:
          #Check the difference between the input angle and orientation in orientation list
          angle_diff = abs(angle - orientation)
          #In case that the angle is less than max Angle
          if angle_diff < max_angle:
              max_angle = angle_diff
              currentOrientation = angle
      return currentOrientation

  def ridge_estimation(self, img, block_size):
      #Assign the orientation to the block in the part of input fingerprint
      rows, cols = img.shape
      orientations_matrix = np.zeros((rows //block_size + 1 , cols // block_size + 1), dtype = np.float32)
      block_rows = block_size
      block_cols = block_size
      for row in range(0, rows, block_size):
          end_row = row + block_size
          for col in range(0, cols, block_size):
              end_col = col + block_size
              block = img[row : end_row, col : end_col]
              orientations_matrix[row // block_size, col // block_size] = self.quantizeOrientation(self.computeOrientation(block))
      return orientations_matrix

  def drawOFimage(self,ofImg,angle,x,y):
    margin = 3
    #Convert the degree -> radian and apply sine function to calculate the destination point
    angle = np.deg2rad(angle)
    x2 =  (self.blockSize - margin ) * np.cos(angle)
    y2 =  (self.blockSize - margin ) * np.sin(angle)

    #Draw a black line with size of 1 px in a block with starting point(x,y) to destination point(x2,y2)  
    cv2.line(ofImg, (x,y), (int(x + x2) , int(y + y2)), (0, 0, 0) , 1)

  def detect(self, fpImg, mskImg):
      tmpImg = fpImg
      rows, cols = tmpImg.shape
      yblocks, xblocks = rows//self.blockSize, cols//self.blockSize
      orientations = self.ridge_estimation(tmpImg, self.blockSize)
      #Create the Matrix that stores the value of orientations
      ofMat = orientations
      #Construct ofImg to be used in Fingerprint Enhancement 
      ofImg = np.full(tmpImg.shape, -1.0)
      #Create empty white image used to plot lines showing orientation field
      #whiteImg = np.ones(tmpImg.shape, dtype=np.uint8) * 255
      for y in range(yblocks):
          for x in range(xblocks):
              #Assign orientation to each block inside of ofImg
              ofImg[y * self.blockSize : (y+1) * self.blockSize, x * self.blockSize : (x+1) * self.blockSize] = ofMat[y, x]
              #Plot local ridge line onto each block on whiteImg
              #self.drawOFimage(whiteImg, ofMat[y, x] ,x * self.blockSize, y * self.blockSize)
      
      #Overlay the plotted image onto original image
      #imshow(cv2.addWeighted(fpImg,0.25,whiteImg,0.75,1),"calculated orientation field")
      return ofMat, ofImg   