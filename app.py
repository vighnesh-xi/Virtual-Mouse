import streamlit as st
import cv2
import HandTrackingModule as htm
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

st.title("Hand Tracking Demo")
st.write("Show your hand to the camera. Index finger = move | Index + Middle = click")

detector = htm.handDetector(maxHands=1)

class HandTrackingProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # Draw index finger tip
            x, y = lmList[8][1], lmList[8][2]
            cv2.circle(img, (x, y), 12, (255, 0, 255), cv2.FILLED)
            cv2.putText(img, f"Index: ({x},{y})", (10, 40),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="hand-tracking",
    video_processor_factory=HandTrackingProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)
