from flask_restful import Resource, abort
import requests

class TimeSeriesMonthly(Resource):
    def get(self,symbol):
        """
        Retrieves quantitative data (open, high, low, close, volume) for a desired stock for each of the past 12 months

        Args:
            symbol (string): The symbol of the desired stock

        Returns:
            dict: quantitative data in JSON format
        
        Raises:
            HTTP status code 404: If the time series monthly data for the desired stock could not be fetched from the API
        """
        key = '8Z7TO0JMURALV8EU'
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&outputsize=compact&apikey={key}'
        r = requests.get(url)

        if not r.ok:
            abort(404, message = "Couldn't fetch time series monthly data from the API")

        data = r.json()

        if "Error Message" in data:
            error_message = data.get("Error Message")
            abort(404, message = error_message)
        
        elif "Note" in data:
            rate_limit_message = data.get("Note")
            abort(404, message = rate_limit_message)

        #Extract all dates from the data to obtain the 12 most recent
        dates = list(data['Monthly Time Series'].keys())
        recent_dates = dates[:12]

        business_year_data = {}

        #Iterate over the recent dates and store the corresponding values
        for date in recent_dates:
            business_year_data[date] = data['Monthly Time Series'][date]

        return business_year_data
        