import cv2
import numpy as np
import utilis

#############

webcam = False
path = "D:\opencv_example\OpenCV Projects\Real Time Object Measurement\\4.png"

cap =cv2.VideoCapture(0)
cap.set(10,160)
cap.set(3,640)
cap.set(4,480)
scale = 3
wP = 210 * scale
hP = 297 *scale

###############

while True:
    if webcam : 
        address = "http://192.168.0.101:8080/video"   
        cap.open(address)
        success, img = cap.read()
        cv2.imshow("Origqqinal", img)

    else: 
        img = cv2.imread(path)
        img = cv2.resize(img, (0,0), None, 0.5,0.5)
        print(img.shape)

        # img = cv2.rectangle(img, (15,7),(500,391),(0,0,0),1)
    img , conts = utilis.getContours(img, minArea = 50000, filter = 4)

    if len(conts) != 0:
        biggest = conts[0][2]
        imgWarp = utilis.warpImg(img, biggest, wP, hP, pad=20)
        # img = cv2.resize(img, (0,0), None, 0.5,0.5)

        # cv2.imshow("Origqqinal", img)
        imgC , conts2 = utilis.getContours(imgWarp, minArea = 2000, filter = 4,cThr=[50,50], draw=False)

        if len(conts) != 0:
            for obj in conts2:
                cv2.polylines(imgC, [obj[2]], True, (0,255,0), 2)
                nPoints = utilis.reorder(obj[2])
                nW = round((utilis.findDist(nPoints[0][0]//scale,nPoints[1][0]//scale)/10),1)
                nH = round((utilis.findDist(nPoints[0][0]//scale,nPoints[2][0]//scale)/10),1)

                cv2.arrowedLine(imgC, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                            (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgC, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                            (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(imgC, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 0, 255), 2)
                cv2.putText(imgC, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 0, 255), 2)


        cv2.imshow("cont in cont", imgC)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


        
