from ultralytics import YOLO
from src.inference.slicing import slice_frame
from src.inference.postprocess import merge_predictions_vectorized, deduplicate_by_distance_kdtree

def load_model(ENGINE_PATH: str):
    print(f"Loading TensorRT engine: {ENGINE_PATH}")
    model = YOLO(ENGINE_PATH)
    print("TensorRT engine loaded successfully")
    return model


def inference_single_frame(
    model,
    frame,
    device,
    conf_thres,
    dist_thresh_px,
    slice_size,
    overlap_ratio,
):
    slices, coords = slice_frame(frame, slice_size, overlap_ratio)

    # ---- HARD SAFETY CHECK ----
    if len(slices) > 8:
        slices = slices[:8]
        coords = coords[:8]

    results = model.predict(
        slices,
        device=device,
        conf=conf_thres,
        verbose=False,
    )

    detections = merge_predictions_vectorized(results, coords)
    detections = deduplicate_by_distance_kdtree(
        detections, dist_thresh_px=dist_thresh_px
    )

    return detections
