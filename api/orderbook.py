bids = []
asks = []

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
    for bid in bids:
        if bid["price"] < order["price"]:
            break
        if bid["quantity"] > order["quantity"]:
            bid["quantity"] = bid["quantity"] - order["quantity"]
            order["quantity"] = 0
            # update transaction history here
            break
        elif order["quantity"] > bid["quantity"]:
            bids.remove(bid)
            order["quantity"] = order["quantity"] - bid["quantity"]
            # update transaction history here
        else:
            bids.remove(bid)
            order["quantity"] = 0
            # update transaction history here
            break

    if order["quantity"] > 0:
        updateAsks(order)
        return "Order partially filled. Remainder placed in orderbook."
    else:
        return "Order completely filled."

def fillAsk(order):
    for ask in asks:
        if ask["price"] > order["price"]:
            break
        if ask["quantity"] > order["quantity"]:
            ask["quantity"] = ask["quantity"] - order["quantity"]
            order["quantity"] = 0
            # update transaction history here
            break
        elif order["quantity"] > ask["quantity"]:
            asks.remove(ask)
            order["quantity"] = order["quantity"] - ask["quantity"]
            # update transaction history here
        else:
            asks.remove(ask)
            order["quantity"] = 0
            # update transaction history here
            break

    if order["quantity"] > 0:
        updateBids(order)
        return "Order partially filled. Remainder placed in orderbook."
    else:
        return "Order completely filled."