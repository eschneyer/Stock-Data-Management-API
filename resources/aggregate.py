from flask_restful import Resource, reqparse, abort, fields, marshal_with
import requests
from models import StockModel, db
from redis_config import redis_client
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

aggregate_post_args = reqparse.RequestParser()
aggregate_post_args.add_argument("quote_endpoint", type=dict, required = True)
aggregate_post_args.add_argument("sentiment", type=dict, required = True)
aggregate_post_args.add_argument("time_series_daily", type=dict, required = True)
aggregate_post_args.add_argument("time_series_weekly", type=dict, required = True)
aggregate_post_args.add_argument("time_series_monthly", type=dict, required = True)

aggregate_put_args = reqparse.RequestParser()
aggregate_put_args.add_argument("quote_endpoint", type=dict)
aggregate_put_args.add_argument("sentiment", type=dict)
aggregate_put_args.add_argument("time_series_daily", type=dict)
aggregate_put_args.add_argument("time_series_weekly", type=dict)
aggregate_put_args.add_argument("time_series_monthly", type=dict)

resource_fields = {
    'stock_symbol' : fields.String,
    'quote_endpoint' : fields.Raw,
    'sentiment' : fields.Raw,
    'time_series_daily' : fields.Raw,
    'time_series_weekly' : fields.Raw,
    'time_series_monthly' : fields.Raw
}

class Aggregate(Resource):

    def fetch(self, symbol):
        BASE = "http://127.0.0.1:5000/"
        
        quote_endpoint_response = requests.get(BASE + f"quoteendpoint/{symbol}")
        quote_endpoint_data = quote_endpoint_response.json()

        sentiments_response = requests.get(BASE + f"sentiments/{symbol}")
        sentiments_data = sentiments_response.json()

        time_series_daily_response = requests.get(BASE + f"timeseriesdaily/{symbol}")
        time_series_daily_data = time_series_daily_response.json()

        time_series_weekly_response = requests.get(BASE + f"timeseriesweekly/{symbol}")
        time_series_weekly_data = time_series_weekly_response.json()

        time_series_monthly_response = requests.get(BASE + f"timeseriesmonthly/{symbol}")
        time_series_monthly_data = time_series_monthly_response.json()

        stock_data = {'stock_symbol' : f'{symbol}', 'quote_endpoint' : quote_endpoint_data, 'sentiment' : sentiments_data, 'time_series_daily' : time_series_daily_data, 'time_series_weekly' : time_series_weekly_data, 'time_series_monthly' : time_series_monthly_data}
        return stock_data

    @marshal_with(resource_fields)
    def get(self, symbol):
        """
        Retrieves the stock data (quote endpoint, sentiment, time series(s)) for a desired stock

        Args:
            symbol (string): The symbol of the desired stock

        Returns:
            dict: stock data in JSON format
        
        Raises:
            HTTP status code 404: If there is an error while fetching data from the API.
        """

        #Checks to see if data is in the cache, if so, data is retrieved from the cache
        stock = redis_client.get(symbol)
        if stock:
            logging.info('We got data through the cache!')
            return json.loads(stock)
        
        #Checks to see if data is in the database, if not, data is retrieved using fetch and added to the cache
        stock = StockModel.query.filter_by(stock_symbol = symbol).first()
        if not stock:
            logging.info('We fetched data!')
            stock = self.fetch(symbol)
            redis_client.setex(symbol, 60, json.dumps(stock))
            return stock
        
        #Data is retrieved from the database and added to the cache
        redis_client.setex(symbol, 60, json.dumps(stock.to_dict()))
        logging.info('We got data through the database!')
        return stock

    @marshal_with(resource_fields)
    def post(self, symbol):
        """
        Stores stock data for a desired stock in the SQLite database.

        Args:
            symbol (string): The symbol of the desired stock

        Returns:
            tuple: A tuple containing the newly stored quote and the HTTP status code 201 (Created).

        Raises:
            HTTP status code 409: If stock data for the desried stock already exists in the SQLite database.
        """
        args = aggregate_post_args.parse_args()
        stock = StockModel.query.filter_by(stock_symbol = symbol).first()
        if stock:
            abort(409, message = "Stock already exists in database")
        stock = StockModel(stock_symbol = symbol, quote_endpoint = args['quote_endpoint'], sentiment = args['sentiment'], time_series_daily = args['time_series_daily'], time_series_weekly = args['time_series_weekly'], time_series_monthly = args['time_series_monthly'])
        db.session.add(stock)
        db.session.commit()
        return stock, 201
    
    @marshal_with(resource_fields)
    def delete(self, symbol):
        """
        Deletes the stock data for a desired stock from the SQLite database.

        Args:
            symbol (string): The symbol of the desired stock

        Returns:
            tuple: An empty tuple representing the successful deletion of the quote and the HTTP status code 204 (No Content).

        Raises:
            HTTP status code 404: If stock data for the desired stock does not exist in the SQLite database.
        """
        stock = StockModel.query.filter_by(stock_symbol = symbol).first()
        if not stock:
            abort(404, message = "Stock doesn't exist in database, can't delete")
        db.session.delete(stock)
        db.session.commit()
        return '', 204
    
    @marshal_with(resource_fields)
    def put(self, symbol):
        """
        Updates the stock data for a desired stock in the SQLite database.

        Args:
            symbol (string): The symbol of the desired stock

        Returns:
            tuple: tuple: A tuple containing the newly stored stock data and the HTTP status code 200 (OK)

        Raises:
            HTTP status code 404: If a quote for the desired stock does not exist in the quote_endpoint_data dictionary.
        """
        args = aggregate_put_args.parse_args()
        stock = StockModel.query.filter_by(stock_symbol = symbol).first()
        if not stock:
            abort(404, message = "Stock doesn't exist in the database, can't update")
        
        if args['quote_endpoint']:
            stock.quote_endpoint = args['quote_endpoint']
        if args['sentiment']:
            stock.sentiment = args['sentiment']
        if args['time_series_daily']:
            stock.time_series_daily = args['time_series_daily']
        if args['time_series_weekly']:
            stock.time_series_weekly = args['time_series_weekly']
        if args['time_series_monthly']:
            stock.time_series_monthly = args['time_series_monthly']
        
        db.session.commit()

        return stock, 200



