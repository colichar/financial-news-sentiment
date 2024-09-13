from fastapi import FastAPI
from app.routes import sentiment_router
from app.s3_utils import check_and_download_model
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from dotenv import load_dotenv
import os

app = FastAPI()

app.include_router(sentiment_router)

load_dotenv()

@app.get('/health')
async def health_check():
    return {'status': 'ok'}

@app.on_event('startup')
def startup_event():
    check_and_download_model()

    MODEL_KEY = os.getenv('LOCAL_MODEL_PATH')

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_KEY)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_KEY)

    app.state.sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, top_k=None)