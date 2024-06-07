from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from resources import time_series_daily
from resources import time_series_weekly
from resources import time_series_monthly
from resources import quote_endpoint
from resources import sentiments
from resources import aggregate
from models import db

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

def create_db():
    with app.app_context():
        db.create_all()

#create_db() # only call this once

api.add_resource(time_series_daily.TimeSeriesDaily, "/timeseriesdaily/<string:symbol>")
api.add_resource(time_series_weekly.TimeSeriesWeekly, "/timeseriesweekly/<string:symbol>")
api.add_resource(time_series_monthly.TimeSeriesMonthly, "/timeseriesmonthly/<string:symbol>")
api.add_resource(quote_endpoint.QuoteEndpoint, "/quoteendpoint/<string:symbol>")
api.add_resource(sentiments.Sentiments, "/sentiments/<string:symbol>")
api.add_resource(aggregate.Aggregate, "/aggregate/<string:symbol>")

if __name__ == "__main__":
    app.run(debug = True)
