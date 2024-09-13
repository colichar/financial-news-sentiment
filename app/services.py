from app.models import SentimentScore
from dotenv import load_dotenv
from fastapi import Request
import os

load_dotenv()

def analyse_sentiment(request: Request, text: str):
    sentiment_pipeline = request.app.state.sentiment_pipeline

    results = sentiment_pipeline(text)


    sentiments = [
        SentimentScore(label=result['label'], score=result['score'])
        for result in results[0]
    ]

    return sentiments