"""
hand_tracker.py
Handles hand detection and landmark extraction using MediaPipe.
"""

from typing import List, Tuple
import cv2
import mediapipe as mp


class HandTracker:
    """
    Detects hands and returns landmark positions.
    """

    def __init__(
        self,
        mode: bool = False,
        max_hands: int = 1,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.7,
    ) -> None:

        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )

        self.results = None

    def find_hands(self, frame, draw: bool = True):
        """
        Detect hands in the frame.
        Args:
            frame: BGR image from OpenCV.
            draw: Draw landmarks if True.

        Returns:
            Frame with landmarks (optional).
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:

            for hand_landmarks in self.results.multi_hand_landmarks:

                if draw:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                    )

        return frame

    def find_position(
        self,
        frame,
        hand_no: int = 0,
        draw: bool = False,
    ) -> List[Tuple[int, int, int]]:
        """
        Returns all landmark positions.

        Returns:
            [
                (id, x, y),
                ...
            ]
        """

        landmark_list = []

        if not self.results:
            return landmark_list

        if not self.results.multi_hand_landmarks:
            return landmark_list

        hand = self.results.multi_hand_landmarks[hand_no]

        h, w, _ = frame.shape

        for idx, landmark in enumerate(hand.landmark):

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            landmark_list.append((idx, x, y))

            if draw:
                cv2.circle(frame, (x, y), 5, (255, 0, 255), cv2.FILLED)

        return landmark_list

    def fingers_up(self, landmarks: List[Tuple[int, int, int]]) -> List[int]:
        """
        Detect which fingers are raised.

        Returns:
            [thumb, index, middle, ring, little]

            1 = Up
            0 = Down
        """

        if not landmarks:
            return []

        fingers = []

        # Tip landmark IDs
        tips = [4, 8, 12, 16, 20]

        # Thumb
        if landmarks[tips[0]][1] > landmarks[tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for tip in tips[1:]:

            if landmarks[tip][2] < landmarks[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers