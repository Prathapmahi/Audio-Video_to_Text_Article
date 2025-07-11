import os
import time
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

if not ASSEMBLYAI_API_KEY:
    raise ValueError("❌ ASSEMBLYAI_API_KEY not set in .env")

# AssemblyAI API endpoints
UPLOAD_URL = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"

headers = {
    "authorization": ASSEMBLYAI_API_KEY
}

def upload_file(filepath_or_url: str) -> str:
    """Uploads a local file or remote URL to AssemblyAI"""
    if filepath_or_url.startswith("http"):
        print(f"[INFO] Downloading audio from URL: {filepath_or_url}")
        response = requests.get(filepath_or_url, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download: {response.status_code}")
        print("[INFO] Uploading to AssemblyAI...")
        upload_response = requests.post(UPLOAD_URL, headers=headers, data=response.raw)
    else:
        print(f"[INFO] Uploading local file: {filepath_or_url}")
        def read_file(filename, chunk_size=5242880):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data
        upload_response = requests.post(UPLOAD_URL, headers=headers, data=read_file(filepath_or_url))

    if upload_response.status_code != 200:
        raise Exception(f"Upload failed: {upload_response.text}")
    
    return upload_response.json()['upload_url']

def transcribe_audio(filepath_or_url: str) -> str:
    """Transcribes audio from a local file or URL using AssemblyAI"""
    upload_url = upload_file(filepath_or_url)

    print("[INFO] Requesting transcription...")
    transcript_request = {
        "audio_url": upload_url,
        "auto_chapters": False,
        "speaker_labels": False,
        "punctuate": True,
        "format_text": True
    }

    response = requests.post(TRANSCRIPT_URL, json=transcript_request, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Transcription request failed: {response.text}")

    transcript_id = response.json()['id']
    polling_endpoint = f"{TRANSCRIPT_URL}/{transcript_id}"

    print("[INFO] Polling for completion...")
    while True:
        polling_response = requests.get(polling_endpoint, headers=headers)
        status = polling_response.json()['status']

        if status == 'completed':
            text = polling_response.json().get('text', '')
            print(f"✅ Transcription complete. Length: {len(text)} characters")
            return text.strip()
        elif status == 'error':
            raise Exception(f"Transcription failed: {polling_response.json().get('error')}")
        else:
            time.sleep(3)
