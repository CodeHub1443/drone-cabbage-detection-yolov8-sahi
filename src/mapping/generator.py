import folium
from folium.plugins import FastMarkerCluster
import re


GOOGLE_TILES = {
    "tiles": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    "attr": "Google",
    "max_zoom": 23,
}


def _create_base_map(center_lat, center_lon, zoom=21):
    return folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        **GOOGLE_TILES
    )


def create_cluster_map(cabbage_positions, MAP_OUTPUT_PATH: str):
    """
    Cluster map. Always creates a map.
    """
    if cabbage_positions:
        lats = [k[0] for k in cabbage_positions]
        lons = [k[1] for k in cabbage_positions]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
    else:
        # fallback base map (no detections)
        center_lat, center_lon = 0.0, 0.0

    m = _create_base_map(center_lat, center_lon)

    if cabbage_positions:
        marker_data = []
        for i, ((cab_lat, cab_lon), records) in enumerate(cabbage_positions.items()):
            max_conf = max(conf for conf, _ in records)
            frames_seen = sorted(set(frame for _, frame in records))
            popup_text = (
                f"<b>Cabbage</b><br>"
                f"Max Conf: {max_conf:.2f}<br>"
                f"Seen in {len(frames_seen)} frames<br>"
                f"First: {frames_seen[0]}, Last: {frames_seen[-1]}"
            )
            marker_data.append([cab_lat, cab_lon, popup_text])

        callback = """(
            function(row) {
                var marker = L.circleMarker(new L.LatLng(row[0], row[1]), {
                    radius: 1.5,
                    color: '#ff0000',
                    weight: 1,
                    fillColor: '#ff3333',
                    fillOpacity: 0.9
                });
                marker.bindPopup(row[2]);
                return marker;
            }
        )"""
        FastMarkerCluster(marker_data, callback=callback).add_to(m)

    m.save(MAP_OUTPUT_PATH)
    _minify_html(MAP_OUTPUT_PATH)
    print(f"Map saved: {MAP_OUTPUT_PATH}")
    print(f"Total unique cabbages mapped: {len(cabbage_positions)}")


def create_map(cabbage_positions, MAP_OUTPUT_PATH: str):
    """
    Individual marker map. Always creates a map.
    """
    if cabbage_positions:
        lats = [k[0] for k in cabbage_positions]
        lons = [k[1] for k in cabbage_positions]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
    else:
        center_lat, center_lon = 0.0, 0.0

    m = _create_base_map(center_lat, center_lon)

    if cabbage_positions:
        for ((cab_lat, cab_lon), records) in cabbage_positions.items():
            max_conf = max(conf for conf, _ in records)
            frames_seen = sorted(set(frame for _, frame in records))
            popup_text = (
                f"<b>Cabbage</b><br>"
                f"Max Conf: {max_conf:.2f}<br>"
                f"Seen in {len(frames_seen)} frames<br>"
                f"First: {frames_seen[0]}, Last: {frames_seen[-1]}"
            )
            folium.CircleMarker(
                location=[cab_lat, cab_lon],
                radius=1.5,
                color="#ff0000",
                weight=1,
                fill=True,
                fill_color="#ff3333",
                fill_opacity=0.9,
                popup=folium.Popup(popup_text, max_width=300),
            ).add_to(m)

    m.save(MAP_OUTPUT_PATH)
    print(f"Map saved: {MAP_OUTPUT_PATH}")
    print(f"Total unique cabbages mapped: {len(cabbage_positions)}")


def _minify_html(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        html = re.sub(r"([0-9a-f]{8})[0-9a-f-]{12,}", r"\1", html)
        lines = [line.rstrip() for line in html.split("\n")]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except Exception:
        pass
