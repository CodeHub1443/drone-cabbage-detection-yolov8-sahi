import cv2
import numpy as np


def create_output_writer(
    OUTPUT_VIDEO_PATH: str,
    fps: float,
    width: int,
    height: int
):
    """
    Creates a browser-compatible H.264 (avc1) video writer.
    """
    # H.264 codec (browser-safe)
    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    return cv2.VideoWriter(
        OUTPUT_VIDEO_PATH,
        fourcc,
        fps,
        (width, height),
        True  # isColor = True
    )


def open_video(
    VIDEO_PATH: str,
    OUTPUT_VIDEO_PATH: str,
    SAVE_OUT_VIDEO: bool = True
):
    """
    Opens the input video and prepares a browser-compatible output video writer.
    """
    cap = cv2.VideoCapture(VIDEO_PATH)
    assert cap.isOpened(), "Cannot open video"

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if SAVE_OUT_VIDEO:
        out = create_output_writer(
            OUTPUT_VIDEO_PATH,
            fps,
            width,
            height
        )
    else:
        out = None

    return cap, out, width, height
