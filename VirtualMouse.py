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

capture = cv2.VideoCapture(0)           
capture.set(3, widthCam)
capture.set(4, heightCam)

handDetector = htm.handDetector(maxHands=1)
screenW, screenH = pyautogui.size()

pyautogui.FAILSAFE = False              
pyautogui.PAUSE = 0                     

while True:
    success, frame = capture.read()
    if not success:
        print("Failed to capture image")
        break

    frame = cv2.flip(frame, 1)          

    frame = handDetector.findHands(frame)
    landmarksList, bbox = handDetector.findPosition(frame)

    if len(landmarksList) != 0:
        xIndex, yIndex = landmarksList[8][1], landmarksList[8][2]
        xMiddle, yMiddle = landmarksList[12][1], landmarksList[12][2]

        fingersState = handDetector.fingersUp()
        cv2.rectangle(frame,
            (frameReduction, frameReduction),
            (widthCam - frameReduction, heightCam - frameReduction),
            (255, 0, 255), 2)

        # ☝️ Index only → Move cursor
        if fingersState[1] == 1 and fingersState[2] == 0:
            xMapped = np.interp(xIndex, (frameReduction, widthCam - frameReduction), (0, screenW))
            yMapped = np.interp(yIndex, (frameReduction, heightCam - frameReduction), (0, screenH))

            currLocX = prevLocX + (xMapped - prevLocX) / smoothFactor
            currLocY = prevLocY + (yMapped - prevLocY) / smoothFactor

            pyautogui.moveTo(screenW - currLocX, currLocY)
            cv2.circle(frame, (xIndex, yIndex), 15, (255, 0, 255), cv2.FILLED)
            cv2.putText(frame, "MOVE", (20, 80),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            prevLocX, prevLocY = currLocX, currLocY

        # ✌️ Index + Middle → Click
        if fingersState[1] == 1 and fingersState[2] == 1:
            distance, frame, lineInfo = handDetector.findDistance(8, 12, frame)
            if distance < 40:
                cv2.circle(frame, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, "CLICK!", (20, 80),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                pyautogui.click()
                time.sleep(0.3)         

    # FPS counter
    currTime = time.time()
    framesPerSecond = 1 / (currTime - prevTime) if (currTime - prevTime) > 0 else 0
    prevTime = currTime
    cv2.putText(frame, f"FPS: {int(framesPerSecond)}", (20, 50),
        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Virtual Mouse", frame)
    if cv2.getWindowProperty("Virtual Mouse", cv2.WND_PROP_VISIBLE) < 1:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
