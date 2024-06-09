from flask_restful import Resource, abort
import requests

class QuoteEndpoint(Resource):     
    def get(self,symbol):
        """
        Retrieves the quote (price and volume information) for a desired stock

        Args:
            symbol (string): The symbol of the desired stock

        Returns:
            dict: quote in JSON format
        
        Raises:
            HTTP status code 404: If the quote endpoint data for the desired stock could not be fetched from the API
        """
        key = 'YOUR API KEY'
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={key}'
        r = requests.get(url)

        if not r.ok:
            abort(404, message = "Couldn't fetch quote endpoint from the API")

        data = r.json()

        if "Error Message" in data:
            error_message = data.get("Error Message")
            abort(404, message = error_message)
        
        elif "Note" in data:
            rate_limit_message = data.get("Note")
            abort(404, message = rate_limit_message)

        return data
        

