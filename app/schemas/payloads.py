from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class TrackEventRequest(BaseModel):
    session_id: str
    search_id: Optional[str] = None
    product_id: Optional[int] = None
    event_type: str # VIEW_ITEM, ADD_TO_CART, INITIATE_CHECKOUT, PURCHASE

class VisualSearchResponse(BaseModel):
    status: str
    search_id: str
    session_id: str
    ai_detected: Dict[str, Any]
    model_used: Optional[str]
    best_match_score: float
    is_unmet_demand: bool
    products: List[Dict[str, Any]]
