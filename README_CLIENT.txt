========================================
CABBAGE DETECTOR — CLIENT USER GUIDE
========================================

This software runs fully on your local computer.
No internet, no cloud, no uploads.

----------------------------------------
SYSTEM REQUIREMENTS (MANDATORY)
----------------------------------------

1. NVIDIA GPU (RTX series recommended)
2. Windows 10 / 11 (64-bit)

You MUST have the following installed BEFORE running the app:

✔ NVIDIA Driver (latest recommended)
✔ CUDA Toolkit 12.1
✔ TensorRT 10.x (tested on 10.12)
✔ Microsoft Visual C++ Redistributable (x64)

⚠ These are system-level GPU dependencies and are NOT bundled.

----------------------------------------
WHAT IS INCLUDED
----------------------------------------

✔ Fully configured Python environment (venv)
✔ Optimized AI pipeline
✔ Web-based user interface
✔ Automatic TensorRT engine generation
✔ Local inference (no cloud cost)

----------------------------------------
FIRST-TIME SETUP (ONE TIME ONLY)
----------------------------------------

STEP 1 — Check system compatibility  
Double-click:

    check_environment.bat

If all checks pass → continue  
If any ❌ appears → contact support

STEP 2 — Generate GPU-optimized engine  
Double-click:

    run_engine_setup.bat

⏳ This may take several minutes  
✔ This step is required ONCE per GPU

----------------------------------------
RUNNING THE APPLICATION
----------------------------------------

Every time you want to use the software:

Double-click:

    start_app.bat

Your browser will open automatically.

----------------------------------------
HOW TO USE
----------------------------------------

1. Open the web interface
2. Upload:
   - MP4 video file
   - Matching SRT subtitle file (same name)
3. Click “Run Inference”
4. Wait for processing to complete
5. Download or view results

----------------------------------------
IMPORTANT NOTES
----------------------------------------

• TensorRT engine is GPU-specific
• If GPU or driver changes → rerun engine setup
• Do NOT delete the venv folder
• Do NOT move files inside the project

----------------------------------------
TESTED ENVIRONMENT
----------------------------------------

CUDA        : 12.1
TensorRT   : 10.12
Torch      : 2.5.1 + cu121
Ultralytics: 8.4.x
GPU        : NVIDIA RTX 30/40 series

----------------------------------------
SUPPORT
----------------------------------------

If setup fails:
✔ Take a screenshot
✔ Send error message + GPU model
✔ Contact the developer

========================================
END OF DOCUMENT
========================================
