from app.services import analyse_sentiment
from unittest.mock import MagicMock

def test_analyse_sentiment():
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = [[{'label': 'LABEL_2', 'score': 0.9817743301391602}, {'label': 'LABEL_1', 'score': 0.014286653138697147}, {'label': 'LABEL_0', 'score': 0.003938947804272175}]]
    sentiments = analyse_sentiment('The stock market is volatile.', sentiment_pipeline=mock_pipeline)
    assert len(sentiments) > 0
    assert sentiments[0].label in ['LABEL_0', 'LABEL_1', 'LABEL_2']
