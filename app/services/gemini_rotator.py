import io
import json
import base64
import hashlib
import logging
from typing import Dict, Any, Tuple
from PIL import Image

from app.core.config import get_gemini_api_keys, get_gemini_models_pool

logger = logging.getLogger("gemini_rotator")
logging.basicConfig(level=logging.INFO)

def calculate_image_hash(image_bytes: bytes) -> str:
    """Rasmning SHA-256 xeshini hisoblash"""
    return hashlib.sha256(image_bytes).hexdigest()

PROMPT_TEXT = """
Siz elektron tijorat do'koni uchun rasmlarni tahlil qiluvchi AI tizimisiz.
Berilgan tovar rasmini tahlil qilib, uni do'kon ma'lumotlar bazasidan qidirish uchun eng mos kalit so'zlar va atributlarni aniqlang.

Javobni FAQAT quyidagi JSON formatida qaytaring:
{
  "category": "asosiy kategoriya (masalan: poyabzal, kiyim, aksessuar, elektronika)",
  "subcategory": "aniq turi (masalan: krossovka, tufli, futbolka, kurtka, sumka)",
  "color": "asosiy rang (masalan: ko'k, qora, oq, qizil, sariq, yashil)",
  "brand": "brend (agar rasmda aniq ko'rinsa, aks holda null)",
  "gender": "erkaklar, ayollar, bolalar yoki universal",
  "search_query": "do'kon qidiruv satri uchun 2-4 ta so'zdan iborat eng aniq qidiruv jumlasi (masalan: ko'k krossovka)",
  "tags": ["teg1", "teg2", "teg3", "teg4"],
  "short_description": "mahsulotning o'zbek tilidagi qisqacha tavsifi"
}
Eslatma: Barcha so'zlarni kichik harflarda va o'zbek tilida yozing. Hech qanday qo'shimcha so'zsiz faqat toza JSON matni bo'lsin.
"""

def _call_gemini_single(api_key: str, model_name: str, image: Image.Image) -> str:
    """Bitta model va kalit orqali so'rov yuborish"""
    from google import genai
    from google.genai import types

    # attempts=1 qilib sozlaymiz, shunda 429/503 bo'lsa kutib o'tirmasdan darhol keyingi modelga o'tadi
    http_opts = types.HttpOptions(
        timeout=15000,
        retry_options=types.HttpRetryOptions(attempts=1)
    )
    client = genai.Client(api_key=api_key, http_options=http_opts)

    buf = io.BytesIO()
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(buf, format="JPEG", quality=85)
    image_bytes = buf.getvalue()

    # 1. Tezkor generate_content orqali so'rov yuboramiz
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[
                PROMPT_TEXT,
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        if response and response.text:
            return response.text
    except Exception as e_gen:
        logger.info(f"generate_content ({e_gen}) bermadi, interactions bilan sinab ko'rilmoqda...")

    # 2. Yangi Interactions API fallback
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    interaction = client.interactions.create(
        model=model_name,
        input=[
            {"type": "text", "text": PROMPT_TEXT},
            {"type": "image", "data": b64_image, "mime_type": "image/jpeg"}
        ]
    )
    return interaction.output_text

def analyze_image_with_fallback(image_bytes: bytes) -> Tuple[Dict[str, Any], str]:
    """
    KETMA-KET MODEL ALMASHTIRUVCHI ASOSIY FUNKSIYA:
    Bir modelda limit (429) yoki xatolik bo'lsa, to'xtamasdan
    keyingi tekin modelga yoki kalitga o'tib ketaveradi.
    
    Qaytaradi: (tahlil_natijasi_json, qaysi_model_ishlatildi)
    """
    api_keys = get_gemini_api_keys()
    models_pool = get_gemini_models_pool()

    if not api_keys:
        raise ValueError("GEMINI_API_KEY sozlanmagan! Iltimos, .env faylida API kalitingizni tekshiring.")

    image = Image.open(io.BytesIO(image_bytes))
    last_error = None

    # Har bir API kalit va har bir model bo'yicha ketma-ket aylanadi
    for key_idx, api_key in enumerate(api_keys):
        for model_name in models_pool:
            try:
                logger.info(f"Sinab ko'rilmoqda: Model '{model_name}' (Kalit #{key_idx + 1})...")
                raw_text = _call_gemini_single(api_key, model_name, image)
                
                # JSON ni tozalab parse qilish
                clean_text = raw_text.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text[7:]
                if clean_text.endswith("```"):
                    clean_text = clean_text[:-3]
                clean_text = clean_text.strip()

                parsed_data = json.loads(clean_text)
                logger.info(f"[MUVAFFAQITYAT] '{model_name}' orqali rasm muvaffaqiyatli tahlil qilindi!")
                return parsed_data, model_name

            except Exception as e:
                logger.warning(f"Model '{model_name}' da xatolik yuz berdi: {e}. Keyingi model sinab ko'rilmoqda...")
                last_error = e
                continue

    raise RuntimeError(f"Barcha modellar va API kalitlar limitga uchradi! Oxirgi xatolik: {last_error}")
