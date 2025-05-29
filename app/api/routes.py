from fastapi import APIRouter
from pydantic import BaseModel
from app.services.agent import llm_agent

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
async def query_data(req: QueryRequest):
    return llm_agent(req.query)
