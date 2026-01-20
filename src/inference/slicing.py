import numpy as np

def slice_frame(
    frame: np.ndarray,
    slice_size: int = 640,
    overlap: float = 0.2
) -> tuple[list[np.ndarray], list[tuple[int, int, int, int]]]:
    """
    Slice frame into fixed-size tiles (slice_size x slice_size).
    Edge tiles are ZERO-PADDED to guarantee uniform shape.
    """

    assert frame.ndim == 3, "Frame must be HxWxC"
    H, W, C = frame.shape
    stride = int(slice_size * (1 - overlap))

    slices = []
    coords = []

    for y in range(0, H, stride):
        for x in range(0, W, stride):
            x2 = min(x + slice_size, W)
            y2 = min(y + slice_size, H)

            tile = frame[y:y2, x:x2]

            # ---- PAD EDGE TILES ----
            if tile.shape[0] != slice_size or tile.shape[1] != slice_size:
                padded = np.zeros((slice_size, slice_size, C), dtype=frame.dtype)
                padded[: tile.shape[0], : tile.shape[1]] = tile
                tile = padded

            slices.append(tile)
            coords.append((x, y, tile.shape[1], tile.shape[0]))

    return slices, coords
