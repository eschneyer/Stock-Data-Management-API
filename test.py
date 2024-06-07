import requests

BASE = "http://127.0.0.1:5000/"

#Test endpoints for the API
def test_get_sentiments(symbol):
    response = requests.get(BASE + f"sentiments/{symbol}")
    print(response.json())

def test_get_quote_endpoint(symbol):
    response = requests.get(BASE + f"quoteendpoint/{symbol}")
    print(response.json())

def test_get_time_series_daily(symbol):
    response = requests.get(BASE + f"timeseriesdaily/{symbol}")
    print(response.json())

def test_get_time_series_weekly(symbol):
    response = requests.get(BASE + f"timeseriesweekly/{symbol}")
    print(response.json())

def test_get_time_series_monthly(symbol):
    response = requests.get(BASE + f"timeseriesmonthly/{symbol}")
    print(response.json())


#Test database functionality
def test_get_aggregate(symbol):
    response = requests.get(BASE + f"aggregate/{symbol}")
    data = response.json()
    print(data)
    return data

def test_post_aggregate(symbol, data):
    post_data = {
        "quote_endpoint": data['quote_endpoint'],
        "sentiment": data['sentiment'],
        "time_series_daily": data['time_series_daily'],
        "time_series_weekly": data['time_series_weekly'],
        "time_series_monthly": data['time_series_monthly']
    }
    response = requests.post(BASE + f"aggregate/{symbol}", json=post_data)
    print(response.json())

def test_put_aggregate(symbol, data):
    put_data = {
        "quote_endpoint": data['quote_endpoint'],
        "sentiment": data['sentiment'],
        "time_series_daily": data['time_series_daily'],
        "time_series_weekly": data['time_series_weekly'],
        "time_series_monthly": data['time_series_monthly']
    }
    response = requests.put(BASE + f"aggregate/{symbol}", json = put_data)
    print(response.json())

def test_delete_aggregate(symbol):
    response = requests.delete(BASE + f"aggregate/{symbol}")
