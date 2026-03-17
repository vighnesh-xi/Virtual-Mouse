import os
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"  # Force CPU before any mediapipe import

import streamlit as st
import cv2
import HandTrackingModule as htm
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

st.title("Hand Tracking Demo")
st.write("Show your hand to the camera.")
st.markdown("""
- ☝️ **Index finger only** → Move cursor  
- ✌️ **Index + Middle finger** → Click  
""")

RTC_CONFIGURATION = {
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
    ]
}


class HandTrackingProcessor(VideoProcessorBase):
    def __init__(self):
        self.detector = htm.handDetector(maxHands=1)
        self.frameReduction = 100
        self.widthCam = 640
        self.heightCam = 480

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        img = self.detector.findHands(img)
        lmList, bbox = self.detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            xIndex, yIndex = lmList[8][1], lmList[8][2]
            xMiddle, yMiddle = lmList[12][1], lmList[12][2]

            fingersState = self.detector.fingersUp()

            cv2.rectangle(
                img,
                (self.frameReduction, self.frameReduction),
                (self.widthCam - self.frameReduction, self.heightCam - self.frameReduction),
                (255, 0, 255), 2
            )

            # Index only → Move mode
            if fingersState[1] == 1 and fingersState[2] == 0:
                cv2.circle(img, (xIndex, yIndex), 15, (255, 0, 255), cv2.FILLED)
                cv2.putText(img, "MOVE MODE", (10, 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            # Index + Middle → Click mode
            if fingersState[1] == 1 and fingersState[2] == 1:
                distance, img, lineInfo = self.detector.findDistance(8, 12, img)
                cv2.putText(img, "CLICK MODE", (10, 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                if distance < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "CLICKED!", (10, 90),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="hand-tracking",
    video_processor_factory=HandTrackingProcessor,
    rtc_configuration=RTC_CONFIGURATION,   # ← fixes NoneType/ICE error
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)
