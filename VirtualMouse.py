import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

widthCam, heightCam = 640, 480
frameReduction = 100
smoothFactor = 7

prevTime = 0
prevLocX, prevLocY = 0, 0
currLocX, currLocY = 0, 0

capture = cv2.VideoCapture(1)
capture.set(3, widthCam)
capture.set(4, heightCam)
handDetector = htm.handDetector(maxHands=1)
screenW, screenH = pyautogui.size()

while True:
    success, frame = capture.read()
    if not success:
        print("Failed to capture image")
        break

    frame = handDetector.findHands(frame)
    landmarksList, bbox = handDetector.findPosition(frame)
    if len(landmarksList) != 0:
        xIndex, yIndex = landmarksList[8][1:]
        xMiddle, yMiddle = landmarksList[12][1:]

        fingersState = handDetector.fingersUp()
        cv2.rectangle(frame, (frameReduction, frameReduction), (widthCam - frameReduction, heightCam - frameReduction), (255, 0, 255), 2)

        if fingersState[1] == 1 and fingersState[2] == 0:
            xMapped = np.interp(xIndex, (frameReduction, widthCam - frameReduction), (0, screenW))
            yMapped = np.interp(yIndex, (frameReduction, heightCam - frameReduction), (0, screenH))

            currLocX = prevLocX + (xMapped - prevLocX) / smoothFactor
            currLocY = prevLocY + (yMapped - prevLocY) / smoothFactor

            pyautogui.moveTo(screenW - currLocX, currLocY)
            cv2.circle(frame, (xIndex, yIndex), 15, (255, 0, 255), cv2.FILLED)
            prevLocX, prevLocY = currLocX, currLocY

        if fingersState[1] == 1 and fingersState[2] == 1:
            distance, frame, lineInfo = handDetector.findDistance(8, 12, frame)
            if distance < 40:
                cv2.circle(frame, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

    currTime = time.time()
    framesPerSecond = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(frame, str(int(framesPerSecond)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Frame", frame)
    if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) < 1:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
