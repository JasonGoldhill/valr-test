bids = []
asks = []
tradeHistory = []

def getOrderbook():
    orderbook = {
        "Asks": asks,
        "Bids": bids
    }

    return orderbook

def getTradeHistory():
    history = {
        "TradeHistory": tradeHistory
    }
    return history

def newLimitOrder(side, quantity, price):
    order = {
        "quantity": quantity,
        "price": price
    }

    if side == "SELL":
        if len(bids) > 0:
            if order["price"] > bids[0]["price"]:
                updateAsks(order)
                return "Order placed."
            else:
                response = fillBid(order)
                return response
        else:
            updateAsks(order)
            return "Order placed."

    if side == "BUY":
        if len(asks) > 0:
            if order["price"] < asks[0]["price"]:
                updateBids(order)
                return "Order placed."
            else:
                response = fillAsk(order)
                return response
        else:
            updateBids(order)
            return "Order placed." 

def updateAsks(order):
    if len(asks) > 0:
        if order["price"] > asks[-1]["price"]:
            asks.append(order)
        else:
            index = 0
            for ask in asks:
                if order["price"] < ask["price"]:
                    break
                else:
                    index = index + 1
            asks.insert(index, order)
    else:
        asks.append(order)

def updateBids(order):
    if len(bids) > 0:
        if order["price"] < bids[-1]["price"]:
            bids.append(order)
        else:
            index = 0
            for bid in bids:
                if order["price"] > bid["price"]:
                    break
                else:
                    index = index + 1
            bids.insert(index, order)
    else:
        bids.append(order)

def fillBid(order):
    for bid in list(bids):
        if bid["price"] < order["price"]:
            break
        if bid["quantity"] > order["quantity"]:
            updateTradeHistory(bid["price"], order["quantity"], "sell")
            bid["quantity"] = bid["quantity"] - order["quantity"]
            order["quantity"] = 0
            break
        elif order["quantity"] > bid["quantity"]:
            updateTradeHistory(bid["price"], bid["quantity"], "sell")
            bids.remove(bid)
            order["quantity"] = order["quantity"] - bid["quantity"]
        else:
            updateTradeHistory(bid["price"], order["quantity"], "sell")
            bids.remove(bid)
            order["quantity"] = 0
            break

    if order["quantity"] > 0:
        updateAsks(order)
        return "Order partially filled. Remainder placed in orderbook."
    else:
        return "Order completely filled."

def fillAsk(order):
    for ask in list(asks):
        if ask["price"] > order["price"]:
            break
        if ask["quantity"] > order["quantity"]:
            updateTradeHistory(ask["price"], order["quantity"], "buy")
            ask["quantity"] = ask["quantity"] - order["quantity"]
            order["quantity"] = 0
            break
        elif order["quantity"] > ask["quantity"]:
            updateTradeHistory(ask["price"], ask["quantity"], "buy")
            asks.remove(ask)
            order["quantity"] = order["quantity"] - ask["quantity"]
        else:
            updateTradeHistory(ask["price"], order["quantity"], "buy")
            asks.remove(ask)
            order["quantity"] = 0
            break

    if order["quantity"] > 0:
        updateBids(order)
        return "Order partially filled. Remainder placed in orderbook."
    else:
        return "Order completely filled."

def updateTradeHistory(price, quantity, takerSide):
    entry = {
        "quantity": quantity,
        "price": price,
        "takerSide": takerSide
    }

    tradeHistory.insert(0, entry)

    if len(tradeHistory) > 100:
        tradeHistory.pop()