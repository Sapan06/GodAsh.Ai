

# 🔊 AI-Powered Voice Calling Agent (Meta Seamless + Twilio)

An **AI-driven voice calling system** built using **FastAPI**, **Meta's Seamless Communication Stack (STT/TTS)**, and **Twilio** for telephony.  
The agent can autonomously call users, converse naturally, understand their responses, and reply intelligently.

---

## 🚀 Features
✅ Make and receive calls using **Twilio**  
✅ **Meta SeamlessM4T** for speech-to-text (STT) and text-to-speech (TTS)  
✅ 2–3 turn **conversational agent loop**  
✅ Intent detection via AI (LLM / NLP-based)  
✅ Logs transcripts and responses for debugging  
✅ FastAPI backend with modular routes and services  

---

## 📂 Project Structure

```
TWILIO/
│
├── app.py                    # Main FastAPI app entrypoint
├── make_call.py              # Script to initiate outbound calls
├── twilio_response.py        # Twilio call response handler
├── voice_agent.log           # Log file for calls and transcripts
│
├── routes/                   # API route handlers
│   ├── followup.py           # Handles follow-up voice interaction
│   ├── process_recording.py  # Download and process Twilio recordings
│   └── respond_call.py       # Responds to Twilio call (AI logic loop)
│
├── services/                 # Core AI/Audio services
│   ├── seamless.py           # Meta Seamless (STT/TTS) integration
│   ├── audio_converter.py    # Convert audio formats for STT/TTS
│
├── utils/                    # Helper functions
│   ├── intent.py             # Intent detection (positive/negative/neutral)
│   ├── stt.py                # Speech-to-text helpers
│   ├── tts_service.py        # Text-to-speech helpers
│   └── twilio_helpers.py     # Twilio-specific utilities
│
├── process_rendering.py      # Optional endpoint testing
├── test_seamless_download.py # Standalone Seamless testing
├── .env                      # Environment variables
├── .gitignore
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repo
```bash
git clone https://github.com/<your-username>/twilio-voice-agent.git
cd twilio-voice-agent
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv .env
source .env/bin/activate      # Mac/Linux
.env\Scripts\activate       # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add `.env` File
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1234567890

META_SEAMLESS_MODEL=seamless_m4t

```

---

## ▶️ Running the Application

### Start FastAPI server:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔌 Public URL via Ngrok
Expose your backend for Twilio:
```bash
ngrok http 8000
```
Copy your ngrok HTTPS URL.

---

## 📞 Twilio Configuration
1. Go to Twilio Console → **Phone Numbers → Active Number**
2. Under **Voice & Fax Webhook**, set:
   - **Webhook URL (POST)** → `https://<ngrok-url>/voice`
3. Save configuration.

---

## 🧠 AI Agent Flow
1️⃣ **Bot calls user** (or receives inbound call)  
2️⃣ **Bot** (Seamless TTS): "Hi! Were you happy with your recent delivery?"  
3️⃣ **User responds**  
4️⃣ **Seamless STT** transcribes speech → text  
5️⃣ **Intent detected** (positive/negative/neutral) via LLM  
6️⃣ **Bot replies** with natural voice  
7️⃣ Call ends after 2–3 turns.

---

## 🧪 Testing
- **Outbound Call**: Run `make_call.py` to trigger a test call:
```bash
python make_call.py
```
- **Inbound Call**: Dial your Twilio number (webhook must be set to `/voice`).

---

## 🧠 Bonus Features
- Multilingual support using Seamless translation  
- Conversation loop using follow-up route  
- Logging transcripts in `voice_agent.log`  

---

## 📜 Logs & Debugging
- All logs stored in `voice_agent.log`
- Twilio debugging via [Twilio Console Logs](https://console.twilio.com/)

---


