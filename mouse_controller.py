"""
mouse_controller.py
Controls the system mouse using hand gestures.
"""

import time
import pyautogui

from utils import (
    clamp,
    get_landmark,
    is_pinching,
    map_coordinates,
    smooth_movement,
)


class MouseController:

    def __init__(self):

        pyautogui.FAILSAFE = True

        self.screen_width, self.screen_height = pyautogui.size()

        # Camera active area
        self.frame_margin = 100

        # Cursor smoothing
        self.smoothing = 7

        self.prev_x = 0
        self.prev_y = 0

        self.dragging = False

        self.last_click_time = 0
        self.click_delay = 0.30

        self.prev_scroll_y = None

    def update(self, frame, landmarks, tracker):

        fingers = tracker.fingers_up(landmarks)

        if len(fingers) != 5:
            return

        frame_height, frame_width, _ = frame.shape

        index_x, index_y = get_landmark(landmarks, 8)

        # ----------------------------------------------------
        # Move Cursor
        # Gesture:
        # Index finger only
        # ----------------------------------------------------

        if fingers == [0, 1, 0, 0, 0]:

            screen_x = map_coordinates(
                index_x,
                (self.frame_margin, frame_width - self.frame_margin),
                (0, self.screen_width),
            )

            screen_y = map_coordinates(
                index_y,
                (self.frame_margin, frame_height - self.frame_margin),
                (0, self.screen_height),
            )

            screen_x = clamp(screen_x, 0, self.screen_width)
            screen_y = clamp(screen_y, 0, self.screen_height)

            smooth_x = smooth_movement(
                self.prev_x,
                screen_x,
                self.smoothing,
            )

            smooth_y = smooth_movement(
                self.prev_y,
                screen_y,
                self.smoothing,
            )

            pyautogui.moveTo(smooth_x, smooth_y)

            self.prev_x = smooth_x
            self.prev_y = smooth_y

        # ----------------------------------------------------
        # Left Click
        # Gesture:
        # Index + Middle fingers
        # Pinch
        # ----------------------------------------------------

        if fingers == [0, 1, 1, 0, 0]:

            if is_pinching(landmarks, 8, 12):

                now = time.time()

                if now - self.last_click_time > self.click_delay:

                    pyautogui.click()

                    self.last_click_time = now

        # ----------------------------------------------------
        # Right Click
        # Gesture:
        # Index + Middle + Ring
        # ----------------------------------------------------

        if fingers == [0, 1, 1, 1, 0]:

            now = time.time()

            if now - self.last_click_time > self.click_delay:

                pyautogui.rightClick()

                self.last_click_time = now

        # ----------------------------------------------------
        # Drag & Drop
        # Gesture:
        # Thumb + Index pinch
        # ----------------------------------------------------

        if is_pinching(landmarks, 4, 8):

            if not self.dragging:

                pyautogui.mouseDown()

                self.dragging = True

        else:

            if self.dragging:

                pyautogui.mouseUp()

                self.dragging = False

        # ----------------------------------------------------
        # Scroll
        # Gesture:
        # Index + Middle fingers
        # Move vertically
        # ----------------------------------------------------

        if fingers == [0, 1, 1, 0, 0]:

            if self.prev_scroll_y is None:
                self.prev_scroll_y = index_y

            difference = self.prev_scroll_y - index_y

            if abs(difference) > 10:

                pyautogui.scroll(int(difference))

                self.prev_scroll_y = index_y

        else:

            self.prev_scroll_y = None