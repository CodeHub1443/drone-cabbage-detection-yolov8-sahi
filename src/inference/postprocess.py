import torch
import numpy as np
from scipy.spatial import cKDTree

def merge_predictions_vectorized(results: list, coords: list):
    merged_boxes = []

    for r, (x_off, y_off, _, _) in zip(results, coords):
        if r.boxes is None or len(r.boxes) == 0:
            continue

        cls = torch.stack([b.cls for b in r.boxes]).squeeze(-1)
        conf = torch.stack([b.conf for b in r.boxes]).squeeze(-1)
        xyxy = torch.stack([b.xyxy for b in r.boxes]).squeeze(1)

        mask = cls == 0
        if mask.sum() == 0:
            continue

        xyxy = xyxy[mask].cpu().numpy().astype(int)
        conf = conf[mask].cpu().numpy().astype(float)

        xyxy[:, [0, 2]] += x_off
        xyxy[:, [1, 3]] += y_off

        merged_boxes.extend([(*xy, c) for xy, c in zip(xyxy, conf)])

    return merged_boxes


def deduplicate_by_distance_kdtree(detections, dist_thresh_px=25):
    if not detections:
        return []

    dets = np.asarray(detections, dtype=np.float32)
    centers = np.column_stack(
        ((dets[:, 0] + dets[:, 2]) * 0.5, (dets[:, 1] + dets[:, 3]) * 0.5)
    )
    scores = dets[:, 4]

    tree = cKDTree(centers)
    order = np.argsort(-scores)
    used = np.zeros(len(dets), dtype=bool)

    keep = []
    for i in order:
        if used[i]:
            continue
        keep.append(tuple(detections[i]))
        idxs = tree.query_ball_point(centers[i], dist_thresh_px)
        used[idxs] = True

    return keep
