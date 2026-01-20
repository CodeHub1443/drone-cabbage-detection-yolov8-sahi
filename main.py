# ===================== Imports =====================
from collections import defaultdict

# ===================== Project related imports =====================
from src.io.paths import check_paths
from src.io.srt import parse_srt
from src.io.video import open_video
from src.visualization.drawing import annotate_frame
from src.geo.projection import global_position
from src.geo.filtering import filter_positions
from src.inference.core import inference_single_frame, load_model
from src.mapping.generator import create_map, create_cluster_map
from config import Config

# ===================== CONFIG =====================
cfg = Config()


def main(cfg: Config | None = None, return_results: bool = False):
    if cfg is None:
        cfg = Config()
    # ------------------ Sanity checks ------------------
    check_paths(cfg.ENGINE_PATH, cfg.VIDEO_PATH, cfg.SRT_PATH)

    model = load_model(cfg.ENGINE_PATH)
    if model is None:
        print("Failed to load model.")
        return

    frame_meta = parse_srt(cfg.SRT_PATH)

    # ------------------ Video IO ------------------
    cap, out, width, height = open_video(
        cfg.VIDEO_PATH,
        cfg.output_video_path(),
        cfg.SAVE_OUT_VIDEO,
    )

    cabbage_positions = defaultdict(list)

    print("Processing video and projecting cabbages to map...")

    frame_idx = 0
    mapped_frames = 0

    # ===================== MAIN LOOP =====================
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1

        # ---------- Get metadata ----------
        meta = frame_meta.get(frame_idx)

        # ---------- Detection (every frame) ----------
        detections = inference_single_frame(
            model,
            frame,
            cfg.DEVICE,
            cfg.CONF_THRES,
            cfg.DEDUPLICATE_DIST_THRES,
            cfg.SLICE_SIZE,
            cfg.OVERLAP_RATIO,
        )

        # ---------- Annotation + video write (every frame) ----------
        if cfg.SAVE_OUT_VIDEO:
            annotated = annotate_frame(
                frame,
                detections,
                cfg.BOX_COLOR,
                cfg.BOX_THICKNESS,
            )
            out.write(annotated)

        # ---------- Mapping cadence (decoupled) ----------
        if (
            meta is not None
            and frame_idx >= cfg.START_MAPPING_FRAME
            and frame_idx % cfg.MAP_EVERY == 0
        ):
            cabbage_positions = global_position(
                detections,
                meta,
                frame_idx,
                cabbage_positions,
                width,
                height,
                cfg.SENSOR_WIDTH_MM,
                cfg.FOCAL_LENGTH_MM,
                cfg.METERS_PER_DEG_LAT,
            )

            mapped_frames += 1
            if cfg.MAX_FRAMES_TO_MAP and mapped_frames >= cfg.MAX_FRAMES_TO_MAP:
                print("\nReached MAX_FRAMES_TO_MAP limit.")
                break

        if frame_idx % 100 == 0:
            print(f"Processed frame {frame_idx}", end="\r")

    # ===================== CLEANUP =====================
    cap.release()
    if cfg.SAVE_OUT_VIDEO:
        out.release()

    print("\nVideo processing complete.")
    print(f"Total cabbage positions found: {len(cabbage_positions)}")

    # ------------------ Filtering ------------------
    if cabbage_positions:
        filtered_cabbage_positions = filter_positions(
            cabbage_positions,
            cfg.GRID_SIZE_METERS,
            cfg.METERS_PER_DEG_LAT
        )
    else:
        filtered_cabbage_positions = {}

    print(f"Filtered cabbage positions: {len(filtered_cabbage_positions)}")

    # ------------------ Mapping ------------------
    if cfg.SAVE_HTML_MAP:
        print("Creating HTML map...")
        if cfg.MAP_TYPE == "cluster":
            create_cluster_map(filtered_cabbage_positions, cfg.map_output_path())
        else:
            create_map(filtered_cabbage_positions, cfg.map_output_path())

    # ===================== RETURN RESULTS (API SAFE) =====================
    result = {
        "total_cabbages": len(filtered_cabbage_positions),
        "video": cfg.output_video_path(),
        "map": cfg.map_output_path(),
    }

    if return_results:
        return result


if __name__ == "__main__":
    main()
