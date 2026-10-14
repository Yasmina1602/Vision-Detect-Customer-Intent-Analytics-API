import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Loyihaning ildiz manzili (qayerdan ishga tushirilishidan qat'i nazar .env ni topadi)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

def reload_env():
    """Har doim .env faylidagi o'zgarishlarni darhol yuklaydi"""
    if ENV_FILE.exists():
        load_dotenv(dotenv_path=ENV_FILE, override=True)
    else:
        load_dotenv(override=True)

# Dastlabki yuklash
reload_env()

def get_gemini_api_keys() -> List[str]:
    """
    GEMINI_API_KEYS yoki GEMINI_API_KEY o'zgaruvchisidan kalitlarni oladi.
    Dinamik: .env fayl tahrirlansa darhol yangi kalitni o'qiydi.
    """
    reload_env()
    raw_keys = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY") or ""
    return [k.strip() for k in raw_keys.split(",") if k.strip()]

def get_gemini_models_pool() -> List[str]:
    """Ketma-ket sinab ko'riladigan modellar ro'yxati"""
    reload_env()
    raw_models = os.getenv("GEMINI_MODELS", "")
    models = [m.strip() for m in raw_models.split(",") if m.strip()]
    if models:
        return models
    return [
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
        "gemini-flash-latest"
    ]

# Boshqa sozlamalar
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./store.db")
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() in ("true", "1", "yes")
