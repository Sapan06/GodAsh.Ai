# process_recording.py

import os
import requests
from fastapi import APIRouter, Request, Form
from fastapi.responses import Response
from pydub import AudioSegment

from services.tts_service import text_to_speech
from services.stt_service import transcribe_audio
from services.intent_service import analyze_intent
from utils.twiml import build_twiml_response

router = APIRouter()

@router.post("/process-recording")
async def process_recording(
    request: Request,
    RecordingUrl: str = Form(...),
    RecordingSid: str = Form(...)
):
    print(f"[INFO] Received recording from: {RecordingUrl}")

    # Step 1: Download recording
    audio_url = RecordingUrl + ".mp3"
    audio_path = f"downloads/{RecordingSid}.mp3"
    wav_path = f"downloads/{RecordingSid}.wav"

    os.makedirs("downloads", exist_ok=True)
    response = requests.get(audio_url)

    with open(audio_path, "wb") as f:
        f.write(response.content)

    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(audio_path)
    audio.export(wav_path, format="wav")

    # Step 2: Transcribe
    transcript = transcribe_audio(wav_path)
    print(f"[TRANSCRIPT]: {transcript}")

    # Step 3: Analyze intent
    bot_reply = analyze_intent(transcript)
    print(f"[BOT REPLY]: {bot_reply}")

    # Step 4: Generate TTS
    tts_path = f"downloads/{RecordingSid}_reply.wav"
    text_to_speech(bot_reply, tts_path)

    # Step 5: Respond with TwiML to play reply
    response_twiml = build_twiml_response(tts_path)
    return Response(content=response_twiml, media_type="application/xml")
