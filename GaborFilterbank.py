class GaborFilterbank:
  def __init__(self, frequency, kernel_size, sigma):
    self.frequency = frequency
    self.kernel_size = kernel_size
    self.sigma = sigma
    self.gaborFilters = {}

    #Using dictionary to store the key of orientation associated with Gabor Filter with the key orientaion
    self.orientations = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5]
    for orientation in self.orientations:
      self.gaborFilters[orientation] = GaborFilter(self.kernel_size, self.sigma, orientation, self.frequency)

  def drawGaborFilterBank(self):
    #Visualise the generated Gabor filter with different angles
    for orientation in self.orientations:
      imshow(self.gaborFilters[orientation].drawFilter(), "Filter" + str(orientation))
      
  def getGaborFilters(self):
    return self.gaborFilters

  def isAtBeginEdge(self, pos, padding):
    #For row -> Left of img
    #For col -> Top of Img
    val = 0
    if(pos - padding > 0):
      val =  pos - padding
    else:
      val =  0
    return val

  def isAtEndEdge(self, pos,border, block, padding):
    #For row -> Right of img
    #For col -> Bottom of Img
    val = 0
    if(pos + padding + block < border):
      val = pos + padding + block
    else:
      val = border
    return val
  
  def filter(self, fpImg, ofImg, mskImg):
    img = fpImg
    fixed_block = self.kernel_size #16
    rows, cols = img.shape

    # Assign the angle from Orientation Field Image to Orientation matrix
    orientations = np.zeros((rows // fixed_block , cols // fixed_block), dtype = np.float32)
    for row in range(orientations.shape[0]):
        for col in range(orientations.shape[1]):
            orientations[row, col] = ofImg[row * fixed_block + 1, col * fixed_block + 1]
    
    block_rows = fixed_block
    block_cols = fixed_block
    padding = self.kernel_size // 2 + 1 #6

    for row in range(0, rows, fixed_block-1):
        r1 = self.isAtBeginEdge(row, padding)
        r2 = self.isAtEndEdge(row, rows, fixed_block, padding)
        
        for col in range(0, cols, fixed_block-1):
            c1 = self.isAtBeginEdge(col ,  padding)
            c2 = self.isAtEndEdge(col, cols, fixed_block, padding)

            block = img[r1 : r2, c1 : c2]
            orientation = orientations[row // fixed_block , col // fixed_block]

            orientation = (orientation - 90)
            if(orientation < 0):
              orientation += 180
            if (orientation > 180):
              orientation /= 2
            
            gabor = self.gaborFilters[orientation]
            img[row : row + fixed_block , col : col + fixed_block] = gabor.filter(block)[row - r1 : row - r1+ fixed_block , col - c1 : col - c1 + fixed_block]
            
            #imshow(gabor.drawFilter() , "Applied Filter") <- Debugging
    
    img = np.where(mskImg==0, img, 255)

    return img
