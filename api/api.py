import math

import flask
from flask import request

import orderbook

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Hello World"

@app.route('/orderbook/<pair>', methods=['GET'])
def getOrderbook(pair):
    try:
        return orderbook.getOrderbook(pair)
    except Exception as e:
        print(e)
        return "An error occured"

@app.route('/limitOrder', methods=['POST'])
def placeLimitOrder():
    try:
        request_data = request.get_json()
        side = request_data.get("side")
        quantity = request_data.get("quantity")
        price = request_data.get("price")
        pair = request_data.get("pair")
        postOnly = request_data.get("postOnly") or False
        if side == None:
            return "Side paramter is missing."
        elif quantity == None or math.isnan(quantity) == True:
            return "Quantity parameter is missing or not a valid quantity."
        elif price == None or math.isnan(price) == True:
            return "Price parameter is missing or not a valid price."
        elif pair == None:
            return "Pair parameter is missing."
        else:
            response = orderbook.newLimitOrder(side, quantity, price, pair, postOnly)
            return response
    except Exception as e:
        print(e)
        return "An error occured"

@app.route('/tradeHistory/<pair>', methods=['GET'])
def getTradeHistory(pair):
    try:
        limit = request.args.get('limit', 100)
        if limit.isnumeric() == False:
            return "Invalid limit set."
        else:
            return orderbook.getTradeHistory(pair, int(limit))
    except Exception as e:
        print(e)
        return "An error occured"

app.run(host="0.0.0.0")