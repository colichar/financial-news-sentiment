from app.services import analyse_sentiment

def test_analyse_sentiment():
    sentiments = analyse_sentiment('The stock market is volatile.')
    assert len(sentiments) > 0
    assert sentiments[0].label in ['LABEL_0', 'LABEL_1', 'LABEL_2']
