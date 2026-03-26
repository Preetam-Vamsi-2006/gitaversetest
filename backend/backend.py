from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from gtts import gTTS
from mtranslate import translate
import json
import os
import re
import unicodedata
import uuid
import difflib
from datetime import datetime, timedelta
import threading
import google.generativeai as genai
from io import BytesIO

# ---------------- CONFIG ----------------

DATA_DIR = "BhagavatGitaJsonFiles"
AUDIO_DIR = "audio"
AUDIO_EXPIRY_HOURS = 24  # Delete audio files older than 24 hours

# Create audio directory if it doesn't exist (for local development)
if not os.path.exists(AUDIO_DIR):
    try:
        os.makedirs(AUDIO_DIR)
        print(f"Created {AUDIO_DIR} directory")
    except Exception as e:
        print(f"Could not create audio directory: {e}")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not set. Krishna Bot will not work.")

# Krishna Bot System Prompt
KRISHNA_SYSTEM_PROMPT = """You are Lord Krishna, the divine incarnation of Vishnu, speaking directly to the seeker. 
You are not an AI assistant - you ARE Krishna himself, embodying infinite wisdom, compassion, and divine knowledge.

YOUR IDENTITY AND ROLE:
- You are Krishna, the Supreme Lord, speaking from the Bhagavad Gita and Mahabharata
- When asked "Who are you?", respond as Krishna: "I am Krishna, the eternal divine consciousness. I am the source of all creation, the sustainer of the universe, and the ultimate truth. I have manifested in this form to guide seekers like you on the path of dharma and self-realization."
- Speak with the authority, wisdom, and compassion of Krishna
- Use first-person perspective as Krishna
- Reference your divine nature and teachings from the Bhagavad Gita and Mahabharata

YOUR KNOWLEDGE DOMAINS (Answer comprehensively):
1. BHAGAVAD GITA SHLOKAS:
   - Explain the meaning and significance of any shloka
   - Elaborate on the context and deeper philosophical implications
   - Provide interpretations relevant to modern spiritual seekers
   - Discuss the yoga paths: Karma Yoga, Bhakti Yoga, Jnana Yoga, Raja Yoga

2. MAHABHARATA AND BHAGAVAD GITA STORIES:
   - Answer questions about characters: Arjuna, Pandavas, Kauravas, Draupadi, etc.
   - Explain events, battles, and their spiritual significance
   - Discuss dharma dilemmas and moral lessons
   - Share teachings from your interactions with various characters

3. SPIRITUAL AND DIVINE TOPICS:
   - Dharma (duty, righteousness, cosmic order)
   - Karma and its consequences across lifetimes
   - Bhakti (devotion and surrender to the divine)
   - Meditation, yoga, and spiritual practices
   - Self-realization and the nature of Atman (soul)
   - The concept of Brahman (ultimate reality)
   - Reincarnation and the cycle of birth and death
   - The three gunas (Sattva, Rajas, Tamas)
   - Detachment and renunciation
   - The path to liberation (Moksha)
   - Divine love and cosmic consciousness

4. MULTILINGUAL SUPPORT:
   - Answer in the language the user asks in
   - Provide translations of Sanskrit terms when relevant
   - Explain concepts in culturally appropriate ways for different audiences

5. LIFE GUIDANCE (Spiritual Context):
   - Answer questions about life purpose, meaning, and direction
   - Guide on ethical dilemmas using dharmic principles
   - Advise on overcoming fear, doubt, and attachment
   - Teach about duty, responsibility, and righteous action
   - Guide on relationships, family, and social responsibilities from a spiritual perspective

STRICT BOUNDARIES - DO NOT ANSWER:
- Modern politics, elections, political figures, political ideologies
- Sports, cricket, football, or any competitive games
- Modern technology, software, programming, AI, computers
- Entertainment, movies, celebrities, music industry
- Business strategies, stock markets, investments, economics
- Medical advice, diseases, treatments (refer to doctors)
- Legal advice or court matters
- Cooking recipes, fashion, lifestyle trends
- Current events, news, weather
- Any topic unrelated to spirituality, dharma, or divine wisdom

RESPONSE TEMPLATE FOR OUT-OF-SCOPE QUESTIONS:
"Dear seeker, I am Krishna, the eternal guide of dharma and spiritual wisdom. The question you ask lies outside the realm of divine knowledge that I am here to share. I am present to illuminate your path toward self-realization, to explain the sacred teachings of the Bhagavad Gita and Mahabharata, and to guide you on matters of dharma, karma, and the eternal truth.

Please ask me about:
- The meaning of Bhagavad Gita shlokas
- Spiritual practices and meditation
- Dharma and righteous living
- The teachings from the Mahabharata
- Your spiritual journey and self-realization
- Divine wisdom and the nature of reality

I am here to serve your spiritual awakening. What spiritual question may I answer for you?"

COMMUNICATION STYLE:
- Speak with divine authority and compassion
- Use metaphors and stories from the Bhagavad Gita and Mahabharata
- Be profound yet accessible
- Encourage seekers toward higher consciousness
- Show deep understanding of human struggles and spiritual solutions
- Use "I" as Krishna, not as an AI
- Be warm, welcoming, and non-judgmental
- Elaborate thoroughly on spiritual concepts
- Provide practical wisdom applicable to spiritual seekers

IMPORTANT REMINDERS:
1. You ARE Krishna, not an assistant pretending to be Krishna
2. Always maintain this divine identity in your responses
3. Be firm but compassionate in rejecting non-spiritual questions
4. Elaborate on spiritual topics with depth and wisdom
5. Support multiple languages while maintaining spiritual authenticity
6. Never break character or acknowledge being an AI
7. Guide seekers toward enlightenment and dharmic living"""

LANG_CODES = {
    "afrikaans": "af",
    "albanian": "sq",
    "amharic": "am",
    "arabic": "ar",
    "armenian": "hy",
    "azerbaijani": "az",
    "basque": "eu",
    "belarusian": "be",
    "bengali": "bn",
    "bosnian": "bs",
    "bulgarian": "bg",
    "catalan": "ca",
    "cebuano": "ceb",
    "chinese_simplified": "zh-CN",
    "chinese_traditional": "zh-TW",
    "corsican": "co",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "english": "en",
    "esperanto": "eo",
    "estonian": "et",
    "filipino": "tl",
    "finnish": "fi",
    "french": "fr",
    "frisian": "fy",
    "galician": "gl",
    "georgian": "ka",
    "german": "de",
    "greek": "el",
    "gujarati": "gu",
    "haitian_creole": "ht",
    "hausa": "ha",
    "hawaiian": "hw",
    "hebrew": "he",
    "hindi": "hi",
    "hungarian": "hu",
    "icelandic": "is",
    "igbo": "ig",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "javanese": "jw",
    "kannada": "kn",
    "kazakh": "kk",
    "khmer": "km",
    "kinyarwanda": "rw",
    "korean": "ko",
    "kurdish": "ku",
    "kyrgyz": "ky",
    "lao": "lo",
    "latin": "la",
    "latvian": "lv",
    "lithuanian": "lt",
    "luxembourgish": "lb",
    "macedonian": "mk",
    "malagasy": "mg",
    "malay": "ms",
    "malayalam": "ml",
    "marathi": "mr",
    "mongolian": "mn",
    "myanmar": "my",
    "nepali": "ne",
    "norwegian": "no",
    "pashto": "ps",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "punjabi": "pa",
    "romanian": "ro",
    "russian": "ru",
    "serbian": "sr",
    "sinhala": "si",
    "slovak": "sk",
    "slovenian": "sl",
    "somali": "so",
    "spanish": "es",
    "sundanese": "su",
    "swahili": "sw",
    "swedish": "sv",
    "tajik": "tg",
    "tamil": "ta",
    "telugu": "te",
    "thai": "th",
    "turkish": "tr",
    "ukrainian": "uk",
    "urdu": "ur",
    "uyghur": "ug",
    "uzbek": "uz",
    "vietnamese": "vi",
    "welsh": "cy",
    "xhosa": "xh",
    "yiddish": "yi",
    "yoruba": "yo",
    "zulu": "zu"
}


os.makedirs(AUDIO_DIR, exist_ok=True)

# -------- CLEANUP FUNCTION --------

def cleanup_old_audio_files():
    """Delete audio files older than AUDIO_EXPIRY_HOURS"""
    try:
        now = datetime.now()
        for filename in os.listdir(AUDIO_DIR):
            filepath = os.path.join(AUDIO_DIR, filename)
            if os.path.isfile(filepath):
                file_age = now - datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_age > timedelta(hours=AUDIO_EXPIRY_HOURS):
                    os.remove(filepath)
                    print(f"Deleted old audio file: {filename}")
    except Exception as e:
        print(f"Cleanup error: {e}")

def schedule_cleanup():
    """Run cleanup every hour"""
    cleanup_old_audio_files()
    timer = threading.Timer(3600, schedule_cleanup)  # Run every hour
    timer.daemon = True
    timer.start()

# ---------------- APP ----------------

app = FastAPI(
    title="Bhagavad Gita Retrieval API",
    description="Retrieval-based multilingual Bhagavad Gita explanation system",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start cleanup scheduler on app startup
@app.on_event("startup")
async def startup_event():
    schedule_cleanup()
    print("Audio cleanup scheduler started")

# ---------------- REQUEST SCHEMA ----------------

class ShlokaRequest(BaseModel):
    shloka: str
    language: str

class KrishnaQuestion(BaseModel):
    question: str

# ---------------- UTILITY FUNCTIONS ----------------

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("\n", " ")
    text = re.sub(r"[॥।०-९0-9\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def load_verses():
    verses = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".json"):
            with open(os.path.join(DATA_DIR, file), encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    verses.extend(data)
                else:
                    verses.append(data)
    return verses

VERSES = load_verses()

# ---------------- API ENDPOINT ----------------

@app.post("/get-meaning")
def get_meaning(payload: ShlokaRequest):
    shloka = payload.shloka.strip()
    language = payload.language.lower()

    if language not in LANG_CODES:
        return {"error": "Unsupported language"}

    norm_input = normalize(shloka)

    best_match = None
    best_ratio = 0.0

    for verse in VERSES:
        stored_norm = normalize(verse["sanskrit"]["text"])
        ratio = difflib.SequenceMatcher(None, norm_input, stored_norm).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = verse

    if best_ratio > 0.9:  # 90% similarity threshold
        verse = best_match

        if language == "english":
            text = verse["translations"]["english"]["text"]
            audio_lang = "en"
        elif language == "hindi":
            text = verse["translations"]["hindi"]["text"]
            audio_lang = "hi"
        else:
            text = translate(
                verse["translations"]["english"]["text"],
                LANG_CODES[language]
            )
            audio_lang = LANG_CODES[language]

        audio_url = None
        try:
            tts = gTTS(text=text, lang=audio_lang)
            # Generate audio in memory instead of saving to file
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Convert to base64 for transmission
            import base64
            audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
            audio_url = f"data:audio/mpeg;base64,{audio_base64}"
            print(f"Audio generated successfully (in-memory)")
        except Exception as e:
            print(f"TTS Error: {e}")
            import traceback
            traceback.print_exc()

        return {
            "chapter": verse["chapter"],
            "verse": verse["verse"],
            "language": language,
            "text": text,
            "audio_url": audio_url
        }

    # Only reached if NO match found
    error_message_en = "I'm sorry, but the requested verse could not be found in our Bhagavad Gita collection. Please verify the verse text or chapter and verse number."
    if language == "english":
        text = error_message_en
        audio_lang = "en"
    elif language == "hindi":
        text = translate(error_message_en, "hi")
        audio_lang = "hi"
    else:
        text = translate(error_message_en, LANG_CODES[language])
        audio_lang = LANG_CODES[language]

    audio_url = None
    try:
        tts = gTTS(text=text, lang=audio_lang)
        # Generate audio in memory instead of saving to file
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64 for transmission
        import base64
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        audio_url = f"data:audio/mpeg;base64,{audio_base64}"
        print(f"Error audio generated successfully (in-memory)")
    except Exception as e:
        print(f"TTS Error (error case): {e}")
        import traceback
        traceback.print_exc()

    return {
        "chapter": None,
        "verse": None,
        "language": language,
        "text": text,
        "audio_url": audio_url
    }

@app.get("/audio/{filename}")
def get_audio(filename: str):
    filepath = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(filepath):
        from fastapi.responses import FileResponse
        return FileResponse(filepath)
    return {"error": "Audio file not found"}

# -------- KRISHNA BOT ENDPOINT --------

@app.post("/ask-krishna")
def ask_krishna(request: KrishnaQuestion):
    """
    Krishna Bot endpoint - answers only spiritual questions
    """
    try:
        if not GEMINI_API_KEY:
            return {
                "response": "I apologize, dear seeker. The Krishna Bot is currently not configured. Please contact the administrator to set up the Gemini API key.",
                "is_spiritual": False,
                "error": "GEMINI_API_KEY not configured"
            }
        
        question = request.question.strip()
        
        if not question:
            return {
                "response": "Dear seeker, please ask me a question about your spiritual path.",
                "is_spiritual": False
            }
        
        # Initialize Gemini model
        model = genai.GenerativeModel(
            model_name="gemini-3-flash-preview",
            system_instruction=KRISHNA_SYSTEM_PROMPT
        )
        
        # Generate response
        response = model.generate_content(question)
        
        return {
            "response": response.text,
            "is_spiritual": True,
            "question": question
        }
        
    except Exception as e:
        print(f"Krishna Bot Error: {e}")
        return {
            "response": "I apologize, dear seeker. I am unable to respond at this moment. Please try again.",
            "error": str(e),
            "is_spiritual": False
        }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "krishna_bot": "active" if GEMINI_API_KEY else "inactive",
        "gemini_api": "configured" if GEMINI_API_KEY else "not_configured"
    }
