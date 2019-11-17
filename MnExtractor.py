class MnExtractor:
    def __init__(self):
        self.binarizer = Binarizer()
        self.skeletonizer = Skeletonizer()

    #Calculate the crossing number
    def calculate_cn(self, img, row_pos, col_pos):
      #Iterating through the neighbour of p from p2 -> p3 -> p4 -> p5 -> p6 -> p7 -> p8
        transitions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        total = 0
        for transition in range(len(transitions) - 1):
            row = row_pos + transitions[transition][0]
            col = col_pos + transitions[transition][1]
            next_row = row_pos + transitions[transition + 1][0]
            next_col = col_pos + transitions[transition + 1][1]
            total += abs(img[row, col] / 255 - img[next_row, next_col] / 255) #Normalize to 0 - 1
        return total / 2

    #Check if the point is located at the edge of the region or not
    #Shifing from right to left
    def isLeftBoundary(self, img, row_pos, col_pos):
        rows, cols = img.shape
        isBound = True
        for k in range(col_pos - 1, -1, -1):
            #If detected black part within the block
            if img[row_pos, k] == 0:
                isBound = False
                break
        return isBound
    #Shifing from left to right
    def isRightBoundary(self, img, row_pos, col_pos):
        rows, cols = img.shape
        isBound = True
        for k in range(col_pos + 1, cols):
             #If detected black part within the block
            if img[row_pos, k] == 0:
                isBound = False
                break
        return isBound

    #This is used to handle bifurcation minutia case since it's joint between 3 lines and not the endpoint.
    def isBoundary(self, img, row_pos, col_pos):
        if self.isLeftBoundary(img, row_pos, col_pos) or self.isRightBoundary(img, row_pos, col_pos):
            return True
        return False

    #Euclidian distance between 2 points
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def extract(self, enhancedImg):
        rows, cols = enhancedImg.shape
        binImg = self.binarizer.binarize(enhancedImg)
        skeletonImg = self.skeletonizer.skeletonize(binImg)
        #Set of minutias
        mnSet = []
        count = 0
        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                if(skeletonImg[row, col] == 0):
                    cn = self.calculate_cn(skeletonImg, row, col)
                    if cn == 1:
                        #In case that crossing number is 1 -> Endpoint Minutia
                        mnSet.append([row, col, M_TYPE_ENDPOINT])
                    elif cn == 3 and not self.isBoundary(enhancedImg, row, col):
                        #In case that crossing number is 3 -> Bifurcation Minutia
                        mnSet.append([row, col, M_TYPE_BIFURCATION])
        #Sort all of detected minutiae by distance between coordinate of minutia point from the center of enhanced image
        mnSet.sort(key=lambda coord: self.distance(rows // 2, cols // 2, coord[0], coord[1]))
        return mnSet
