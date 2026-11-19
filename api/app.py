from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from main import run_pipeline  # your existing pipeline entry

# -----------------------
# Paths
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
STATIC_DIR = BASE_DIR / "static"
FRONTEND_DIR = BASE_DIR / "frontend_dist"
ASSETS_DIR = FRONTEND_DIR / "assets"

UPLOAD_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# -----------------------
# App
# -----------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Static files & Outputs
# -----------------------
# Serve generated videos + maps from the project root
app.mount("/outputs", StaticFiles(directory=BASE_DIR, html=True), name="outputs")

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# -----------------------
# Health
# -----------------------
@app.post("/health")
def health():
    return {"status": "ok"}

# -----------------------
# Upload (STRICT: MP4 + SRT required)
# -----------------------
@app.post("/upload")
async def upload_files(
    video: UploadFile = File(...),
    srt: UploadFile = File(...)
):
    if not video.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Video must be .mp4")

    if not srt.filename.lower().endswith(".srt"):
        raise HTTPException(status_code=400, detail="SRT must be .srt")

    # Save video with original name
    video_path = UPLOAD_DIR / video.filename
    with open(video_path, "wb") as f:
        f.write(await video.read())

    # Save SRT with original name
    srt_path = UPLOAD_DIR / srt.filename
    with open(srt_path, "wb") as f:
        f.write(await srt.read())

    # SAVE SIDECAR MAPPING (Critical for mismatched filenames)
    # We save a file like "video.mp4.srt_name" containing "geographical_data.srt"
    sidecar_path = UPLOAD_DIR / f"{video.filename}.srt_name"
    with open(sidecar_path, "w", encoding="utf-8") as f:
        f.write(srt.filename)

    # Return structure expected by frontend
    return {"filename": video.filename}

# -----------------------
# Run inference (Mandatory Video + SRT via Sidecar)
# -----------------------
@app.post("/run")
def run_inference(filename: str):
    video_path = UPLOAD_DIR / filename
    sidecar_path = UPLOAD_DIR / f"{filename}.srt_name"

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Uploaded video not found")

    if not sidecar_path.exists():
        raise HTTPException(
            status_code=400, 
            detail="Mandatory SRT metadata missing for this video. Please re-upload both."
        )

    # Read the original SRT filename from the sidecar
    with open(sidecar_path, "r", encoding="utf-8") as f:
        srt_filename = f.read().strip()
    
    srt_path = UPLOAD_DIR / srt_filename
    if not srt_path.exists():
        raise HTTPException(status_code=404, detail=f"Linked SRT file '{srt_filename}' not found")

    return run_pipeline(filename, srt_filename)

# -----------------------
# Frontend SPA
# -----------------------
@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/{path:path}")
def spa_fallback(path: str):
    return FileResponse(FRONTEND_DIR / "index.html")
