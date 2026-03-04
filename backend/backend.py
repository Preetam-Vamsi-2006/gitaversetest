from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
from mtranslate import translate
import json
import os
import re
import unicodedata
import uuid

# ---------------- CONFIG ----------------

DATA_DIR = "BhagavatGitaJsonFiles"
AUDIO_DIR = "audio"

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

# ---------------- REQUEST SCHEMA ----------------

class ShlokaRequest(BaseModel):
    shloka: str
    language: str

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

    for verse in VERSES:
        if normalize(verse["sanskrit"]["text"]) == norm_input:

            if language == "english":
                text = verse["translations"]["english"]["text"]
            elif language == "hindi":
                text = verse["translations"]["hindi"]["text"]
            else:
                text = translate(
                    verse["translations"]["hindi"]["text"],
                    LANG_CODES[language]
                )

            # ✅ THIS RETURN WAS MISSING
            return {
                "chapter": verse["chapter"],
                "verse": verse["verse"],
                "language": language,
                "text": text
            }

    # Only reached if NO match found
    return {"error": "Shloka not found"}
