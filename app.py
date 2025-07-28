import os
import asyncio
import logging
from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv

from utils.intent import get_intent  # Implement this
from services.seamless import speech_to_text  # Implement this

from routes.process_recording import process_router
from routes.respond_call import respond_router

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Voice Agent App")
app.include_router(process_router)
app.include_router(respond_router)

# Setup logging
logging.basicConfig(level=logging.INFO)

# ✅ Twilio Caller Class
class VoiceAgent:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)

    def call_user(self, to_number: str):
        call = self.client.calls.create(
            to=to_number,
            from_=self.twilio_number,
            url=f"{os.getenv('NGROK_URL')}/voice"
        )
        logging.info(f"✅ Call initiated: {call.sid}")
        return call.sid

# ✅ When Twilio starts the call
@app.post("/voice")
async def voice():
    response = VoiceResponse()
    response.say("Hi! We noticed you recently placed an order. Were you happy with the delivery?", voice='alice')
    response.record(
        timeout=5,
        transcribe=False,
        max_length=5,
        play_beep=True,
        action=f"{os.getenv('NGROK_URL')}/gather"
    )
    return Response(content=str(response), media_type="application/xml")

# ✅ After recording, Twilio posts to this endpoint
@app.post("/gather")
async def gather(request: Request):
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    
    if not recording_url:
        return Response(content="No RecordingUrl", media_type="text/xml")

    # Forward to /process-audio
    async with httpx.AsyncClient() as client:
        audio_response = await client.post("http://localhost:8000/process-audio/", data={"url": recording_url})

    # Get transcript
    text = audio_response.json().get("transcript", "")

    # Forward to /followup
    async with httpx.AsyncClient() as client:
        followup_response = await client.post("http://localhost:8000/followup", json={"text": text})

    result = followup_response.json()
    audio_url = result.get("audio_url")

    # Respond to Twilio with TTS audio playback
    twiml_response = f"""
    <Response>
        <Play>{audio_url}</Play>
    </Response>
    """
    return Response(content=twiml_response, media_type="text/xml")

# ✅ Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
