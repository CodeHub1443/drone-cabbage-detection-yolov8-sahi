import math
from collections import defaultdict

def global_position(detections: list[tuple[int, int, int, int, float]], 
                    frame_meta: tuple[float, float, float], 
                    frame_idx: int, 
                    cabbage_positions: defaultdict[tuple[float, float], list[tuple[float, int]]], 
                    width: int, height: int, 
                    SENSOR_WIDTH_MM: float, FOCAL_LENGTH_MM: float, 
                    METERS_PER_DEG_LAT: float) -> defaultdict[tuple[float, float], list[tuple[float, int]]]:
    '''
    Converts pixel coordinates to global GPS coordinates.
    args:
        detections: List of detection tuples (x1, y1, x2, y2, confidence).
        frame_meta: Tuple containing (drone_lat, drone_lon, altitude).
        frame_idx: Index of the frame being processed.
        cabbage_positions: Dictionary to store cabbage positions.
        width: Width of the frame.
        height: Height of the frame.
        SENSOR_WIDTH_MM: Sensor width in mm.
        FOCAL_LENGTH_MM: Focal length in mm.
        METERS_PER_DEG_LAT: Meters per degree of latitude.
    '''
    drone_lat, drone_lon, alt = frame_meta
    gsd = (alt * SENSOR_WIDTH_MM) / (FOCAL_LENGTH_MM * width)

    for x1, y1, x2, y2, conf in detections:
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        dx_px = cx - width / 2
        dy_px = cy - height / 2
        dx_m = dx_px * gsd
        dy_m = -dy_px * gsd
        dlat = dy_m / METERS_PER_DEG_LAT
        dlon = dx_m / (METERS_PER_DEG_LAT * math.cos(math.radians(drone_lat)))
        cab_lat = drone_lat + dlat
        cab_lon = drone_lon + dlon

        key = (round(cab_lat, 7), round(cab_lon, 7))
        cabbage_positions[key].append((conf, frame_idx))
        
    return cabbage_positions
