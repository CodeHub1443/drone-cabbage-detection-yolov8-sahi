# Drone Cabbage Detection & Localization (Back-end)

A high-precision computer vision API built with **FastAPI**, **YOLOv8**, and **SAHI (Slicing Aided Hyper Inference)**. This system is designed to detect and geolocate cabbage crops from high-altitude drone imagery.

## 🌟 Key Features
- **Tiled Inference:** Uses SAHI to detect small objects (cabbages) in high-resolution 4K drone frames.
- **Geospatial Projection:** Converts pixel coordinates from the video into real-world geographic coordinates using camera telemetry.
- **FastAPI Integration:** Robust REST API to communicate with the Front-end dashboard.
- **TensorRT Support:** Includes scripts to convert models to TensorRT for edge-device acceleration.

## 🛠️ Tech Stack
- **Framework:** FastAPI
- **Inference:** Ultralytics YOLOv8, SAHI
- **Data Processing:** OpenCV, NumPy, Pandas
- **Environment:** Conda / Python 3.10+

## 💻 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/CodeHub1443/drone-cabbage-detection-yolov8-sahi.git
cd drone-cabbage-detection-yolov8-sahi
```

### 2. Create an environment and install dependencies
```bash
python -m venv venv
venv\Scriptsctivate            # Windows (Linux/macOS: source venv/bin/activate)
pip install -r requirements.lock.txt
```
Install a CUDA build of PyTorch if you have an NVIDIA GPU; without one the API falls back to CPU (very slow on 4K video).

### 3. Run the API
```bash
python -m uvicorn api.app:app --host 127.0.0.1 --port 8000
```
Check it with `http://127.0.0.1:8000/health`. If `best.engine` (TensorRT) is not present, the API uses `best.pt`.

### 4. Run the dashboard
Clone and start the front-end: https://github.com/CodeHub1443/Agro-insights-dashboard (it talks to `http://127.0.0.1:8000` by default).

## 🔌 API
- `POST /upload` — multipart form with `video` (.mp4) and `srt` (.srt). Returns `{ "video": "<name>", "srt": "<name>" }`.
- `POST /run?video_filename=<name>&srt_filename=<name>` — runs detection and returns `{ "total_cabbages", "video", "map" }`. Outputs are served under `/outputs/`.
