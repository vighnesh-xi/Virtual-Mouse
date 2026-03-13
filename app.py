import streamlit as st
import cv2
import HandTrackingModule as htm
import numpy as np

st.title("Hand Tracking Demo")

run = st.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)

detector = htm.handDetector(maxHands=1)

while run:
    success, frame = cap.read()
    if not success:
        st.write("Camera error")
        break

    frame = detector.findHands(frame)
    lmList, bbox = detector.findPosition(frame)

    if len(lmList) != 0:
        st.write("Index Finger:", lmList[8])

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)

cap.release()
