from gtts import gTTS
import tempfile
import os

def synthesize_speech(text: str) -> str:
    tts = gTTS(text)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(temp_path)
    # In real apps, you'd upload this somewhere and return the URL
    return f"/static/audio/{os.path.basename(temp_path)}"
