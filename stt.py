import whisper
import tempfile
import requests
import os
import logging

model = whisper.load_model("base")  # or "small", "medium", "large"

def transcribe_audio(recording_url: str) -> str:
    logging.info(f"Downloading audio from: {recording_url}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        response = requests.get(recording_url)
        tmp_file.write(response.content)
        tmp_path = tmp_file.name
    
    logging.info("Audio downloaded. Starting transcription...")
    
    result = model.transcribe(tmp_path)
    
    logging.info(f"Transcription result: {result['text']}")
    
    os.remove(tmp_path)
    return result["text"]
