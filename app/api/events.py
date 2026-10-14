from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import UserEvent
from app.schemas.payloads import TrackEventRequest

router = APIRouter(prefix="/api/v1", tags=["Event Tracker"])

@router.post("/track-event")
def track_event(data: TrackEventRequest, db: Session = Depends(get_db)):
    """
    Foydalanuvchi harakatini qayd etish (Ko'rdi, Savatga soldi, Xarid qildi).
    Har qanday saytdan yoki Meta Pixel bilan bir vaqtda chaqiriladi.
    """
    event = UserEvent(
        session_id=data.session_id,
        search_id=data.search_id,
        product_id=data.product_id,
        event_type=data.event_type.upper()
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    return {
        "status": "success",
        "event_id": event.event_id
    }
