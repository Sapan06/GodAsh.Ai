# services/seamless.py

from utils.stt import transcribe_audio
from utils.tts_service import synthesize_speech

def speech_to_text(recording_url: str) -> str:
    return transcribe_audio(recording_url)

def text_to_speech(text: str) -> str:
    return synthesize_speech(text)
