from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from app.models import SentimentScore
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_KEY = os.getenv('LOCAL_MODEL_PATH')

model = AutoModelForSequenceClassification.from_pretrained(MODEL_KEY)
tokenizer = AutoTokenizer.from_pretrained(MODEL_KEY)

sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, top_k=None)

def analyse_sentiment(text: str):

    results = sentiment_pipeline(text)


    sentiments = [
        SentimentScore(label=result['label'], score=result['score'])
        for result in results[0]
    ]

    return sentiments