import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector


detector = HandDetector(detectionCon=0.5)


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def drawButton(self, img):
        cv2.rectangle(img, self. pos, (self.pos[0]+self.width,
                                       self.pos[1]+self.height), (255, 255, 255), cv2.FILLED)

        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                                      self.pos[1]+self.height), (0, 0, 0), 2)
        cv2.putText(img, self.value, (self.pos[0]+20, self.pos[1]+60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

    def findNumber(self, x, y, i):
        # print(self.pos[0], x)
        # print(self.pos[1], y)

        if self.pos[0] < x < self.pos[0]+self.width and self.pos[1] < y < self.pos[1]+self.height:
            return i


calcu = [["7", "8", "9", "*"], ["4", "5", "6", "-"],
         ["1", "2", "3", "+"], ["/", "0", ".", "="]]


buttons = []
delyCounter = 0

for x in range(4):
    for y in range(4):
        xPoint = (100*y+800)
        yPoint = (100*x+200)
        buttons.append(Button((xPoint, yPoint), 100, 100, calcu[x][y]))

result = ""

cap = cv2.VideoCapture(0)
cap.set(3, 1900)
cap.set(4, 1300)


while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=True, flipType=True)

    cv2.rectangle(img, (800, 120), (1200, 200), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (800, 120), (1200, 200), (0, 0, 0), 2)

    cv2.putText(img, result, (810, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

    for button in buttons:
        button.drawButton(img)

    if hands:

        lmList1 = hands[0]["lmList"]
        length, info, img = detector.findDistance(
            lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),    scale=10)

        x, y, _ = lmList1[8]

        if (length < 50 and delyCounter == 0):

            for i, button in enumerate(buttons):
                index = button.findNumber(x, y, i)
                if index is not None:

                    number = calcu[int(index/4)][int(index % 4)]
                    delyCounter = 1
                    if number == "=":
                        result = str(eval(result))

                    else:
                        result += number

    if delyCounter != 0:
        delyCounter += 1
        if delyCounter > 10:
            delyCounter = 0

    # print(result)
    cv2.imshow("img", img)
    key = cv2.waitKey(1)

    if key & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
    if key == ord("r"):
        result = ""
        counter = 0
