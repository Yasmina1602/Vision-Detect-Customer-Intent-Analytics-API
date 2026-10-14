import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from app.db.session import Base

class Product(Base):
    """Do'kondagi mahsulotlar"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    color = Column(String(50), nullable=True, index=True)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    tags = Column(String(500), nullable=True)

class VisualSearch(Base):
    """Mijozlar rasm yuklab qidirgan barcha so'rovlar jurnali"""
    __tablename__ = "visual_searches"

    search_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(100), nullable=False, index=True)
    image_hash = Column(String(64), nullable=False, index=True)
    detected_category = Column(String(100), nullable=True)
    detected_color = Column(String(50), nullable=True)
    query_text = Column(String(255), nullable=True)
    tags = Column(String(500), nullable=True)
    matched_count = Column(Integer, default=0)
    model_used = Column(String(100), nullable=True) # Qaysi Gemini modeli tahlil qildi
    created_at = Column(DateTime, default=datetime.utcnow)

class UserEvent(Base):
    """Mijoz xatti-harakatlari hodisalari (Funnel)"""
    __tablename__ = "user_events"

    event_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(100), nullable=False, index=True)
    search_id = Column(String(36), nullable=True, index=True)
    product_id = Column(Integer, nullable=True)
    event_type = Column(String(50), nullable=False) # VIEW_ITEM, ADD_TO_CART, INITIATE_CHECKOUT, PURCHASE
    created_at = Column(DateTime, default=datetime.utcnow)
