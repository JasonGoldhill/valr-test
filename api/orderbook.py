btcBids = []
btcAsks = []
ethBids = []
ethAsks = []
xrpBids = []
xrpAsks = []

btcTradeHistory = []
ethTradeHistory = []
xrpTradeHistory = []

def getOrderbook(pair):
    if pair.upper() == "BTCZAR":
        bids = btcBids
        asks = btcAsks
    elif pair.upper() == "ETHZAR":
        bids = ethBids
        asks = ethAsks
    elif pair.upper() == "XRPZAR":
        bids = xrpBids
        asks = xrpAsks
    else:
        return "Not a valid currency pair."
    
    orderbook = {
        "Asks": asks,
        "Bids": bids
    }

    return orderbook

def getTradeHistory(pair, limit):
    if pair.upper() == "BTCZAR":
        tradeHistory = btcTradeHistory
    elif pair.upper() == "ETHZAR":
        tradeHistory = ethTradeHistory
    elif pair.upper() == "XRPZAR":
        tradeHistory = xrpTradeHistory
    else:
        return "Not a valid currency pair."
    
    if len(tradeHistory) > limit:
        history = {
            "TradeHistory": tradeHistory[:limit]
        }
    else:
        history = {
            "TradeHistory": tradeHistory[:limit]
        }
    
    return history

def newLimitOrder(side, quantity, price, pair):
    order = {
        "quantity": quantity,
        "price": price
    }

    if pair.upper() == "BTCZAR":
        bids = btcBids
        asks = btcAsks
        tradeHistory = btcTradeHistory
    elif pair.upper() == "ETHZAR":
        bids = ethBids
        asks = ethAsks
        tradeHistory = ethTradeHistory
    elif pair.upper() == "XRPZAR":
        bids = xrpBids
        asks = xrpAsks
        tradeHistory = xrpTradeHistory
    else:
        return "Not a valid currency pair."

    if side.upper() == "SELL":
        if len(bids) > 0:
            if order["price"] > bids[0]["price"]:
                updateAsks(order, asks)
                return "Order placed."
            else:
                response = fillBid(order, bids, asks, tradeHistory)
                return response
        else:
            updateAsks(order, asks)
            return "Order placed."

    if side.upper() == "BUY":
        if len(asks) > 0:
            if order["price"] < asks[0]["price"]:
                updateBids(order, bids)
                return "Order placed."
            else:
                response = fillAsk(order, bids, asks, tradeHistory)
                return response
        else:
            updateBids(order, bids)
            return "Order placed." 

def updateAsks(order, asks):
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

def updateBids(order, bids):
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

def fillBid(order, bids, asks, tradeHistory):
    for bid in list(bids):
        if bid["price"] < order["price"]:
            break
        if bid["quantity"] > order["quantity"]:
            updateTradeHistory(bid["price"], order["quantity"], "sell", tradeHistory)
            bid["quantity"] = bid["quantity"] - order["quantity"]
            order["quantity"] = 0
            break
        elif order["quantity"] > bid["quantity"]:
            updateTradeHistory(bid["price"], bid["quantity"], "sell", tradeHistory)
            bids.remove(bid)
            order["quantity"] = order["quantity"] - bid["quantity"]
        else:
            updateTradeHistory(bid["price"], order["quantity"], "sell", tradeHistory)
            bids.remove(bid)
            order["quantity"] = 0
            break

    if order["quantity"] > 0:
        updateAsks(order, asks)
        return "Order partially filled. Remainder placed in orderbook."
    else:
        return "Order completely filled."

def fillAsk(order, bids, asks, tradeHistory):
    for ask in list(asks):
        if ask["price"] > order["price"]:
            break
        if ask["quantity"] > order["quantity"]:
            updateTradeHistory(ask["price"], order["quantity"], "buy", tradeHistory)
            ask["quantity"] = ask["quantity"] - order["quantity"]
            order["quantity"] = 0
            break
        elif order["quantity"] > ask["quantity"]:
            updateTradeHistory(ask["price"], ask["quantity"], "buy", tradeHistory)
            asks.remove(ask)
            order["quantity"] = order["quantity"] - ask["quantity"]
        else:
            updateTradeHistory(ask["price"], order["quantity"], "buy", tradeHistory)
            asks.remove(ask)
            order["quantity"] = 0
            break

    if order["quantity"] > 0:
        updateBids(order, bids)
        return "Order partially filled. Remainder placed in orderbook."
    else:
        return "Order completely filled."

def updateTradeHistory(price, quantity, takerSide, tradeHistory):
    entry = {
        "quantity": quantity,
        "price": price,
        "takerSide": takerSide
    } 

    tradeHistory.insert(0, entry)

    if len(tradeHistory) > 100:
        tradeHistory.pop()