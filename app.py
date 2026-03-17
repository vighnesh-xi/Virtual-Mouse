import os
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"

import streamlit as st
import cv2
import numpy as np
import HandTrackingModule as htm

st.title("Hand Tracking Demo")
st.write("Allow camera access, then show your hand!")

detector = htm.handDetector(maxHands=1)

img_file = st.camera_input("Show your hand to the camera")

if img_file is not None:
    # Decode image from browser camera
    file_bytes = np.frombuffer(img_file.getvalue(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Run hand detection
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingersState = detector.fingersUp()
        fingers_up = sum(fingersState)

        xIndex, yIndex = lmList[8][1], lmList[8][2]

        # Draw bounding box
        cv2.rectangle(img, (bbox[0]-20, bbox[1]-20),
                      (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)

        # Index only → Move
        if fingersState[1] == 1 and fingersState[2] == 0:
            cv2.circle(img, (xIndex, yIndex), 15, (255, 0, 255), cv2.FILLED)
            cv2.putText(img, "MOVE MODE", (10, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            st.success(f"☝️ MOVE MODE — Index tip at ({xIndex}, {yIndex})")

        # Index + Middle → Click
        elif fingersState[1] == 1 and fingersState[2] == 1:
            distance, img, lineInfo = detector.findDistance(8, 12, img)
            cv2.putText(img, "CLICK MODE", (10, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            if distance < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "CLICKED!", (10, 90),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                st.success("✌️ CLICK detected!")
            else:
                st.info(f"✌️ CLICK MODE — fingers distance: {int(distance)}px")

        else:
            st.info(f"🖐️ {fingers_up} finger(s) detected")

        # Show result
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, caption="Hand Detection Result", use_container_width=True)
    else:
        st.warning("No hand detected. Try again!")
