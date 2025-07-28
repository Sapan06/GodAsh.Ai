from fastapi import APIRouter, Request, Form
from fastapi.responses import Response
import requests
import os
from utils.audio_converter import convert_to_wav
from services.seamless_stt import transcribe_audio
from services.intent_analyzer import analyze_intent
from services.seamless_tts import generate_tts_audio
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/process-recording")
async def process_recording(
    RecordingUrl: str = Form(...),
    RecordingSid: str = Form(...),
    CallSid: str = Form(...),
    From: str = Form(...),
    To: str = Form(...)
):
    print(f"🔄 Received recording from: {RecordingUrl}")

    # 1. Download the audio from Twilio
    audio_url = RecordingUrl + ".mp3"
    audio_response = requests.get(audio_url)
    input_path = f"temp/{RecordingSid}.mp3"
    os.makedirs("temp", exist_ok=True)
    with open(input_path, "wb") as f:
        f.write(audio_response.content)

    # 2. Convert to WAV if needed
    wav_path = convert_to_wav(input_path)

    # 3. Transcribe with SeamlessM4T
    transcript = transcribe_audio(wav_path)
    print(f"📄 Transcript: {transcript}")

    # 4. Analyze intent (your own logic)
    reply_text = analyze_intent(transcript)
    print(f"🤖 Bot Reply: {reply_text}")

    # 5. TTS the reply using SeamlessM4T
    tts_output_path = generate_tts_audio(reply_text, output_name=RecordingSid)

    # 6. Return TwiML to play the TTS response
    twiml = f"""
    <Response>
        <Play>{os.getenv('NGROK_URL')}/static/{os.path.basename(tts_output_path)}</Play>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")
