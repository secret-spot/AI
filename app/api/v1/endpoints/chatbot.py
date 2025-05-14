import anyio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import models

router = APIRouter()


# Request 
class ChatRequest(BaseModel):
    prompt: str

def call_gemini_sync(prompt: str) -> str:
    model_name = "chatbot"
    model = models.get(model_name)
    response = model.generate_content(prompt)
    if not response.candidates or not response.candidates[0].content.parts:
        raise Exception("No response")
    return ''.join([part.text for part in response.candidates[0].content.parts])

@router.post("/")
async def chatbot(request: ChatRequest):
    try:
        generated_text = await anyio.to_thread.run_sync(call_gemini_sync, request.prompt)

        response = generated_text.strip()
        
        return {
            "content": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")