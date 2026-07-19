from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    request_id: str

class FeedbackRequest(BaseModel):
    request_id: str
    feedback: str