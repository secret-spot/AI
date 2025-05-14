import anyio
from fastapi import APIRouter, HTTPException
from app.config import models
from pydantic import BaseModel
import re

router = APIRouter()

def call_gemini_sync(prompt: str) -> str:
    model_name = "recommend"
    model = models.get(model_name)
    response = model.generate_content(prompt)
    if not response.candidates or not response.candidates[0].content.parts:
        raise Exception("No Response")
    return ''.join([part.text for part in response.candidates[0].content.parts])

# Request model
class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
async def recommend(request: ChatRequest):
    try:
        body = request.prompt
        
        generated_text = await anyio.to_thread.run_sync(call_gemini_sync, body)

        # Extract 3 small cities and 3 one-line descriptions
        smallcities = []
        shortreviews = []
        for i in range(3):
            smallcities.append(re.search(fr"Small City {i+1}[:：]\s*(.+)", generated_text))
            shortreviews.append(re.search(fr"One-Line Description {i+1}[:：]\s*(.+)", generated_text))

        # Before adding extracted text to the list, check if a match exists
        smallcities_text = [match.group(1).strip() if match else "" for match in smallcities]
        shortreviews_text = [match.group(1).strip() if match else "" for match in shortreviews]

        # Construct the result list
        result = []
        for i in range(3):
            smallCity = smallcities_text[i]
            shortReview = shortreviews_text[i]
            result.append({
                "smallCity": smallCity,
                "shortReview": shortReview
            })

        return {
            "region": body,
            "recommendations": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
