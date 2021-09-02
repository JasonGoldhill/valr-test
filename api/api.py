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
        side = request_data["side"]
        quantity = request_data["quantity"]
        price = request_data["price"]
        pair = request_data["pair"]
        response = orderbook.newLimitOrder(side, quantity, price, pair)
        return response
    except Exception as e:
        print(e)
        return "An error occured"

@app.route('/tradeHistory/<pair>', methods=['GET'])
def getTradeHistory(pair):
    try:
        limit = request.args.get('limit', 100)
        return orderbook.getTradeHistory(pair, int(limit))
    except Exception as e:
        print(e)
        return "An error occured"

app.run(host="0.0.0.0")