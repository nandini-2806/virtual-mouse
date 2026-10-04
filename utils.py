"""
utils.py

Helper functions for the Virtual Mouse project.
"""

import math
from typing import Tuple

import numpy as np


def calculate_distance(
    point1: Tuple[int, int],
    point2: Tuple[int, int],
) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        point1: (x1, y1)
        point2: (x2, y2)

    Returns:
        Distance as a float.
    """

    return math.hypot(
        point2[0] - point1[0],
        point2[1] - point1[1],
    )


def map_coordinates(
    value: float,
    input_range: Tuple[int, int],
    output_range: Tuple[int, int],
) -> float:
    """
    Map a value from one range to another.

    Example:
        Camera X: 100-1180
        Screen X: 0-1920
    """

    return np.interp(
        value,
        input_range,
        output_range,
    )


def smooth_movement(
    previous: float,
    current: float,
    smoothing: int = 7,
) -> float:
    """
    Apply smoothing to cursor movement.

    Higher smoothing:
        Slower
        More stable

    Lower smoothing:
        Faster
        Less stable
    """

    return previous + (current - previous) / smoothing


def get_landmark(
    landmarks,
    landmark_id: int,
):
    """
    Return the (x, y) coordinates of a landmark.

    Args:
        landmarks:
            List returned by HandTracker.find_position()

    Returns:
        (x, y)
    """

    _, x, y = landmarks[landmark_id]

    return x, y


def is_pinching(
    landmarks,
    finger1: int,
    finger2: int,
    threshold: int = 35,
) -> bool:
    """
    Check if two fingertips are close enough
    to be considered pinching.
    """

    p1 = get_landmark(landmarks, finger1)
    p2 = get_landmark(landmarks, finger2)

    distance = calculate_distance(p1, p2)

    return distance < threshold


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """
    Restrict a value to a range.
    """

    return max(minimum, min(value, maximum))