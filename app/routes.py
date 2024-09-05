from fastapi import APIRouter, HTTPException
from app.models import SentimentRequest, SentimentScore, SentimentResponse
from app.services import analyse_sentiment

sentiment_router = APIRouter()

@sentiment_router.post('/analyse', response_model=SentimentResponse)
async def analyse_sentiment_route(request: SentimentRequest):
    try:
        print(request.text)
        sentiments = analyse_sentiment(request.text)
        return SentimentResponse(sentiments=sentiments)
    except e:
        raise HTTPException(status_code=500, detail=str(e))