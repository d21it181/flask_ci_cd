from flask import Flask
from flask_restx import Api, Resource

from flask_restx import Api, Resource, reqparse

from bs4 import BeautifulSoup
import datetime, time
import requests
import json
import pandas as pd

app = Flask(__name__)
appFlask = Api(app = app, 
    version = "1.0", 
    title = "Stock Api", 
    description = "I am here to provide most accurate financial data API out there.")

fundamentalParser = reqparse.RequestParser()
fundamentalParser.add_argument('query', type=str, help='Enter query')

fundamental = appFlask.namespace('Fundamentals API', path="/", description='This api returns realtime data provided symbol.')
@fundamental.route("/search/")    
class FundamentalClass(Resource):
    @appFlask.doc(responses={ 200: 'Success', 400: 'Invalid Argument', 500: 'Internal server error' }, parser=fundamentalParser)
    def get(self):
        try:
            queryData = fundamentalParser.parse_args()
            
            header = ({'User-Agent':
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
              (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
              'Accept-Language': 'en-US, en;q=0.5'})

            query = queryData["query"]
            page = requests.get("https://finance.yahoo.com/lookup/equity?s=" + query,headers = header)

            code = BeautifulSoup(page.content, 'html.parser')
            soup = code.find('section',  {"id": 'lookup-page'})


            soup = soup.find('table')
            tbody = soup.find('tbody')

            result = {}
            data = []

            for row in tbody.find_all('tr'):
                stock_data = {}


                symbol = row.find_all('td')[0].text
                name = row.find_all('td')[1].text
                category = row.find_all('td')[3].text
                exchange = row.find_all('td')[5].text

                stock_data["symbol"] = symbol
                stock_data["name"] = name
                stock_data["category"] = category
                stock_data["exchange"] = exchange

                data.append(stock_data)

            result["count"] = len(tbody.find_all('tr'))
            result["result"] = data
            return result
        except Exception as e:
            print(e)
            historical.abort(400, "Please enter date in valid format.", statusCode = "400")

parser = reqparse.RequestParser()
parser.add_argument('from', type=str, help='Enter starting date in YYYY-MM-DD')
parser.add_argument('to', type=str, help='Enter ending date in YYYY-MM-DD')
                    
historical = appFlask.namespace('Core API', path="/historical/", description='This api returns historical data about dialy with open, low, high, close and volume.')
@historical.route("/daily/<string:symbol>")
class daily(Resource):
    @appFlask.doc(responses={ 200: 'Success', 400: 'Invalid Argument', 500: 'Internal server error' }, parser=parser, params={'symbol': 'Specify the symbol' })
    def get(self, symbol):
        
        try:
        
            queryData = parser.parse_args()
            fromDate = queryData['from'].split("-")
            toDate = queryData['to'].split("-")

            startSecond = datetime.datetime(int(fromDate[0]), int(fromDate[1]), int(fromDate[2]), 0, 0)
            startSecond = int(time.mktime(startSecond.timetuple()))

            endSecond = datetime.datetime(int(toDate[0]), int(toDate[1]), int(toDate[2]), 0, 0)
            endSecond = int(time.mktime(endSecond.timetuple()))

            data = pd.read_csv("https://query1.finance.yahoo.com/v7/finance/download/" + symbol + "?period1=" + str(startSecond) + "&period2=" + str(endSecond) + "&interval=1d&events=history&includeAdjustedClose=true")
            out = data.to_json(orient='records')
            return json.loads(out)
        except Exception as e:
            historical.abort(400, "Please enter date in valid format.", statusCode = "400")

#historical = app.namespace('Core API', path="/historical/", description='This api returns historical data about dialy with open, low, high, close and volume.')
@historical.route("/weekly/<string:symbol>")    
class weekly(Resource):
    @appFlask.doc(responses={ 200: 'Success', 400: 'Invalid Argument', 500: 'Internal server error' }, parser=parser, params={'symbol': 'Specify the symbol' })
    def get(self, symbol):
        
        try:
            queryData = parser.parse_args()
            fromDate = queryData['from'].split("-")
            toDate = queryData['to'].split("-")



            startSecond = datetime.datetime(int(fromDate[0]), int(fromDate[1]), int(fromDate[2]), 0, 0)
            startSecond = int(time.mktime(startSecond.timetuple()))

            endSecond = datetime.datetime(int(toDate[0]), int(toDate[1]), int(toDate[2]), 0, 0)
            endSecond = int(time.mktime(endSecond.timetuple()))

            data = pd.read_csv("https://query1.finance.yahoo.com/v7/finance/download/" + symbol + "?period1=" + str(startSecond) + "&period2=" + str(endSecond) + "&interval=1wk&events=history&includeAdjustedClose=true")
            out = data.to_json(orient='records')
            return json.loads(out)
        except Exception as e:
            historical.abort(400, "Please enter date in valid format.", statusCode = "400")
    
#historical = app.namespace('Core API', path="/historical/", description='This api returns historical data about dialy with open, low, high, close and volume.')
@historical.route("/monthly/<string:symbol>")    
class monthly(Resource):
    @appFlask.doc(responses={ 200: 'Success', 400: 'Invalid Argument', 500: 'Internal server error' }, parser=parser, params={'symbol': 'Specify the symbol' })
    def get(self, symbol):
        try:
            queryData = parser.parse_args()
            fromDate = queryData['from'].split("-")
            toDate = queryData['to'].split("-")



            startSecond = datetime.datetime(int(fromDate[0]), int(fromDate[1]), int(fromDate[2]), 0, 0)
            startSecond = int(time.mktime(startSecond.timetuple()))

            endSecond = datetime.datetime(int(toDate[0]), int(toDate[1]), int(toDate[2]), 0, 0)
            endSecond = int(time.mktime(endSecond.timetuple()))

            data = pd.read_csv("https://query1.finance.yahoo.com/v7/finance/download/" + symbol + "?period1=" + str(startSecond) + "&period2=" + str(endSecond) + "&interval=1mo&events=history&includeAdjustedClose=true")
            out = data.to_json(orient='records')
            return json.loads(out)
        except Exception as e:
            historical.abort(400, "Please enter date in valid format.", statusCode = "400")
            
            
price = appFlask.namespace('Price API', path="/quote", description='This api returns realtime data provided symbol.')
@price.route("/<string:symbol>")    
class PricceClass(Resource):
    @appFlask.doc(responses={ 200: 'Success', 400: 'Invalid Argument', 500: 'Internal server error' }, params={'symbol': 'Specify the symbol (comma seprated if multiple)' })
    def get(self, symbol):
        try:
            header = ({'User-Agent':
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
              (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
              'Accept-Language': 'en-US, en;q=0.5'})

            query = symbol
            page = requests.get("https://finance.yahoo.com/quotes/" + query + "/view/v1",headers = header)

            code = BeautifulSoup(page.content, 'html.parser')
            soup = code.find('div',  {"id": 'pf-detail-table'})


            soup = soup.find('table')
            tbody = soup.find('tbody')

            data = {}
            for row in tbody.find_all('tr'):
                stock_data = {}


                symbol = row.find_all('td')[0].text
                price = float(row.find_all('td')[1].text.replace(',', ''))
                change = float(row.find_all('td')[2].text.replace(',', ''))
                changePer = row.find_all('td')[3].text
                currency = row.find_all('td')[4].text

                stock_data["price"] = price
                stock_data["change"] = change
                stock_data["change per"] = changePer
                stock_data["currency"] = currency

                data[symbol] = stock_data
                #print(symbol, price, change, changePer)

            return data
        except Exception as e:
            print(e)
            historical.abort(400, "Please enter date in valid format.", statusCode = "400")
   
if __name__ == "__main__":
    app.run()
