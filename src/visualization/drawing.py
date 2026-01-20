import cv2
import numpy as np

def annotate_frame(frame:np.ndarray, detections: list[tuple[int, int, int, int, float]],
                BOX_COLOR:tuple[int, int, int]=(0, 0, 255), 
                BOX_THICKNESS:int=2)->np.ndarray:
    '''
    Puts the given bboxes and their confidence scores on the frame.
    '''
    for x1, y1, x2, y2, conf in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, BOX_THICKNESS)
        cv2.putText(frame, f"{conf:.2f}", (x1, max(y1 - 5, 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, BOX_COLOR, 1)

    return frame
