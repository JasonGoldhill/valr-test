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
        return "An unexpected error occured."


@app.route('/limitOrder', methods=['POST'])
def placeLimitOrder():
    try:
        request_data = request.get_json()
        side = request_data.get("side")
        quantity = request_data.get("quantity")
        price = request_data.get("price")
        pair = request_data.get("pair")
        postOnly = request_data.get("postOnly") or False

        if side is None or isinstance(side, str) is False:
            return "The side parameter is required and must be a valid string."
        elif quantity is None or (isinstance(quantity, float) or isinstance(quantity, int)) is False:
            return "The quantity parameter is required and must be a valid int or float."
        elif price is None or (isinstance(price, float) or isinstance(price, int)) is False:
            return "The price parameter is required and must be a valid int or float."
        elif pair is None or isinstance(pair, str) is False:
            return "The pair parameter is required and must be a valid string."
        elif isinstance(postOnly, bool) is False:
            return "The postOnly parameter is optional, but must be a valid boolean value (true or false) if provided (defaults to false)."

        else:
            return orderbook.newLimitOrder(
                side,
                quantity,
                price,
                pair,
                postOnly)

    except Exception as e:
        print(e)
        return "An unexpected error occured."


@app.route('/tradeHistory/<pair>', methods=['GET'])
def getTradeHistory(pair):
    try:
        limit = request.args.get('limit', 100)

        if limit.isnumeric() is False:
            return "The limit query parameter is optional, but must be a valid int if provided (defaults to 100)."
        else:
            return orderbook.getTradeHistory(
                pair,
                int(limit))

    except Exception as e:
        print(e)
        return "An unexpected error occured."


app.run(host="0.0.0.0")
