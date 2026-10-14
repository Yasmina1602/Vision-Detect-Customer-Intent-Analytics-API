from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.session import init_db
from app.api.search import router as search_router
from app.api.events import router as events_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title="Vision Detect & Customer Intent Analytics API",
    description="E-commerce uchun AI vizual qidiruv va xaridor talablarini tahlil qilish mikroxizmati",
    version="2.0.0"
)

# CORS: Istalgan e-commerce frontendidan so'rov qabul qilishga ruxsat
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse
import os

# Statik fayllar (boshqa saytlar uchun vidjet skripti)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routerlarni ulash
app.include_router(search_router)
app.include_router(events_router)
app.include_router(analytics_router)

@app.on_event("startup")
def startup_event():
    init_db()
    try:
        from app.db.session import SessionLocal
        from app.models.entities import VisualSearch
        from app.api.analytics import seed_demo_analytics_endpoint
        db = SessionLocal()
        if db.query(VisualSearch).count() < 8:
            seed_demo_analytics_endpoint(db)
        db.close()
    except Exception as e:
        print("[Startup Seed Notice]:", e)

@app.get("/")
def root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"service": "Vision Detect & Intent Analytics API", "status": "online"}

@app.get("/store")
def store_view():
    if os.path.exists("test_external_integration.html"):
        return FileResponse("test_external_integration.html")
    return {"message": "Store page not found"}

@app.get("/api/info")
def api_info():
    return {
        "service": "Vision Detect & Intent Analytics API",
        "status": "online",
        "version": "2.0.0",
        "docs_url": "/docs",
        "store_url": "/store",
        "widget_script": "/static/vision-widget.js"
    }

