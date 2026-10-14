import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import DATABASE_URL

logger = logging.getLogger("database")

# PostgreSQL uchun drayverni avtomatik psycopg2 ga yo'naltiramiz
db_url = DATABASE_URL
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(db_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        # Modellarni import qilamiz, shunda Base ularni ko'radi
        from app.models.entities import Product, VisualSearch, UserEvent
        Base.metadata.create_all(bind=engine)
        logger.info("[DB OK] PostgreSQL bazasiga muvaffaqiyatli ulandi va jadvallar (products, visual_searches, user_events) yaratildi!")
    except Exception as e:
        logger.error(f"❌ [DB ULANISHDA XATO]: {e}")
        logger.error(f"Iltimos, .env faylidagi DATABASE_URL to'g'riligini tekshiring! Hozirgi qiymat: {db_url}")
        raise e
