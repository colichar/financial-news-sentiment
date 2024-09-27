from fastapi import APIRouter, Request, HTTPException, Depends
from app.models import SentimentScore, SentimentResponse
from app.services import analyse_sentiment
from typing import Annotated
from transformers import pipeline

sentiment_router = APIRouter()

def get_sentiment_pipeline(request: Request):
    pipeline = request.app.state.sentiment_pipeline
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Sentiment model not loaded")
    return pipeline

@sentiment_router.post('/analyse', response_model=SentimentResponse)
async def analyse_sentiment_route(request: Request, sentiment_pipeline: Annotated[pipeline, Depends(get_sentiment_pipeline)]):
    try:
        body = await request.json()
        text = body.get('text')

        sentiments = analyse_sentiment(text=text, sentiment_pipeline=sentiment_pipeline)
        return SentimentResponse(sentiments=sentiments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))