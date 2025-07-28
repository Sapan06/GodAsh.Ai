# routes/respond_call.py

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from services.seamless import speech_to_text
from utils.intent import get_intent
import logging

respond_router = APIRouter()

@respond_router.post("/gather", response_class=PlainTextResponse)
async def gather(request: Request):
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    logging.info(f"Received recording: {recording_url}")

    transcription = speech_to_text(recording_url)
    intent = get_intent(transcription)

    if intent == "positive":
        response_text = "That's great to hear! Thank you for your feedback."
    elif intent == "negative":
        response_text = "We're sorry to hear that. We'll work on improving."
    else:
        response_text = "Thanks for your response. Have a great day!"

    # TwiML response for Twilio
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{response_text}</Say>
</Response>"""

@respond_router.post("/followup", response_class=PlainTextResponse)
async def followup(request: Request):
    try:
        form = await request.form()
        recording_url = form.get("RecordingUrl")

        if not recording_url:
            return """<?xml version="1.0" encoding="UTF-8"?><Response><Say>We couldn't hear you. Goodbye!</Say></Response>"""

        transcription = speech_to_text(recording_url)
        logging.info(f"[Follow-up] Transcribed: {transcription}")

        # You could analyze further here...
        followup_intent = get_intent(transcription)
        logging.info(f"[Follow-up] Intent: {followup_intent}")

        response_text = "Thanks for sharing! We'll use your feedback to improve."

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{response_text}</Say>
    <Hangup/>
</Response>"""

    except Exception as e:
        logging.exception("Error in /followup")
        return """<?xml version="1.0" encoding="UTF-8"?><Response><Say>Something went wrong. Goodbye!</Say></Response>"""
