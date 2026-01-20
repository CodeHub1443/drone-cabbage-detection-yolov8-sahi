from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os, shutil

from main import main as run_pipeline
from config import Config


print(">>> api.app LOADED <<<")

app = FastAPI()

# ===================== CORS CONFIG =====================
# Allow frontend dev servers to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== STATIC OUTPUTS =====================
# Serve generated videos + maps
app.mount("/outputs", StaticFiles(directory=".", html=True), name="outputs")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===================== ROUTES =====================

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
def upload_video(file: UploadFile = File(...)):
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.post("/run")
def run_inference(filename: str):
    # Bind uploaded file to pipeline config
    cfg = Config()
    cfg.VIDEO_PATH = f"uploads/{filename}"

    # Execute real pipeline and return structured JSON
    result = run_pipeline(cfg=cfg, return_results=True)
    return result
