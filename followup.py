# routes/followup.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from services.intent import get_intent
from services.tts_services import synthesize_response

router = APIRouter()

class FollowUpInput(BaseModel):
    text: str

@router.post("/followup")
async def followup(input: FollowUpInput):
    user_text = input.text

    if not user_text:
        raise HTTPException(status_code=400, detail="Input text is empty")

    intent = get_intent(user_text)

    # Custom responses based on intent
    if intent == "positive":
        response_text = "I'm really glad to hear that. Is there anything else I can help you with?"
    elif intent == "negative":
        response_text = "I'm sorry to hear that. Let me connect you to a human representative."
    else:
        response_text = "Thanks for your response. Could you please tell me more?"

    # Convert response to speech using TTS
    try:
        audio_path = synthesize_response(response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")

    return {
        "intent": intent,
        "response_text": response_text,
        "audio_url": audio_path  # This path should be accessible from frontend or Twilio
    }
