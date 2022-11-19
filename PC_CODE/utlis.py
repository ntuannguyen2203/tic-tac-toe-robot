import cv2
import numpy as np



#### 1 - Preprocessing Image
def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
   # imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 5)  # APPLY ADAPTIVE THRESHOLD
    imgThreshold = cv2.Canny(imgBlur, 50, 100)
    return imgThreshold


#### 3 - Reorder points for Warp Perspective
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew


#### 3 - FINDING THE BIGGEST COUNTOUR ASSUING THAT IS THE SUDUKO PUZZLE
def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
       # print(area)
        if area > 80000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest,max_area


#### 4 - TO SPLIT THE IMAGE INTO 81 DIFFRENT IMAGES
def splitBoxes(sizechess,img):
    rows = np.vsplit(img,sizechess)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,sizechess)
        for box in cols:
            boxes.append(box)
    return boxes


def kiemtradauO(img):
    gray = cv2.medianBlur(img, 1)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    if circles is None:
        codauO = 0
    else:
        codauO = 1
    return codauO

def kiemtradauX(img):
    anhphu = cv2.Canny(img, 75, 150)
    lines = cv2.HoughLinesP(anhphu, 1, np.pi / 180, 50)
    if lines is None:
        codaux=0
    else:
        codaux=1
    return codaux
def hamlocovuongnho(sizechess,Image):
    heightImg = 450
    widthImg = 450
    img = Image
    img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgThreshold = preProcess(img)
    imgContours = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)  # DRAW ALL DETECTED CONTOURS
   # cv2.imshow("caccoutor",imgContours)
    #### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
    biggest, maxArea = biggestContour(contours)  # FIND THE BIGGEST CONTOUR
    if biggest.size != 0:
        biggest = reorder(biggest)
        # print(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25)  # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgWarpColored = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        anhk=cv2.resize(imgWarpColored,(900,900))
        cv2.imshow("Banco",anhk)
        boxes = splitBoxes(sizechess,imgWarpColored)
    else:
        boxes=333
    return boxes
def docanhsangmatran(kichthuocbanco,list_img):
    list=list_img
    kt=kichthuocbanco
    matranco = np.zeros((kt, 1, kt), dtype=np.int32)
    k=0
    for i in range(0,kt):
        for j in range(0,kt):
            if kiemtradauO(list[k])==1:
                matranco[i,0,j]=1
            elif kiemtradauX(list[k][10:80,10:80])==1:
                matranco[i, 0, j] = 2
            else:
                matranco[i, 0, j] = 0
            k=k+1
    #print("matranco",matranco)
    return matranco
def kiemtrasukhacnhau2mang(sizechess,mangtruoc,mangsau):
    hieu=mangsau-mangtruoc
    vitri=-1;
    a=0
    b=0
    kt=sizechess
    for i in range(0, kt):
        for j in range(0, kt):
            if hieu[i, 0, j] != 0:
                a=i
                b=j

    return a,b
def kiemtrahople(sizechess,mangtruoc,mangsau):
    demtr=0
    demsau=0
    mtr=mangtruoc
    msau=mangsau
    for i in range(0, sizechess):
        for j in range(0, sizechess):
            if mtr[i, 0, j] != 0:
                demtr=demtr+1
            if msau[i, 0, j] != 0:
                demsau=demsau+1
    if demsau>demtr:
        return 1
    else:
        return 0
def kiemtrahoa(sizechess,mang):
    a=1
    manghoa=mang
    for i in range(0, sizechess):
        for j in range(0, sizechess):
            if  manghoa[i, 0, j] == 0:
                a=0
                break
    if a==1:
        return True
    else:
        return False
def chuyenhangcotsangso(sizechess,hang,cot):
    so=sizechess*(hang-1)+cot
    return so
