from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.entities import Product

def match_products(
    db: Session, 
    ai_data: Dict[str, Any], 
    limit: int = 10
) -> Tuple[List[Dict[str, Any]], float]:
    """
    AI tomonidan olingan strukturaviy atributlar bo'yicha bazadan eng mos mahsulotlarni qidirish.
    Vektorlarsiz — oddiy matn, kategoriya va rang moslashuvi.
    """
    category = (ai_data.get("category") or "").strip().lower()
    color = (ai_data.get("color") or "").strip().lower()
    subcategory = (ai_data.get("subcategory") or "").strip().lower()
    query_text = (ai_data.get("search_query") or "").strip().lower()
    tags = [t.lower().strip() for t in ai_data.get("tags", []) if t.strip()]

    search_words = set(query_text.split() + tags)
    if subcategory:
        search_words.add(subcategory)

    # 1. Nomzodlarni olish
    query = db.query(Product)
    if category:
        candidates = query.filter(
            or_(
                Product.category.ilike(f"%{category}%"),
                Product.name.ilike(f"%{category}%"),
                Product.tags.ilike(f"%{category}%")
            )
        ).all()
    else:
        candidates = query.all()

    if not candidates:
        candidates = db.query(Product).all()

    scored_products = []

    # 2. Har bir mahsulotga moslik foizi hisoblash
    for prod in candidates:
        prod_text = f"{prod.name} {prod.description or ''} {prod.tags or ''}".lower()
        score = 0.0
        total_weight = 0.0

        # Kategoriya (30%)
        total_weight += 0.3
        if category and (category in (prod.category or "").lower() or category in prod_text):
            score += 0.3

        # Rang (30%)
        total_weight += 0.3
        if color and (color in (prod.color or "").lower() or color in prod_text):
            score += 0.3

        # Kalit so'zlar (40%)
        total_weight += 0.4
        if search_words:
            matched = sum(1 for w in search_words if len(w) > 2 and w in prod_text)
            score += 0.4 * (matched / max(len(search_words), 1))

        final_score = round(min(score / total_weight if total_weight > 0 else 0.0, 1.0), 2)

        if final_score >= 0.40:
            scored_products.append({
                "product": {
                    "id": prod.id,
                    "name": prod.name,
                    "category": prod.category,
                    "color": prod.color,
                    "price": prod.price,
                    "image_url": prod.image_url,
                    "description": prod.description
                },
                "match_score": final_score
            })

    scored_products.sort(key=lambda x: x["match_score"], reverse=True)
    results = scored_products[:limit]
    best_score = results[0]["match_score"] if results else 0.0

    return results, best_score
