from fastapi import APIRouter, Request, HTTPException
from app.models import SentimentScore, SentimentResponse
from app.services import analyse_sentiment

sentiment_router = APIRouter()

@sentiment_router.post('/analyse', response_model=SentimentResponse)
async def analyse_sentiment_route(request: Request):
    try:
        body = await request.json()
        text = body.get('text')

        sentiment_pipeline = request.app.state.sentiment_pipeline

        sentiments = analyse_sentiment(text=text, sentiment_pipeline=sentiment_pipeline)
        return SentimentResponse(sentiments=sentiments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))