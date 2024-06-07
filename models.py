from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StockModel(db.Model):
    stock_symbol = db.Column(db.String(5), primary_key = True)
    quote_endpoint = db.Column(db.JSON, nullable = False)
    sentiment = db.Column(db.JSON, nullable = False)
    time_series_daily = db.Column(db.JSON, nullable = False)
    time_series_weekly = db.Column(db.JSON, nullable = False)
    time_series_monthly = db.Column(db.JSON, nullable = False)

    def __repr__(self):
        return f"Stock(stock_symbol = {self.stock_symbol}, quote_endpoint = {self.quote_endpoint}, time_series_daily = {self.time_series_daily}, time_series_weekly = {self.time_series_weekly}, time_series_monthly = {self.time_series_monthly})"
    
    def to_dict(self):
        return {
            'stock_symbol': self.stock_symbol,
            'quote_endpoint': self.quote_endpoint,
            'sentiment': self.sentiment,
            'time_series_daily': self.time_series_daily,
            'time_series_weekly': self.time_series_weekly,
            'time_series_monthly': self.time_series_monthly
        }