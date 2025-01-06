from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response models
class Message(BaseModel):
    role: str
    content: str

class CompletionRequest(BaseModel):
    conversation_id: str
    messages: list[Message]
    quote: bool

class CompletionResponse(BaseModel):
    reply: str

# Configuration for the external API
API_URL = "http://216.48.188.231/v1/api/completion"
HEADERS = {
    "Authorization": "Bearer rag-djNmZiZjZlYzhmZTExZWZiYTFjMjJjOD",
    "Content-Type": "application/json"
}

@app.post("/chat", response_model=CompletionResponse)
async def chat(request: CompletionRequest):
    try:
        logger.info("Received request: %s", request.dict())
        async with httpx.AsyncClient(timeout=100) as client:
            async with client.stream(
                "POST", API_URL, headers=HEADERS, json=request.dict()
            ) as response:
                response.raise_for_status()
                reply_content = ""
                async for chunk in response.aiter_text():
                    reply_content += chunk
                logger.info("Received response: %s", reply_content.strip())
                return {"reply": reply_content.strip() or "No response received."}
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error: %s", e.response.text)
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise HTTPException(status_code=500, detail=str(e))
