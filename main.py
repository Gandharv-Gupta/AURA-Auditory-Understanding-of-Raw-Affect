from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import asyncio
import json
from utils import (
    generate_filename,
    get_audio_emotions,
    log_to_csv
)
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/download-logs")
async def download_logs():
    return FileResponse("logs.csv", media_type='text/csv', filename="logs.csv")


@app.post("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    name: str = Form(...),
    user_emotion: str = Form(...),
    audio: UploadFile = File(...)
):
    try:
        # Generate filename and save audio locally
        filename = generate_filename(name)
        path = f"Screams/{filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # Analyze emotion
        top3 = await get_audio_emotions(filename)

        if not top3:
            # Hume could not predict emotions
            print(f"Warning: Hume API returned no predictions for {filename}")
            return templates.TemplateResponse("index.html", {
                "request": request,
                "scream_failed": True,
                "name": name,
                "user_emotion": user_emotion,
                "results": {},
                "results_json": json.dumps({}),
                "audio_file": path
            })

        # Log locally
        log_to_csv(name, user_emotion, top3, filename)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "name": name,
            "user_emotion": user_emotion,
            "results": top3,
            "results_json": json.dumps(top3),
            "audio_file": path
        })

    except Exception as e:
        print(f"Error processing audio: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })
