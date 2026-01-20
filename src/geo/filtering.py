import math
from collections import defaultdict

def filter_positions(
    cabbage_positions: defaultdict,
    GRID_SIZE_METERS: float = 0.5,
    METERS_PER_DEG_LAT: int = 111320,
):
    valid_positions = []
    for k in cabbage_positions.keys():
        if isinstance(k, tuple) and len(k) == 2:
            valid_positions.append(k)

    if not valid_positions:
        raise ValueError("No cabbages detected.")

    center_lat = sum(lat for lat, _ in valid_positions) / len(valid_positions)
    METERS_PER_DEG_LON = METERS_PER_DEG_LAT * math.cos(math.radians(center_lat))

    def grid_hash(lat, lon):
        gx = int(lon * METERS_PER_DEG_LON / GRID_SIZE_METERS)
        gy = int(lat * METERS_PER_DEG_LAT / GRID_SIZE_METERS)
        return gx, gy

    occupied = set()
    filtered = defaultdict(list)

    for lat, lon in valid_positions:
        cell = grid_hash(lat, lon)
        if cell not in occupied:
            filtered[(lat, lon)] = cabbage_positions[(lat, lon)]
            occupied.add(cell)

    print(f"Original unique positions: {len(valid_positions)}")
    print(f"Filtered positions: {len(filtered)}")
    return filtered
