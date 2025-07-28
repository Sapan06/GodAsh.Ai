import requests
import uuid
from pydub import AudioSegment

def download_audio(url: str) -> str:
    local_filename = f"downloads/{uuid.uuid4()}.mp3"
    with requests.get(f"{url}.mp3", stream=True) as r:
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def convert_to_wav(input_path: str) -> str:
    audio = AudioSegment.from_file(input_path)
    output_path = input_path.replace(".mp3", ".wav")
    audio.export(output_path, format="wav")
    return output_path
