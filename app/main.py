from fastapi import FastAPI
from app.routes import sentiment_router

app = FastAPI()

app.include_router(sentiment_router)

@app.get('/health')
async def health_check():
    return {'status': 'ok'}