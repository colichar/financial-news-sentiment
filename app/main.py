from fastapi import FastAPI
from app.routes import sentiment_router
from app.s3_utils import check_and_download_model
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from mangum import Mangum

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    check_and_download_model()

    MODEL_KEY = os.getenv('LOCAL_MODEL_PATH')

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_KEY)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_KEY)

    app.state.sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, top_k=None)

    yield

    app.state.sentiment_pipeline

    

app = FastAPI(lifespan=lifespan)

app.include_router(sentiment_router)


@app.get('/health')
async def health_check():
    return {'status': 'ok'}


handler = Mangum(app)