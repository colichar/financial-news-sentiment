from fastapi import FastAPI
from app.routes import sentiment_router
from app.s3_utils import check_and_download_model
import os

app = FastAPI()

app.include_router(sentiment_router)

@app.get('/health')
async def health_check():
    return {'status': 'ok'}

@app.on_event('startup')
def startup_event():
    check_and_download_model()