from pydantic import BaseModel
from typing import List

class SentimentScore(BaseModel):
    label: str
    score: float

class SentimentResponse(BaseModel):
    sentiments: List[SentimentScore]