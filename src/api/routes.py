from fastapi import APIRouter

from src.api.models import ChatRequest, ChatResponse
from src.chat.service import ask

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    return ask(request.question)