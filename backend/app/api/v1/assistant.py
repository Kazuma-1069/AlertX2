from fastapi import APIRouter, Depends
from app.schemas.assistant import AssistantQueryRequest, AssistantQueryResponse
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/query", response_model=AssistantQueryResponse)
async def query_assistant(req: AssistantQueryRequest):
    res = await ai_service.get_safety_guidance(req.user_message, req.situation_context)
    return res
