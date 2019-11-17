class Skeletonizer:
  # Thinning is performed by iterating through 3 x 3 region and observe its neighbours
  # --------------------------
  #    p1  |   p2   |   p3   |   
  #    p8  |   p2   |   p4   |
  #    p7  |   p6   |   p5   |
  # --------------------------
  def __init__(self):
    pass
  def count_black_neighbour(self, img, row_pos, col_pos):
    #Iterating through the neighbour of p from p2 -> p3 -> p4 -> p5 -> p6 -> p7 -> p8
    count = 0
    for neighbour_row in range(-1, 2):
        for neighbour_col in range(-1, 2):
            if neighbour_row == 0 and neighbour_col == 0:
                continue
            elif img[row_pos + neighbour_row][col_pos + neighbour_col] == 0:
                count += 1
    return count

  def count_transition(self, img, row_pos, col_pos):
    #Iterating through the neighbour of p from p2 -> p3 -> p4 -> p5 -> p6 -> p7 -> p8
    transitions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
    count = 0
    for transition in range(1, len(transitions)):
      row = row_pos + transitions[transition][0]
      col = col_pos + transitions[transition][1]
      prev_row = row_pos + transitions[transition - 1][0]
      prev_col = col_pos + transitions[transition - 1][1]
      if img[prev_row, prev_col] == 255 and img[row, col] == 0:
        count += 1
    return count

  def areConPixelsWhite(self, img):
      #Case 2 4 6
      if img[0, 1] == 255 or img[1, 2] == 255 or img[2, 1] == 255:
        return True
      #Case 4 6 8
      elif img[1, 2] == 255 or img[2, 1] == 255 or img[1, 0] == 255:
        return True
      #Case 2 4 8
      elif img[0, 1] == 255 or img[1, 2] == 255 or img[1, 0] == 255:
          return True
      #Case 2 6 8
      elif img[0, 1] == 255 or img[2, 1] == 255 or img[1, 0] == 255:
          return True
      return False
  
  def skeletonize(self, binImg):
    rows, cols = binImg.shape
    for row in range(1, rows - 1):
      for col in range(1, cols - 1):
          if binImg[row][col] == 0:
              if(self.count_black_neighbour(binImg, row, col) >= 2) and (self.count_black_neighbour(binImg, row, col) <= 6):
                  if self.count_transition(binImg, row, col) == 1:
                    if self.areConPixelsWhite(binImg[row - 1 : row + 2 , col - 1 : col + 2 ]):
                      binImg[row][col] = 255
    return binImg
