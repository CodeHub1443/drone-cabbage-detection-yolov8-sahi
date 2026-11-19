@echo off
title Cabbage Detector Backend

cd /d %~dp0

call venv\Scripts\activate

echo ====================================
echo Starting Cabbage Detector Backend...
echo ====================================

python -m uvicorn api.app:app --host 127.0.0.1 --port 8000
