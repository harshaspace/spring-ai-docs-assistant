from fastapi import APIRouter

from src.monitoring.metrics import get_metrics, save_feedback
from src.api.models import ChatRequest, ChatResponse, FeedbackRequest
from src.chat.service import ask

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    return ask(request.question)

@router.get("/metrics")
def metrics():
    return get_metrics()

@router.post("/feedback")
def feedback(request: FeedbackRequest):
    save_feedback(request.request_id, request.feedback)
    return {"status": "ok"}