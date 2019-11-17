class Binarizer:
  def __init__(self):
    pass
  def binarize(self,fpImg):
    #Blurring image to optimize the performance of Thresholding
    #bluredImg = cv2.GaussianBlur(fpImg,(3,3),cv2.BORDER_DEFAULT)
    retVal, binarized_image = cv2.threshold(fpImg, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binarized_image
