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
git clone [https://github.com/CodeHub1443/drone-cabbage-detection-yolov8-sahi.git](https://github.com/CodeHub1443/drone-cabbage-detection-yolov8-sahi.git)
cd drone-cabbage-detection-yolov8-sahi