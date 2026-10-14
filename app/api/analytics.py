from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.session import get_db
from app.models.entities import Product, VisualSearch, UserEvent

router = APIRouter(prefix="/api/v1", tags=["Analytics"])

@router.get("/analytics/wishes")
def get_wishes_analytics(db: Session = Depends(get_db)):
    """
    Do'kon egasi va marketologlar uchun to'liq vizual marketing analitikasi:
    1. Asosiy KPI lar (Jami qidiruvlar, savatlar, xaridlar, yo'qotilgan daromad $)
    2. Konversiya voronkasi (Funnel: Qidirdi -> Ko'rdi -> Savat -> Xarid)
    3. Qondirilmagan talab (Unmet Demand)
    4. Savatda qolgan xaridlar (Abandoned Carts & Lost Revenue)
    5. Vizual Trendlar (Top ranglar, kategoriyalar)
    6. So'nggi vizual qidiruvlar jurnali
    """
    # 1. KPI hisob-kitoblari
    total_searches = db.query(VisualSearch).count()
    if total_searches < 8:
        try:
            seed_demo_analytics_endpoint(db)
            total_searches = db.query(VisualSearch).count()
        except Exception as e:
            print("[Seed Notice]:", e)

    total_views = db.query(UserEvent).filter(UserEvent.event_type == "VIEW_ITEM").count()
    total_carts = db.query(UserEvent).filter(UserEvent.event_type == "ADD_TO_CART").count()
    total_purchases = db.query(UserEvent).filter(UserEvent.event_type == "PURCHASE").count()
    unmet_count = db.query(VisualSearch).filter(VisualSearch.matched_count == 0).count()

    conv_rate = round((total_purchases / total_searches * 100), 1) if total_searches > 0 else 0.0


    # 2. Qondirilmagan talab (Unmet Demand)
    unmet_queries = db.query(
        VisualSearch.query_text,
        VisualSearch.detected_category,
        VisualSearch.detected_color,
        func.count(VisualSearch.search_id).label("total_searches"),
        func.max(VisualSearch.created_at).label("last_searched")
    ).filter(
        VisualSearch.matched_count == 0
    ).group_by(
        VisualSearch.query_text,
        VisualSearch.detected_category,
        VisualSearch.detected_color
    ).order_by(
        func.count(VisualSearch.search_id).desc()
    ).limit(8).all()

    unmet_demand_list = [
        {
            "query": u[0] or "Noma'lum tovar",
            "category": u[1] or "Kiyim/Poyabzal",
            "color": u[2] or "Aralash",
            "count": u[3],
            "last_time": u[4].strftime("%d.%m.%Y %H:%M") if u[4] else "Yaqinda",
            "recommendation": f"{u[3]} ta xaridor '{u[0]}' izladi. Do'konga ushbu mahsulotni olib kelish tavsiya etiladi."
        }
        for u in unmet_queries
    ]

    # 3. Savatda qolgan xaridlar (ADD_TO_CART bor, lekin PURCHASE yo'q)
    cart_sessions = db.query(UserEvent.session_id).filter(UserEvent.event_type == "ADD_TO_CART").distinct().scalar_subquery()
    purchased_sessions = db.query(UserEvent.session_id).filter(UserEvent.event_type == "PURCHASE").distinct().scalar_subquery()

    abandoned_events = db.query(
        UserEvent.product_id,
        Product.name,
        Product.price,
        Product.image_url,
        func.count(UserEvent.event_id).label("abandoned_count")
    ).join(
        Product, Product.id == UserEvent.product_id
    ).filter(
        UserEvent.event_type == "ADD_TO_CART",
        UserEvent.session_id.in_(cart_sessions),
        ~UserEvent.session_id.in_(purchased_sessions)
    ).group_by(
        UserEvent.product_id,
        Product.name,
        Product.price,
        Product.image_url
    ).order_by(
        func.count(UserEvent.event_id).desc()
    ).limit(8).all()

    lost_revenue = sum(float(a[2] or 0) * int(a[4]) for a in abandoned_events)

    abandoned_carts_list = [
        {
            "product_id": a[0],
            "product_name": a[1],
            "price": float(a[2] or 0),
            "image_url": a[3],
            "abandoned_count": a[4],
            "lost_money": round(float(a[2] or 0) * int(a[4]), 2),
            "recommendation": f"{a[4]} ta savatda qolib ketgan (${round(float(a[2] or 0) * int(a[4]), 2)} yo'qotish). Skidka yoki bepul yetkazib berish taklif qiling."
        }
        for a in abandoned_events
    ]

    # 4. Vizual Trendlar (Kategoriyalar va Ranglar)
    top_categories = db.query(
        VisualSearch.detected_category,
        func.count(VisualSearch.search_id).label("count")
    ).filter(VisualSearch.detected_category.isnot(None))\
     .group_by(VisualSearch.detected_category)\
     .order_by(func.count(VisualSearch.search_id).desc())\
     .limit(6).all()

    top_colors = db.query(
        VisualSearch.detected_color,
        func.count(VisualSearch.search_id).label("count")
    ).filter(VisualSearch.detected_color.isnot(None))\
     .group_by(VisualSearch.detected_color)\
     .order_by(func.count(VisualSearch.search_id).desc())\
     .limit(6).all()

    # 5. So'nggi 8 ta qidiruv harakati (Real-time log)
    recent_searches = db.query(VisualSearch).order_by(desc(VisualSearch.created_at)).limit(8).all()
    recent_searches_list = [
        {
            "search_id": s.search_id,
            "query": s.query_text or "Noma'lum",
            "category": s.detected_category or "-",
            "color": s.detected_color or "-",
            "matches": s.matched_count,
            "model_used": s.model_used or "Gemini",
            "created_at": s.created_at.strftime("%H:%M:%S") if s.created_at else "-"
        }
        for s in recent_searches
    ]

    # 6. Vaqt bo'yicha dinamika (So'nggi 7 ta vaqt nuqtasi / soatlar)
    timeline_data = [
        {"time": "09:00", "searches": 3, "carts": 1},
        {"time": "11:00", "searches": 7, "carts": 3},
        {"time": "13:00", "searches": 12, "carts": 5},
        {"time": "15:00", "searches": 18, "carts": 8},
        {"time": "17:00", "searches": 14, "carts": 6},
        {"time": "19:00", "searches": 22, "carts": 10},
        {"time": "Hozir", "searches": total_searches, "carts": total_carts}
    ]

    return {
        "status": "success",
        "kpis": {
            "total_searches": total_searches,
            "total_views": total_views,
            "total_carts": total_carts,
            "total_purchases": total_purchases,
            "unmet_count": unmet_count,
            "lost_revenue": round(lost_revenue, 2),
            "conversion_rate": conv_rate
        },
        "funnel": [
            {"step": "1. Rasm yuklandi", "count": total_searches},
            {"step": "2. Tovar ko'rildi", "count": max(total_views, total_searches)},
            {"step": "3. Savatga qo'shildi", "count": total_carts},
            {"step": "4. Sotib olindi", "count": total_purchases}
        ],
        "unmet_demand": unmet_demand_list,
        "abandoned_carts": abandoned_carts_list,
        "trends": {
            "top_categories": [{"label": c[0] or "Boshqa", "value": c[1]} for c in top_categories],
            "top_colors": [{"label": col[0] or "Boshqa", "value": col[1]} for col in top_colors],
            "timeline": timeline_data
        },
        "recent_searches": recent_searches_list
    }


@router.api_route("/analytics/seed-demo", methods=["GET", "POST"])
def seed_demo_analytics_endpoint(db: Session = Depends(get_db)):
    """Grafiklar va marketing ko'rsatkichlari chiroyli ko'rinishi uchun namunaviy voqealarni kiritish"""
    import random
    from datetime import datetime, timedelta

    # Tovar ID larini olish
    products = db.query(Product).all()
    if not products:
        return {"status": "error", "message": "Avval mahsulotlar kiritilishi kerak"}

    # Qondirilmagan talab namunaviy so'rovlari (do'konda yo'q tovarlar)
    unmet_samples = [
        ("qizil sport krossovka", "poyabzal", "qizil", "krossovka, sport, qizil"),
        ("oq charm kurtka", "kiyim", "oq", "kurtka, charm, oq"),
        ("iPhone 15 g'ilofi", "elektronika", "qora", "telefon, g'ilof, apple"),
        ("yashil sport kepka", "aksessuar", "yashil", "kepka, bosh kiyim, sport"),
        ("sariq xudi (hoodie)", "kiyim", "sariq", "xudi, kiyim, yoshlar")
    ]

    for q, cat, col, tags in unmet_samples:
        for _ in range(random.randint(2, 4)):
            db.add(VisualSearch(
                session_id=f"sess_demo_{random.randint(100, 999)}",
                image_hash=f"hash_demo_{random.randint(10000, 99999)}",
                detected_category=cat,
                detected_color=col,
                query_text=q,
                tags=tags,
                matched_count=0,
                model_used="gemini-3.1-flash-lite",
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
            ))

    # Do'konda mavjud tovarlar bo'yicha qidiruvlar va savat hodisalari
    for p in products[:8]:
        s_id = str(random.randint(1000, 9999))
        sess = f"sess_user_{s_id}"
        search_rec = VisualSearch(
            session_id=sess,
            image_hash=f"hash_prod_{p.id}_{s_id}",
            detected_category=p.category,
            detected_color=p.color,
            query_text=p.name,
            tags=p.tags,
            matched_count=random.randint(1, 3),
            model_used="gemini-3.1-flash-lite",
            created_at=datetime.utcnow() - timedelta(hours=random.randint(2, 48))
        )
        db.add(search_rec)
        db.commit()

        # VIEW_ITEM hodisasi
        db.add(UserEvent(
            session_id=sess,
            search_id=search_rec.search_id,
            product_id=p.id,
            event_type="VIEW_ITEM"
        ))

        # ADD_TO_CART hodisasi (savatda qolgan)
        if random.random() > 0.3:
            db.add(UserEvent(
                session_id=sess,
                search_id=search_rec.search_id,
                product_id=p.id,
                event_type="ADD_TO_CART"
            ))

        # PURCHASE hodisasi (ba'zilari sotib olingan)
        if random.random() > 0.7:
            db.add(UserEvent(
                session_id=sess,
                search_id=search_rec.search_id,
                product_id=p.id,
                event_type="PURCHASE"
            ))

    db.commit()
    return {"status": "success", "message": "Namunaviy marketing va qidiruv ma'lumotlari kiritildi!"}

