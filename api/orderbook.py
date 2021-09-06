# lists for handling the in-memory orderbooks
btcBids = []
btcAsks = []
ethBids = []
ethAsks = []
xrpBids = []
xrpAsks = []

# lists for handling the trade histories
btcTradeHistory = []
ethTradeHistory = []
xrpTradeHistory = []


# called when a request is made to the /orderbook endpoint
def getOrderbook(pair):
    # checks that pair received in the request is valid and sets the correct lists to work with going forward
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
        return "The pair parameter must be a valid currency pair."

    # creates the orderbook to be returned to the user
    orderbook = {
        "Asks": asks,
        "Bids": bids
    }

    return orderbook


# called when a request is made to the /tradeHistory endpoint
def getTradeHistory(pair, limit):
    # checks that pair received in the request is valid and sets the correct lists to work with going forward
    if pair.upper() == "BTCZAR":
        tradeHistory = btcTradeHistory
    elif pair.upper() == "ETHZAR":
        tradeHistory = ethTradeHistory
    elif pair.upper() == "XRPZAR":
        tradeHistory = xrpTradeHistory
    else:
        return "The pair parameter must be a valid currency pair."

    # creates the history to be returned to the user and only uses the first x number of entries in the list based on the limit set
    history = {
        "TradeHistory": tradeHistory[:limit]
    }

    return history


# called when a request is made to the /limitOrder endpoint
def newLimitOrder(side, quantity, price, pair, postOnly):
    order = {
        "quantity": quantity,
        "price": price
    }

    # checks that pair received in the request is valid and sets the correct lists to work with going forward
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
        return "The pair parameter must be a valid currency pair."

    if side.upper() == "SELL": # if the user is trying to create a new ask
        if len(bids) > 0: # check whether there are any existing bids it could match against
            if order["price"] > bids[0]["price"]: # check whether it should match against any bids, if not just place the order on the asks side of the orderbook
                updateAsks(order, asks)
                return "Order placed."
            else: # if it should match check whether the order was postOnly, if yes cancel the order, if no fill bids
                if postOnly is True:
                    return "Post Only order cancelled as it would have matched."
                else:
                    response = fillBid(order, bids, asks, tradeHistory)
                    return response
        else: # if there are no bids it could match against then just place the order on the asks side of the orderbook
            updateAsks(order, asks)
            return "Order placed."

    elif side.upper() == "BUY": # if the user is trying to create a new bid
        if len(asks) > 0: # check whether there are any existing asks it could match against
            if order["price"] < asks[0]["price"]: # check whether it should match against any bids, if not just place the order on the bids side of the orderbook
                updateBids(order, bids)
                return "Order placed."
            else: # if it should match check whether the order was postOnly, if yes cancel the order, if no fill asks
                if postOnly is True:
                    return "Post Only order cancelled as it would have matched."
                else:
                    response = fillAsk(order, bids, asks, tradeHistory)
                    return response
        else: # if there are no asks it could match against then just place the order on the bids side of the orderbook
            updateBids(order, bids)
            return "Order placed."

    else: # handles the side parameter not being valid
        return "The side parameter must be either BUY or SELL."


# called either when an ask order had no orders on the other side of the orderbook it should match against first, or after part has been filled but there is still an unfilled portion left
def updateAsks(order, asks):
    if len(asks) > 0: # checks whether there is anything on the asks side of the order book
        if order["price"] > asks[-1]["price"]: # checks whether the order price is greater than the highest ask, if yes just append the order
            asks.append(order)
        else: # if the order price is not higher than the highest ask then we need to loop through all the asks and find the right position for the order
            index = 0
            for ask in asks:
                if order["price"] < ask["price"]:
                    break
                else:
                    index = index + 1
            asks.insert(index, order)
    else: # if the asks are empty then just place the order straight in
        asks.append(order)


# called either when a bid order had no orders on the other side of the orderbook it should match against first, or after part has been filled but there is still an unfilled portion left
def updateBids(order, bids):
    if len(bids) > 0: # checks whether there is anything on the bids side of the order book
        if order["price"] < bids[-1]["price"]: # checks whether the order price is smaller than the lowest bid, if yes just append the order
            bids.append(order)
        else: # if the order price is not lower than the lowest bid then we need to loop through all the bids and find the right position for the order
            index = 0
            for bid in bids:
                if order["price"] > bid["price"]:
                    break
                else:
                    index = index + 1
            bids.insert(index, order)
    else: # if the bids are empty then just place the order straight in
        bids.append(order)


# called when a new ask order should match against existing bids
def fillBid(order, bids, asks, tradeHistory):
    # loops through all the bids until either the order has been filled or it should no longer match based on price
    for bid in list(bids):
        if bid["price"] < order["price"]: # if the order should not match based on price any more then break out of the loop
            break
        if bid["quantity"] > order["quantity"]: # if the next bid has a higher quantity, then fill the order, reduce the bids quantity and break out of the loop
            updateTradeHistory(bid["price"], order["quantity"], "sell", tradeHistory)
            bid["quantity"] = bid["quantity"] - order["quantity"]
            order["quantity"] = 0
            break
        elif order["quantity"] > bid["quantity"]: # if the next bid has a lower quantity than the order, then fill and remove the bid, reduce the order quantity and move onto the next bid
            updateTradeHistory(bid["price"], bid["quantity"], "sell", tradeHistory)
            bids.remove(bid)
            order["quantity"] = order["quantity"] - bid["quantity"]
        else: # if the order and bid are for the same quantity, then fill both the order and the bid, remove the bid and break out of the loop
            updateTradeHistory(bid["price"], order["quantity"], "sell", tradeHistory)
            bids.remove(bid)
            order["quantity"] = 0
            break
    
    # if after the above loop completes and the order still has an unfilled quantity left, then place that onto the asks side of the orderbook
    if order["quantity"] > 0:
        updateAsks(order, asks)
        return "Order partially filled. Remainder placed in orderbook."
    else:
        return "Order completely filled."


# called when a new bids order should match against existing asks
def fillAsk(order, bids, asks, tradeHistory):
    # loops through all the asks until either the order has been filled or it should no longer match based on price
    for ask in list(asks):
        if ask["price"] > order["price"]: # if the order should not match based on price any more then break out of the loop
            break
        if ask["quantity"] > order["quantity"]: # if the next ask has a higher quantity, then fill the order, reduce the asks quantity and break out of the loop
            updateTradeHistory(ask["price"], order["quantity"], "buy", tradeHistory)
            ask["quantity"] = ask["quantity"] - order["quantity"]
            order["quantity"] = 0
            break
        elif order["quantity"] > ask["quantity"]: # if the next ask has a lower quantity than the order, then fill and remove the ask, reduce the order quantity and move onto the next ask
            updateTradeHistory(ask["price"], ask["quantity"], "buy", tradeHistory)
            asks.remove(ask)
            order["quantity"] = order["quantity"] - ask["quantity"]
        else: # if the order and ask are for the same quantity, then fill both the order and the ask, remove the ask and break out of the loop
            updateTradeHistory(ask["price"], order["quantity"], "buy", tradeHistory)
            asks.remove(ask)
            order["quantity"] = 0
            break

    # if after the above loop completes and the order still has an unfilled quantity left, then place that onto the bids side of the orderbook
    if order["quantity"] > 0:
        updateBids(order, bids)
        return "Order partially filled. Remainder placed in orderbook."
    else:
        return "Order completely filled."


# called whenever a new order matched against an existing bid or ask in the orderbook and a transaction occurs
def updateTradeHistory(price, quantity, takerSide, tradeHistory):
    # creates the new tradeHistory entry
    entry = {
        "quantity": quantity,
        "price": price,
        "takerSide": takerSide
    }

    # inserts the new tradeHistory entry at the front of the list
    tradeHistory.insert(0, entry)

    # removes the last (oldes) entry in the tradeHistory list if a new one pushes it over 100 entries long
    if len(tradeHistory) > 100:
        tradeHistory.pop()
