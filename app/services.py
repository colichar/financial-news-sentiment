from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from app.models import SentimentScore

model_directory = './model'

model = AutoModelForSequenceClassification.from_pretrained(model_directory)
tokenizer = AutoTokenizer.from_pretrained(model_directory)

sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, top_k=None)

def analyse_sentiment(text: str):

    results = sentiment_pipeline(text)


    sentiments = [
        SentimentScore(label=result['label'], score=result['score'])
        for result in results[0]
    ]

    return sentiments