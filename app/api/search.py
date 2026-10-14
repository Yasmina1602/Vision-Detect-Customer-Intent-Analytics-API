import uuid
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import VisualSearch
from app.schemas.payloads import VisualSearchResponse
from app.services.gemini_rotator import calculate_image_hash, analyze_image_with_fallback
from app.services.search_engine import match_products
from app.core.config import CACHE_ENABLED

router = APIRouter(prefix="/api/v1", tags=["Visual Search"])

@router.post("/visual-search", response_model=VisualSearchResponse)
async def visual_search(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Rasm orqali qidirish:
    1. SHA-256 xesh tekshiriladi (agar avval qidirilgan bo'lsa keshdan olinadi).
    2. Yangi rasm bo'lsa, tekin Gemini modellari hovuzidan navbatma-navbat chaqiriladi.
    3. Bazadan oddiy matnli moslik bo'yicha tovarlar topiladi.
    4. Qidiruv jurnali saqlanadi.
    """
    if not session_id:
        session_id = str(uuid.uuid4())

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Rasm fayli bo'sh!")

    image_hash = calculate_image_hash(image_bytes)
    model_used = None

    # 1. Keshni tekshirish
    previous_search = None
    if CACHE_ENABLED:
        previous_search = db.query(VisualSearch).filter(VisualSearch.image_hash == image_hash).first()

    if previous_search:
        ai_data = {
            "category": previous_search.detected_category,
            "color": previous_search.detected_color,
            "search_query": previous_search.query_text,
            "tags": [t.strip() for t in (previous_search.tags or "").split(",") if t.strip()],
            "from_cache": True
        }
        model_used = f"{previous_search.model_used} (Cached)"
    else:
        # 2. Yangi rasm -> Ketma-ket tekin modellar rotatori
        try:
            ai_data, model_used = analyze_image_with_fallback(image_bytes)
            ai_data["from_cache"] = False
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini tahlilida xatolik yuz berdi: {str(e)}")

    # 3. Bazadan mos tovarlarni qidirish
    matched_results, best_score = match_products(db, ai_data, limit=10)

    # 4. Qidiruv jurnalini saqlash
    search_record = VisualSearch(
        session_id=session_id,
        image_hash=image_hash,
        detected_category=ai_data.get("category"),
        detected_color=ai_data.get("color"),
        query_text=ai_data.get("search_query"),
        tags=", ".join(ai_data.get("tags", [])),
        matched_count=len(matched_results),
        model_used=model_used
    )
    db.add(search_record)
    db.commit()
    db.refresh(search_record)

    return {
        "status": "success",
        "search_id": search_record.search_id,
        "session_id": session_id,
        "ai_detected": ai_data,
        "model_used": model_used,
        "best_match_score": best_score,
        "is_unmet_demand": len(matched_results) == 0 or best_score < 0.65,
        "products": matched_results
    }

@router.get("/products")
def get_all_products(
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Barcha mahsulotlar ro'yxatini qaytaruvchi endpoint"""
    from app.models.entities import Product
    from sqlalchemy import or_

    query = db.query(Product)
    if category and category.lower() != "all":
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if q and q.strip():
        search_term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.tags.ilike(search_term),
                Product.color.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
    products = query.order_by(Product.id.asc()).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "color": p.color,
            "price": p.price,
            "description": p.description,
            "image_url": p.image_url,
            "tags": p.tags
        }
        for p in products
    ]
