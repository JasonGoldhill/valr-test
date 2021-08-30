import flask
from flask import request

import orderbook

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Hello World"

@app.route('/limitOrder', methods=['POST'])
def placeLimitOrder():
    try:
        request_data = request.get_json()
        side = request_data["side"]
        quantity = request_data["quantity"]
        price = request_data["price"]
        response = orderbook.newLimitOrder(side, quantity, price)
        return response
    except Exception as e:
        print(e)
        return "An error occured"

app.run(host="0.0.0.0")