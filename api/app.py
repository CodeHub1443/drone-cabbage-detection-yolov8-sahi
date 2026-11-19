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

# The bundled frontend is optional (frontend_dist/ is not tracked in git).
if ASSETS_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# -----------------------
# Health
# -----------------------
@app.api_route("/health", methods=["GET", "POST"])
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
    # Strip any directory components to prevent path traversal
    video_name = Path(video.filename or "").name
    srt_name = Path(srt.filename or "").name

    if not video_name.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Video must be .mp4")

    if not srt_name.lower().endswith(".srt"):
        raise HTTPException(status_code=400, detail="SRT must be .srt")

    with open(UPLOAD_DIR / video_name, "wb") as f:
        f.write(await video.read())

    with open(UPLOAD_DIR / srt_name, "wb") as f:
        f.write(await srt.read())

    # Response shape expected by the frontend (src/lib/api.ts)
    return {"video": video_name, "srt": srt_name}

# -----------------------
# Run inference (video + SRT filenames from /upload)
# -----------------------
@app.post("/run")
def run_inference(video_filename: str, srt_filename: str):
    video_name = Path(video_filename).name
    srt_name = Path(srt_filename).name

    if not (UPLOAD_DIR / video_name).exists():
        raise HTTPException(status_code=404, detail=f"Uploaded video '{video_name}' not found")

    if not (UPLOAD_DIR / srt_name).exists():
        raise HTTPException(status_code=404, detail=f"Uploaded SRT '{srt_name}' not found")

    return run_pipeline(video_name, srt_name)

# -----------------------
# Frontend SPA
# -----------------------
def _spa_index():
    index_file = FRONTEND_DIR / "index.html"
    if not index_file.exists():
        return {"status": "ok", "detail": "API running. Frontend not bundled; run the dashboard separately."}
    return FileResponse(index_file)

@app.get("/")
def index():
    return _spa_index()

@app.get("/{path:path}")
def spa_fallback(path: str):
    return _spa_index()
