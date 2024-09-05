from pydantic import BaseModel
from typing import List

class SentimentRequest(BaseModel):
    text: str

class SentimentScore(BaseModel):
    label: str
    score: float

class SentimentResponse(BaseModel):
    sentiments: List[SentimentScore]