from flask_restful import Resource, abort
import requests

class Sentiments(Resource):
    def get(self,symbol):
        """
        Retrieves the sentiment data for a desired stock

        Args:
            symbol (string): The symbol of the desired stock

        Returns:
            dict: overall sentiment score and overall sentiment label in JSON format
        
        Raises:
            HTTP status code 404: If the sentiment data for the desired stock could not be fetched from the API.
        """
        key = '8Z7TO0JMURALV8EU'
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={key}'
        r = requests.get(url)

        if not r.ok:
            abort(404, message = "Couldn't fetch sentiments from the API")

        data = r.json()

        if "Error Message" in data:
            error_message = data.get("Error Message")
            abort(404, message = error_message)
        
        elif "Note" in data:
            rate_limit_message = data.get("Note")
            abort(404, message = rate_limit_message)

        relevance_scores = []
        sentiment_scores = []

        #Extracting the relevant scores for symbol across multiple articles
        for item in data["feed"]:
            for ticker_sentiment in item["ticker_sentiment"]:
                if ticker_sentiment["ticker"] == symbol:
                    relevance_scores.append(float(ticker_sentiment["relevance_score"]))
                    sentiment_scores.append(float(ticker_sentiment["ticker_sentiment_score"]))

        #Compute weighted average sentiment score for symbol
        sum_of_weights = sum(relevance_scores)
        if sum_of_weights != 0:
            normalized_relevance_scores = [score / sum_of_weights for score in relevance_scores]
            overall_sentiment = sum(relevance * sentiment for relevance, sentiment in zip(normalized_relevance_scores, sentiment_scores))
        else:
            overall_sentiment = None

        overall_sentiment_label = ""

        #"sentiment_score_definition": "x <= -0.35: Bearish; -0.35 < x <= -0.15: Somewhat-Bearish; -0.15 < x < 0.15: Neutral; 0.15 <= x < 0.35: Somewhat_Bullish; x >= 0.35: Bullish"
        #According to Alpha Vantage
        if(overall_sentiment <= -0.35):
            overall_sentiment_label = "Bearish"
        elif(overall_sentiment <= -0.15):
            overall_sentiment_label = "Somewhat Bearish"
        elif(overall_sentiment < 0.15):
            overall_sentiment_label = "Neutral"
        elif(overall_sentiment < 0.35):
            overall_sentiment_label = "Somewhat Bullish"
        elif(overall_sentiment >= 0.35):
            overall_sentiment_label = "Bullish"
        else:
            overall_sentiment_label = "Error"

        sentiment_data = {"overall sentiment" : overall_sentiment, "overall sentiment label" : overall_sentiment_label}
        return sentiment_data
        